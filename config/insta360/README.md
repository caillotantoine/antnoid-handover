# Insta360 calibration

The XML files configure dual-fisheye stitching in `ros_insta360`. The Stella YAML configures the resulting equirectangular images. Keep both aligned with the selected camera and image dimensions.

The supplied [bringup.xml](../../launch/insta360/bringup.xml) selects camera **IAQFB23129J8E6**. For another camera, change its `calibFile` to the matching serial-specific XML.

## Install the selected calibration

Set `INSTA_WS` in [config/local.env](../../README.md#local-paths), then copy the calibration into the driver source:

```bash
source ~/antnoid-handover/config/local.env
cp -r ~/antnoid-handover/config/insta360/Insta360X3_IAQFB23129J8E6 \
  "$INSTA_WS/src/ros_insta360/config/"

source /opt/ros/humble/setup.bash
cd "$INSTA_WS"
colcon build --packages-select ros_insta360
source install/setup.bash
```

The launchfile resolves the XML from the installed package share. This command shows that directory:

```bash
ros2 pkg prefix --share ros_insta360
```

Supply the Insta360 Camera SDK and any required `lut_*.yml` stitching table separately. Large lookup tables are not included here. Keep the existing tables in the driver configuration directory when using the robot installation.

Then follow [the Insta360 launch step](../../docs/Mapping_and_Waypoint_Navigation.md#insta360).
