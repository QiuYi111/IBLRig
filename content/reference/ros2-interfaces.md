---
title: "ROS 2 话题、服务与动作"
weight: 40
summary: "当前公开 ROS 2 接口速查。"
---

# ROS 2 话题、服务与动作

## Topics

### `/rig/session/status`

类型：`rig_msgs/msg/SessionStatus`

整场实验状态。

主要字段：

| 字段 | 含义 |
|---|---|
| `session_id` | 会话编号 |
| `state` | 实验状态 |
| `current_trial_id` | 当前 Trial |
| `completed_trials` | 已完成 Trial |
| `total_trials` | 总 Trial |
| `correct_trials` | 正确 |
| `incorrect_trials` | 错误 |
| `no_response_trials` | 无响应 |
| `reward_requested_total_nl` | 请求奖励总量 |
| `elapsed_time_ms` | 已用时间 |
| `estimated_remaining_ms` | 预计剩余时间 |
| `latest_trial_outcome` | 上一个结果 |
| `fault_reason` | 故障原因 |

状态值：

| 值 | 状态 |
|---:|---|
| 0 | UNCONFIGURED |
| 1 | INACTIVE |
| 2 | READY |
| 3 | RUNNING |
| 4 | PAUSED |
| 5 | STOPPING |
| 6 | FAULTED |
| 7 | FINALIZED |

### `/rig/device_health`

类型：`rig_msgs/msg/DeviceHealth`

设备健康状态。

状态：

| 值 | 状态 |
|---:|---|
| 0 | OK |
| 1 | WARN |
| 2 | ERROR |
| 3 | STALE |

字段：

- `device_id`
- `state`
- `code`
- `summary`
- `detail_json`

### `/rig/capabilities`

类型：`rig_msgs/msg/CapabilityManifest`

设备和服务能力清单。

字段：

- device id
- device type
- clock id
- firmware version
- actions
- events
- features

### `/rig/time/status`

类型：`rig_msgs/msg/TimeStatus`

时间同步状态。

状态：

| 值 | 状态 |
|---:|---|
| 0 | LOCKED |
| 1 | HOLDOVER |
| 2 | DEGRADED |
| 3 | FREERUN |
| 4 | FAULT |

字段：

- clock id
- offset
- uncertainty
- mapping version
- detail

### `/rig/events`

类型：`rig_msgs/msg/RigEvent`

行为和硬件事件流。

字段：

- sequence
- source device
- event type
- timestamp
- state before
- state after
- payload

### `/rig/wheel/state`

类型：`rig_msgs/msg/WheelState`

转轮实时状态。

字段：

- position rad
- velocity rad/s
- encoder count
- sample sequence
- device tick
- global time

### `/rig/motor/state`

类型：`rig_msgs/msg/MotorState`

M2006/C610 状态。

字段：

- commanded torque N·m
- measured current A
- temperature °C
- force profile id
- fault flags

### `/rig/stimulus/status`

类型：`rig_msgs/msg/StimulusStatus`

刺激屏状态。

字段：

- HDMI connector
- display connected
- width / height
- target FPS
- measured FPS
- frame index
- dropped frames
- queue depth
- cache statistics
- detail

### `/rig/stimulus/command`

类型：`rig_msgs/msg/StimulusCommand`

视觉刺激命令。

### `/rig/stimulus/presentation`

类型：`rig_msgs/msg/StimulusPresentation`

刺激屏显示结果和 page-flip 时间。

显示详情包含：

- Trial 编号
- 起始像素位置
- 当前像素位置
- 当前转轮-屏幕增益 `gain_px_per_deg`
- 响应阈值
- 转轮当前位置
- Trial 转轮参考位置
- 屏幕中心残差
- 闭环状态

### `/rig/sound/presentation`

类型：`rig_msgs/msg/SoundPresentation`

C Board 蜂鸣器行为声音记录。

### `/rig/recording/status`

类型：`rig_msgs/msg/RecordingStatus`

记录状态：

| 值 | 状态 |
|---:|---|
| 0 | IDLE |
| 1 | RECORDING |
| 2 | FINALIZING |
| 3 | FINALIZED |
| 4 | FAULTED |

字段：

- recording id
- session id
- event log URI
- records written
- bytes written
- fault reason

### `/rig/camera/frame_metadata`

类型：`rig_msgs/msg/FrameMetadata`

每个持久化视频 access unit 的索引。

字段：

- camera id
- device timestamp
- global time
- frame sequence
- exposure µs
- gain
- video URI
- file offset

### `/rig/diagnostics`

类型：`diagnostic_msgs/msg/DiagnosticArray`

系统诊断状态。

### `/rig/mcu/pps_status`

类型：`rig_mcu_msgs/msg/PpsStatus`

C Board 捕获的 PPS 状态。

## Services

### `/rig/get_status`

类型：`rig_msgs/srv/GetRigStatus`

返回当前 `SessionStatus`。

```bash
ros2 service call /rig/get_status rig_msgs/srv/GetRigStatus
```

### `/rig/get_capabilities`

类型：`rig_msgs/srv/GetCapabilities`

返回当前设备和服务能力。

### `/rig/camera/get_inventory`

类型：`rig_msgs/srv/GetCameraInventory`

请求：

- `refresh`

返回：

- success
- inventory JSON
- detail

```bash
ros2 service call /rig/camera/get_inventory   rig_msgs/srv/GetCameraInventory "{refresh: true}"
```

### `/rig/diagnostics/check_preflight`

类型：`rig_msgs/srv/CheckPreflight`

执行实验预检。

返回：

- passed
- failures
- report JSON

### `/rig/reset_fault`

类型：`rig_msgs/srv/ResetFault`

输入：

- fault id
- operator id
- reason

返回：

- accepted
- detail

### `/rig/task/load_table`

类型：`rig_msgs/srv/LoadTrialTable`

加载训练 Trial。

### `/rig/recording/prepare`

类型：`rig_msgs/srv/PrepareRecording`

开始本次实验记录。

### `/rig/recording/finalize`

类型：`rig_msgs/srv/FinalizeRecording`

结束实验记录并生成校验信息。

### `/rig/diagnostics/write_quality_report`

类型：`rig_msgs/srv/WriteQualityReport`

写入实验质量报告。

## Actions

### `/rig/run_session`

类型：`rig_msgs/action/RunSession`

运行整场实验。

结果：

- success
- completed trials
- event log URI
- recording manifest URI
- quality report URI
- detail

反馈：

- 当前状态
- 当前 Trial
- 已完成 Trial
- detail

### `/rig/run_calibration`

类型：`rig_msgs/action/RunCalibration`

运行标定流程。

反馈：

- progress
- step
- detail

结果：

- artifact URI
- artifact SHA-256
- detail

## 常用查询

```bash
ros2 topic echo /rig/session/status
ros2 topic echo /rig/device_health
ros2 topic echo /rig/time/status
ros2 topic echo /rig/wheel/state
ros2 topic echo /rig/motor/state
ros2 topic echo /rig/recording/status
ros2 topic echo /rig/stimulus/status
```
