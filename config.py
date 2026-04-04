# 3 MX-106R
# 2 MX-64R
Kt_MX106R = 1.615 # Nm/A (at 12V)
Kt_MX64R = 1.463 # Nm/A (at 12V)
MOTOR_Kt = {1: Kt_MX106R, 2: Kt_MX106R, 3: Kt_MX106R, 4: Kt_MX64R, 5: Kt_MX64R}


from dynamixel_sdk import PortHandler, PacketHandler # Classes to open gate, set baudrate, packets, control many motors in one function
import numpy as np

# Functions
def degree_bit_convert(degree: float):
    degree = np.clip(degree, 0, 360)
    return int(degree * (4095 / 360))
def bit_degree_convert(bit: int):
    bit = np.clip(bit, 0, 4095)
    return round((bit * 360 / 4095), 2)

def torque_to_current(dxl_id, torque: float):
    current_amp = torque / MOTOR_Kt[dxl_id]
    return int(current_amp / 0.00336)
def current_to_torque(dxl_id, current: int):
    torque = current * 0.00336 * MOTOR_Kt[dxl_id]
    return torque

def deg2rad(deg):
    return deg * np.pi / 180

def rad2deg(rad):
    return rad * 180 / np.pi

def rpm_to_dxl(rpm: int):
    return int(rpm / 0.229)

def dxl_to_rpm(value):
    return (value * 0.229)

# Configuration
DEVICENAME = "/dev/ttyUSB0"
BAUDRATE = 1000000
PROTOCOL_VERSION = 2.0
portHandler = PortHandler(DEVICENAME)
packetHandler = PacketHandler(PROTOCOL_VERSION)

DXL_IDS = [1, 2, 3, 4, 5]

CONTROL_MODES = {0: "Current", 1: "Velocity", 3: "Position"}

home_position_list = [180, 180, 180, 180, 180]

TORQUE_ENABLE = 1
TORQUE_DISABLE= 0

# Adresses to control
# For motors
ADDR_TORQUE_ENABLE = 64 # To enable or disable torque
ADDR_OPERATING_MODE = 11   # To choose mode
ADDR_VELOCITY_LIMIT = 44 # To get and set velocity limit

# Position mode
ADDR_GOAL_POSITION = 116 # Tell the motor going to the desired position value
ADDR_PRESENT_POSITION = 132 # Address stores the current encoder reading
ADDR_PROFILE_VELOCITY = 112 # To set the velocity for the position mode

# Velocity mode
ADDR_PRESENT_VELOCITY = 128 # To read the current velocity
ADDR_GOAL_VELOCITY = 104 # To set the velocity

# Current mode
ADDR_GOAL_CURRENT = 102 # To set the current
ADDR_PRESENT_CURRENT = 126 # To get the current

