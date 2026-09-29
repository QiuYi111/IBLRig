---
title: "IBL Rig Documentation"
type: docs
---

# IBL Rig Documentation

IBL Rig 是对 IBL 行为训练装置与训练流程的现代化重构：STM32/FreeRTOS 负责实时执行和安全，Raspberry Pi 5 上的 ROS 2 负责实验编排，浏览器与飞书负责配置、监看、协作和实验后处理。

本站按系统本身组织，不区分“实验者文档”和“开发者文档”。从 Quick Start 可以直接开始一次实验，也可以继续向下读到配置、硬件和 ROS 2 的实现边界。

**当前文档基线：[QiuYi111/IBL main @ `6c2ea40`](https://github.com/QiuYi111/IBL/commit/6c2ea40067cbfe20a0c748c7da68f80270a20016)。**

- [认识系统](docs/00-system/)
- [Quick Start](docs/01-quick-start/)
- [配置文件](docs/02-configuration/)
- [身份与权限](docs/03-identity/)
- [实验数据](docs/04-data/)
- [硬件介绍](docs/05-hardware/)
- [ROS 2](docs/06-ros2/)

<div class="status-note">
仓库当前仍把正式动物训练与生产科学采集列为尚未完成整体验收的阶段。本文档只描述当前代码、配置和已有验证，不把“已经实现”写成“已经完成物理或动物验收”。
</div>
