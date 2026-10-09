#!/usr/bin/env python3

from datetime import datetime
from pathlib import Path

from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, LogInfo
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node


def generate_launch_description():
    # Dossier contenant ce fichier launch
    launch_directory = Path(__file__).resolve().parent

    # Launch existant correspondant au terminal 0
    ids_gps_launch_file = launch_directory / "ids_gps_forRecord.launch.py"

    if not ids_gps_launch_file.exists():
        raise FileNotFoundError(
            f"Launch file introuvable : {ids_gps_launch_file}"
        )

    # Même nom de dossier que dans les scripts shell
    current_date = datetime.now().strftime("%Y-%m-%d")
    record_directory = Path.home() / "Desktop" / f"record_{current_date}"

    # mkdir -p : ne génère pas d'erreur si le dossier existe déjà
    record_directory.mkdir(parents=True, exist_ok=True)

    return LaunchDescription([
        LogInfo(
            msg=f"Enregistrement dans : {record_directory}"
        ),

        # Équivalent du terminal 1
        Node(
            package="ant_one",
            executable="gps_recorder",
            name="gps_recorder",
            output="screen",
            emulate_tty=True,
            cwd=str(record_directory),
        ),

        # Équivalent du terminal 2
        Node(
            package="ant_one",
            executable="img_recorder",
            name="img_recorder",
            output="screen",
            emulate_tty=True,
            cwd=str(record_directory),
            remappings=[
                (
                    "/img_recorder/image_raw",
                    "/ids_camera/image_raw",
                ),
            ],
            parameters=[
                {
                    "png_compression": 0,
                },
            ],
        ),
    ])
