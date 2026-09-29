---
title: "IBL Rig Documentation"
type: docs
---

# IBL Rig Documentation

IBL Rig 是一套小鼠行为训练系统，覆盖视觉刺激、转轮交互、奖励给水、四路视频记录、实验控制和数据归档。

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

## Reference

- [实验与设备参数](reference/configuration/)
- [硬件参数](reference/hardware/)
- [ROS 2 节点](reference/ros2-nodes/)
- [ROS 2 话题、服务与动作](reference/ros2-interfaces/)
- [数据文件](reference/data/)
- [Daemon / systemd](reference/daemons/)
- [Chaos / HIL](reference/chaos/)
