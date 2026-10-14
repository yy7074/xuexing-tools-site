# 雪行工具官网

公开产品页、用户支持、隐私政策和使用条款。此仓库不包含 iOS App 源码、生产账号、审核账号、个人资料或运行日志。

- 官网 / 营销网址：https://yy7074.github.io/xuexing-tools-site/
- 支持：https://yy7074.github.io/xuexing-tools-site/support/
- 隐私政策：https://yy7074.github.io/xuexing-tools-site/privacy/
- 条款：https://yy7074.github.io/xuexing-tools-site/terms/

纯静态 HTML/CSS，无第三方前端依赖。`assets/screenshots/` 是实际 App 的中文界面素材，不含生产用户数据。

## 检查与部署

`python3 scripts/verify_site.py` 检查页面、链接和截图。
GitHub Pages 使用 GitHub Actions，主分支更新后自动验证并仅上传明确的公开页面目录；App 源码和 Git 信息不会打包进网站。

官网状态为“正在准备上架”，没有虚构 App Store 下载链接。App 正式发布后再添加真实商店链接。

## 内容维护

运营者提供真实公开客服邮箱及法定名称后，同步更新支持与隐私页面。当前公开联系渠道是本仓库的 Issues，提交需 GitHub 账号；它不是已经核实的邮箱联系方式。
后端数据处理和保留期限须由服务运营者确认，政策更新应保持与最终发布版本一致。
