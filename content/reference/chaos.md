---
title: "Chaos / HIL"
weight: 70
summary: "测试命令、事件类型、规则、安全等级和证据格式。"
---

# Chaos / HIL Reference

代码目录：

```text
tools/rig-chaos/
```

## 基本命令

进入工具目录：

```bash
cd tools/rig-chaos
```

查看事件：

```bash
uv run rig-chaos events
```

查看规则：

```bash
uv run rig-chaos rules
```

检查配置：

```bash
uv run rig-chaos check --config configs/ratrot.yaml
```

安装 Pi 本地测试代理：

```bash
uv run rig-chaos install-agent --host ratRot
```

执行实机预检：

```bash
uv run rig-chaos preflight   --config configs/ratrot.yaml   --platform live   --ack "operator confirms no animal is on the rig"   --ack "motor and pump stay disabled for this run"
```

执行：

```bash
uv run rig-chaos run   --config configs/ratrot.yaml   --platform live   --ack "operator confirms no animal is on the rig"
```

回放：

```bash
uv run rig-chaos replay runs/<run-directory>
```

## Safety profiles

| Profile | 用途 |
|---|---|
| `read_only` | 状态读取、网页检查、日志 |
| `no_animal_dry` | 进程、服务、网络、设备生命周期扰动 |
| `actuator_bounded` | MCU reset、有限 Session、有限输出事件 |
| `hardware_destructive` | 高风险硬件故障注入 |

配置示例：

```yaml
safety:
  profile: actuator_bounded
  max_actuator_events_per_run: 8
```

## Event groups

### systemd / process

- `systemd.restart`
- `systemd.stop`
- `systemd.start`
- `unit.crash`
- `process.signal`
- `pi.reboot`

### Capability

- `capability.signal`
- `capability.crash`
- `capability.restart`

目标示例：

```text
capability:mcu
capability:camera
capability:stimulus
```

### Network

- `net.flap`
- `net.link`

### ROS 2

- `ros.node.restart`
- `ros.daemon.restart`

`ros2 daemon` 负责 ROS 2 CLI graph cache；Rig 的实验服务由 systemd 和 ROS 2 节点运行。

### MCU

- `mcu.reset`
- `mcu.status`
- `telemetry.stop`
- `telemetry.start`
- `mcu.telemetry.pause`
- `mcu.telemetry.resume`

### Controller link

- `controller_link.probe`
- `controller_link.mcu_reset`
- `controller_link.gateway_restart`
- `controller_link.bus_error`
- `controller_link.nack`
- `controller_link.fake_transport`
- `controller_link.command`

### Stimulus

- `stimulus.preload`
- `stimulus.show`
- `stimulus.hide`
- `stimulus.freeze`

### Safety

- `safety.lease.pause`
- `safety.lease.resume`

### Outputs

- `reward.request`
- `motor.command`

### Peripherals

- `oak.service.restart`
- `oak.service.crash`
- `oak.usb.reset`
- `usb.reset`
- `usb.rebind`
- `stimulus.service.restart`
- `timing.consumer.stop`

### Web

- `api.preflight`
- `api.session.start`
- `api.session.stop`
- `api.reset_fault`
- `api.session.control`
- `ws.disconnect`
- `browser.check`

### Observation

- `state.snapshot`
- `journal.tail`
- `kernel.log`
- `watchdog.resets`

## Long-run config

当前 `configs/ratrot-long.yaml`：

| 参数 | 当前值 |
|---|---:|
| duration | 1,200,000 ms |
| delay range | 400–1500 ms |
| burst probability | 0.15 |
| burst max | 60 ms |
| max concurrent events | 3 |
| barrier probability | 0.35 |
| barrier max offset | 40 ms |
| sample interval | 500 ms |
| sample budget | 1000 ms |
| MCU deep probe | 3000 ms |
| ROS deep probe | 3000 ms |
| actuator budget | 8 |

## Core rules

当前 long-run 配置启用：

- `RULE-FAULT-STICKY`
- `RULE-NO-SESSION-AFTER-RESTART`
- `RULE-SPI-SINGLE-OWNER`
- `RULE-STALE-NOT-HEALTHY`
- `RULE-NO-STALE-MARKER`
- `RULE-NO-OLD-SEQUENCE`
- `RULE-RUNNING-REQUIRES-DEVICES`
- `RULE-UI-ACTIONS`
- `RULE-ACTUATOR-SAFE-ON-LOSS`
- `RULE-MCU-TIMEOUT-FAULT`
- `RULE-PREFLIGHT-BOUNDED`

## Barrier timing

Barrier 中每个事件都有：

| 字段 | 含义 |
|---|---|
| `planned_offset_ms` | 计划开始时间 |
| `dispatch_offset_ms` | Pi 实际开始时间 |
| `completed_offset_ms` | 完成时间 |
| `dispatch_jitter_ms` | 调度误差 |
| `duration_ms` | 执行耗时 |

当前 ratRot 示例：

```text
process.signal
planned 517.0 ms
dispatch 517.014 ms
jitter 0.014 ms

mcu.status
planned 531.0 ms
dispatch 531.018 ms
jitter 0.018 ms

ros.daemon.restart
planned 544.0 ms
dispatch 544.006 ms
jitter 0.006 ms
```

## Sampling

每个 sample 记录：

- planned time
- actual time
- sampling lag
- read duration
- 各观察项耗时
- systemd
- ROS
- MCU
- Web
- peripherals

`sampling.json` 汇总：

- scheduled
- taken
- missed
- worst read
- worst lag

## Failure package

失败包目录通常包含：

- `manifest.json`
- `event-plan.json`
- `events.jsonl`
- `observations.jsonl`
- `failures.json`
- `systemd.json`
- `journal.txt`
- `kernel-journal.txt`
- `dmesg.txt`
- `ros.json`
- `mcu.json`
- `usb.json`
- `drm.json`
- `resources.json`
- `browser-state.json`
- `browser.png`
- `versions.json`
- `command-transcript.json`

## 当前 evidence

### 20 分钟实机长跑

`RATROT-CHAOS-LONG-002`

| 项目 | 结果 |
|---|---:|
| Seed | 20260916 |
| 已执行事件 | 1091 |
| 完成采样 | 2237 / 2402 |
| Violation | 0 |
| Median read | 318 ms |
| p90 | 459 ms |
| p99 | 815 ms |
| Worst read | 1007 ms |
| Worst lag | 1008 ms |

### UI projection

`RATROT-UI-PROJECTION-002`

- 12 events
- 68 samples
- 0 violations

### 实验控制服务重启

`RATROT-FAULT-LIVE-002`

- 12 events
- 385 samples
- 0 violations
- UI projection: IDLE → UNKNOWN → IDLE

### Deterministic matrix

`NO-OAK-DETERMINISTIC-001`

- platform: sim
- 48 matched
- 0 failed
- 0 evidence incomplete
