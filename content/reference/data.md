---
title: "数据文件"
weight: 50
summary: "实验目录、行为日志、视频、帧索引、质量报告和分析结果。"
---

# 数据文件

## Session root

```text
/home/jingyi/rig-os/data/sessions/<session_id>/
```

每场实验对应一个独立目录。

## 行为事件文件

文件名：

```text
<recording_id>.events.jsonl
```

格式：JSON Lines。

每行一条记录。

常见 `kind`：

- `session_start`
- `rig_event`
- `stimulus_command`
- `stimulus_presentation`
- `sound_presentation`
- `session_command`
- `camera_frame_metadata`
- `device_health`
- `time_status`
- `session_end`

## Recording manifest

文件名：

```text
<recording_id>.manifest.json
```

主要字段：

- schema version
- recording id
- session id
- subject id
- records written
- event log URI
- event log SHA-256
- session metadata
- finalized time

## Video directory

```text
<session_id>/video/
```

当前包含四路 H.265。

文件命名：

```text
<camera_id>.h265
<camera_id>.frames.jsonl
<camera_id>.camera-manifest.json
camera-recording-manifest.json
```

## Camera IDs

四路物理 socket：

- CAM_A
- CAM_B
- CAM_C
- CAM_D

录像文件中的 camera id 由当前相机配置生成，并与 socket 一一对应。

## Frame index

文件：

```text
<camera_id>.frames.jsonl
```

每行字段：

| 字段 | 含义 |
|---|---|
| `schema_version` | schema |
| `camera_id` | 相机 |
| `frame_sequence` | 帧序号 |
| `device_timestamp_ns` | 相机时间戳 |
| `exposure_us` | 曝光 |
| `gain` | 增益 |
| `native_file_offset` | H.265 文件 byte offset |
| `encoded_size` | access unit 大小 |
| `encoded_sha256` | access unit SHA-256 |

## 闭环视觉记录

每次刺激显示记录中包含当前画面的闭环参数：

| 字段 | 含义 |
|---|---|
| `trial_id` | Trial 编号 |
| `start_position_px` | 刺激起始像素位置 |
| `position_px` | 当前刺激像素位置 |
| `start_position_deg` | 起始视觉角度 |
| `visual_position_deg` | 当前视觉角度 |
| `gain_px_per_deg` | 当前转轮-屏幕增益，px/轮角° |
| `response_threshold_rad` | 当前响应阈值 |
| `center_residual_px` | 到达响应阈值时距离中心的像素残差 |
| `wheel_position_rad` | 当前转轮角度 |
| `wheel_reference_rad` | 当前 Trial 的转轮参考位置 |
| `closed_loop` | 闭环显示状态 |

这些字段可以把转轮运动、行为判定和屏幕位置放到同一条 Trial 记录中。

## Camera manifest

文件：

```text
<camera_id>.camera-manifest.json
```

主要字段：

- camera id
- device id
- codec
- width / height
- FPS
- bitrate
- frame count
- sequence gap count
- first / last sequence
- first / last device timestamp
- bytes written
- video SHA-256
- frame index SHA-256

## Multi-camera manifest

文件：

```text
camera-recording-manifest.json
```

主要字段：

- camera count
- total frames
- total sequence gaps
- 四路 camera manifest

## Quality report

实验结束时生成 quality report。

质量项包括：

- event sequence gaps
- event source restarts
- frame sequence gaps
- reported data loss
- time mapping

## Analysis

目录：

```text
<session_id>/analysis/
```

当前报告：

```text
behavior-qc-v1.json
```

### Behavior

字段：

- trial count
- outcome counts
- accuracy
- accuracy denominator
- requested reward count
- requested reward total
- timing statistics

### Trials

每个 Trial：

- trial id
- outcome
- start time
- end time

### Quality

字段：

- state
- replay sequence gaps
- source restarts
- mapping versions
- global time complete
- diagnostics

质量状态：

- `pass`
- `degraded`
- `fail`

## 配置文件

实验配置保存在：

```text
/home/jingyi/rig-os/data/compiled/web/<session_id>/
```

目录包含：

- 最终 YAML
- task JSON
- Trial table
- session config
- resolution record

## Training history

目录：

```text
/home/jingyi/rig-os/data/training-policy/
```

按小鼠保存连续训练状态。

## NAS

NAS 目录：

```text
sessions/<session_id>/
```

发布完成后包含：

```text
ibl-rig-copy-v1.json
```

该文件记录 NAS 中的文件列表、大小和校验值。

## W&B

每场实验对应一个 run。

常用 summary：

- `trial_count`
- `accuracy`
- `requested_reward_count`
- `requested_reward_total_nl`
- `quality_state`
- `global_time_complete`
- `outcome/correct`
- `outcome/incorrect`
- `outcome/no_response`

## 飞书

飞书记录用于索引：

- session
- rig
- operator
- subject
- template
- task
- quality
- W&B
- NAS
