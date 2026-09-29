---
title: "Daemon / systemd"
weight: 60
summary: "当前 systemd unit、触发方式、重启策略和后台任务。"
---

# Daemon / systemd Reference

## 核心服务

| Unit | 类型 | 启动方式 | Restart | 作用 |
|---|---|---|---|---|
| `ibl-rig-supervisor.service` | simple | 开机 | on-failure / 3 s | 实验控制、设备服务管理 |
| `ibl-rig-web.socket` | socket | sockets.target | — | 监听 TCP 18080 |
| `ibl-rig-web.service` | simple | socket activation | on-failure / 2 s | 网页控制台 |
| `ibl-rig-peer-monitor.service` | simple | 开机 | on-failure / 2 s | Tailnet peer 状态监看 |

## 实验控制服务

`ibl-rig-supervisor.service` 执行：

```bash
ros2 launch rig_bringup supervisor.launch.py
```

运行环境：

| 项目 | 当前值 |
|---|---|
| User | `jingyi` |
| Group | `jingyi` |
| ROS_DOMAIN_ID | 42 |
| RMW | CycloneDDS |
| CAP_SYS_NICE | enabled |
| RuntimeDirectory | `/run/ibl-rig` |
| CPUWeight | 1000 |
| MemoryLow | 64M |
| MemorySwapMax | 0 |
| OOMScoreAdjust | -500 |

该 service 内包含：

- 实验状态服务
- lifecycle manager
- 设备服务管理器

实验设备能力由它的子进程按需启动。

当前设备服务启动顺序：

| 顺序 | 能力 |
|---:|---|
| 10 | MCU |
| 20 | Calibration |
| 30 | Time |
| 40 | Diagnostics |
| 50 | Recorder |
| 60 | Task |
| 70 | Camera |
| 80 | Stimulus |

Camera 和 Stimulus 采用分阶段启动。

## Web socket

`ibl-rig-web.socket`：

```ini
ListenStream=0.0.0.0:18080
NoDelay=true
Service=ibl-rig-web.service
```

Web service 使用独立账号：

```text
User=ibl-rig-web
Group=ibl-rig-web
```

可写目录：

- `/var/lib/ibl-rig-web`
- `/home/jingyi/rig-os/data/compiled/web`
- `/home/jingyi/rig-os/data/config/templates`

## Post-session workers

### Analysis

Units：

- `ibl-rig-analysis.path`
- `ibl-rig-analysis.service`
- `ibl-rig-analysis.timer`

Path：

```text
/var/lib/ibl-rig-web/queue
```

Timer：

```text
OnBootSec=3min
OnUnitActiveSec=5min
```

Service 类型：oneshot  
Restart：on-failure / 5 s

### NAS

Units：

- `ibl-rig-nas.path`
- `ibl-rig-nas.service`
- `ibl-rig-nas.timer`

Timer：

```text
OnBootSec=3min
OnUnitActiveSec=5min
```

Restart：on-failure / 10 s

### W&B

Units：

- `ibl-rig-wandb.path`
- `ibl-rig-wandb.service`
- `ibl-rig-wandb.timer`

Timer：

```text
OnBootSec=3min
OnUnitActiveSec=5min
```

Restart：on-failure / 15 s

### Feishu

Units：

- `ibl-rig-feishu.path`
- `ibl-rig-feishu.service`
- `ibl-rig-feishu.timer`

Timer：

```text
OnBootSec=3min
OnUnitActiveSec=5min
```

Restart：on-failure / 15 s

### Cleanup

Units：

- `ibl-rig-cleanup.path`
- `ibl-rig-cleanup.service`
- `ibl-rig-cleanup.timer`

Timer：

```text
OnBootSec=5min
OnUnitActiveSec=10min
```

Restart：on-failure / 10 s

## Failure notification

`ibl-rig-supervisor.service` 和 `ibl-rig-web.service` 使用：

```ini
OnFailure=ibl-rig-notify-failure@%n.service
```

通知 unit：

```text
ibl-rig-notify-failure@.service
```

它以 oneshot 方式发送飞书故障通知。

Restart：on-failure / 30 s  
TimeoutStartSec：35 s

## 维护服务

### `ibl-rig-adaptive-wheel-demo.service`

运行受限的 M2006 adaptive-transparent demo。

Restart：no  
TimeoutStopSec：3 s

### `ibl-rig-pps-scope.service`

在 direct-KMS HDMI 上运行 PPS diagnostic scope。

Restart：on-failure / 5 s

## 设备恢复参数

设备服务管理器当前参数：

| 参数 | 当前值 |
|---|---:|
| 状态 freshness | 15 s |
| recovery grace | 60 s |
| stable reset window | 60 s |
| recovery cooldown | 300 s |
| max attempts | 3 |
| retry interval | 10 s |
| reconcile interval | 1 s |
| stop timeout | 45 s |

## MCU recovery

| Level | 动作 |
|---:|---|
| 1 | 重启 MCU capability process group |
| 2 | SWD reset STM32 |
| 3 | ST-Link USB reset → SWD reset → reopen control link |

## OAK recovery

| Level | 动作 |
|---:|---|
| 1 | 重启 Camera capability process group |
| 2 | USB re-enumeration → rebuild pipeline |
| 3 | USB recovery → rebuild pipeline |

## 常用命令

核心服务：

```bash
systemctl status ibl-rig-supervisor.service
systemctl status ibl-rig-web.socket
systemctl status ibl-rig-web.service
systemctl status ibl-rig-peer-monitor.service
```

后台任务：

```bash
systemctl status ibl-rig-analysis.service
systemctl status ibl-rig-nas.service
systemctl status ibl-rig-wandb.service
systemctl status ibl-rig-feishu.service
systemctl status ibl-rig-cleanup.service
```

定时器：

```bash
systemctl list-timers 'ibl-rig-*'
```

日志：

```bash
journalctl -u ibl-rig-supervisor.service
journalctl -u ibl-rig-web.service
```

精确状态：

```bash
systemctl show ibl-rig-supervisor.service   -p ActiveState -p SubState -p MainPID   -p NRestarts -p ExecMainStatus -p InvocationID
```
