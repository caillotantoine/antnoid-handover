from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue


def generate_launch_description():

    frame_rate = LaunchConfiguration('frame_rate')

    return LaunchDescription([

        DeclareLaunchArgument(
            'frame_rate',
            default_value='22.0',
            description='Camera frame rate'
        ),

        Node(
            package='ids_camera_driver',
            executable='ids_camera_node',
            parameters=[
                {
                    'frame_rate': ParameterValue(frame_rate, value_type=float),
                    'dual_expo': 12
                }
            ],
            output='screen',
            emulate_tty=True,
        ),

        Node(
            package='deo-hdr-node',
            executable='hdr_processor',
            parameters=[{
                    'hdr_prev': True,
                    'discrete_ae': True,
                    'dualExpRatio_': 0.12
                }],
            remappings=[
                ('/camera/image_raw', '/ids_camera/image_raw')
            ],
            output='screen',
        ),

        Node(
            package='deo-hdr-node',
            executable='qos_changer',
            parameters=[{
                    'qos_best_effort_out': True,
                    'qos_keep_last_out': 1
                }],
            remappings=[
                ('/qos_changer/image_in', '/camera/HDR/image_raw'),
                ('/qos_changer/image_out', '/camera/image_raw')
            ],
            output='screen',
        )
    ])
