---
title: "02 · 配置文件"
weight: 30
baseline: "IBL main @ 6c2ea40 · 2026-09-28"
summary: "配置不是一份随手改的 YAML：模板经过解析、override、编译和哈希锁定后才成为 session 的执行输入。"
---

IBL Rig 的配置系统解决两个问题：

1. **人要能方便地选择和修改实验参数。**
2. **真正运行时必须知道“到底运行了哪一份配置”。**

因此，系统把“模板”和“执行 artifact”分开。

## 从模板到 Session

```text
Template YAML
    ↓
用户选择 subject / overrides
    ↓
权限策略检查 + diff
    ↓
Resolved configuration
    ├─ task.json
    ├─ compiled trial table / online-policy descriptor
    ├─ session.json
    └─ resolved.yaml
    ↓
SHA-256 锁定
    ↓
Supervisor / Gateway 执行
```

每个 session 使用 UUID。解析完成后，artifact 被写入独立目录；如果同一 session 已存在，系统拒绝覆盖。

## 模板的基本结构

典型模板包含：

| 字段 | 作用 |
|---|---|
| `template_id` / `revision` | 模板身份与版本 |
| `rig_id` | 目标 rig |
| `operating_mode` | 运行模式 |
| `task` | task type 与 plan |
| `online_policy` | 需要逐 trial 决策时的策略状态 |
| `session` | protocol、notes、required devices 等 session 元数据 |

Web 不把 `required_devices` 当作最终设备清单。真正需要哪些能力由编译后的 task 与 session artifact 推导，避免调用方随意声明“这场实验不需要某个实际会被用到的设备”。

## 参数与物理意义

下面列的是当前 ChoiceWorld 路径常见参数。

| 参数 | 物理意义 |
|---|---|
| `positions_deg` | 刺激初始视角位置 |
| `contrast` / contrast set | 视觉对比度 |
| `orientation_deg` | Gabor 方向 |
| `spatial_frequency_cpd` | 空间频率 |
| `sigma_deg` | Gabor 尺寸 |
| `quiescent_base_us` | 静止窗口基准时间 |
| `quiescence_threshold_deg` | 静止判据对应的轮动阈值描述 |
| `response_window_us` | 允许响应的窗口 |
| `reward` | 奖励模式、方向和持续时间/体积 |
| `feedback_correct_us` | 正确反馈持续时间 |
| `feedback_error_us` | 错误反馈持续时间 |
| `iti_us` | trial 间隔 |
| `force_profile_id` | MCU 电机/触觉 profile |
| `required_time_quality` | session 对时间质量的最低要求 |

这些值最终要进入 trial 合同，或者成为编译器明确处理的 session 参数。不能把一个“看起来没被用”的字段默认理解为无害。

## 当前正式预训练模板

当前 `main` 中的 `choice-world-formal-pretraining.yaml`：

- 左右位置：±35°；
- contrast：1.0；
- 侧面刺激约 10 ± 2 s；
- 到中央后 0.5 s 请求奖励；
- 奖励默认反转 2 s；
- 请求奖励后约 0.5 s 隐藏；
- 400 trial 是上限，不代替每日训练时长安排；
- session seed 由 session 身份派生，避免每场重复相同随机序列。

仓库文档明确说明：声音/定时给水等部分是当前实现相对 PDF v4.6 的例外，不能把 2 s 奖励直接解释为某个固定 µL。

## 当前正式训练模板

当前 `main` 中正式训练模板 revision 为 1，使用独立的 `ibl_pdf_v4_6` online policy。

关键点：

- 六阶段训练；
- ±35°位置；
- 自动读取同一 subject 的训练历史；
- 首场必须明确声明没有旧历史；
- 已经有历史时禁止把动物重新声明成“新动物”；
- 阶段、成绩窗口、增益等状态跨 session 继承；
- 奖励当前仍按用户定制为反转 2 s；
- 正确反馈扩展到 2.2 s 以覆盖泵动作。

当前 `main` 仍使用 `wheel_radius_mm: 31.0` 的配置路径。仓库中今天出现的 direct wheel-to-screen gain 改动位于未合并分支，不属于本站当前基线。

## 为什么要锁定和哈希

配置系统会保存：

- 模板源文件哈希；
- task source 哈希；
- compiled table 哈希；
- session config 哈希；
- resolved YAML 哈希；
- override diff。

这样实验结束后可以回答：

> 这只动物、这一场、到底执行了哪一个 trial 逻辑？

而不是只能回答“当时应该是那个 YAML”。

## 自动训练历史

正式 PDF 路径支持 `auto_history`。

系统不会把“历史目录打不开”解释成“这只动物没有历史”。目录不可读、历史不完整、快照校验失败、上一场尚未结束都会 fail closed。

这是训练状态的一部分，不是 UI 便利功能。

## 修改配置的原则

推荐：

- 从模板库复制后修改；
- 只改 Web 明确允许的字段；
- 看 diff；
- 每次 session 生成新的 resolved artifact；
- 模板含义改变时升级 revision。

不要：

- session 开始后直接改生成文件；
- 手工修改哈希；
- 用旧 resolved artifact 假装新 session；
- 因为某个设备“不想用”就手写 required device 清单绕过编译结果。

### 相关源码与文档

- [Web configuration implementation](https://github.com/QiuYi111/IBL/blob/main/software/host/rig-os/ros2_ws/src/rig_web/rig_web/configuration.py)
- [Formal pretraining template](https://github.com/QiuYi111/IBL/blob/main/software/host/rig-os/ros2_ws/src/rig_web/templates/choice-world-formal-pretraining.yaml)
- [Formal training template](https://github.com/QiuYi111/IBL/blob/main/software/host/rig-os/ros2_ws/src/rig_web/templates/choice-world-formal-training.yaml)
- [Formal protocol status](https://github.com/QiuYi111/IBL/blob/main/software/host/rig-os/docs/formal-pdf-protocol.md)
