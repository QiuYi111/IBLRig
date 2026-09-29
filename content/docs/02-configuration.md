---
title: "02 · 配置文件"
weight: 30
baseline: "IBL main @ 6c2ea40"
summary: "模板库、revision、override、resolve、Trial 编译和训练状态。"
---

# 配置文件

Rig Web 使用 YAML 模板描述实验。模板经过 resolve 后变成固定 Session artifact。

## 模板库

模板分成两类目录：

```text
builtin templates
software/host/rig-os/ros2_ws/src/rig_web/templates/

user templates
/home/jingyi/rig-os/data/config/templates/
```

内置模板随代码发布。用户模板由 Web 管理。

当前内置模板：

```text
choice-world-formal-pretraining
choice-world-formal-training
choice-world-office-silent
choice-world-pretraining-auto-reward
choice-world-training-online
choice-world-training-phase0-hil
ratrot-training-choice-world-v2
verification-choice-world-fast-three
verification-choice-world-office-silent-no-oak
```

## TemplateStore

`TemplateStore` 提供完整版本管理：

- create
- version
- history
- rollback
- archive
- restore

用户模板首次创建为 revision 1。

保存新版本时：

```text
revision N
    ↓
保存到 .history/<template_id>/N.yaml
    ↓
新内容写成 revision N+1
    ↓
原子替换 active YAML
```

Template id 在整个 builtin + user catalog 中保持唯一。

## Schema v1

核心字段：

```yaml
schema_version: 1
template_id: example
revision: 1
display_name: Example
rig_id: ratrot
operating_mode: active_shaping
mode: online_policy

task:
  schema_version: 1
  task_type: training_choice_world
  plan: {}

online_policy: {}

session:
  protocol: ...
  notes: ...
  required_devices: []
```

### operating_mode

当前三种模式：

| 值 | ROS enum |
|---|---:|
| `maintenance` | 0 |
| `standard_compatibility` | 1 |
| `active_shaping` | 2 |

### mode

| 值 | 执行方式 |
|---|---|
| `precompiled` | 整场 Trial 预编译 |
| `online_policy` | 每个 outcome 后生成下一 Trial |

## Schema v2

v2 模板把 protocol 和 rig profile 分开。

当前 protocol id：

```text
ibl.training_choice_world
```

当前 rig profile：

```text
ratrot
```

加载时，configuration layer 把 v2 展开成 v1 execution template，再进入相同 resolve 流程。

## Override

Web policy 定义允许修改的路径。

Override 使用 dotted path，例如：

```text
task.plan.response_window_us
task.plan.feedback_error_us
online_policy.trial_cap
```

Resolve 会记录每项改动：

```yaml
override_diff:
  task.plan.response_window_us:
    before: 60000000
    after: 30000000
```

## Resolve 输出

一次 resolve 生成：

### `task.json`

最终 task 定义。

### `<sha>.trial-table.json`

MCU 可执行的编译 artifact。

Online policy 模式下，该 artifact 同时携带：

- session identity
- subject identity
- policy build
- plan template
- seed
- epoch
- trial cap
- training info
- state file name

### `session.json`

Session metadata：

- rig id
- operating mode
- protocol
- operator
- subject id
- template id
- template revision
- notes
- required devices

### `resolved.yaml`

完整锁定结果：

- template
- source SHA
- overrides
- override diff
- artifact SHA
- required devices

### `resolution.json`

Web / coordinator 使用的紧凑索引。

## Required devices

Required device 集合由编译结果计算。

`required_session_devices()` 读取 Trial 和 Session config，得到实际 capability 需求。

因此 Session 的设备需求与执行内容保持一致。

## 正式预训练

当前正式预训练：

```yaml
task_type: habituation_choice_world
positions_deg: [-35, 35]
contrast_set: [1.0]
trial_count: 400
lateral_mean_s: 10
lateral_sd_s: 2
center_pre_reward_us: 500000
reward:
  direction: reverse
  mode: duration
  duration_ms: 2000
reward_hold_us: 40000
center_post_reward_us: 460000
stimulus_ack_timeout_us: 3000000
required_time_quality: freerun
```

`seed_source: session` 让每个 Session 从 Session id 派生独立随机序列。

## 正式训练

当前正式训练：

```yaml
task_type: training_choice_world
protocol: ibl_pdf_v4_6
positions_deg: [-35, 35]
stimulus_reverse: true
wheel_radius_mm: 31
quiescence_threshold_deg: 2
quiescent_base_us: 200000
response_window_us: 60000000
feedback_correct_us: 2200000
feedback_error_us: 2000000
feedback_nogo_us: 2000000
iti_us: 500000
stimulus_ack_timeout_us: 3000000
sound_enabled: true
force_profile_id: 27
required_time_quality: freerun
```

Online policy：

```yaml
auto_history: true
trial_cap: 2000
```

## Training history

训练状态存放在：

```text
/home/jingyi/rig-os/data/training-policy/
```

Web 按 subject id 找最近完成的 policy snapshot，并恢复：

- training phase
- adaptive reward
- adaptive gain
- performance history
- phase trial counts

每个 snapshot 带 state digest 和 decision digest。

## Trial 随机性

Online Trial 的随机 seed 由：

```text
epoch
trial_id
policy_state_sha256
```

共同派生。

相同 policy state 与相同 Trial id 会得到相同编译结果。

## 参数 Reference

完整参数、默认值、单位和所在配置见：

[实验参数 Reference](/IBLRig/reference/configuration/)。
