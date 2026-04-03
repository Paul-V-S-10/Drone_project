import collections
import collections.abc
# Fix for Python 3.10+ compatibility with DroneKit
collections.MutableMapping = collections.abc.MutableMapping

from dronekit import connect, VehicleMode, LocationGlobalRelative
import time
import argparse  
import numpy as np
import cv2

# --- CONFIGURATION ---
TARGET_ID = 2  # Changed from 53 to 2 based on your terminal output
TARGET_ALTITUDE = 5 

# 1. Initialize Camera
cap = cv2.VideoCapture(0)

# 2. Connection Setup
parser = argparse.ArgumentParser()
parser.add_argument('--connect', default='127.0.0.1:14550')
args = parser.parse_args()

print(f'Connecting to vehicle on: {args.connect}')
vehicle = connect(args.connect, baud=921600, wait_ready=True)

# 3. Takeoff Function
def arm_and_takeoff(aTargetAltitude):
    print("Basic pre-arm checks")
    while not vehicle.is_armable:
        print(" Waiting for vehicle to initialise...")
        time.sleep(1)
        
    print("Arming motors")
    vehicle.mode = VehicleMode("GUIDED")
    vehicle.armed = True

    while not vehicle.armed:
        print(" Waiting for arming...")
        time.sleep(1)

    print("Taking off!")
    vehicle.simple_takeoff(aTargetAltitude)

    while True:
        print(f" Altitude: {vehicle.location.global_relative_frame.alt:.2f}m") 
        if vehicle.location.global_relative_frame.alt >= aTargetAltitude * 0.95: 
            print("Reached target altitude")
            break
        time.sleep(1)

# --- START MISSION ---
arm_and_takeoff(TARGET_ALTITUDE)
print(f"Hovering at {TARGET_ALTITUDE}m. Searching for Marker ID: {TARGET_ID}")

# 4. Modern OpenCV ArUco Configuration
aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_100)
parameters = cv2.aruco.DetectorParameters()
detector = cv2.aruco.ArucoDetector(aruco_dict, parameters)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    corners, ids, rejected = detector.detectMarkers(gray)
    
    # Visual Feedback
    if ids is not None:
        cv2.aruco.drawDetectedMarkers(frame, corners, ids)
        detected_ids = ids.flatten()
        print(f"Detected IDs: {detected_ids}")

        # Check if our specific target ID is found
        if TARGET_ID in detected_ids:
            print(f"MATCH FOUND! Marker {TARGET_ID} detected. Landing...")
            vehicle.mode = VehicleMode("LAND")
            
            # Final visual confirmation on screen
            cv2.putText(frame, "MATCH FOUND: LANDING", (50, 50), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)
            cv2.imshow('Drone Vision Debug', frame)
            cv2.waitKey(2000) 
            break
    else:
        cv2.putText(frame, "Searching...", (50, 50), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    cv2.imshow('Drone Vision Debug', frame)

    # Emergency Manual Exit (Press 'q')
    if cv2.waitKey(1) & 0xFF == ord('q'):
        print("Manual exit by user.")
        break

# 5. Cleanup
print("Shutting down...")
cap.release()
cv2.destroyAllWindows()
vehicle.close()
