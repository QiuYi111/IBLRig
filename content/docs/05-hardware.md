---
title: "05 · 硬件介绍"
weight: 60
baseline: "IBL main @ 6c2ea40 · 2026-09-28"
summary: "从 C Board、M2006、蠕动泵、OAK 到机械 R5：介绍当前工程版本和已知验证边界。"
---

IBL Rig 的硬件不是一张静态 BOM。仓库区分：

- engineering current；
- integration / manufacturing candidate；
- manufacturing candidate；
- production release。

文件名里写着 `final` 或时间更晚，都不能自动成为“当前版本”。当前身份由 `hardware/configuration/current-hardware.json` 注册。

## Raspberry Pi 5 Host

当前 ratRot Host 基线是 Raspberry Pi 5：

- 8 GiB RAM；
- Ubuntu 24.04 arm64；
- ROS 2 Jazzy；
- SD 启动；
- NVMe 作为主要 `/data` 数据盘；
- 相机、session、日志、缓存和 swap 放到 NVMe 路径。

Pi 负责 orchestration，不负责 500 Hz 电机控制闭环。

## RoboMaster C Board / STM32F407

C Board 是实时控制核心。

职责包括：

- Trial FSM；
- wheel/input capture；
- M2006/C610；
- pump；
- TTL；
- safety lease；
- fault latch；
- controller link 的应用侧。

当前代码的 production controller link 合同使用 ST-Link/SWD 非停核 SRAM data plane。维护、刷机和运行链路必须遵守单 owner 规则，避免 Gateway、watchdog 和调试工具同时占用 probe。

## 转轮、M2006 与 C610

M2006 + C610 用于转轮与触觉/力反馈。

固件支持多种控制模式和 profile，实时闭环留在 STM32 本地。

维护 TUI 有独立安全限制：

- 默认 disarmed；
- 需要显式 arm；
- 维护 heartbeat；
- heartbeat / SSH / Agent 丢失后撤防；
- current limit 有 Host 与 MCU 双重上限。

动物训练所需的力学标定仍是独立工作，软件存在 profile 不代表已经完成动物级力反馈标定。

## 蠕动泵

奖励泵由 MCU 执行。

系统区分：

- 按体积的奖励合同；
- 当前正式模板中按持续时间定制的反转泵动作。

正式训练模板当前默认反转 2 s，但仓库明确写明：

> 2 s 不是自动等价于 3 µL。

泵体积、重复性、温升和真实液路仍需要物理验收。

## OAK-FFC-4P

当前相机系统：

- OAK-FFC-4P；
- 四个 camera socket；
- 1280×800；
- USB3；
- 外部供电；
- 原生 H.265 录制；
- 并行 MJPEG Web preview。

2026-09-21 的第一次 Pi 5 组合长测因为 USB over-current 中断。把显示器移出 Pi USB 供电路径、OAK 保持外部 5 V 后，15 fps 的 60 分钟测试通过。

因此，供电拓扑本身是相机系统的一部分，不只是“能亮就行”。

## 显示与视觉刺激

刺激显示使用独立 direct-KMS renderer。

特点：

- task node 不直接画图；
- 支持 PRELOAD / SHOW / CLOSED_LOOP / FREEZE / HIDE；
- 每次语义命令有 page-flip acknowledgement；
- photodiode patch 用于把物理显示时刻带回 MCU 捕获。

软件 page-flip 时间只用于诊断；真正的视觉 onset/off 应以物理光电边沿为准。

当前仓库仍把显示几何、眼距和 photodiode timing 的完整标定列为未完成项。

## 时钟与同步

系统设计里 timing station 是 global time authority。

当前 PPS 可以作为边沿/频率参考，但如果没有机器可读的 UTC second number，就不能把 Host 接收时间凑成“UTC 已锁定”。

时间质量必须显式表示。

## 机械结构

当前硬件注册表记录：

| 部件 | 当前版本 | 状态 |
|---|---|---|
| Full rig | R5 | engineering-candidate |
| Core mechanism | V3-ENG P4 | engineering-candidate |
| Pad holder | CNC V4 | engineering-current |
| Mouse cover | true B-Rep rebuild | engineering-current |
| Compact camera/lamp | R2 | integration-candidate |
| Adjustable camera/lamp | Rev B | manufacturing-candidate |

制造包仍是 candidate，`production_release` 为空。

## 辅助模块

整个 rig 还包括：

- IR illumination；
- display / photodiode；
- C-board sound；
- PPS / timing path；
- 电源分配；
- NAS / 网络基础设施。

这些模块不一定都在一个 ROS 2 节点里，但都会影响一场实验的可运行状态。

## 当前最重要的硬件边界

已经有的软件/HIL结果不能代替这些物理量：

- 真实屏幕几何；
- photodiode 时序；
- pump volume/repeatability；
- 动物所需的 wheel force / haptic calibration；
- 当前 30 fps H.265 配置的长时间整机验证；
- 完整 PPS/UTC 映射；
- 制造与供应商放行。

### 相关源码与文档

- [Current hardware registry](https://github.com/QiuYi111/IBL/blob/main/hardware/configuration/current-hardware.json)
- [M2006 haptic platform](https://github.com/QiuYi111/IBL/tree/main/software/embedded/m2006-haptic-platform)
- [Camera integration](https://github.com/QiuYi111/IBL/blob/main/software/host/rig-os/docs/camera-integration.md)
- [Pi 5 camera soak](https://github.com/QiuYi111/IBL/blob/main/software/host/rig-os/docs/pi5-camera-soak-2026-09-21.md)
