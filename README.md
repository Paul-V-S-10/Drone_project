# ArduPilot & Gazebo SITL Environment (Ubuntu 24.04)

This repository contains the setup guide and configuration for a modern ArduPilot Software-In-The-Loop (SITL) simulation environment integrated with Gazebo Harmonic. 

This guide is specifically tailored for **Ubuntu 24.04 LTS**, which requires strict Python virtual environments and relies on the modern Gazebo architecture (formerly Ignition) rather than the deprecated Gazebo Classic (Gazebo 9/11).

## System Architecture
* **OS:** Ubuntu 24.04 LTS
* **Workspace:** `~/drone_project/` *(You can rename this, but update the paths below accordingly)*
* **Simulator:** Gazebo Harmonic
* **Python Environment:** `drone_env` (Virtual Environment)

---

## Phase 1: Core Framework Installation

### 1. Install ArduPilot Source Code
Clone the main flight controller software and install its base system dependencies.

```bash
mkdir ~/drone_project && cd ~/drone_project
git clone --recurse-submodules [https://github.com/Ardupilot/ardupilot.git](https://github.com/Ardupilot/ardupilot.git)
cd ardupilot
Tools/environment_install/install-prereqs-ubuntu.sh -y
```

### 2. Install Gazebo Harmonic
Add the modern OSRF repository keys and install the 3D physics engine.
```bash
sudo apt update
sudo apt install curl lsb-release gnupg
sudo curl [https://packages.osrfoundation.org/gazebo.gpg](https://packages.osrfoundation.org/gazebo.gpg) --output /usr/share/keyrings/pkgs-osrf-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/pkgs-osrf-archive-keyring.gpg] [http://packages.osrfoundation.org/gazebo/ubuntu-stable](http://packages.osrfoundation.org/gazebo/ubuntu-stable) $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/gazebo-stable.list > /dev/null
sudo apt update
sudo apt install gz-harmonic
```
### 3. Build the Communications Plugin
Compile the official bridge that allows ArduPilot to communicate with Gazebo Harmonic.
#### Install development dependencies
```bash


sudo apt install libgz-sim8-dev rapidjson-dev libopencv-dev libgstreamer1.0-dev libgstreamer-plugins-base1.0-dev gstreamer1.0-plugins-bad gstreamer1.0-libav gstreamer1.0-gl

```
#### Clone and build the plugin

```bash

cd ~/drone_project
git clone [https://github.com/ArduPilot/ardupilot_gazebo](https://github.com/ArduPilot/ardupilot_gazebo)
cd ardupilot_gazebo
export GZ_VERSION=harmonic
mkdir build && cd build
cmake .. -DCMAKE_BUILD_TYPE=RelWithDebInfo
make -j4
```
## Phase 2: System Configuration
### 1. Configure Paths & Aliases
Map out where the files live and create a global shortcut to easily activate your Python environment from anywhere.
```bash
sudo apt install -y gedit
gedit ~/.bashrc
```
Add these lines to the very bottom of the file:

```bash
# ArduPilot SITL Path
export PATH=$PATH:$HOME/drone_project/ardupilot/Tools/autotest

# Gazebo Plugin & Models Paths
export GZ_SIM_SYSTEM_PLUGIN_PATH=$HOME/drone_project/ardupilot_gazebo/build:${GZ_SIM_SYSTEM_PLUGIN_PATH}
export GZ_SIM_RESOURCE_PATH=$HOME/drone_project/ardupilot_gazebo/models:$HOME/drone_project/ardupilot_gazebo/worlds:${GZ_SIM_RESOURCE_PATH}

# Global alias to activate the Python environment
alias flydrone='source ~/drone_project/drone_env/bin/activate'
```
Apply the changes to your current terminal:

```bash
source ~/.bashrc
```
### 2. Equip the Python Virtual Environment
Ubuntu 24.04 blocks system-wide pip installs. Load all required builder tools and graphical map dependencies directly into your isolated environment.
```bash
flydrone
pip install empy==3.3.4 pexpect future MAVProxy pymavlink wxPython matplotlib opencv-python numpy
```
## Phase 3: Flight Operations Manual
Whenever you want to run the simulation, follow this standard operating procedure using two separate terminal windows.
### Step 1: Start the 3D World (Terminal 1)
Open a fresh terminal and launch the Gazebo runway environment:
```bash
gz sim -v4 -r iris_runway.sdf
```
### Step 2: Connect the Drone's Brain (Terminal 2)
Open a second terminal, activate your Python environment, and launch the SITL bridge with the graphical map enabled:
```bash
flydrone
cd ~/drone_project/ardupilot/ArduCopter/
sim_vehicle.py -v ArduCopter -f gazebo-iris --model JSON --map --console
```
