# Go1 — Mapping and waypoint navigation

Use one camera to build a map, save it, record waypoints in that map, then reload both files to follow the route.

## Requirements and preparation

- Camera and its ROS 2 driver.
- The native Go1 ROS 2 driver `unitree_ros`, installed on the NUC.
- `stella_vslam-ros-socket` Docker image and `orb_vocab.fbow`.
- Navigation workspace: `$NAV_WS` (configured in `config/local.env`).
- This repository cloned at `~/antnoid-handover` on the NUC.

Connect with `ssh ROBOT_USER@ROBOT_HOST`, using the login provided by the robot administrator. On the NUC, configure [local paths](../README.md#local-paths), then:

```bash
source ~/antnoid-handover/config/local.env
mkdir -p "$STELLA_DATA/input" "$STELLA_DATA/maps/waypoints"
mkdir -p "$WAYPOINT_DIR"
cp -rn ~/antnoid-handover/config/stella/input/. "$STELLA_DATA/input"/
```

Copy `orb_vocab.fbow` to `$STELLA_DATA/input/`. The command above leaves existing configuration files untouched.

In each host ROS terminal:

```bash
source ~/antnoid-handover/config/local.env
source /opt/ros/humble/setup.bash
export ROS_DOMAIN_ID=231
export RMW_IMPLEMENTATION=rmw_cyclonedds_cpp
```

Use `route1` for a new route, or replace it consistently with another name. Keep its map and waypoint YAML together.

## 1. Power on the Go1 and start its driver

### Power and remote control

1. Place the Go1 on the floor with space around it.
2. Power on the battery with a short press followed by a long press; release when the four LEDs finish their sequence (about 3 seconds). Switch on the remote control.
3. Use **L2 + A** to change between the low and standing positions. Keep the remote in hand while operating the robot.

**L2 + B** selects the damping/soft-stop mode; it is not the battery power-off command.

### Native ROS 2 driver on the NUC

[`unitree_ros`](https://github.com/snt-arg/unitree_ros) is installed directly on the NUC. Run it in a **host terminal**, outside the SLAM Docker container, with the ROS environment above loaded:

```bash
ros2 pkg prefix unitree_ros
ros2 launch unitree_ros unitree_driver_launch.py
```

Leave the driver running throughout manual walking, waypoint recording and route following. It receives `geometry_msgs/msg/Twist` on `/cmd_vel` and sends velocity commands to the Go1.

The default launch uses the robot's wired network connection. Operator SSH over the NUC hotspot does not change this. Use `wifi:=true` only when the driver itself connects to the Go1 through its Wi-Fi network.

If ROS cannot find `unitree_ros`, source the `install/setup.bash` of the workspace containing the installed driver, then retry.

### Manual walking

Use the robot's remote control for manual walking before starting navigation. To drive with a USB gamepad connected to the NUC, launch **one** teleoperation node in another host ROS terminal.

PS5:

```bash
ros2 launch teleop_twist_joy teleop-launch.py joy_config:='ps5'
```

Xbox:

```bash
ros2 launch teleop_twist_joy teleop-launch.py joy_config:='xbox' enable_button:=2
```

Hold the configured enable button and use the sticks to send movement commands. Release it to stop the teleoperation command. Stop this USB-gamepad node with Ctrl+C before starting `baseline_nav`; keep the robot's own remote in hand.

In another host terminal, confirm the driver subscribes to the velocity topic:

```bash
ros2 topic info /cmd_vel --verbose
```

## 2. Start one image source

### IDS HDR

Follow [the HDR manual](IDS_HDR_Adaptive_Exposure.md), or launch directly after sourcing its workspace:

```bash
source "$IDS_WS/install/setup.bash"
ros2 launch ~/antnoid-handover/launch/ids/ids_hdr.launch.py
```

SLAM input: `/camera/image_raw`.

### Insta360

Connect and turn on the camera. Install the matching calibration using [these instructions](../config/insta360/README.md), then:

```bash
source "$INSTA_WS/install/setup.bash"
ros2 launch ~/antnoid-handover/launch/insta360/bringup.xml
```

SLAM input: `/insta360/equi/image_raw`. The supplied SLAM YAML expects equirectangular 1440 × 720 RGB images. Match the output dimensions to this configuration.

## 3. Open the SLAM container

In another host terminal:

```bash
docker run -it --net=host \
  -v "$STELLA_DATA:/stella_data" \
  --entrypoint bash stella_vslam-ros-socket
```

Inside it:

```bash
source /ros2_ws/install/setup.bash
export ROS_DOMAIN_ID=231
export RMW_IMPLEMENTATION=rmw_cyclonedds_cpp
mkdir -p /stella_data/maps/waypoints
```

Set the camera arguments **inside this same container terminal**.

For IDS:

```bash
SLAM_CAMERA_ARGS=(
  -c /stella_data/input/rap_rev/IDS_1024_AC_2122.yaml
  --mask /stella_data/input/rap_rev/IDS_89_496_498.png
)
SLAM_IMAGE_TOPIC=/camera/image_raw
```

For Insta360:

```bash
SLAM_CAMERA_ARGS=(-c /stella_data/input/JRL_equirgb_1280x720.yaml)
SLAM_IMAGE_TOPIC=/insta360/equi/image_raw
```

## 4. Build and save the map

Inside the container:

```bash
ros2 run stella_vslam_ros run_slam \
  -v /stella_data/input/orb_vocab.fbow \
  "${SLAM_CAMERA_ARGS[@]}" \
  --viewer none \
  --map-db-out /stella_data/maps/waypoints/route1.msg \
  --ros-args -r /camera/image_raw:="$SLAM_IMAGE_TOPIC"
```

Move the camera along the route under manual control. Revisit visible areas so the map can close loops. Stop SLAM with **Ctrl+C** and wait for map saving to finish. Confirm the file exists:

```bash
ls -lh /stella_data/maps/waypoints/route1.msg
```

## 5. Reload the map and record waypoints

Inside the same container, with the camera still running:

```bash
ros2 run stella_vslam_ros run_slam \
  -v /stella_data/input/orb_vocab.fbow \
  "${SLAM_CAMERA_ARGS[@]}" \
  --viewer none \
  --map-db-in /stella_data/maps/waypoints/route1.msg \
  --disable-mapping \
  --ros-args -r /camera/image_raw:="$SLAM_IMAGE_TOPIC"
```

Place the camera in a recognisable area and wait for localisation. In a host navigation terminal:

```bash
source "$NAV_WS/install/setup.bash"
ros2 topic info /run_slam/camera_pose
ros2 topic echo /run_slam/camera_pose --once --field pose
```

The pose input must be `nav_msgs/msg/Odometry`. Start recording only once live poses are available:

```bash
ros2 run robot_sim_toolbox pose2wpt_rec --ros-args \
  -r /simple_robot/controller/odom:=/run_slam/camera_pose \
  -p yaml_path:="$WAYPOINT_DIR/route1.yaml"
```

Move along the route manually. Press **Space** at each target pose; each press saves a waypoint immediately. Press **Ctrl+C** to finish. An existing YAML is appended to: choose a new filename for a new route. Yaw is stored in degrees.

## 6. Follow the route

Keep the camera and SLAM running with the same map and `--disable-mapping`.

Keep the robot remote control in hand throughout waypoint following. The current setup moves slowly and is easy to supervise. Keep an emergency-stop control within reach.

Manual and autonomous velocity commands are **added together**. The robot executes the sum, rather than giving the remote control exclusive priority. Use the remote to counteract motion and stop the robot. To keep it stopped, also stop the waypoint client and servo; centring the remote does not remove the autonomous command.

Host terminal 1, with the navigation workspace sourced:

```bash
ros2 run robot_sim_toolbox simple_servo --ros-args \
  -r /simple_robot/controller/odom:=/run_slam/camera_pose
```

Host terminal 2, with the same workspace sourced:

```bash
ros2 run robot_sim_toolbox baseline_nav --ros-args \
  -p yaml_path:="$WAYPOINT_DIR/route1.yaml"
```

The servo produces `/cmd_vel` for the `unitree_ros` driver started in step 1. Keep that driver running and use its configured velocity topic. The waypoint nodes do not provide obstacle avoidance. Keep the map's metric scale and camera-to-body transform consistent with the robot.

For the supplied reference route, use `lab5.msg` with `lab5_0.yaml`; these files must be supplied separately.

## 7. Display guidance and stop

Optional host terminal, with the navigation workspace sourced:

```bash
ros2 run robot_sim_toolbox joystick_guide_web --ros-args \
  -p image_enabled:=true \
  -p image_topic:=/camera/HDR/preview \
  -p port:=3002 \
  -p qos_best_effort:=true -p qos_keep_last:=1
```

For Insta360, replace the image topic with `/insta360/equi/image_raw`. Open `http://ROBOT_HOST:3002`. This displays guidance, not browser teleoperation.

Stop physical motion using the remote control or an emergency-stop button. Stop navigation, servo, SLAM and camera, in that order, using Ctrl+C in their terminals. Lower the robot with the remote control, then stop `unitree_ros`. Switch off the battery with the short-press/long-press sequence.

## Troubleshooting: ROS nodes cannot communicate

A matching `ROS_DOMAIN_ID` is not always sufficient. CycloneDDS may need an explicit network interface in its XML configuration.

1. List the available interfaces:

   ```bash
   ip -brief address
   printenv CYCLONEDDS_URI
   ```

2. Select the interface connected to the other ROS machine in the CycloneDDS XML. For example, replace `INTERFACE_NAME` below with the actual interface name:

   ```xml
   <CycloneDDS xmlns="https://cdds.io/config">
     <Domain id="any">
       <General>
         <Interfaces>
           <NetworkInterface name="INTERFACE_NAME"/>
         </Interfaces>
       </General>
     </Domain>
   </CycloneDDS>
   ```

3. Point each ROS terminal to the file before launching nodes:

   ```bash
   export CYCLONEDDS_URI="file://$HOME/.ros/cyclonedds.xml"
   ```

   Save the XML at that path first. Restart the affected ROS processes. If the CLI still shows stale discovery, run `ros2 daemon stop` and retry. For host-network Docker containers, make the XML available inside the container and set `CYCLONEDDS_URI` there as well. Use each machine's own interface name.

If an older CycloneDDS version rejects `Interfaces`, use its `General/NetworkInterfaceAddress` setting instead. See the [CycloneDDS configuration guide](https://cyclonedds.io/docs/cyclonedds/latest/config/index).
