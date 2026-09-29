---
title: "实验与设备参数"
weight: 10
summary: "正式预训练、正式训练、相机、显示和声音参数。"
---

# 实验与设备参数

## 正式预训练

配置：`choice-world-formal-pretraining`

| YAML 字段 | 当前值 | 单位 | 含义 |
|---|---:|---|---|
| `trial_count` | 400 | Trial | 单场 Trial 上限 |
| `positions_deg` | [-35, 35] | ° | 左右刺激起始位置 |
| `contrast_set` | [1.0] | 0–1 | 刺激对比度 |
| `orientation_deg` | 0 | ° | Gabor 条纹方向 |
| `spatial_frequency_cpd` | 0.1 | cycles/° | 空间频率 |
| `sigma_deg` | 7 | ° | Gabor 包络 σ |
| `phase_max_rad` | π | rad | 随机相位范围 |
| `grey_period_us` | 1,000,000 | µs | 灰屏时间 |
| `lateral_mean_s` | 10 | s | 侧边刺激平均停留时间 |
| `lateral_sd_s` | 2 | s | 侧边停留时间标准差 |
| `center_pre_reward_us` | 500,000 | µs | 刺激到中心后等待奖励 |
| `reward.direction` | reverse | — | 奖励泵方向 |
| `reward.mode` | duration | — | 奖励按持续时间执行 |
| `reward.duration_ms` | 2000 | ms | 奖励泵动作时长 |
| `reward_hold_us` | 40,000 | µs | 奖励开始后的保持时间 |
| `center_post_reward_us` | 460,000 | µs | 奖励后的中心显示时间 |
| `stimulus_ack_timeout_us` | 3,000,000 | µs | 刺激显示确认等待时间 |
| `required_time_quality` | freerun | — | 实验要求的时间状态 |

每场预训练使用会话编号生成独立随机种子。

## 正式训练

配置：`choice-world-formal-training`

| YAML 字段 | 当前值 | 单位 | 含义 |
|---|---:|---|---|
| `protocol` | ibl_pdf_v4_6 | — | 训练协议 |
| `positions_deg` | [-35, 35] | ° | 左右刺激位置 |
| `stimulus_reverse` | true | — | 转轮与刺激方向映射 |
| `orientation_deg` | 0 | ° | Gabor 条纹方向 |
| `spatial_frequency_cpd` | 0.1 | cycles/° | 空间频率 |
| `sigma_deg` | 7 | ° | Gabor 包络 σ |
| `phase_max_rad` | π | rad | 随机相位范围 |
| `wheel_radius_mm` | 31 | mm | 转轮半径 |
| `quiescence_threshold_deg` | 2 | ° | Trial 前允许的转轮运动阈值 |
| `quiescent_base_us` | 200,000 | µs | 基础静止时间 |
| `quiescence_wait_budget_us` | 600,000,000 | µs | 等待静止的最长时间 |
| `interactive_delay_us` | 0 | µs | 刺激出现到响应阶段的额外延迟 |
| `response_window_us` | 60,000,000 | µs | 响应窗口 |
| `reward.mode` | duration | — | 奖励按持续时间执行 |
| `reward.direction` | reverse | — | 奖励泵方向 |
| `reward.duration_ms` | 2000 | ms | 奖励泵动作时长 |
| `feedback_correct_us` | 2,200,000 | µs | 正确反馈 |
| `feedback_error_us` | 2,000,000 | µs | 错误反馈 |
| `feedback_nogo_us` | 2,000,000 | µs | 无响应反馈 |
| `iti_us` | 500,000 | µs | Trial 间隔 |
| `stimulus_ack_timeout_us` | 3,000,000 | µs | 刺激显示确认等待时间 |
| `sound_enabled` | true | — | 行为声音 |
| `sync_pulse_us` | 100 | µs | 同步脉冲宽度 |
| `force_profile_id` | 27 | — | 转轮力反馈 profile |
| `required_time_quality` | freerun | — | 实验要求的时间状态 |
| `online_policy.trial_cap` | 2000 | Trial | 单场 Trial 上限 |
| `online_policy.auto_history` | true | — | 自动延续同一小鼠训练状态 |

## 训练阶段自动延续

正式训练按小鼠编号读取之前保存的训练状态，并延续：

- 训练阶段
- 刺激条件统计
- 表现窗口
- 奖励设置
- 转轮增益
- 阶段 Trial 数

小鼠编号是训练历史的主索引。

## 相机参数

当前 OAK-FFC-4P 参数：

| 参数 | 当前值 | 含义 |
|---|---:|---|
| Resolution | 1280 × 800 | 四路传感器采集分辨率 |
| FPS | 30 | 每秒帧数 |
| Codec | H.265 | 原始录像编码 |
| Bitrate | 12,000 kbps / camera | 每路编码码率 |
| MJPEG quality | 70 | 浏览器预览质量 |
| Sync window | 50 ms | 四路帧时间归组窗口 |
| USB | USB 3 | 主机数据链路 |
| Main preview | CAM_A | 默认主预览 |
| Main preview stride | 1 | 主画面每帧输出 |
| Thumbnail stride | 3 | 缩略图每 3 帧输出 1 帧 |

## 刺激显示参数

| 参数 | 当前值 | 含义 |
|---|---:|---|
| 分辨率 | 1920 × 1080 | 刺激屏模式 |
| 刷新目标 | 60 Hz | 渲染目标帧率 |
| `pixels_per_degree` | 20 px/° | 视觉角度到像素换算 |
| `visual_gain_deg_per_rad` | 57.2957795 | 默认转轮角到视觉角换算 |
| 背景亮度 | 0.5 | 中性灰背景 |
| 光电标记 | 80 px | 屏幕角落同步方块 |
| 缓存表面数 | 32 | 预生成刺激缓存 |
| 命令队列深度 | 64 | 待显示命令容量 |
| HDMI connector | HDMI-A-2 | 当前刺激输出 |

## 行为声音参数

当前训练声音由 C Board 蜂鸣器产生。

| 声音 | 当前参数 |
|---|---|
| Go tone | 4 kHz，100 ms |
| Error sound | 2 kHz / 4 kHz 交替 |
| Error segment | 50 ms |
| Error segments | 10 |
| Error total | 500 ms |
| 蜂鸣器输出 | PD14 / TIM4_CH3 |
| 蜂鸣器频率范围 | 100–10,000 Hz |

## 奖励泵参数

| 参数 | 当前值 |
|---|---:|
| STEP rate | 12,000 pulse/s |
| Microstep | 1/32 |
| STEP pin | PE9 / TIM1_CH1 |
| DIR pin | PE11 |
| 校准脉冲数 | 14,399,993 |
| 校准体积 | 5.5 mL |
| 换算 | 0.381944630 nL/pulse |
| 换算 | 2618.180545 pulse/µL |
| 当前连续流量 | 约 0.275 mL/min |
| 队列容量 | 200 µL |

## 预检相关参数

| 项目 | 当前值 |
|---|---:|
| 最低剩余存储 | 5 GB |
| 设备状态刷新 | 约 1 s |
| 相机启动等待 | 20 s |
| 相机录像启动等待 | 5 s |
| PPS 超时 | 2.5 s |

这些参数主要用于网页预检和设备状态显示。
