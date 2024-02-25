
# Author: Addison Sears-Collins
# Date: September 14, 2021
# Description: Launch a two-wheeled robot URDF file using Rviz.
# https://automaticaddison.com

import os
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.conditions import IfCondition, UnlessCondition
from launch.substitutions import Command, LaunchConfiguration
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare
from launch import LaunchDescription
from launch.actions import RegisterEventHandler
from launch.event_handlers import OnProcessExit
from launch.substitutions import Command, FindExecutable, PathJoinSubstitution,LaunchConfiguration

from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare
from launch.actions import DeclareLaunchArgument, RegisterEventHandler

def generate_launch_description():

  gui = LaunchConfiguration('gui')
    
  declare_use_joint_state_publisher_cmd = DeclareLaunchArgument(
    name='gui',
    default_value='True',
    description='Flag to enable joint_state_publisher_gui')
  

  # Publish the joint state values for the non-fixed joints in the URDF file.
  start_joint_state_publisher_cmd = Node(
    condition=UnlessCondition(gui),
    package='joint_state_publisher',
    executable='joint_state_publisher',
    name='joint_state_publisher')

  # A GUI to manipulate the joint state values
  start_joint_state_publisher_gui_node = Node(
    condition=IfCondition(gui),
    package='joint_state_publisher_gui',
    executable='joint_state_publisher_gui',
    name='joint_state_publisher_gui')

  # Subscribe to the joint states of the robot, and publish the 3D pose of each link.
  start_robot_state_publisher_cmd = Node(
    package='robot_state_publisher',
    executable='robot_state_publisher',
    parameters=[{'use_sim_time': True, 
    'robot_description': Command([PathJoinSubstitution(
            [FindPackageShare("bot_base"), "urdf", "bot_base.urdf.xacro"]
        ),
        " ",
        "use_mock_hardware:=True"])}],
    )

  # Create the launch description and populate
  ld = LaunchDescription()

  # Declare the launch options
  ld.add_action(declare_use_joint_state_publisher_cmd)

  # Add any actions
  ld.add_action(start_joint_state_publisher_cmd)
  ld.add_action(start_joint_state_publisher_gui_node)
  ld.add_action(start_robot_state_publisher_cmd)

  return ld