import os
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.substitutions import Command, LaunchConfiguration
from launch_ros.substitutions import FindPackageShare
from launch.conditions import IfCondition
from launch_ros.actions import Node
from launch.launch_description_sources import PythonLaunchDescriptionSource

#https://automaticaddison.com/how-to-load-a-urdf-file-into-rviz-ros-2/
#https://answers.ros.org/question/382000/ros2-makes-launch-files-crazy-too-soon-to-be-migrating/#:~:text=#!/usr/bin/env,condition=UnlessCondition(use_gui)%0A%20%20%20%20)%0A%0A%20%20])

#https://automaticaddison.com/how-to-create-a-simulated-mobile-robot-in-ros-2-using-urdf/#Create_the_Launch_File
#https://www.theconstructsim.com/how-to-use-xacro-in-ros2-gazebo/

#http://wiki.ros.org/simulator_gazebo/Tutorials/SpawningObjectInSimulation
#https://automaticaddison.com/set-up-lidar-for-a-simulated-mobile-robot-in-ros-2/

#Penser à utiliser la commande pour générer correctement l'urdf depuis le xacro

def generate_launch_description():

    use_sim_time = LaunchConfiguration('use_sim_time', default='false')
    use_rviz = LaunchConfiguration('use_rviz',default='true')
    urdf_model = LaunchConfiguration('urdf_model')

    pkg_gazebo = FindPackageShare(package='gazebo_ros').find('gazebo_ros')
    pkg_exo = FindPackageShare(package='osiris_exo').find('osiris_exo')
    

    rviz_config_file = os.path.join(pkg_exo,'demo_bis.rviz')
    urdf_file = os.path.join(pkg_exo,'simple_robot.urdf')
    

    return LaunchDescription([
        DeclareLaunchArgument(
            'use_sim_time',
            default_value='true',
            description='Use Gazebo\'s clock if true'),
        DeclareLaunchArgument(
            'use_rviz',
            default_value='true',
            description='Whether to start RVIZ or not'),
        DeclareLaunchArgument(
            name='urdf_model',
            default_value=urdf_file,
            description='Absolute path to model file'),
        
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(os.path.join(pkg_gazebo, 'launch', 'gazebo.launch.py'))),

        Node(
            package='joint_state_publisher',
            executable='joint_state_publisher',
            name='joint_state_publisher',
            parameters=[{'use_sim_time': use_sim_time}]),
        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            parameters=[{'use_sim_time': use_sim_time, 
            'robot_description': Command(['xacro ',' ', urdf_model])}],
            arguments=[urdf_model]),
        Node(
            condition=IfCondition(use_rviz),
            package='rviz2',
            executable='rviz2',
            name='rviz2',
            output='screen',
            arguments=['-d', rviz_config_file])
    ])
