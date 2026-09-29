---
title: "04 · 实验数据"
weight: 50
baseline: "IBL main @ 6c2ea40 · 2026-09-28"
summary: "原始数据先在 rig 上形成不可变记录，再经过 analysis、NAS、W&B、飞书和验证后清理。"
---

IBL Rig 不把 ROS 2 topic 当成全部数据真值。

当前原则是：

> **高带宽原始数据写原生文件；行为语义写追加式事件日志；DDS 负责语义消息、健康状态、索引和低频元数据。**

## 一次 Session 产生什么

最核心的几类文件：

- semantic event log；
- recorder manifest；
- camera native streams；
- per-frame camera index；
- camera manifest；
- diagnostics / quality report；
- resolved configuration；
- 后续生成的 analysis 结果。

每个关键 artifact 都使用 SHA-256 绑定身份。

## 行为事件

Recorder 写追加式事件日志。Session 成功并不以“MCU 说跑完了”为终点：

1. Controller 完成；
2. Recorder finalize；
3. fsync；
4. 生成 manifest；
5. 才能形成成功结果。

物理事件保留自己的：

- clock id；
- device tick；
- 可选 global time；
- mapping version；
- uncertainty；
- time quality。

Host 收到 DDS 消息的时间不能替换真实物理时间。

## 相机录制

当前 `main` 的 OAK runtime 默认：

- OAK-FFC-4P；
- 4 路；
- 1280 × 800；
- 30 fps；
- H.265；
- 12 Mbps / camera；
- USB3 required。

浏览器预览并不从 H.265 在 Pi 上转码。设备端并行生成 MJPEG 预览流，Host 侧再做主画面/缩略图抽样。

每一帧的 index 保存：

- camera id；
- frame sequence；
- device timestamp；
- exposure；
- gain；
- native file offset；
- encoded size；
- encoded SHA-256。

H.264/H.265 writer 会在文件开头预留空间，并在拿到 VPS/SPS/PPS 后复制到前缀，使 elementary stream 可以从文件头开始解码，同时保留原始帧 offset。

## 当前相机证据边界

这里必须区分“当前配置”和“已有长测”。

### 已通过的 60 分钟组合测试

2026-09-21 的 Pi 5 长测在 **15 fps production profile** 下通过：

- 四路相机；
- Web preview；
- 真实 1920×1080 stimulus；
- NVMe recording；
- 60 分钟；
- 0 sequence gaps。

45 fps 的 full-load gate 没通过，因此没有被采用。

### 当前 H.265 默认

PR #134 把 production OAK 录制切到 H.265，并完成一次真实三 trial Web session：

- 四路 1280×800；
- 每路 627 个 indexed frames；
- NAS verified；
- 本地 cleanup 完成；
- ffprobe 能从文件开头识别 HEVC。

但该样本仍有少量非致命 POC decoder warnings。

因此：

> 当前 30 fps H.265 是代码默认；此前 15 fps 的 60 分钟 soak 不能直接当成当前 H.265 配置的长时间验收。

## 自动分析

Session finalize 后会创建独立 job。

Analysis worker：

- 验证输入 hash；
- 读取 finalized artifact；
- replay semantic event log；
- 生成确定性的行为/QC JSON；
- 统计 outcome、reward request 和数据质量。

如果 global time 不完整，trial timing 就保持 unavailable，不用 Host receipt time 填一个假时间。

## NAS

NAS worker 只发布 finalized session artifact。

关键保护：

- mount 根目录必须有专用 marker；
- 复制先进入 `.incoming/<session_id>`；
- 按路径、字节数和 SHA-256 验证；
- 验证后原子发布到 `sessions/<session_id>`；
- 已经存在的发布目录只做验证，不覆盖。

这避免 NAS 掉线时，Pi 上一个普通空目录被误认为 NAS。

## W&B

W&B 在 analysis 与 NAS 都成功后运行。

上传的是：

- 解析后的配置；
- summary metrics；
- trial rows；
- behavior/QC；
- diagnostics；
- NAS destination reference。

原始视频、完整 event log 和 camera stream 不直接交给 W&B SDK。

## 飞书存档

最终 Feishu worker 等待：

1. analysis；
2. verified NAS；
3. W&B。

然后把固定 session index schema 发给中央 Broker。

按 session ID 先查再更新，因此远端已经成功、Pi 端重试时不会轻易重复创建多行。

## 本地清理

本地 cleanup 的必要条件是 **NAS 副本已验证**。

Analysis 失败本身不再阻止清理已经安全复制的原始数据。

当 session filesystem 使用率达到 90% 时，cleanup worker 会提前释放已经 verified 的可清理数据；它不会为了磁盘压力跳过 NAS 校验。

## 数据真值

如果 Web、W&B、飞书和本地 summary 之间出现冲突，排查顺序应该回到：

1. resolved session artifact；
2. event log；
3. recorder/camera manifest；
4. 原生 camera files；
5. 对应 hash。

飞书不是原始数据源。

### 相关源码与文档

- [ROS 2 protocol contract](https://github.com/QiuYi111/IBL/blob/main/software/host/rig-os/docs/protocols.md)
- [Camera integration](https://github.com/QiuYi111/IBL/blob/main/software/host/rig-os/docs/camera-integration.md)
- [Pi 5 camera soak](https://github.com/QiuYi111/IBL/blob/main/software/host/rig-os/docs/pi5-camera-soak-2026-09-21.md)
- [Native camera writer](https://github.com/QiuYi111/IBL/blob/main/software/host/rig-os/ros2_ws/src/rig_depthai/rig_depthai/recording.py)
