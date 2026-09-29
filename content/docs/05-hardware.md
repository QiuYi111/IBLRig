---
title: "05 · 硬件介绍"
weight: 60
summary: "主机、控制器、电机、奖励泵、相机、显示、同步、照明、电源和机械结构。"
---

# 硬件介绍

IBL Rig 的硬件围绕一件事组织：让小鼠在转轮上完成 ChoiceWorld 训练，同时得到稳定的视觉刺激、力反馈、奖励和四路视频记录。

## 整机

当前整机机械版本为 R5。

整机尺寸约：

```text
300 × 300 × 312.7 mm
```

R5 包含：

- V3-ENG P4 主机构
- 两个 CNC V4 PadHolder
- MouseCover
- 四个紧凑相机/照明模块 R2
- 转轮与 M2006
- 刺激显示器
- 四路相机
- 奖励液路
- 控制与供电模块

四个相机/照明模块安装在整机四周，模块支持约 ±30° 俯仰调整。

## Raspberry Pi 5

Raspberry Pi 5 是实验主机。

当前设备：

| 项目 | 参数 |
|---|---|
| CPU | Broadcom BCM2712 |
| CPU 核心 | 4 × Arm Cortex-A76 |
| 主频 | 2.4 GHz |
| 内存 | 8 GB LPDDR4X |
| USB 3 | 2 × 5 Gbps |
| 网口 | Gigabit Ethernet |
| PCIe | PCIe 2.0 ×1 |
| 系统 | Ubuntu 24.04 |
| ROS | ROS 2 Jazzy |

官方规格还提供双 4K60 HDMI 输出和硬件 HEVC 解码能力。

### 在 IBL Rig 中怎么用

Pi 5 负责：

- 网页控制台
- ROS 2 实验服务
- H.265 视频落盘
- 视觉刺激
- 行为声音
- 数据分析
- NAS 上传
- W&B 和飞书同步

系统从 microSD 启动，实验数据写入 256 GB SK hynix BC711 NVMe。

项目、录像、日志和缓存均放在 NVMe。

