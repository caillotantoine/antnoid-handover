from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue


def generate_launch_description():

    frame_rate = LaunchConfiguration('frame_rate')
    maxsaturated = LaunchConfiguration('maxsaturated')
    maxdark = LaunchConfiguration('maxdark')

    return LaunchDescription([

        DeclareLaunchArgument(
            'frame_rate',
            default_value='15.0',
            description='Camera frame rate'
        ),

        DeclareLaunchArgument(
            'maxsaturated',
            default_value='10.0',
            description='Maximum percentage of saturated pixels for discrete auto exposure'
        ),

        DeclareLaunchArgument(
            'maxdark',
            default_value='20.0',
            description='Maximum percentage of dark pixels for discrete auto exposure'
        ),

        Node(
            package='ids_camera_driver',
            executable='ids_camera_node',
            parameters=[
                {
                    'frame_rate': ParameterValue(frame_rate, value_type=float),
                    'dual_expo': 12,
                    'exposure_ms': 45.0
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
                    'discrete_ae': False,
                    'dualExpRatio_': 0.12,
                    'maxsaturated': ParameterValue(maxsaturated, value_type=float),
                    'maxdark': ParameterValue(maxdark, value_type=float)
                }],
            remappings=[
                ('/camera/image_raw', '/ids_camera/image_raw')
            ],
            output='screen',
        ),

        Node(
            package='nmea_gps_node',
            executable='nmea_gps_node',
            name='nmea_gps_node',
            parameters=[]
        )

        # Node(
        #     package='deo-hdr-node',
        #     executable='qos_changer',
        #     parameters=[{
        #             'qos_best_effort_out': True,
        #             'qos_keep_last_out': 1
        #         }],
        #     remappings=[
        #         ('/qos_changer/image_in', '/camera/HDR/image_raw'),
        #         ('/qos_changer/image_out', '/camera/image_raw')
        #     ],
        #     output='screen',
        # )

    ])
