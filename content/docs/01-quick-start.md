---
title: "01 · Quick Start"
weight: 20
baseline: "IBL main @ 6c2ea40"
summary: "从登录到 Session finalize 的完整操作路径。"
---

# Quick Start

## 1. 打开 Rig Web

当前 ratRot Web 监听：

```text
0.0.0.0:18080
```

可通过局域网地址或配置好的 Tailnet 地址访问。

页面加载后，Web 会建立 ROS bridge，并持续读取：

- Session 状态
- Runtime Graph
- Device Health
- Camera status
- Post-session jobs
- 当前控制权

## 2. 飞书登录

点击登录后，浏览器进入中央 Auth Broker，再进入飞书 OAuth。

成功后浏览器获得本地 `ibl_rig_session` cookie。页面右上角显示：

- display name
- role
- control holder
- online state

如果 rig 当前空闲，登录会尝试获取控制权。

## 3. 选择模板

打开 Configuration。

内置模板包括：

- 正式预训练
- 正式训练
- office silent
- automatic-reward pretraining
- online training
- phase-0 HIL
- fast-three verification
- no-OAK verification
- v2 training template

输入 subject id，然后选择模板。

## 4. 修改参数

Web 根据 override policy 开放可修改字段。

修改后页面显示 diff：

```text
before → after
```

常见参数包括：

- response window
- ITI
- contrast
- stimulus position
- reward
- sound
- force profile
- trial cap

完整参数见 [实验参数 Reference](/IBLRig/reference/configuration/)。

## 5. Resolve

点击锁定配置后，Web 调用：

```text
POST /api/v1/config/resolve
```

Resolve 会：

1. 校验模板
2. 应用 overrides
3. 解析训练历史
4. 编译 Trial
5. 生成 Session config
6. 计算 required devices
7. 写入 resolved artifact
8. 返回 `resolved_sha256`

页面随后持有一个固定的 Session resolution。

## 6. Prepare

Prepare 把 Session intent 提交给 Supervisor。

Supervisor 读取：

- compiled table URI + SHA
- session config URI + SHA
- rig id
- operating mode
- session id

随后发布 Runtime Graph。

Runtime Manager 按 graph 启动需要的 capability。

例如一场带视觉、相机和 MCU 的训练会启动：

```text
mcu
stimulus
camera
recorder
diagnostics
time
task
```

## 7. Preflight

Preflight 汇总当前 capability、health、time、storage 和 recording 状态。

页面直接显示检查结果。

常见检查项：

- required device 是否 live
- DeviceHealth
- time quality
- session directory
- NVMe free space
- recorder state
- camera state
- stimulus state
- MCU status

通过后即可 Start。

## 8. Start

Start 调用 SessionCoordinator，最终进入 ROS action：

```text
/rig/run_session
```

执行顺序：

```text
prepare recorder
    ↓
arm camera recording
    ↓
stage trial table
    ↓
send START to controller
    ↓
receive progress events
    ↓
run trials
```

页面开始显示：

- current trial
- completed trials
- correct / incorrect / no-response
- requested reward
- elapsed time
- device status
- camera preview

## 9. Session 控制

Web 当前操作集合：

| 操作 | 含义 |
|---|---|
| `pause-after-trial` | 当前 Trial 结束后暂停 |
| `resume` | 继续运行 |
| `stop-after-trial` | 当前 Trial 结束后正常结束 |
| `abort` | 立即进入中止流程 |
| `cancel_prepare` | 取消已 Prepare 的 Session |
| `reset_fault` | 清理 Supervisor fault，管理员操作 |

这些动作统一走：

```text
POST /api/v1/session/control/{operation}
```

## 10. Camera Preview

Web Camera 区域显示四路画面。

当前 preview 结构：

- CAM_A：主预览，stride 1
- CAM_B/C/D：缩略图，stride 3
- 浏览器最多同时接受 8 个 camera client

切换主画面时，Web 更新 `/rig/camera/preview_primary`，OAK pipeline 保持运行。

## 11. Session 结束

RunSession action 结束后，Supervisor 执行：

1. controller final state
2. recorder finalize
3. diagnostics quality report
4. Session result 写入
5. post-session jobs 创建

页面随后展示：

```text
analysis
NAS
W&B
Feishu
cleanup
```

每个 job 都有独立状态和重试。

## 12. 找数据

Session 数据根目录：

```text
/home/jingyi/rig-os/data/sessions/<session_id>/
```

配置 resolution：

```text
/home/jingyi/rig-os/data/compiled/web/<session_id>/
```

训练状态：

```text
/home/jingyi/rig-os/data/training-policy/
```

具体文件见 [数据 Reference](/IBLRig/reference/data/)。

## 13. 常用系统检查

SSH 进入 ratRot：

```bash
ssh ratRot
```

查看控制面：

```bash
systemctl status ibl-rig-supervisor.service
systemctl status ibl-rig-web.socket
systemctl status ibl-rig-web.service
```

查看 ROS 状态：

```bash
ros2 topic echo --once /rig/session/status
ros2 topic echo --once /rig/runtime/graph
ros2 topic echo --once /rig/runtime/status
ros2 topic echo --once /rig/device_health
```

查看相机：

```bash
ros2 service call /rig/camera/get_inventory rig_msgs/srv/GetCameraInventory
```
