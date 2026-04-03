# ==============================================================================
# ARDUPILOT & GAZEBO SITL AUTOMATED SETUP SCRIPT (UBUNTU 24.04)
# ==============================================================================

# 1. Create workspace and clone the core ArduPilot repository
mkdir -p ~/drone_project
cd ~/drone_project
git clone --recurse-submodules https://github.com/Ardupilot/ardupilot.git

# 2. Install base ArduPilot system prerequisites
cd ardupilot
Tools/environment_install/install-prereqs-ubuntu.sh -y

# 3. Add modern OSRF keys and install Gazebo Harmonic
sudo apt update
sudo apt install -y curl lsb-release gnupg
sudo curl https://packages.osrfoundation.org/gazebo.gpg --output /usr/share/keyrings/pkgs-osrf-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/pkgs-osrf-archive-keyring.gpg] http://packages.osrfoundation.org/gazebo/ubuntu-stable $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/gazebo-stable.list > /dev/null
sudo apt update
sudo apt install -y gz-harmonic

# 4. Install C++ development dependencies for the Gazebo plugin
sudo apt install -y libgz-sim8-dev rapidjson-dev libopencv-dev libgstreamer1.0-dev libgstreamer-plugins-base1.0-dev gstreamer1.0-plugins-bad gstreamer1.0-libav gstreamer1.0-gl

# 5. Clone and compile the official ArduPilot-Gazebo communications bridge
cd ~/drone_project
git clone https://github.com/ArduPilot/ardupilot_gazebo
cd ardupilot_gazebo
export GZ_VERSION=harmonic
mkdir -p build && cd build
cmake .. -DCMAKE_BUILD_TYPE=RelWithDebInfo
make -j4

# 6. Inject environment variables and global aliases into .bashrc
echo '' >> ~/.bashrc
echo '# ArduPilot SITL & Gazebo Configuration' >> ~/.bashrc
echo 'export PATH=$PATH:$HOME/drone_project/ardupilot/Tools/autotest' >> ~/.bashrc
echo 'export GZ_SIM_SYSTEM_PLUGIN_PATH=$HOME/drone_project/ardupilot_gazebo/build:${GZ_SIM_SYSTEM_PLUGIN_PATH}' >> ~/.bashrc
echo 'export GZ_SIM_RESOURCE_PATH=$HOME/drone_project/ardupilot_gazebo/models:$HOME/drone_project/ardupilot_gazebo/worlds:${GZ_SIM_RESOURCE_PATH}' >> ~/.bashrc
echo "alias flydrone='source ~/drone_project/drone_env/bin/activate'" >> ~/.bashrc

# 7. Activate virtual environment and install simulation Python packages
# Note: We use the absolute path here because the 'flydrone' alias requires a terminal restart to take effect
source ~/drone_project/drone_env/bin/activate
pip install empy==3.3.4 pexpect future MAVProxy pymavlink wxPython matplotlib opencv-python numpy

# 8. Completion Message
echo "=============================================================================="
echo "INSTALLATION COMPLETE!"
echo "Please completely close this terminal window and open a new one to apply changes."
echo "=============================================================================="
