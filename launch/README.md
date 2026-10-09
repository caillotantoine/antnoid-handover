# Launchfiles

| File | Use |
| --- | --- |
| [ids_hdr.launch.py](ids/ids_hdr.launch.py) | IDS HDR with adaptive exposure, 22 FPS |
| [ids_gps_forRecord.launch.py](ids/ids_gps_forRecord.launch.py) | IDS + HDR + GPS, fixed 45 ms exposure, 15 FPS |
| [ids_gps_recorder.launch.py](ids/ids_gps_recorder.launch.py) | Raw IDS image and GPS recording; start acquisition separately |
| [bringup.xml](insta360/bringup.xml) | Insta360 X3 using IAQFB23129J8E6 calibration |
| [bringup_22AB43221.xml](insta360/bringup_22AB43221.xml) | Alternate Insta360 launcher for camera 22AB43221 |

Source the camera workspace, then run `ros2 launch` with the absolute launchfile path. Choose one IDS acquisition launcher at a time.

The Insta360 launcher reads calibration from the installed `ros_insta360` package. Follow [the calibration instructions](../config/insta360/README.md).

Procedures: [IDS HDR](../docs/IDS_HDR_Adaptive_Exposure.md), [Go1 navigation](../docs/Mapping_and_Waypoint_Navigation.md), [virtual navigation](../docs/Virtual_HRP5_Engine3D_Navigation.md).
