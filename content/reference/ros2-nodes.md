---
title: "ROS 2 节点"
weight: 30
summary: "当前运行节点、作用和常用查看方法。"
---

# ROS 2 节点

使用：

```bash
ros2 node list
```

查看当前节点。

## 实验控制

### `/rig_supervisor`

负责整场实验状态：

- 预检
- 开始
- 暂停
- 继续
- 停止
- 中止
- Trial 计数
- 正确/错误/无响应统计
- 实验时间
- 故障状态

常用状态：

```bash
ros2 topic echo /rig/session/status
```

### `/rig_lifecycle_manager`

负责实验控制服务的 ROS 2 lifecycle 启动。

### `/rig_runtime_manager`

根据当前实验需求启动相机、显示、控制器、记录等服务，并汇总运行状态。

## MCU 与电机

### `/mcu_watchdog`

实验控制器启动前检查 C Board，并执行 SWD 恢复。

### `/mcu_watchdog_companion`

实验期间持续保留 MCU 恢复入口。

### `/controller_gateway`

Pi 与 C Board 的运行时通信节点。

提供：

- Trial 下发
- Trial 结果
- 转轮状态
- 电机状态
- PPS
- 奖励事件
- 行为声音事件
- 视觉刺激请求

### `/rig_safety_agent`

监看实验控制状态和 C Board 安全状态。

## 刺激显示

### `/stimulus_server`

控制 HDMI 刺激屏。

提供：

- Gabor 预加载
- 显示
- 转轮闭环运动
- 固定
- 居中
- 隐藏
- 显示帧率
- HDMI 状态

## 相机

### `/depthai_manager`

管理 OAK-FFC-4P。

提供：

- 四路相机
- H.265 录像
- MJPEG 预览
- Camera inventory
- Frame metadata
- 设备恢复
- 相机状态

## 数据记录

### `/recorder_manager`

保存行为事件记录。

提供：

- 实验记录开始
- JSONL event log
- 录像帧索引引用
- 数据记录状态
- 实验结束校验

## 诊断

### `/diagnostics_server`

提供网页预检和实验质量统计。

关注：

- 存储空间
- 设备状态
- 时间同步
- 事件连续性
- 视频帧连续性

## 时间

### `/time_monitor`

读取 C Board PPS 状态，发布实验时间质量。

## 训练任务

### `/task_compiler`

把训练配置生成控制器可执行的 Trial。

## 标定

### `/calibration_manager`

运行系统标定任务并保存标定结果。

## 常用命令

查看节点：

```bash
ros2 node list
```

查看节点信息：

```bash
ros2 node info /depthai_manager
```

查看实验状态：

```bash
ros2 topic echo /rig/session/status
```

查看设备状态：

```bash
ros2 topic echo /rig/device_health
```
