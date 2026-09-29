---
title: "03 · 身份与权限"
weight: 40
baseline: "IBL main @ 6c2ea40 · 2026-09-28"
summary: "飞书解决‘你是谁’，控制租约解决‘谁现在能写’，MCU 安全链解决‘输出是否安全’——三者不是一回事。"
---

IBL Rig 的身份系统围绕多人共享一台 rig 设计。

## 飞书登录

登录链路不是让 Pi 保存飞书应用 secret。

当前结构是：

```text
Browser
  ↓
中央 Auth Broker
  ↓ Feishu OAuth
飞书身份
  ↓
Broker 签发短时 Ed25519 ticket
  ↓
Rig Web 验签并换成本地 session
```

中央 Broker 持有飞书 secret；rig 保存 ticket 公钥。Ticket 绑定具体 `rig_id`，并且是一次性的短时凭据。

Web 当前定义两种角色：

- `operator`
- `admin`

认证成功后，本地 Web session 与浏览器会话绑定。

## 控制权不是登录状态

多人可以同时登录并看同一台 rig，但同一时刻只有一个浏览器 session 持有写控制权。

当前配置：

- heartbeat window：15 s；
- offline takeover：300 s。

这里最容易误解的是 15 s。

**15 s 只是判断持有人“当前在线”的心跳窗口，不是控制权 15 秒自动过期。**

控制权是 sticky 的。持有人即使：

- 浏览器进后台；
- 临时断网；
- Web 短暂 502；
- 页面刷新；

也不会仅因为 15 s 没心跳就自动把控制权交给别人。

## 什么情况下控制权会变

正常路径包括：

1. 持有人主动释放；
2. 持有人退出登录；
3. 另一位操作者在原持有人长时间离线后接管；
4. 在线持有人审批接管请求；
5. 管理员强制接管。

这些动作都写审计记录。

同一个飞书账户开的两个浏览器，也不是同一个控制 session。写权限按浏览器 session 判定，而不是“用户名相同就都能写”。

## 在线接管

当前持有人仍在线时，另一位 operator 不应直接抢走控制权，而是发送 takeover request。

请求会记录：

- requester；
- holder；
- reason；
- 创建与过期时间；
- 决策状态。

飞书卡片可以用于通知/审批；最终决定仍要经过 Rig Web 的已验证请求状态。

## Admin

Admin 用于需要更高权限的操作，例如强制接管等。

管理员能力不应该被理解成“可以绕过系统安全边界”。即使 admin 获得 Web 控制权，MCU 自己的 lease、watchdog、fault latch 和执行器限制仍然独立存在。

## 本机应急登录

代码还保留本机一次性 emergency code 路径，用于中央登录链不可用时的维护。

它生成短时、单次使用的本地 admin 身份，并留下审计记录。正常训练不应把它当作日常登录方式。

## 控制权与实验安全完全不同

三个概念必须分开：

| 概念 | 解决的问题 |
|---|---|
| 身份认证 | 你是谁 |
| Web 控制权 | 谁可以提交操作意图 |
| MCU safety lease / watchdog | Host 出问题时物理输出是否会回到安全状态 |

因此：

> 控制权接管不会自动中止正在运行的实验，也不等于接管了 MCU 的实时安全链。

反过来，Web 崩溃也不能成为执行器继续输出的理由。

## 审计

身份数据库保存登录、退出、租约、接管和相关管理操作的审计记录。需要理由的操作应该填写真实原因，而不是统一写“test”。

### 相关源码与文档

- [Auth implementation](https://github.com/QiuYi111/IBL/blob/main/software/host/rig-os/ros2_ws/src/rig_web/rig_web/auth.py)
- [Rig auth config](https://github.com/QiuYi111/IBL/blob/main/software/host/rig-os/ros2_ws/src/rig_web/config/rig-auth.yaml)
- [Takeover notifications](https://github.com/QiuYi111/IBL/blob/main/software/host/rig-os/docs/control-takeover-notifications.md)
