---
title: "硬件参数"
weight: 20
summary: "整机、电源、控制器、电机、泵、相机、显示和同步接口速查。"
---

# 硬件参数

## 整机

| 项目 | 当前值 |
|---|---|
| 整机版本 | R5 |
| 外形范围 | 约 300 × 300 × 312.7 mm |
| 主机构 | V3-ENG P4 |
| PadHolder | CNC V4 ×2 |
| MouseCover | true B-Rep rebuild |
| 相机/照明模块 | Compact R2 ×4 |
| 相机模块俯仰 | 约 ±30° |

## 电源拓扑

```text
AC
├── Raspberry Pi 5 官方 USB-C 电源
├── 刺激显示器
├── 监看显示器
├── GPSDO
└── 24 V DC
      ├── RoboMaster C Board
      │     └── C610 + M2006
      └── Auxiliary DC-DC
            ├── 5 V → OAK-FFC-4P
            ├── 5 V → DRV8834 + pump
            └── 12 V → MOSFET + IR lamp
```

## Raspberry Pi 5

| 项目 | 参数 |
|---|---|
| SoC | Broadcom BCM2712 |
| CPU | 4 × Cortex-A76 @ 2.4 GHz |
| RAM | 8 GB LPDDR4X |
| USB 3 | 2 × 5 Gbps |
| Ethernet | 1 Gbps |
| PCIe | PCIe 2.0 ×1 |
| HDMI | 双 4K60 输出能力 |
| 当前系统 | Ubuntu 24.04 |
| ROS | ROS 2 Jazzy |
| 数据盘 | SK hynix BC711 256 GB NVMe |
| 系统启动盘 | microSD |

## RoboMaster Development Board Type C

| 项目 | 参数 |
|---|---|
| MCU | STM32F407 |
| CPU | Arm Cortex-M4，168 MHz |
| 输入电压 | 8–28 V |
| 当前输入 | 24 V |
| 工作温度 | 0–55 °C |
| CAN | CAN1 ×2；CAN2 ×2 |
| UART | 2 |
| PWM | 7 |
| USB | 1 |
| I²C | 1 |
| SPI | 1 |
| IMU + E-compass | 1 |
| 尺寸 | 60 × 41 × 16 mm |
| 重量 | 38 g |
| Host link | ST-Link / SWD |

### 当前引脚使用

| 功能 | C Board / MCU |
|---|---|
| Pump STEP | J16 C1 / PE9 / TIM1_CH1 |
| Pump DIR | J16 C2 / PE11 |
| Pump GND | J16 A1 / A2 |
| PPS | J16 C7 / PI7 / TIM8_CH3 |
| PPS GND | J16 A7 |
| Buzzer | PD14 / TIM4_CH3 |
| Motor | CAN1 |
| Host link | SWD |

## M2006 + C610

| 项目 | 参数 |
|---|---:|
| 额定电压 | 24 V |
| 空载转速 | 500 rpm |
| 持续最大扭矩 | 1 N·m |
| 1 N·m 时转速 | 416 rpm |
| 减速比 | 36:1 |
| 电机重量 | 90 g |
| 电机外径 | 24.4 mm |
| 电机长度 | 64.8 mm |
| 输出轴 | 6 mm D 轴 |
| C610 持续电流 | 10 A |
| C610 控制 | CAN |
| C610 尺寸 | 50 × 22 × 7.3 mm |
| C610 重量 | 17 g |
| 控制频率 | 500 Hz |

### 当前力反馈模式

- encoder
- assist
- virtual
- transparent
- adaptive transparent
- current
- velocity
- position

正式训练使用 profile 27。

## 奖励泵

| 项目 | 参数 |
|---|---:|
| 类型 | 四线步进蠕动泵 |
| 驱动 | DRV8834 |
| 驱动电压 | 5 V |
| STEP | PE9 / TIM1_CH1 |
| DIR | PE11 |
| STEP rate | 12 kHz |
| Microstep | 1/32 |
| 校准 | 14,399,993 pulse / 5.5 mL |
| 单脉冲体积 | 0.381944630 nL |
| 脉冲密度 | 2618.180545 pulse/µL |
| 当前流量 | 约 0.275 mL/min |
| 队列容量 | 200 µL |

## OAK-FFC-4P

| 项目 | 参数 |
|---|---|
| 平台 | Luxonis RVC2 |
| 主机接口 | USB 3 |
| 当前链路 | 5 Gbps SuperSpeed |
| 供电 | 外部 5 V |
| Camera sockets | CAM_A/B/C/D |
| 录像 | H.265 |
| 预览 | MJPEG |
| 当前帧率 | 30 fps |
| 当前分辨率 | 1280 × 800 |
| 当前码率 | 12 Mbps / camera |
| 设备 ID | 1944301041BE502E00 |

### Camera sensor

| Camera | Sensor | Color | Shutter | Native 800p max |
|---|---|---|---|---:|
| CAM_A | OV9782 | Color | Global | 129 fps |
| CAM_B | OV9282 | Mono | Global | 129 fps |
| CAM_C | OV9282 | Mono | Global | 129 fps |
| CAM_D | OV9282 | Mono | Global | 129 fps |

### OAK 功耗

Luxonis 官方 RVC2 平台典型值：

| 负载 | 功耗 |
|---|---:|
| Base + camera streaming | 2.5–3 W |
| Video encoder | +0.5 W |
| AI subsystem | +1 W |
| Stereo depth | +0.5 W |

## 刺激显示

| 项目 | 参数 |
|---|---:|
| 输出 | HDMI-A-2 |
| 分辨率 | 1920 × 1080 |
| 刷新目标 | 60 Hz |
| 像素换算 | 20 px/° |
| 背景亮度 | 0.5 |
| 光电标记 | 80 px |

## 行为蜂鸣器

| 项目 | 参数 |
|---|---|
| MCU pin | PD14 |
| Timer | TIM4_CH3 |
| 输出频率范围 | 100–10,000 Hz |
| Go tone | 4 kHz / 100 ms |
| Error sound | 2 kHz ↔ 4 kHz，每段 50 ms，共 500 ms |

## PPS

| 项目 | 参数 |
|---|---|
| 来源 | GPSDO PPS |
| C Board pin | J16 C7 |
| MCU | PI7 / TIM8_CH3 |
| 状态超时 | 2.5 s |

## 相机/照明模块 R2

| 项目 | 参数 |
|---|---|
| 数量 | 4 |
| 模块体积 | 约 5380 mm³ |
| 俯仰 | 约 ±30° |
| 集成器件 | OAK camera + lamp |
| 安装 | 导轨 + 球铰 + 锁紧 |

## 主要连接

| 从 | 到 | 连接 |
|---|---|---|
| Pi 5 | OAK | USB 3 |
| Pi 5 | Stimulus display | HDMI |
| Pi 5 | C Board | ST-Link / SWD |
| C Board | C610 | CAN |
| C610 | M2006 | 官方电机线束 |
| C Board | Pump driver | STEP / DIR |
| GPSDO | C Board | PPS |
| Aux 5 V | OAK | DC barrel |
| Aux 5 V | DRV8834 | DC |
| Aux 12 V | IR MOSFET | DC |
