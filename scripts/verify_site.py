#!/usr/bin/env python3
"""Dependency-free static website, local link and Apple screenshot checks."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit, unquote
import re
import struct
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]

class Page(HTMLParser):
    def __init__(self, source):
        super().__init__()
        self.links, self.ids, self.images = [], set(), []
        self.language = False
        self.feed(source.read_text(encoding='utf-8'))

    def handle_starttag(self, tag, attrs):
        props = dict(attrs)
        if tag == 'html':
            self.language = props.get('lang') == 'zh-Hans'
        if 'id' in props:
            assert props['id'] not in self.ids, 'Duplicate HTML ID'
            self.ids.add(props['id'])
        for field in ['href', 'src']:
            if field in props:
                self.links.append(props[field])
        if tag == 'img':
            assert props.get('alt'), 'Missing image alt text'
            assert props.get('width') and props.get('height'), 'Missing intrinsic image size'
            self.images.append(props['src'])

pages = [ROOT / name for name in ['index.html', 'privacy/index.html', 'support/index.html', 'terms/index.html', '404.html']]
parsed = {}
for path in pages:
    assert path.is_file(), 'Missing page ' + str(path)
    parsed[path.resolve()] = Page(path)
    assert parsed[path.resolve()].language, 'Missing Chinese language declaration'
    assert 'id="main"' in path.read_text(encoding='utf-8'), 'Missing main landmark'
links = 0
for path, page in parsed.items():
    for url in page.links:
        part = urlsplit(url)
        if part.scheme or part.netloc:
            assert part.scheme in ['https', 'mailto'], 'Insecure external URL'
            continue
        target = (path.parent / unquote(part.path)).resolve() if part.path else path
        if target.is_dir():
            target /= 'index.html'
        assert target.is_relative_to(ROOT.resolve()), 'Link escapes site root'
        assert target.is_file(), 'Broken local link: ' + str(path) + ' -> ' + url
        if part.fragment:
            target_page = parsed.get(target) or Page(target)
            assert part.fragment in target_page.ids, 'Missing link target: ' + url
        links += 1
screens = sorted((ROOT / 'assets/screenshots').glob('*.png'))
assert len(screens) == 8, 'Expected eight real screenshots'
for image in screens:
    data = image.read_bytes()
    assert data[:8] == b'\x89PNG\r\n\x1a\n'
    assert struct.unpack('>IIBB', data[16:26]) == (1206, 2622, 8, 2), 'Invalid screenshot dimensions or alpha'
home = (ROOT / 'index.html').read_text(encoding='utf-8')
assert '正在准备上架' in home
assert not re.search(r'apps\.apple\.com/[^\s"<>]*id\d+', home), 'Unexpected unverified store URL'
assert not re.search(r'<(?:script|iframe)\b', home), 'Unexpected script or embed'
ET.parse(ROOT / 'sitemap.xml')
assert (ROOT / '.nojekyll').exists()
print('PASS: 5 pages, local links, 8 RGB screenshots, sitemap and accessibility basics')
