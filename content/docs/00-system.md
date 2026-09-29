---
title: "00 · 认识系统"
weight: 10
baseline: "IBL main @ 6c2ea40"
summary: "从一场实验看清 MCU、ROS 2、Web、相机、显示和数据链。"
---

# 认识系统

IBL Rig 把一场行为训练拆成三个执行层：

```text
Browser / Feishu
      │
      │ HTTP / WebSocket
      ▼
Rig Web ──────────────── Session configuration / control
      │
      │ ROS 2
      ▼
Rig Supervisor ──────── Session authority + Runtime Graph
      │
      ├── Task Compiler
      ├── Recorder
      ├── Diagnostics
      ├── Stimulus Server ─── HDMI display
      ├── DepthAI Manager ─── OAK-FFC-4P
      └── Controller Gateway
                │
                │ SWD / fixed SRAM ABI
                ▼
        STM32F407 / FreeRTOS
                │
                ├── wheel input
                ├── M2006 + C610
                ├── peristaltic pump
                ├── TTL / PPS
                └── Trial FSM
```

## 一场实验的主链路

### 1. 配置

Rig Web 从模板库读取 YAML。操作者选择模板、填写 subject、应用允许的参数修改，然后执行 resolve。

Resolve 会生成一组固定 artifact：

```text
resolved.yaml
task.json
<sha>.trial-table.json
session.json
resolution.json
```

每个文件都有 SHA-256。Session 启动时，Supervisor 使用这些 artifact 作为输入。

### 2. Runtime Graph

Supervisor 根据 Session artifact 计算需要的 capability。

常见 capability 包括：

- `mcu`
- `stimulus`
- `camera`
- `recorder`
- `diagnostics`
- `time`
- `task`
- `calibration`

Runtime Manager 订阅 `/rig/runtime/graph`，按当前 graph 启停对应 launch。每个 capability 以独立进程组运行，并发布 `CapabilityManifest` 和 `DeviceHealth`。

### 3. Trial 编译

训练任务分成两种执行方式：

**Precompiled**

整场 Trial 在 Session 开始前编译成有限状态表。

**Online policy**

Host 保存训练策略状态。每完成一个 Trial，Gateway 根据 MCU 返回的 outcome 请求下一个 Trial，再把新的 Trial 编译成固定表并发送给 MCU。

两种方式最终都得到同一种 MCU 执行对象：有界 Trial table。

### 4. MCU 执行

STM32F407 负责 Trial 的实时执行。

典型 ChoiceWorld Trial 包含：

```text
trial_start
    ↓
quiescent_period
    ↓
show stimulus
    ↓
interactive delay
    ↓
go tone
    ↓
closed loop
    ↓
response window
    ├── correct
    ├── incorrect
    └── no response
    ↓
feedback / reward
    ↓
ITI
```

轮子阈值、奖励动作、电机 profile、TTL 和状态转换都在 MCU 本地执行。

## 视觉刺激

Stimulus Server 运行在 Pi 上，使用 direct-KMS 输出到 HDMI。

公开命令包括：

- `PRELOAD`
- `SHOW`
- `CLOSED_LOOP`
- `FREEZE`
- `FREEZE_CENTER`
- `HIDE`

渲染器目标模式为 1920 × 1080 @ 60 Hz。每次显示命令完成后发布 `StimulusPresentation`，包含 command id、page-flip 时间、frame index 和显示状态。

闭环视觉使用 MCU 同一 Trial 的 wheel reference。屏幕位置由 Trial 初始位置、wheel reference 和 Trial gain 共同确定。

## 声音

Audio Server 使用 PortAudio 生成行为声音。

当前提供：

- 5 kHz、100 ms go tone
- 500 ms error white noise
- 48 kHz stereo output

第一次 PortAudio output callback 作为软件 onset acknowledgement，经 `SoundPresentation` 返回。

## 相机

当前相机为 OAK-FFC-4P，连接四个 1280 × 800 global-shutter sensor：

- CAM_A：OV9782，彩色
- CAM_B/C/D：OV9282，黑白

当前生产配置：

- 30 fps
- H.265
- 12 Mbps / camera
- USB 3
- 4 路同步分组
- CAM_A 主预览
- MJPEG 浏览器预览

DepthAI Manager 在设备端完成编码。录制线程把 H.265 access unit 直接写入 Session 目录，同时发布精确的 frame metadata。

## Recorder

Recorder Manager 创建 Session 目录并打开 append-only JSONL event log。

它记录：

- MCU semantic event
- stimulus command
- stimulus presentation
- sound presentation
- session command
- camera frame metadata
- device health
- time status

Finalize 时执行 fsync、计算 SHA-256，并写 manifest。

## 实验后处理

Session finalize 后创建持久化 jobs：

```text
analysis
   ├── nas
   └── wandb
         └── feishu
nas ─────────┘
   └── cleanup
```

具体内容：

- **analysis**：重放 event log，生成 behavior/QC
- **NAS**：复制并逐文件校验
- **W&B**：上传配置、行为指标和 QC
- **Feishu**：写入 Session 索引
- **cleanup**：清理已经完成 NAS 校验的本地文件

## 系统状态入口

调系统时最有用的四个状态源：

| 状态 | Topic |
|---|---|
| Session | `/rig/session/status` |
| Runtime | `/rig/runtime/status` |
| Device | `/rig/device_health` |
| Capability | `/rig/capabilities` |

详细接口见 [ROS 2 Reference](/IBLRig/reference/ros2-interfaces/)。

## 代码入口

- [Rig OS](https://github.com/QiuYi111/IBL/tree/main/software/host/rig-os)
- [Supervisor](https://github.com/QiuYi111/IBL/tree/main/software/host/rig-os/ros2_ws/src/rig_supervisor)
- [Controller Gateway](https://github.com/QiuYi111/IBL/tree/main/software/host/rig-os/ros2_ws/src/rig_controller_gateway)
- [DepthAI](https://github.com/QiuYi111/IBL/tree/main/software/host/rig-os/ros2_ws/src/rig_depthai)
- [Stimulus](https://github.com/QiuYi111/IBL/tree/main/software/host/rig-os/ros2_ws/src/rig_stimulus)
- [Recorder](https://github.com/QiuYi111/IBL/tree/main/software/host/rig-os/ros2_ws/src/rig_recorder)
