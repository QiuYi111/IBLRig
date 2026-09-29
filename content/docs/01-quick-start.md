---
title: "01 · Quick Start"
weight: 20
baseline: "IBL main @ 6c2ea40 · 2026-09-28"
summary: "从打开网页到结束一次 session：登录、选择配置、预检、运行、监看、收尾。"
---

本章只讲最短路径。配置参数、权限和数据格式在后续章节展开。

<div class="status-note">
当前仓库的正式协议文档仍写明：尚未完成正式动物训练整体验收。第一次接触 rig 时，应先按无动物工程集成流程熟悉系统。
</div>

## 1. 打开 Rig Web

使用桌面浏览器打开当前 rig 的局域网或 Tailnet 地址。Web 页面只是控制面，不是实时安全链；页面刷新、浏览器休眠或网络短暂断开不会让 MCU 继续输出失去约束的动作。

如果页面要求登录，进入飞书 OAuth 流程并返回 rig。

登录完成后先看两件事：

1. 页面右上角显示的身份是不是自己；
2. 当前是否持有控制权。

没有控制权时可以查看状态，但写操作会受限。

## 2. 认识主界面

开始实验前主要关注这些区域：

| 区域 | 看什么 |
|---|---|
| Session / Configuration | subject、模板、配置 revision、是否已锁定 |
| Device / Health | MCU、刺激、相机、recorder、时间、磁盘 |
| Camera Preview | 四路 OAK 画面与主预览 |
| Control | Prepare / Preflight / Start / Pause / Stop / Abort |
| Performance | trial 数、正确/错误、奖励、耗时和训练评估 |
| Post-session | analysis、NAS、W&B、飞书、cleanup |

名称会随前端迭代略有变化，但状态机含义不变。

## 3. 选择配置

1. 输入 **subject id**。
2. 从配置库选择需要的模板。
3. 如需改参数，先复制/编辑允许修改的字段，不要直接绕过配置系统改生成文件。
4. 检查页面展示的差异。

正式路径目前包括“正式预训练”和“正式训练”模板；仓库也保留其它自定义/工程模板。正式模板本身仍包含仓库明确记录的协议例外，因此“模板名字里有正式”不等于物理验收已经完成。

## 4. 锁定配置

准备 session 时，系统会把模板解析成一组不可变 artifact：

- task source；
- compiled trial table / online policy descriptor；
- session config；
- resolved YAML；
- 各自 SHA-256。

锁定后，真正运行的是这些 artifact，不是浏览器里一份可随时变化的表单。

这一步要确认：

- subject 正确；
- 参数和单位正确；
- 模板 revision 正确；
- override diff 符合预期；
- 配置 SHA 已生成。

## 5. Preflight

预检的目标不是“看起来都在线”，而是判断当前 session 能不能安全开始。

典型检查包括：

- Supervisor 与 session 状态；
- 该 session 真正需要的设备是否健康；
- MCU / controller link；
- 刺激显示；
- 相机；
- recorder 与 session 目录；
- 磁盘空间；
- 时间质量；
- 已锁定 artifact 是否仍匹配。

红色项先处理。不要通过反复点击 Start 绕过一个稳定失败的 preflight。

## 6. 开始实验

预检通过后按页面流程确认 arm / start。

Session 开始后：

- 配置保持锁定；
- Supervisor 成为 session 生命周期权威；
- MCU 按 trial 合同执行；
- Recorder 创建并持续写入事件日志；
- 如配置需要相机，OAK 开始原生录制；
- Web 持续显示状态，但不参与毫秒级执行。

## 7. 监看

运行中至少看四类信息：

**行为**
- 当前 trial；
- correct / incorrect / no response；
- reward；
- 当前训练阶段或评估。

**设备**
- MCU；
- camera；
- stimulus；
- recorder；
- time / storage。

**画面**
- 四路相机是否持续更新；
- 主预览是否符合预期。

**异常**
- fault 是否锁存；
- 是否出现 recorder/camera 数据缺口；
- 是否出现磁盘或网络后处理告警。

## 8. 暂停、停止和 Abort

三者语义不同。

- **Pause**：按系统允许的边界暂停，不等同紧急停机。
- **Stop**：正常结束，等待当前执行边界后完成收尾。
- **Abort**：异常或安全问题下中止，保留原因和 session id。

遇到机械干涉、异常给水、不可接受的运动或其它安全问题时，不应为了“保住数据”而延迟 abort。

## 9. 实验结束

正常结束并不代表整个数据链已经结束。

依次确认：

1. Session 到达终态；
2. Recorder 已 finalize；
3. 相机 manifest 完成；
4. analysis 状态；
5. NAS 是否 verified；
6. W&B / 飞书是否完成；
7. 本地 cleanup 是否仍在等待。

保留 session id。所有后处理任务都围绕它做幂等追踪。

## 常见问题

### 页面刷新后实验还在跑

正常。Web 不是 session 权威，重新登录后读取 Supervisor 状态。

### 页面是只读的

控制权属于另一浏览器 session。按“身份与权限”章节处理，不要绕过 Web 直接下执行器命令。

### 相机没有画面

先看 camera health 和 USB 状态。当前 production 配置要求 USB3；相机恢复也受到 session/recording 状态保护。

### 数据上传没完成

只要 NAS 还未通过完整性验证，本地原始数据就不应被自动清理。先查对应 job 状态，不要手动删 session。

### 相关源码与文档

- [当前用户手册](https://github.com/QiuYi111/IBL/blob/main/docs/USER_GUIDE.md)
- [Rig OS operations](https://github.com/QiuYi111/IBL/blob/main/software/host/rig-os/docs/operations.md)
- [Formal protocol status](https://github.com/QiuYi111/IBL/blob/main/software/host/rig-os/docs/formal-pdf-protocol.md)
