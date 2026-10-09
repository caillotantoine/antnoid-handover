# Stella camera configurations

| Camera | YAML | Images | Mask |
| --- | --- | --- | --- |
| IDS HDR | [IDS_1024_AC_2122.yaml](input/rap_rev/IDS_1024_AC_2122.yaml) | Fisheye, 1024 × 1024, BGR, 21.22 FPS | [IDS_89_496_498.png](input/rap_rev/IDS_89_496_498.png) |
| Insta360 | [JRL_equirgb_1280x720.yaml](input/JRL_equirgb_1280x720.yaml) | Equirectangular, 1440 × 720, RGB, 9 FPS | No mask selected by the manual |
| Engine3D | [JRL_MC_equirgb_thetaS_1280x720.yaml](input/JRL_MC_equirgb_thetaS_1280x720.yaml) | Equirectangular, 1440 × 720, RGB, 9 FPS | No mask selected by the manual |
| FLIR | [FLIR_1024.yaml](input/rap_rev/old/FLIR_1024.yaml), [20 FPS variant](input/rap_rev/old/FLIR_1024_20FPS.yaml) | Fisheye, 1024 × 1024, BGR, 10 / 20 FPS | Select a mask matching the lens and image centre |

Use the YAML matching the images sent to SLAM. The two equirectangular files specify **1440 × 720**, despite their filenames. They use a monocular model.

`FLIR_1024_AC.yaml` contains an IDS camera description: do not select it by filename alone. Files in `old/` are alternate configurations; their parameter names must match the Stella version in use.

Copy the `input/` contents to the directory mounted as `/stella_data/input`. Supply `orb_vocab.fbow` separately. Select the YAML with `-c` and the mask with `--mask`.

Use `--map-db-out` to save, `--map-db-in` to load, and `--disable-mapping` to follow a route in a fixed map. Full commands are in the [Go1](../../docs/Mapping_and_Waypoint_Navigation.md) and [virtual](../../docs/Virtual_HRP5_Engine3D_Navigation.md) manuals.
