---
title: "IBL Rig Documentation"
type: docs
---

# IBL Rig Documentation

IBL Rig 是一套小鼠行为训练系统。系统由三层组成：

- **RoboMaster C Board / STM32F407**：执行 Trial 状态机，读取转轮，控制 M2006、电泵、TTL 和本地安全逻辑。
- **Raspberry Pi 5 / ROS 2 Jazzy**：编译任务，管理 Session，控制相机和视觉刺激，记录数据，运行诊断与实验后处理。
- **Rig Web / 飞书**：完成登录、配置、控制权、预检、实验控制、实时监看和结果索引。

当前文档对应 [QiuYi111/IBL main @ `6c2ea40`](https://github.com/QiuYi111/IBL/commit/6c2ea40067cbfe20a0c748c7da68f80270a20016)。

## 文档

- [认识系统](docs/00-system/)
- [Quick Start](docs/01-quick-start/)
- [配置文件](docs/02-configuration/)
- [身份与权限](docs/03-identity/)
- [实验数据](docs/04-data/)
- [硬件介绍](docs/05-hardware/)
- [ROS 2](docs/06-ros2/)

## Reference

- [实验参数](reference/configuration/)
- [ROS 2 节点](reference/ros2-nodes/)
- [ROS 2 Topic / Service / Action](reference/ros2-interfaces/)
- [Web API](reference/web-api/)
- [数据与文件](reference/data/)
