# 1. System Preparation (Terminal Commands)
These commands were used to set up the Ubuntu environment and bypass modern Python restrictions.
## Update system package list
```
sudo apt-get update
```
## Install Python 3 development tools and virtual environment creator
```
sudo apt-get install python3-pip python3-dev python3-venv
```
## Create a new folder
```
mkdir ~/drone_project
```
## Navigate to project folder and create a virtual environment
```
cd ~/drone_project
python3 -m venv drone_env
```
## Activate the virtual environment (Must be done in every new terminal)
```
source drone_env/bin/activate
```
## Install DroneKit and required compatibility libraries
```
pip install dronekit dronekit-sitl future setuptools
```
# 2. The Complete Script: hello_drone.py
Create a file named hello_drone.py and paste the code below into it.
```
nano hello_drone.py
```
This script connects to the simulator and prints the drone's current health and status.
## If using a real drone, replace '127.0.0.1:14550' with your serial port (e.g., '/dev/ttyUSB0')
```
import collections
import collections.abc

# 1. Apply Compatibility Patch. Because DroneKit is a legacy library, the following lines must be # added to the top of every script to make it work with Python 3.10 and newer. It maps old library # locations to new ones.
collections.MutableMapping = collections.abc.MutableMapping
collections.Iterable = collections.abc.Iterable
collections.Mapping = collections.abc.Mapping

from dronekit import connect, VehicleMode
import time

# 2. Connection Logic
## 'tcp:127.0.0.1:5760' is the specific address provided by the SITL simulator
print("Connecting to vehicle...")
vehicle = connect('tcp:127.0.0.1:5760', wait_ready=True)

# 3. Reading Vehicle State
print("\n--- Vehicle Status ---")
print(f" GPS: {vehicle.gps_0}")
print(f" Battery: {vehicle.battery}")
print(f" Last Heartbeat: {vehicle.last_heartbeat}")
print(f" Is Armable?: {vehicle.is_armable}")
print(f" System status: {vehicle.system_status.state}")
print(f" Mode: {vehicle.mode.name}")

# 4. Clean Up
print("\nClosing vehicle object")
vehicle.close()
```

Press Ctrl+O, Enter, and Ctrl+X to save and exit

# 3. Execution Workflow (The Two-Terminal Method)
To run the project, two separate terminal processes must be active simultaneously:
## Terminal 1: The Simulator (SITL)
This acts as the virtual drone hardware.
```
source drone_env/bin/activate
dronekit-sitl copter
```
Status: Wait until you see Waiting for connection...
## Terminal 2: The Script (The Pilot)
This runs your logic and communicates with the simulator.
```
source drone_env/bin/activate
python3 hello_drone.py
```
