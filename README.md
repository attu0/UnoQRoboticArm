<div align="center">

  ![Logo White](./docs/logo_white.svg#gh-dark-mode-only)

</div>

<div align="center">

  ![Logo Black](./docs/logo_black.svg#gh-light-mode-only)

</div>

Andino is a fully open-source diff drive robot designed for educational purposes and low-cost applications.
It is fully integrated with ROS 2 and it is a great base platform to improve skills over the robotics field.
With its open-source design, anyone can modify and customize the robot to suit their specific needs.

<p align="center">
  <img src="docs/real_robot.png" width=900 />
</p>

_Note: For videos go to [Media](#selfie-media) section._

## :books: Package Summary

- :rocket: [`andino_bringup`](./andino_bringup): Contains mainly launch files in order to launch all related driver and nodes to be used in the real robot.
- :robot: [`andino_hardware`](./andino_hardware): Contains information about the Andino assembly and hardware parts.
- :ledger: [`andino_description`](./andino_description): Contains the URDF description of the robot.
- :hammer_and_pick: [`andino_firmware`](./andino_firmware): Contains the code be run in the microcontroller for interfacing low level hardware with the SBC.
- :gear: [`andino_base`](./andino_base): [ROS Control hardware interface](https://control.ros.org/master/doc/ros2_control/hardware_interface/doc/writing_new_hardware_interface.html) is implemented.
- :control_knobs: [`andino_control`](./andino_control/): It launches the [`controller_manager`](https://control.ros.org/humble/doc/ros2_control/controller_manager/doc/userdoc.html) along with the [ros2 controllers](https://control.ros.org/master/doc/ros2_controllers/doc/controllers_index.html): [diff_drive_controller](https://control.ros.org/master/doc/ros2_controllers/diff_drive_controller/doc/userdoc.html) and the [joint_state_broadcaster](https://control.ros.org/master/doc/ros2_controllers/joint_state_broadcaster/doc/userdoc.html).
- :world_map: [`andino_slam`](./andino_slam/): Provides support for SLAM with your `andino` robot.
- :compass: [`andino_navigation`](./andino_navigation/): Navigation stack based on `nav2`.

## :paperclips: Related projects

Projects built upon Andino! :rocket:

- :rocket: [`andino_ansible_config`](https://github.com/garyservin/andino_ansible_config): (**Thanks @garyservin !**): Ansible configuration to easily setup an Andino robot.
- :computer: [`andino_gz`](https://github.com/Ekumen-OS/andino_gz): [Gazebo](https://gazebosim.org/home)(non-classic)-based simulation of the `andino` robot.
- :lady_beetle: [`andino_webots`](https://github.com/Ekumen-OS/andino_webots): [Webots](https://github.com/cyberbotics/webots)-based simulation of the Andino robot fully integrated with ROS 2.
- :joystick: [`andino_o3de`](https://github.com/Ekumen-OS/andino_o3de): [O3DE](https://o3de.org/)-based simulation of the Andino robot.
- :green_circle: [`andino_isaac`](https://github.com/Ekumen-OS/andino_isaac): [Isaac Sim](https://docs.omniverse.nvidia.com/isaacsim/latest/index.html)-based simulation of the Andino robot.
- :m: [`andino_mujoco`](https://github.com/Ekumen-OS/andino_mujoco): [MuJoCo](https://mujoco.org/)-based simulation of the Andino robot.
- :robot: [`andino_rmf`](https://github.com/Ekumen-OS/andino_rmf): [OpenRMF](https://www.open-rmf.org/) integration of Andino simulation.
- :test_tube: [`andino_integration_tests`](https://github.com/Ekumen-OS/andino_integration_tests): Extension to the Andino robot showing how to build integration tests.
- :framed_picture: [`andino_lichtblick`](https://github.com/Ekumen-OS/andino_lichtblick): [Lichtblick](https://github.com/lichtblick-suite/lichtblick/) integration with Andino for web-based visualization.
- :crab: [`andino-rs`](https://github.com/Ekumen-OS/andino-rs): Rustacean version of *andino* robot. It also provides integration with [*dora*](https://github.com/dora-rs/dora) framework for both real and simulated *andino*.
- :nerd_face: [`robotics_essentials_ros2`](https://github.com/henki-robotics/robotics_essentials_ros2): ROS 2 Essentials material for robotic course at [*University of Eastern Finland*](https://www.uef.fi/en).

## :busts_in_silhouette: Community

[<img src="docs/discord-mark-blue.png" width=30 hspace="20"/>](https://discord.gg/tHhH32CTHu) Join our Discord and contribute to the community!


## :pick: Robot Assembly

Visit [`andino_hardware`](./andino_hardware/) for assembly instructions.

## :mechanical_arm: Installation

Remember to first go over the assembly instructions at [`andino_hardware`](./andino_hardware/)!

### Platforms

- ROS 2:
  - Humble Hawksbill
  - Jazzy Jalisco
- OS:
  - Ubuntu 22.04 Jammy Jellyfish (Humble)
  - Ubuntu 24.04 Noble Numbat (Jazzy)
  - Ubuntu Mate 22.04 / Ubuntu Server 24.04 (On real robot e.g: Raspberry Pi 4B)


#### Dependencies


#### colcon workspace


### Install the binaries


## :rocket: Usage

### Robot bringup



### Teleoperation



#### Keyboard


#### Joystick


### RViz


## :compass: Navigation

## :computer: Simulation


## :selfie: Media

### RVIZ Visualization



### slam



## :star2: Inspirational sources

This section is dedicated to recognizing and expressing gratitude to the open-source repositories that have served as a source of inspiration for this project. We highly recommend exploring these repositories for further inspiration and learning.

 * [articubot_one](https://github.com/joshnewans/articubot_one)
 * [diffbot](https://github.com/ros-mobile-robots/diffbot)
 * [noah_hardware](https://github.com/GonzaCerv/noah-hardware)
 * [linorobot](https://github.com/linorobot/linorobot2)

## :raised_hands: Contributing

Issues or PRs are always welcome!