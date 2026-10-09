# Antnoid handover

Research handover by Caillot, updated 9 October 2026.

This repository contains deployment notes and recovered configurations for IDS dual-exposure HDR, Go1 visual mapping and waypoint navigation, Insta360 equirectangular images, and virtual HRP5P navigation with Engine3D. Software implementations remain in their own repositories.

## Guides

- [IDS HDR and adaptive exposure](docs/IDS_HDR_Adaptive_Exposure.md)
- [Go1 mapping and waypoint navigation](docs/Mapping_and_Waypoint_Navigation.md)
- [Virtual HRP5P, Engine3D and navigation](docs/Virtual_HRP5_Engine3D_Navigation.md)
- [SLAM configurations and masks](config/stella/README.md)
- [Recovered launchfiles](launch/README.md)
- [Insta360 calibration assets](config/insta360/README.md)

## Software dependencies

| Software | Repository | Recovered version |
| --- | --- | --- |
| HDR and discrete exposure | [DEO-HDR](https://github.com/isri-aist/DEO-HDR) | main, b05e5e31145247886d42a251c8901b5f6b9589ef |
| IDS camera driver | [ids_camera_driver](https://github.com/isri-aist/ids_camera_driver) | jazzy, f7b181df73a3136d33a3a7640a61961f9d7290c8; robot host uses Humble |
| Waypoint toolbox | [robotControlSim](https://github.com/isri-aist/robotControlSim) | main, d6dfd76b1f974571bb201ef6af2a3af4779a2bac |
| Insta360 ROS 2 driver | [ros_insta360 fork](https://github.com/caillotantoine/ros_insta360/tree/humble) | humble, 5a1c3eb5b12e5bc4dab54c271002d6c7ccaba2ce; local launcher differs |
| Stella Docker assets | [StellaDockerSet](https://github.com/isri-aist/StellaDockerSet) | Public recipe is ROS 1; does not reproduce the recovered ROS 2 images |
| Stella ROS interface | [stella_vslam_ros](https://github.com/stella-cv/stella_vslam_ros/tree/ros2) | Exact installed source revision not recovered |
| Engine3D | [Engine3D](https://github.com/PerceptionRobotique/Engine3D) | Historical version not recovered |
| Engine3D ROS wrapper | [ros_Engine3D](https://github.com/PerceptionRobotique/ros_Engine3D) | Exact launchfiles not recovered |

Additional simulator/controller dependencies are listed in the virtual guide.

## Evidence and validation

Files under launch and config are recovered copies from go1-handover-XDkkyt.tar.gz supplied by the operator. [PROVENANCE.json](config/PROVENANCE.json) records original archive paths and SHA-256 hashes. Originals are preserved, including historical comments and misleading filenames. New documentation is in English.

The Go1 reports Ubuntu 22.04.5, ROS 2 Humble, CycloneDDS and domain 231. The installed Stella CLI confirms map input/output, mapping disabling and viewer selection. HDR startup confirms adaptive exposure enabled, ratio 0.12 and mask loading. The IDS driver detected zero cameras during the check; live processing and complete navigation were not revalidated. The original simulation PC is unavailable.

The source checkout named IDSHDR actually points to bag_to_video and contains unresolved/local changes. Its source backup remains a separate preservation task. These configuration files do not replace a backup of that checkout.

Map databases, recorded datasets, ORB vocabulary, Docker images, vendor SDKs and large stitching lookup tables are not included. The two JRL equirectangular YAMLs specify 1440 x 720, despite 1280x720 in their filenames. A camera model does not establish metric scale or camera-to-body registration.

## Deployment

Install the software first, then follow the relevant guide. The recovered Stella input layout is retained under config/stella/input so files can be copied to a new shared input directory without changing relative mask paths. Inspect existing files before replacing a robot installation.

The Insta360 launcher resolves calibration through the installed ros_insta360 package share. Merely cloning this repository does not install those assets. Follow the calibration instructions before launching.

Use paired maps and waypoint files from the same coordinate frame. Rebuilding maps, changing camera geometry or switching between simulation and physical cameras requires a new validation of scale, transforms and localisation.
