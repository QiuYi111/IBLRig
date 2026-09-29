---
title: "00 · 认识系统"
weight: 10
baseline: "IBL main @ 6c2ea40 · 2026-09-28"
summary: "先把 IBL Rig 看成一个系统：实时控制、实验编排、用户交互三层分工。"
---

IBL Rig 是对 IBL 行为训练装置和行为训练协议的现代化重构。它不是单独的一台训练盒，也不是单独一个 ROS 2 工程，而是一套从实时控制、刺激呈现、相机记录到实验后处理的完整 rig。

当前系统可以先分成三个大块：

```text
┌─────────────────────────────────────────────────────────────┐
│ 用户交互：Browser / Rig Web / 飞书                          │
│ 配置、身份、控制权、预检、监看、通知、实验结果              │
└───────────────────────┬─────────────────────────────────────┘
                        │ HTTPS / API / ROS 2 intent
┌───────────────────────▼─────────────────────────────────────┐
│ 实验编排：Raspberry Pi 5 / Ubuntu 24.04 / ROS 2 Jazzy       │
│ Supervisor、任务编译、相机、刺激、记录、诊断、后处理        │
└───────────────────────┬─────────────────────────────────────┘
                        │ Controller link
┌───────────────────────▼─────────────────────────────────────┐
│ 硬件控制：RoboMaster C Board / STM32F407 / FreeRTOS         │
│ Trial FSM、转轮、M2006/C610、蠕动泵、TTL、输入捕获与安全     │
└─────────────────────────────────────────────────────────────┘
```

## 硬件控制系统

RoboMaster C Board 是实时控制核心。STM32 侧承担“物理因果”：

- 执行 trial 状态机；
- 读取转轮和输入；
- 控制 M2006/C610；
- 控制奖励泵和 TTL；
- 判断轮子阈值；
- 在 Host 丢失时保持本地安全约束。

因此，浏览器卡顿、ROS 2 消息延迟或 Web 重启都不应该被当作毫秒级控制环的一部分。Host 发的是已经编译好的有限 trial 合同，真正的实时执行留在 MCU。

当前 `rig-os` 把 SWD 作为 production controller link 的代码合同：Host 通过 ST-Link 对保留 SRAM 区域进行非停核访问，协议包含固定 ABI、环形队列、CRC、会话握手和可靠消息去重。仓库里仍有部分历史文档保留 SPI 口径，阅读时以当前 `rig-os/README.md` 与 `docs/swd-controller-link.md` 为准。

## 实验编排系统

实验编排运行在 Raspberry Pi 5 的 ROS 2 Jazzy 上。ROS 2 不承担电机实时闭环，而负责：

- 系统拓扑与生命周期；
- Session 权威状态；
- Trial 编译与逐 trial 扩展；
- OAK-FFC-4P 相机；
- HDMI 视觉刺激与显示确认；
- 行为事件记录；
- 时间质量、诊断和标定；
- 自动分析和外部存档任务。

系统的中心是 **Supervisor**。Web 或 CLI 只提交“我要运行哪一个 session”的意图，Supervisor 根据锁定后的 artifact 自己推导需要哪些能力。空闲状态下 Runtime Graph 可以是空的：相机、刺激器等能力没有被需求时，不需要常驻。

## 用户交互系统

Rig Web 针对训练流程直接设计：

- 飞书登录；
- 显示当前操作者与控制权；
- 选择、复制和编辑配置；
- 输入 subject；
- 查看配置差异并锁定；
- 预检；
- 开始、暂停、停止和 abort；
- 四路相机预览和设备状态；
- 查看实验结果与后处理状态。

飞书还承担通知、控制权接管交互和最终实验索引。它不是实验数据真值：原始数据仍由本地 session 文件、相机原生文件、事件日志和哈希 manifest 定义。

## 一次实验是怎样跑起来的

```text
选择模板 + subject
        ↓
解析并锁定配置
        ↓
生成 task / compiled table / session config
        ↓
Supervisor 根据 artifact 推导所需能力
        ↓
预检设备、时间、存储、配置状态
        ↓
MCU 执行 trial
 ├─ stimulus 请求 → 屏幕显示确认
 ├─ wheel/input → MCU 本地判定
 ├─ reward/motor/TTL → MCU 本地执行
 └─ semantic event → recorder
        ↓
相机原生录像 + event log + manifest
        ↓
analysis → NAS → W&B → 飞书 → verified cleanup
```

## 四个“谁说了算”

系统最重要的设计不是 ROS 2 节点数量，而是权威边界：

| 问题 | 权威 |
|---|---|
| Trial、执行器和本地安全 | MCU |
| 哪些能力应该存在、Session 能否运行 | Supervisor |
| 操作者想做什么 | Web / CLI，只表达意图 |
| 原始数据是什么 | 原生文件 + 不可变事件日志 + manifest |

这也是为什么系统不会让 Web 直接控制执行器，也不会用 DDS 收包时间代替真实物理事件时间。

## 当前状态

当前代码已经覆盖完整的软件链路，并有多项无动物 HIL 和设备级验证；但正式协议文档仍明确列出显示几何、光电二极管时序、给水、完整行为分支等待验收项。

**“代码存在”“软件测试通过”“HIL 通过”“可正式动物训练”是不同状态。**

### 相关源码与文档

- [IBL 根 README](https://github.com/QiuYi111/IBL/blob/main/README.md)
- [Rig OS README](https://github.com/QiuYi111/IBL/blob/main/software/host/rig-os/README.md)
- [Host architecture](https://github.com/QiuYi111/IBL/blob/main/software/host/rig-os/docs/architecture.md)
- [SWD controller link](https://github.com/QiuYi111/IBL/blob/main/software/host/rig-os/docs/swd-controller-link.md)
