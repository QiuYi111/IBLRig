# IBL Rig Documentation

IBL Rig 文档站。

当前内容同步 [QiuYi111/IBL](https://github.com/QiuYi111/IBL)：
- `main`：`6c2ea40067cbfe20a0c748c7da68f80270a20016`
- `codex/mcu-oak-recovery-chain`：`5c1a6190bf9253be0c880d5dc204b7f233c1f4bf`

## 内容

- 系统架构
- Quick Start
- 配置系统
- 身份与权限
- 实验数据
- 硬件
- ROS 2
- Reference

## 本地运行

```bash
hugo mod npm pack
npm install
npm run start
```

## 部署

`master` 推送后由 GitHub Actions 构建 Hugo，并部署到 GitHub Pages。

https://qiuyi111.github.io/IBLRig/