官方规格：
[Raspberry Pi 5](https://www.raspberrypi.com/products/raspberry-pi-5/)

## RoboMaster 开发板 C 型

RoboMaster C Board 是整套装置的实时控制器。

核心 MCU 为 STM32F407 系列，运行 FreeRTOS。

开发板官方规格：

| 项目 | 参数 |
|---|---|
| 输入电压 | 8–28 V |
| 当前供电 | 24 V |
| 工作温度 | 0–55 °C |
| CAN | CAN1 ×2，CAN2 ×2 |
| UART | 2 |
| PWM | 7 |
| USB | 1 |
| I²C | 1 |
| SPI | 1 |
| IMU + 电子罗盘 | 1 |
| 尺寸 | 60 × 41 × 16 mm |
| 重量 | 38 g |

当前固件以 168 MHz STM32F407 为控制核心。

### 在 IBL Rig 中怎么用

C Board 负责：

- 读取转轮
- 500 Hz 电机控制
- Trial 状态执行
- 奖励泵控制
- CAN 电机通信
- PPS 捕获
- 行为同步输出
- 硬件安全停止

Pi 5 通过 ST-Link/SWD 与 C Board 保持运行时通信。

官方规格：
[RoboMaster Development Board Type C](https://www.robomaster.com/en-US/products/components/general/development-board-type-c)

## M2006 + C610

转轮使用 RoboMaster M2006 P36 减速电机和 C610 电调。

官方参数：

| 项目 | 参数 |
|---|---:|
| 系统电压 | 24 V |
| 空载转速 | 500 rpm |
| 持续最大扭矩 | 1 N·m |
| 1 N·m 下转速 | 416 rpm |
| 减速比 | 36:1 |
| 电机重量 | 90 g |
| 电机外径 | 24.4 mm |
| 电机长度 | 64.8 mm |
| 输出轴直径 | 6 mm |
| C610 持续电流 | 10 A |
| C610 通信 | CAN |
| C610 尺寸 | 50 × 22 × 7.3 mm |
| C610 重量 | 17 g |

### 在 IBL Rig 中怎么用

M2006 连接转轮，为转轮提供：

- 位置与速度反馈
- 阻尼
- 惯性
- 弹簧感
- 棘轮感
- 透明模式
- 自适应透明模式

正式训练当前使用 profile 27。

电机控制环在 C Board 上以 500 Hz 运行。

官方规格：
[RoboMaster M2006 Power System](https://www.robomaster.com/en-US/products/components/general/M2006)

## 奖励蠕动泵

奖励系统使用四线步进蠕动泵和 DRV8834 步进驱动器。

当前驱动参数：

| 项目 | 参数 |
|---|---:|
| 驱动电压 | 5 V |
| STEP 频率 | 12,000 pulse/s |
| 微步 | 1/32 |
| STEP | C Board PE9 |
| DIR | C Board PE11 |
| 单次队列上限 | 200 µL |

当前校准：

```text
14,399,993 pulses → 5.5 mL
0.381944630 nL / pulse
2618.180545 pulses / µL
```

在 12 kHz 下，对应约：

```text
4.58 µL/s
0.275 mL/min
```

### 在 IBL Rig 中怎么用

泵承担两种用途：

**训练奖励**

正式训练当前设置为反转 2 s。

**管路排气**

网页提供“蠕动泵排气 · 反转 1 分钟”，用于装液和清除气泡。

C Board 直接产生 STEP/DIR 信号，因此奖励动作和 Trial 时间保持在同一硬件时序中。

## OAK-FFC-4P

视频系统使用 Luxonis OAK-FFC-4P。

OAK-FFC-4P 基于 RVC2，官方支持 USB 2/3 连接。RVC2 提供 H.264、H.265 和 MJPEG 硬件编码。

OAK-FFC-4P 官方典型功耗：

- 相机 streaming：2.5–3 W
- 视频编码：最高约 0.5 W
- RVC2 满负载环境温度范围：-20–50 °C

### 四个传感器

| 位置 | Sensor | 类型 | 快门 | 分辨率 |
|---|---|---|---|---|
| CAM_A | OV9782 | 彩色 | Global shutter | 1280 × 800 |
| CAM_B | OV9282 | 黑白 | Global shutter | 1280 × 800 |
| CAM_C | OV9282 | 黑白 | Global shutter | 1280 × 800 |
| CAM_D | OV9282 | 黑白 | Global shutter | 1280 × 800 |

OV9782 和 OV9282 在 RVC2 上的 1280 × 800 原生模式最高为 129 fps。

### 当前使用参数

| 项目 | 当前值 |
|---|---:|
| 分辨率 | 1280 × 800 |
| 帧率 | 30 fps |
| 录像编码 | H.265 |
| 码率 | 12 Mbps / 路 |
| 浏览器预览 | MJPEG |
| 主预览 | CAM_A |
| 数据连接 | USB 3，5 Gbps |
| 供电 | 外部 5 V |

### 在 IBL Rig 中怎么用

OAK 在设备端完成视频编码。

Pi 5 接收编码后的视频流并直接写入 NVMe，同时保存：

- 帧序号
- 相机时间戳
- 曝光
- 增益
- 文件位置

浏览器显示四路实时预览。

官方规格：

- [OAK-FFC-4P](https://docs.luxonis.com/hardware/products/OAK-FFC%204P)
- [OV9782](https://docs.luxonis.com/hardware/sensors/OV9782)
- [OV9282](https://docs.luxonis.com/hardware/sensors/OV9282)

## 刺激显示器

刺激显示器连接 Pi 5 HDMI。

当前参数：

| 项目 | 当前值 |
|---|---:|
| 分辨率 | 1920 × 1080 |
| 目标刷新率 | 60 Hz |
| 视觉几何 | 20 px/视觉° |
| 转轮-屏幕增益 | 85.172 px/轮角° |
| 背景亮度 | 0.5 |
| 光电标记尺寸 | 80 px |
| HDMI 输出 | HDMI-A-2 |

### 在 IBL Rig 中怎么用

显示器呈现 Gabor 刺激。

训练中支持：

- 预加载
- 显示
- 转轮闭环移动
- 固定
- 居中
- 隐藏

当前增益下，转轮每转动 1°，刺激移动约 85.172 px。±35° 刺激距离屏幕中心 700 px，对应约 8.22° 转轮行程。训练增益调整时，这个映射比例同步更新。

## 行为蜂鸣器

行为声音由 C Board 的板载蜂鸣器产生。

当前参数：

| 项目 | 当前值 |
|---|---:|
| 输出引脚 | PD14 / TIM4_CH3 |
| Go tone | 4 kHz / 100 ms |
| Error sound | 2 kHz / 4 kHz 交替 |
| 单段时长 | 50 ms |
| Error 总时长 | 500 ms |
| 支持频率 | 100–10,000 Hz |

## 时间同步

C Board 接收 GPSDO PPS。

当前输入：

```text
J16 C7 → PI7 / TIM8_CH3
```

主机持续读取 PPS 状态，并把时间质量显示到实验状态中。

## 红外照明

红外灯使用 12 V 电源，通过 MOSFET 模块由 C Board 控制。

供电链：

```text
24 V
 ↓
辅助电源模块
 ↓
12 V
 ↓
MOSFET
 ↓
IR lamp
```

相机与照明模块安装在同一可调结构上，便于同时调整视野和照明方向。

## 电源系统

整机使用分域供电。

```text
AC
├── Pi 5 官方 USB-C 电源
├── 刺激显示器
├── 监看显示器
├── GPSDO
└── 24 V 电源
      ├── C Board + C610 + M2006
      └── 辅助电源
            ├── 5 V → OAK
            ├── 5 V → DRV8834 / pump
            └── 12 V → IR lamp
```

OAK 使用独立 5 V 供电，USB 3 负责数据连接。

## 主机构

当前主机构为 V3-ENG P4。

主要结构件采用 6061-T651 铝合金设计。

当前装配包含 9 类制造件和 28 个紧固件/螺套位置。

整机的两侧 PadHolder 使用同一个 CNC V4 几何，左右位置通过平移安装。

## 相机/照明模块 R2

R5 使用四个 compact R2 模块。

模块集成：

- OAK camera
- lamp
- 导轨安装
- 球铰
- 俯仰锁紧

模块体积约 5380 mm³，俯仰调节范围约 ±30°。

## 硬件速查

详细参数、接口和接线见 [硬件参数 Reference](/IBLRig/reference/hardware/)。
