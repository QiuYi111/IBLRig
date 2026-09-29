---
title: "08 · Chaos / HIL"
weight: 90
summary: "用可重放随机事件持续测试重启、掉线、竞态、恢复和网页状态一致性。"
---

# Chaos / HIL

IBL Rig 带有一套独立的随机 HIL / Chaos 测试系统。

它会主动制造：

- 服务重启
- 进程暂停
- Pi 重启
- 网络短断
- MCU 复位
- OAK USB 恢复
- 相机服务故障
- ROS 2 节点扰动
- Web API 操作
- 浏览器状态检查

测试期间持续采集系统状态，并用规则自动判断系统行为。

## 整体结构

```text
外部测试电脑
│
├── Seed / Config
│       ↓
├── Event Plan
│       ↓
├── Control Channel ───────────────┐
├── Observation Channel ──────────┤
├── Web API / Browser ────────────┤
│                                 ▼
│                         Raspberry Pi 5
│                         ├── 本地测试代理
│                         ├── systemd
│                         ├── ROS 2
│                         ├── MCU / SWD
│                         ├── OAK / USB
│                         └── Web
│
├── Observer
├── Rule Engine
└── Failure Package
```

测试器运行在 Rig 外部，因此 Pi 重启期间仍能继续计时、记录和等待设备恢复。

## Seed 与完整事件计划

每次随机测试从一个 seed 开始。

系统先生成完整事件计划，再开始执行。

计划提前确定：

- 事件类型
- 目标设备
- 执行时间
- 参数
- 并发组
- 安全等级

完整计划会保存到测试结果中。

同一个计划可以直接 replay。

## 随机事件

事件带有状态感知和权重。

例如：

- 实验空闲时更常执行预检
- 设备运行时增加进程暂停和重启
- 故障状态下执行故障复位
- 相机工作时注入 USB 或相机服务事件

随机测试因此覆盖真实状态转换。

## 毫秒级并发

多个事件可以放进同一个 barrier。

例如：

```text
T0
├── +17 ms  暂停一个进程
├── +31 ms  读取 MCU
└── +44 ms  重启 ROS CLI daemon
```

这些事件一次性发到 Pi，由本地测试代理按照 Pi 自己的单调时钟调度。

当前实机 barrier 记录中，17 / 31 / 44 ms 三个事件的 dispatch jitter 保持在约 0.006–0.018 ms。

这类测试用于覆盖：

- 启动顺序变化
- 设备晚到
- 短暂卡顿
- 两个故障近同时发生
- 恢复过程中的竞态

## 持续观察

Chaos 测试使用独立观察通道持续采样。

当前长跑配置：

| 项目 | 当前值 |
|---|---:|
| 采样周期 | 500 ms |
| 单次轻量读取预算 | 1000 ms |
| MCU 深度检查 | 3 s |
| ROS 深度检查 | 3 s |
| 最大并发事件 | 3 |
| 并发 barrier 最大偏移 | 40 ms |

持续观察内容包括：

- systemd 服务状态
- 实验状态
- 设备状态
- 控制链路 owner
- MCU 状态
- OAK / USB
- ROS 2 graph
- Web 状态
- 浏览器状态
- CPU / 内存 / 温度 / 存储

## 自动规则

规则引擎持续检查系统约束。

当前核心规则覆盖：

- 故障状态保持锁存直到明确复位
- 重启后 Session 生命周期保持唯一
- 控制链路保持单 owner
- 状态新鲜度与网页显示一致
- 新 Session 使用新的 sequence / transfer 身份
- RUNNING 状态具备所需设备
- Host 或 MCU 异常时执行器进入安全状态
- MCU 状态超时进入故障状态
- 网页可用操作与后台允许操作一致
- Preflight 在限定时间内完成

规则在每个采样点持续计算。

## Web 端到端检查

Chaos 测试同时读取：

1. 后台当前允许的操作
2. 浏览器实际显示的操作
3. 后台再次读取的操作

浏览器状态因此可以和真实系统状态直接对比。

页面检查覆盖：

- 锁定配置
- 预检
- 开始实验
- 停止实验
- 复位故障
- 控制权
- Session 状态

## 当前实机长跑结果

当前保留的 20 分钟 ratRot Chaos 长跑：

| 项目 | 结果 |
|---|---:|
| Seed | 20260916 |
| 时长 | 20 min |
| 已执行事件 | 1091 |
| 计划采样 | 2402 |
| 完成采样 | 2237 |
| Rule violation | 0 |
| Light read median | 318 ms |
| Light read p90 | 459 ms |
| Light read p99 | 815 ms |
| 最差 light read | 1007 ms |
| 最大 sampling lag | 1008 ms |

系统状态观察的最长盲区约为 1 秒。

## 确定性回归矩阵

NO-OAK 确定性回归矩阵当前包含 48 个场景。

结果：

```text
48 matched
0 failed
0 evidence incomplete
```

覆盖场景包括：

- 正常实验路径
- abort 后恢复
- 控制链路重启
- 单 owner
- CRC / 重试 / sequence
- MCU reset
- 安全状态
- stale 状态
- Web 状态投影
- 相机需求
- 输出队列
- reward
- stimulus
- bounded chaos

## 故障场景验证

固定故障场景用于验证具体规则。

### 实验控制服务重启

当前 clean run：

- 12 个事件
- 385 个采样
- 0 violation
- 网页状态自动经历 IDLE → UNKNOWN → IDLE

### 双 owner 注入

测试器会创建第二个控制链路 owner，并检查单 owner 规则触发，同时收集完整现场。

## Failure Package

规则触发后，系统自动保存失败证据包。

典型内容：

```text
manifest.json
event-plan.json
events.jsonl
observations.jsonl
failures.json
systemd.json
journal.txt
kernel-journal.txt
dmesg.txt
ros.json
mcu.json
usb.json
drm.json
resources.json
browser-state.json
browser.png
versions.json
command-transcript.json
```

失败包记录：

- seed
- 完整事件顺序
- 精确时间
- 系统状态
- 日志
- 软件版本
- 固件版本
- 配置版本
- 触发的规则

一次随机故障可以直接重放和定位。

## 安全等级

每个 Chaos 事件都带安全等级。

从低到高：

1. `read_only`
2. `no_animal_dry`
3. `actuator_bounded`
4. `hardware_destructive`

一次测试使用固定 safety profile，并记录到结果中。

带电机、泵和 MCU 复位的事件使用明确预算控制每次运行的最大执行次数。

## 使用方式

完整命令、事件列表和规则列表见 [Chaos Reference](/IBLRig/reference/chaos/)。
