# IDS HDR and adaptive exposure

## Requirements

- IDS camera connected to the Go1 NUC.
- Acquisition workspace: `$IDS_WS` (configured in `config/local.env`).
- This repository cloned at `~/antnoid-handover`.
- Internet and RTK correction access when recording GPS.

Connect to the robot:

```bash
ssh ROBOT_USER@ROBOT_HOST
```

Replace `ROBOT_USER` and `ROBOT_HOST` with the login provided by the robot administrator. Configure [local paths](../README.md#local-paths) first.

In each ROS terminal:

```bash
source ~/antnoid-handover/config/local.env
source /opt/ros/humble/setup.bash
source "$IDS_WS/install/setup.bash"
export ROS_DOMAIN_ID=231
export RMW_IMPLEMENTATION=rmw_cyclonedds_cpp
```

## 1. Run HDR with adaptive exposure

```bash
ros2 launch ~/antnoid-handover/launch/ids/ids_hdr.launch.py
```

This starts the camera, HDR processor and output adapter. Settings: 22 FPS, `dual_expo=12`, processing ratio 0.12, adaptive exposure enabled.

| Topic | Contents |
| --- | --- |
| `/ids_camera/image_raw` | Raw IDS images |
| `/camera/HDR/image_raw` | HDR output |
| `/camera/HDR/preview` | Preview |
| `/camera/image_raw` | HDR stream for SLAM, best effort with queue depth 1 |

Display `/camera/HDR/preview` in RViz. Leave this terminal running while using SLAM.

To change acquisition rate:

```bash
ros2 launch ~/antnoid-handover/launch/ids/ids_hdr.launch.py frame_rate:=15.0
```

Stop with **Ctrl+C** before switching to the recording procedure below.

## 2. Record raw images and GPS with fixed exposure

Terminal 1 — acquisition:

```bash
ros2 launch ~/antnoid-handover/launch/ids/ids_gps_forRecord.launch.py
```

Settings: 15 FPS, exposure 45 ms, dual-exposure ratio 0.12, adaptive exposure disabled. Camera, HDR and GPS nodes run together.

Terminal 2 — recording:

```bash
ros2 launch ~/antnoid-handover/launch/ids/ids_gps_recorder.launch.py
```

The recorder saves **raw IDS images and GPS** under `~/Desktop/record_YYYY-MM-DD/`. It does not record the HDR output. Acquisition must be running separately. Runs on the same day use the same directory; move the completed recording before starting another session.

Finish by pressing **Ctrl+C** in the recording terminal, then in the acquisition terminal.

## 3. Adjust exposure behaviour

Edit [ids_hdr.launch.py](../launch/ids/ids_hdr.launch.py), then restart it.

| Parameter | Role |
| --- | --- |
| HDR `discrete_ae` | Enable or disable adaptive exposure |
| HDR `dualExpRatio_` | Short/full exposure ratio used by processing |
| Camera `dual_expo` | Driver setting for the short exposure |
| Camera `exposure_ms` | Initial/fixed full exposure in milliseconds |
| HDR `maxsaturated`, `maxdark` | Percentages used in exposure selection |

Keep driver and processing ratios consistent. Leave `dual_expo=12` and `dualExpRatio_=0.12` for the supplied configuration.

## If no images appear

If the driver reports zero cameras, check camera power, USB connection and whether another process is using it. If nodes remain after Ctrl+C, identify their PIDs with:

```bash
pgrep -af 'ids_camera_node|hdr_processor|qos_changer'
```

Stop the leftover processes from this session before restarting.
