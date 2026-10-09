# Antnoid — Operating manuals

Three procedures for camera acquisition, visual mapping and waypoint navigation:

1. [IDS HDR and adaptive exposure](docs/IDS_HDR_Adaptive_Exposure.md)
2. [Go1 mapping and waypoint navigation](docs/Mapping_and_Waypoint_Navigation.md)
3. [Virtual HRP5P with Engine3D](docs/Virtual_HRP5_Engine3D_Navigation.md)

## Get the files

Clone this repository on the machine running the procedure:

```bash
git clone https://github.com/caillotantoine/antnoid-handover.git "$HOME/antnoid-handover"
```

The manuals use `~/antnoid-handover` as the checkout path. Open a separate terminal for each long-running process.

## Contents

| Directory | Contents |
| --- | --- |
| `docs/` | The three operating manuals |
| [launch/](launch/README.md) | IDS acquisition/recording and Insta360 launchfiles |
| [config/stella/](config/stella/README.md) | SLAM camera configurations and masks |
| [config/insta360/](config/insta360/README.md) | Serial-specific camera calibrations and masks |

## Required software

- ROS 2 Humble and CycloneDDS.
- [ids_camera_driver](https://github.com/isri-aist/ids_camera_driver) and [DEO-HDR](https://github.com/isri-aist/DEO-HDR) for IDS acquisition.
- [ros_insta360](https://github.com/caillotantoine/ros_insta360/tree/humble) and its Camera SDK for Insta360 acquisition.
- [unitree_ros](https://github.com/snt-arg/unitree_ros) for Go1 velocity control on the NUC.
- [robotControlSim](https://github.com/isri-aist/robotControlSim) for waypoint recording and following.
- A ROS 2 Stella image, the ORB vocabulary `orb_vocab.fbow`, and the matching viewer image if used.
- For simulation: mc_rtc, mc_mujoco, HRP5P robot assets, BaselineWalkingController, Engine3D and its ROS wrapper.

This repository contains launch/configuration files, not installed software. Map databases, image recordings, vocabulary, Docker images, vendor SDKs and large Insta360 lookup tables are supplied separately.

## Local paths

On the machine running the cameras and navigation, create a private settings file:

```bash
cp ~/antnoid-handover/config/local.env.example ~/antnoid-handover/config/local.env
```

Edit `config/local.env` to match the installed workspace and data directories. Source it in each host terminal. It is ignored by Git; do not commit robot credentials or internal network details. Obtain the robot login from the administrator.
