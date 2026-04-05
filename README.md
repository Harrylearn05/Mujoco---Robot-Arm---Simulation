# 🤖 MuJoCo Robot Arm Simulation

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.8%2B-blue">
  <img src="https://img.shields.io/badge/MuJoCo-Simulator-green">
  <img src="https://img.shields.io/badge/License-Apache%202.0-orange">
</p>

A simple and modular robotic arm simulation built using **MuJoCo**.
This project is designed for learning robotics, control systems, and simulation.

---

## 🚀 Features

* 🦾 Robotic arm simulation in MuJoCo
* 🎯 Joint-level control
* 📊 Data logging for analysis
* 🧩 Clean and modular structure
* 🧪 Suitable for robotics and reinforcement learning experiments

---

## 📁 Project Structure

```
Mujoco---Robot-Arm---Simulation/
|-- assets/                    # Assets and resources
|-- config.py                  # Configuration settings
|-- dt_run.py                  # Digital twin running script
|-- interpolator.py            # Interpolation functions for trajectories
|-- open_manipulator_x.png     # Reference image of the manipulator
|-- open_manipulator_x.xml     # Robot model (MJCF format)
|-- real_interface.py          # Hardware interface for the real robot arm
|-- robot_tasks.py             # Defined tasks and movements
|-- scene.xml                  # Main MuJoCo simulation scene
|-- sim_interface.py           # Interface for the simulated robot
|-- sim_run.py                 # Simulation execution script
|-- twin_bridge.py             # Bridge logic for the digital twin
|-- LICENSE                    # Apache-2.0 License
|-- README.md                  # Project documentation

---

## ⚙️ Installation

```
# Clone repository
git clone https://github.com/Harrylearn05/Mujoco---Robot-Arm---Simulation.git
cd Mujoco---Robot-Arm---Simulation

# Install dependencies
pip install dynamixel_sdk 

# Install MuJoCo
pip install mujoco
```

---

## ▶️ Usage

Run the simulation:

```
python3 sim_run.py
```

---

## 🎮 Simulation Capabilities

* Load robotic arm model (MJCF format)
* Perform joint-level control
* Visualize motion using MuJoCo viewer
* Simulate:

  * Free motion
  * Controlled movement
  * Interaction with environment

---

## 🧠 Learning Objectives

This project helps you understand:

* Robot kinematics and dynamics
* MuJoCo simulation workflow
* Control of articulated systems
* Data collection for robotics and AI

---
