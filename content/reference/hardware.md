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
| RAM | 8 GB LPDDR4X-4267 |
| USB 3 | 2 × 5 Gbps，可同时工作 |
| USB 2 | 2 |
| Ethernet | 1 Gbps |
| PCIe | PCIe 2.0 ×1 |
| HDMI | 双 4K60 |
| HEVC | 4K60 hardware decode |
| Wi-Fi | 802.11ac dual-band |
| Bluetooth | 5.0 / BLE |
| 推荐供电 | USB-C 5 V / 5 A |
| 当前系统 | Ubuntu 24.04 |
| ROS | ROS 2 Jazzy |
| 数据盘 | SK hynix BC711 256 GB NVMe |
| 系统启动盘 | microSD |

用途：运行网页控制台、ROS 2、视觉刺激、四路视频落盘、实验分析和自动归档。

厂商资料：[Raspberry Pi 5](https://www.raspberrypi.com/products/raspberry-pi-5/)

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
| 工作温度 | 0–55 °C |
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

### 蠕动泵

| 项目 | 参数 |
|---|---:|
| 类型 | 四线步进蠕动泵 |
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

用途：Trial 奖励给水和网页“蠕动泵排气 · 反转 1 分钟”。

### DRV8834

| 项目 | TI 规格 |
|---|---:|
| 电源范围 | 2.5–10.8 V |
| 当前使用 | 5 V |
| 连续输出电流 | 1.5 A / H-bridge |
| 峰值输出电流 | 2.2 A / H-bridge |
| 控制方式 | STEP/DIR 或 PH/EN |
| 最大微步 | 1/32 |
| H-bridge | 2 |
| 电流调节 | PWM current regulation |
| 工作温度 | -40–85 °C |

厂商资料：[TI DRV8834](https://www.ti.com/product/DRV8834)

## OAK-FFC-4P

| 项目 | 参数 |
|---|---|
| 平台 | Luxonis RVC2 |
| 主机接口 | USB 3 |
| OAK 主机接口能力 | USB 2/3，最高 10 Gbps |
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

满负载环境温度范围：-20–50 °C。

厂商资料：[Luxonis OAK-FFC-4P](https://docs.luxonis.com/hardware/products/OAK-FFC%204P)

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

## GPSDO 与同步

GPSDO 提供 10 MHz 和 PPS。

| 信号 | 当前接口 |
|---|---|
| 10 MHz | SMA 输出，约 3 V 正弦 |
| PPS | SMA 输出，3.3 V / 1 Hz |
| PPS 输入 | C Board J16 C7 |
| MCU 捕获 | PI7 / TIM8_CH3 |
| PPS 状态超时 | 2.5 s |

### TLV3501

10 MHz 整形使用 TLV3501 高速比较器。

| 项目 | TI 规格 |
|---|---:|
| 通道 | 1 |
| 传播延迟 | 4.5 ns |
| 供电 | 2.7–5.5 V |
| 输出 | Push-pull CMOS |
| 静态电流 | 3.2 mA typ. |
| 工作温度 | -40–125 °C |

用途：把 GPSDO 的 10 MHz 正弦信号整形成 3.3 V 数字时钟。

厂商资料：[TI TLV3501](https://www.ti.com/product/TLV3501)

## 辅助电源与照明

### 辅助 DC-DC

输入 24 V，提供：

- 5 V：OAK-FFC-4P
- 5 V：DRV8834 与奖励泵
- 12 V：红外照明 MOSFET
- 3.3 V：低压逻辑模块

### MOSFET 照明开关

MOSFET 模块接收 C Board 3.3 V 控制信号，开关 12 V 红外灯。

用途：训练过程中为四路相机提供稳定红外照明。

### PDU

整机 PDU 同时提供：

- AC：Pi 5 电源、GPSDO 等
- USB-C PD：刺激显示器、监看显示器

用途：集中完成整机上电和双显示器供电。

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
