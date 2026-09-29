---
title: "IBL Rig Documentation"
type: docs
---

# IBL Rig Documentation

IBL Rig 是一套小鼠行为训练系统，覆盖视觉刺激、转轮交互、奖励给水、四路视频记录、实验控制和数据归档。

## 产品定位

**兼容 IBL 任务的下一代行为学平台。**

*A next-generation behavioral platform compatible with IBL tasks.*

IBL Rig 以 International Brain Laboratory 的 ChoiceWorld 任务为兼容目标：刺激参数、训练阶段、转轮增益规则与 IBL 协议保持一致。

在此之上，平台采用机器人与工业系统的成熟架构：

- **实时控制**：STM32 / FreeRTOS 执行完整 Trial，500 Hz 电机控制环。
- **系统编排**：ROS 2 管理设备与服务，systemd 保证进程存活，设备故障分级自恢复。
- **可编程转轮**：M2006 力反馈电机让转轮同时成为传感器和执行器，可产生阻尼、弹簧、惯性、棘轮和透明手感。
- **多视角视频**：四路全局快门相机，设备端 H.265 编码。
- **网络化运维**：网页控制台、权限与控制权、NAS 校验归档、实验索引。
- **系统测试**：HIL / Chaos 随机故障注入与确定性回归，失败现场可重放。

IBL 是平台的兼容层，而不是能力上限。

平台的目标是：

> 像工业设备一样可靠，像机器人一样可交互，同时保持行为学实验的可重复性。

与 IBL 原版的逐项对比见 [09 · 与 IBL 原版对比](docs/09-ibl-comparison/)。

系统由三部分组成：

- **实验装置**：转轮、M2006 电机、蠕动泵、四路相机、刺激显示器、红外照明和同步信号。
- **实验主机**：Raspberry Pi 5 运行 ROS 2，负责实验控制、设备管理、刺激呈现、录像和数据处理。
- **网页控制台**：完成飞书登录、训练配置、小鼠编号、预检、开始/暂停/停止、视频预览和表现统计。

## 使用文档

- [认识系统](docs/00-system/)
- [Quick Start](docs/01-quick-start/)
- [配置文件](docs/02-configuration/)
- [身份与权限](docs/03-identity/)
- [实验数据](docs/04-data/)
- [硬件介绍](docs/05-hardware/)
- [ROS 2](docs/06-ros2/)
- [Daemon 与自恢复](docs/07-daemon-recovery/)
- [Chaos / HIL](docs/08-chaos-hil/)
- [与 IBL 原版对比](docs/09-ibl-comparison/)

## Reference

- [实验与设备参数](reference/configuration/)
- [硬件参数](reference/hardware/)
- [ROS 2 节点](reference/ros2-nodes/)
- [ROS 2 话题、服务与动作](reference/ros2-interfaces/)
- [数据文件](reference/data/)
- [Daemon / systemd](reference/daemons/)
- [Chaos / HIL](reference/chaos/)
- [IBL 对比](reference/ibl-comparison/)
