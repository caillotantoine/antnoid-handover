# Virtual HRP5P — Engine3D and waypoint navigation

Run all commands locally on the simulation workstation.

## Requirements and preparation

Install:

- [mc_rtc](https://github.com/jrl-umi3218/mc_rtc) and [mc_mujoco](https://github.com/isri-aist/mc_mujoco).
- HRP5P robot assets and BaselineWalkingController (BWC).
- [Engine3D](https://github.com/PerceptionRobotique/Engine3D) and [ros_Engine3D](https://github.com/PerceptionRobotique/ros_Engine3D).
- [robotControlSim](https://github.com/isri-aist/robotControlSim).
- The ROS 2 Docker image `stella_vslam-ros-socket` and `orb_vocab.fbow`.

The Engine3D package must provide `ros_engine3d_JRLpts_hrp5_equi.xml`, with the laboratory point cloud path and camera TF configured. This launchfile, the point cloud, HRP5P assets and BWC are separate requirements; they are not included here.

Set `MainRobot: HRP5P` and `Enabled: BaselineWalkingController` in the workstation's mc_rtc configuration.

Clone this repository at `~/antnoid-handover`, then:

```bash
mkdir -p ~/stella_data/input ~/stella_data/maps ~/antnoid_routes
cp -rn ~/antnoid-handover/config/stella/input/. ~/stella_data/input/
```

Copy `orb_vocab.fbow` to `~/stella_data/input/`. Existing input files are preserved.

In each host ROS terminal, source ROS and the installed simulation, rendering and navigation workspaces. Replace the three workspace paths below with your installation paths:

```bash
source /opt/ros/humble/setup.bash
source /path/to/simulation_ws/install/setup.bash
source /path/to/engine3d_ws/install/setup.bash
source /path/to/robotControlSim/ros2/install/setup.bash
export ROS_DOMAIN_ID=230
export RMW_IMPLEMENTATION=rmw_cyclonedds_cpp
```

## 1. Start the simulated robot and camera

Terminal 1:

```bash
mc_mujoco --sync
```

Terminal 2:

```bash
ros2 launch mc_rtc_ticker display.launch
```

In RViz, open the mc_rtc panel and the BWC tab. Start the controller and use **GuiWalk** to move manually.

Terminal 3:

```bash
ros2 launch ros_engine3d ros_engine3d_JRLpts_hrp5_equi.xml
```

Display `/ros2_engine3d/camera/image` in RViz. The SLAM configuration expects 1440 × 720 equirectangular RGB images. Set the rendered image size accordingly.

## 2. Build and save a map

Terminal 4:

```bash
docker run -it --net=host \
  -v "$HOME/stella_data:/stella_data" \
  --entrypoint bash stella_vslam-ros-socket
```

Inside the container:

```bash
source /ros2_ws/install/setup.bash
export ROS_DOMAIN_ID=230
export RMW_IMPLEMENTATION=rmw_cyclonedds_cpp

ros2 run stella_vslam_ros run_slam \
  -v /stella_data/input/orb_vocab.fbow \
  -c /stella_data/input/JRL_MC_equirgb_thetaS_1280x720.yaml \
  --viewer none \
  --map-db-out /stella_data/maps/virtual_route1.msg \
  --ros-args -r /camera/image_raw:=/ros2_engine3d/camera/image
```

Move the simulated robot through the route with GuiWalk and revisit visible areas. Stop SLAM with **Ctrl+C**, wait for saving to finish, then confirm:

```bash
ls -lh /stella_data/maps/virtual_route1.msg
```

## 3. Reload the map and record waypoints

Inside the same container:

```bash
ros2 run stella_vslam_ros run_slam \
  -v /stella_data/input/orb_vocab.fbow \
  -c /stella_data/input/JRL_MC_equirgb_thetaS_1280x720.yaml \
  --viewer none \
  --map-db-in /stella_data/maps/virtual_route1.msg \
  --disable-mapping \
  --ros-args -r /camera/image_raw:=/ros2_engine3d/camera/image
```

Wait for localisation. In a host terminal, check that `/run_slam/camera_pose` is `nav_msgs/msg/Odometry` and supplies live poses:

```bash
ros2 topic info /run_slam/camera_pose
ros2 topic echo /run_slam/camera_pose --once --field pose
```

Start the recorder:

```bash
ros2 run robot_sim_toolbox pose2wpt_rec --ros-args \
  -r /simple_robot/controller/odom:=/run_slam/camera_pose \
  -p yaml_path:="$HOME/antnoid_routes/virtual_route1.yaml"
```

Move manually with GuiWalk. Press **Space** at each waypoint and **Ctrl+C** to finish. Each press saves immediately; an existing YAML is appended to. Use a new filename for a new route.

## 4. Follow the waypoint sequence

Keep rendering and SLAM running with the same map. In BWC, enable **Start Teleop** and connect its velocity input to `/cmd_vel`.

Host terminal 1:

```bash
ros2 run robot_sim_toolbox simple_servo --ros-args \
  -r /simple_robot/controller/odom:=/run_slam/camera_pose
```

Host terminal 2:

```bash
ros2 run robot_sim_toolbox baseline_nav --ros-args \
  -p yaml_path:="$HOME/antnoid_routes/virtual_route1.yaml"
```

Use the same map and pose frame for recording and following. SLAM scale and camera-to-body registration must match the controller coordinates.

To use controller odometry instead of SLAM, replace `/run_slam/camera_pose` with `/control/hrp5_p/odom` in **both** recorder and servo commands, and record a separate waypoint YAML.

## 5. Display guidance and stop

Optional host terminal:

```bash
ros2 run robot_sim_toolbox joystick_guide_web --ros-args \
  -p image_enabled:=true \
  -p image_topic:=/ros2_engine3d/camera/image \
  -p port:=3002
```

Open `http://localhost:3002`.

Disable BWC teleoperation to stop motion. Stop navigation, servo, SLAM, rendering and simulation, in that order, with Ctrl+C in their terminals.
