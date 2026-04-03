# ArduPilot & Gazebo SITL Environment (Ubuntu 24.04)

This repository contains the setup guide and configuration for a modern ArduPilot Software-In-The-Loop (SITL) simulation environment integrated with Gazebo Harmonic. 

This guide is specifically tailored for **Ubuntu 24.04 LTS**, which requires strict Python virtual environments and relies on the modern Gazebo architecture (formerly Ignition) rather than the deprecated Gazebo Classic (Gazebo 9/11).

## 📋 System Architecture
* **OS:** Ubuntu 24.04 LTS
* **Workspace:** `~/drone_project/` *(You can rename this, but update the paths below accordingly)*
* **Simulator:** Gazebo Harmonic
* **Python Environment:** `drone_env` (Virtual Environment)

---

## 🚀 Phase 1: Core Framework Installation

### 1. Install ArduPilot Source Code
Clone the main flight controller software and install its base system dependencies.

```bash
mkdir ~/drone_project && cd ~/drone_project
git clone --recurse-submodules [https://github.com/Ardupilot/ardupilot.git](https://github.com/Ardupilot/ardupilot.git)
cd ardupilot
Tools/environment_install/install-prereqs-ubuntu.sh -y
```
```bash
sudo apt update
sudo apt install curl lsb-release gnupg
sudo curl [https://packages.osrfoundation.org/gazebo.gpg](https://packages.osrfoundation.org/gazebo.gpg) --output /usr/share/keyrings/pkgs-osrf-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/pkgs-osrf-archive-keyring.gpg] [http://packages.osrfoundation.org/gazebo/ubuntu-stable](http://packages.osrfoundation.org/gazebo/ubuntu-stable) $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/gazebo-stable.list > /dev/null
sudo apt update
sudo apt install gz-harmonic
```

```bash

# Install development dependencies
sudo apt install libgz-sim8-dev rapidjson-dev libopencv-dev libgstreamer1.0-dev libgstreamer-plugins-base1.0-dev gstreamer1.0-plugins-bad gstreamer1.0-libav gstreamer1.0-gl

```

```bash

# Clone and build the plugin
cd ~/drone_project
git clone [https://github.com/ArduPilot/ardupilot_gazebo](https://github.com/ArduPilot/ardupilot_gazebo)
cd ardupilot_gazebo
export GZ_VERSION=harmonic
mkdir build && cd build
cmake .. -DCMAKE_BUILD_TYPE=RelWithDebInfo
make -j4
```

```bash
nano ~/.bashrc
```


# ArduPilot SITL Path
```bash
export PATH=$PATH:$HOME/drone_project/ardupilot/Tools/autotest
```


# Gazebo Plugin & Models Paths
```bash
export GZ_SIM_SYSTEM_PLUGIN_PATH=$HOME/drone_project/ardupilot_gazebo/build:${GZ_SIM_SYSTEM_PLUGIN_PATH}
export GZ_SIM_RESOURCE_PATH=$HOME/drone_project/ardupilot_gazebo/models:$HOME/drone_project/ardupilot_gazebo/worlds:${GZ_SIM_RESOURCE_PATH}
```

# Global alias to activate the Python environment
```bash
alias flydrone='source ~/drone_project/drone_env/bin/activate'
```


```bash
source ~/.bashrc
```


```bash
flydrone
pip install empy==3.3.4 pexpect future MAVProxy pymavlink wxPython matplotlib opencv-python numpy
```

```bash
gz sim -v4 -r iris_runway.sdf
```

```bash
flydrone
cd ~/drone_project/ardupilot/ArduCopter/
sim_vehicle.py -v ArduCopter -f gazebo-iris --model JSON --map --console
```
