from dynamixel_sdk import GroupSyncWrite, COMM_SUCCESS # Classes to open gate, set baudrate, packets, control many motors in one function
from dynamixel_sdk import DXL_LOBYTE, DXL_HIBYTE, DXL_LOWORD, DXL_HIWORD
import numpy as np
from config import (portHandler,packetHandler,DXL_IDS,BAUDRATE,ADDR_GOAL_POSITION,ADDR_PROFILE_VELOCITY,ADDR_PRESENT_POSITION,ADDR_PRESENT_VELOCITY,ADDR_TORQUE_ENABLE,ADDR_OPERATING_MODE,TORQUE_ENABLE,TORQUE_DISABLE,CONTROL_MODES,ADDR_GOAL_VELOCITY,ADDR_GOAL_CURRENT, ADDR_PRESENT_CURRENT,ADDR_VELOCITY_LIMIT,MOTOR_Kt, home_position_list,
                    degree_bit_convert,bit_degree_convert,torque_to_current, current_to_torque, rpm_to_dxl, dxl_to_rpm)

class MX_Motors:
    def __init__(self):
        self.portHandler = portHandler
        self.packetHandler = packetHandler
        self.DXL_IDS = DXL_IDS
        self.home_position_list = home_position_list
        self.velocity_limits = {}

        try:
            if not self.portHandler.openPort():
                raise RuntimeError("Failed to open port")

            if not self.portHandler.setBaudRate(BAUDRATE):
                raise RuntimeError("Failed to set baudrate")

            print("Connected to Dynamixel!")

        except Exception as e:
            raise RuntimeError(f"Motor initialization failed: {e}")
        
        for dxl_id in self.DXL_IDS:
            limit, dxl_comm_result, dxl_error = self.packetHandler.read4ByteTxRx(self.portHandler,dxl_id,ADDR_VELOCITY_LIMIT)
            if dxl_comm_result != COMM_SUCCESS:
                raise RuntimeError(f"Failed to read velocity limit for ID {dxl_id}")
            self.velocity_limits[dxl_id] = limit    

        self.groupSyncWritePos = GroupSyncWrite(self.portHandler, self.packetHandler, ADDR_GOAL_POSITION, 4)

        self.groupSyncWriteProfileVel = GroupSyncWrite(self.portHandler,self.packetHandler,ADDR_PROFILE_VELOCITY,4)

        self.groupSyncWriteGoalVel = GroupSyncWrite(self.portHandler,self.packetHandler,ADDR_GOAL_VELOCITY,4)

        self.groupSyncWriteCurrent = GroupSyncWrite(self.portHandler,self.packetHandler,ADDR_GOAL_CURRENT,2)

    # MAIN CONTROL (ALL MOTORS - ALL MODES)

    def choose_mode(self, mode: int): # 0: current mode, 1: velocity mode, 3: position mode
        success = True
        if (mode not in CONTROL_MODES):
            raise ValueError("Invalid operating mode!")
        else:
            for dxl_id in self.DXL_IDS:
                self.packetHandler.write1ByteTxRx(self.portHandler, dxl_id, ADDR_TORQUE_ENABLE, TORQUE_DISABLE) # Disable torque

                dxl_comm_result, dxl_error = self.packetHandler.write1ByteTxRx(self.portHandler, dxl_id, ADDR_OPERATING_MODE, mode)
                
                if dxl_comm_result != COMM_SUCCESS:
                    print(f"Mode change failed for ID {dxl_id}")
                    success = False
                self.packetHandler.write1ByteTxRx(self.portHandler, dxl_id, ADDR_TORQUE_ENABLE, TORQUE_ENABLE) # Enable torque again

            if success:
                print(f"{CONTROL_MODES[mode]} mode selected.")
            else:
                print("Mode change completed with errors.")


    def enable_torque(self):
        for dxl_id in self.DXL_IDS:
            dxl_comm_result = self.packetHandler.write1ByteTxRx(self.portHandler, dxl_id, ADDR_TORQUE_ENABLE, TORQUE_ENABLE)
            if dxl_comm_result != COMM_SUCCESS:
                print(f"Communication failed for ID {dxl_id}")
        print("Torque enabled!")

    def disable_torque(self):
        for dxl_id in self.DXL_IDS:
            self.packetHandler.write1ByteTxRx(self.portHandler, dxl_id, ADDR_TORQUE_ENABLE, TORQUE_DISABLE)
        print("Torque disabled!")

    def close_port(self):
        self.portHandler.closePort()
        print("Port closed.")
    
    def get_velocity_limit(self, dxl_id: int):
        limit, dxl_comm_result, dxl_error = self.packetHandler.read4ByteTxRx(self.portHandler,dxl_id,ADDR_VELOCITY_LIMIT)

        if dxl_comm_result != 0:
            print(f"Communication failed for ID {dxl_id}")
        elif dxl_error != 0:
            print(f"Motor error for ID {dxl_id}: {dxl_error}")
        else:
            print(f"Velocity limit of motor {dxl_id}: {limit} ({dxl_to_rpm(limit):.2f} RPM)")
    
    def set_velocity_limit(self, dxl_id: int, limit_rpm: int):
        if dxl_id not in self.DXL_IDS:
            raise ValueError("Invalid motor ID")
        
        limit_dxl = rpm_to_dxl(limit_rpm)

        dxl_comm_result, dxl_error = self.packetHandler.write4ByteTxRx(self.portHandler,dxl_id,ADDR_VELOCITY_LIMIT,limit_dxl)

        if dxl_comm_result != COMM_SUCCESS:
            print(f"Communication failed for ID {dxl_id}")
        elif dxl_error != 0:
            print(f"Motor error for ID {dxl_id}: {dxl_error}")
        else:
            print(f"Velocity limit of motor {dxl_id} set to {limit_dxl}")
        
    # POSITION MODE
        # Control single motor
    def set_position_single(self, dxl_id: int, degree:float):
        if dxl_id not in self.DXL_IDS:
            raise ValueError("Invalid motor ID")
        
        goal_position = degree_bit_convert(degree)

        dxl_comm_result, dxl_error = self.packetHandler.write4ByteTxRx(self.portHandler, dxl_id, ADDR_GOAL_POSITION, goal_position)

        if dxl_comm_result != COMM_SUCCESS:
            print("Communication failed")
        elif dxl_error != 0:
            print(f"Motor error: {dxl_error}")
        else:
            print(f"Motor {dxl_id} moving to {degree} degrees.")

    def set_profile_velocity_single(self, dxl_id: int, velocity: int):
        if dxl_id not in self.DXL_IDS:
            raise ValueError("Invalid motor ID")
        


        dxl_comm_result, dxl_error = self.packetHandler.write4ByteTxRx(self.portHandler, dxl_id,ADDR_PROFILE_VELOCITY, velocity)

        if dxl_comm_result != COMM_SUCCESS:
            print(f"Communication failed for ID {dxl_id}")
        elif dxl_error != 0:
            print(f"Motor error for ID {dxl_id}: {dxl_error}")
        else:
            print(f"Motor {dxl_id} velocity set to {velocity}")

        # Control sync motors
    def set_profile_velocity_sync(self, velocity_list: list):

        if len(velocity_list) != len(self.DXL_IDS):
            raise ValueError("Velocity list length must match motor count!")

        for dxl_id, velocity in zip(self.DXL_IDS, velocity_list):
            limit = self.velocity_limits[dxl_id]
            if not (-limit <= velocity <= limit):
                raise ValueError(f"Velocity {velocity} exceeds limit {limit} for motor {dxl_id}")
        
            param_velocity = [DXL_LOBYTE(DXL_LOWORD(velocity)), DXL_HIBYTE(DXL_LOWORD(velocity)), DXL_LOBYTE(DXL_HIWORD(velocity)), DXL_HIBYTE(DXL_HIWORD(velocity))]

            self.groupSyncWriteProfileVel.addParam(dxl_id, param_velocity)

        dxl_comm_result = self.groupSyncWriteProfileVel.txPacket()

        if dxl_comm_result != COMM_SUCCESS:
            print("Velocity sync write failed")
        else:
            print("All motor velocities updated")

        self.groupSyncWriteProfileVel.clearParam()

    def read_all_positions(self):
        positions = []

        for dxl_id in self.DXL_IDS:
            position, dxl_comm_result, dxl_error = self.packetHandler.read4ByteTxRx(self.portHandler, dxl_id, ADDR_PRESENT_POSITION)

            if dxl_comm_result != COMM_SUCCESS:
                print(f"Communication failed for ID {dxl_id}")
                positions.append(None)
            elif dxl_error != 0:
                print(f"Motor error for ID {dxl_id}: {dxl_error}")
                positions.append(None)
            else:
                degree = bit_degree_convert(position)
                positions.append(degree)

        print(f"Motor positions: {positions}")
        
        return positions
    
    def set_position_sync(self, degree_list: list):
        if len(degree_list) != len(self.DXL_IDS):
            raise ValueError("Degree list length must match motor count!")
        
        for dxl_id, degree in zip(self.DXL_IDS, degree_list):

            goal_position = degree_bit_convert(degree)

            param_goal_position = [DXL_LOBYTE(DXL_LOWORD(goal_position)), DXL_HIBYTE(DXL_LOWORD(goal_position)), DXL_LOBYTE(DXL_HIWORD(goal_position)), DXL_HIBYTE(DXL_HIWORD(goal_position))]

            self.groupSyncWritePos.addParam(dxl_id, param_goal_position)

        dxl_comm_result = self.groupSyncWritePos.txPacket()

        if dxl_comm_result != COMM_SUCCESS:
            print("Sync write communication failed")
        else:
            print("All motors moving synchronously.")

        self.groupSyncWritePos.clearParam() 
    
    def update_home_position(self, home_position_list: list):
        if len(home_position_list) != len(self.DXL_IDS):
            raise ValueError("Degree list length must match motor count!")
        self.home_position_list = home_position_list
        return home_position_list
    
    def go_home(self):
        for dxl_id, degree in zip(self.DXL_IDS, self.home_position_list):

            goal_position = degree_bit_convert(degree)

            param_goal_position = [DXL_LOBYTE(DXL_LOWORD(goal_position)), DXL_HIBYTE(DXL_LOWORD(goal_position)), DXL_LOBYTE(DXL_HIWORD(goal_position)), DXL_HIBYTE(DXL_HIWORD(goal_position))]

            self.groupSyncWritePos.addParam(dxl_id, param_goal_position)

        dxl_comm_result = self.groupSyncWritePos.txPacket()

        if dxl_comm_result != COMM_SUCCESS:
            print("Sync write communication failed")
        else:
            print("Robot moved to home position.")

        self.groupSyncWritePos.clearParam()
    
    def read_all_velocities(self):
        velocities = []
        for dxl_id in self.DXL_IDS:

            velocity, dxl_comm_result, dxl_error = self.packetHandler.read4ByteTxRx(self.portHandler, dxl_id, ADDR_PRESENT_VELOCITY)

            if dxl_comm_result != COMM_SUCCESS:
                print(f"Communication failed for ID {dxl_id}")
                velocities.append(None)

            elif dxl_error != 0:
                print(f"Motor error for ID {dxl_id}: {dxl_error}")
                velocities.append(None)

            else:
                velocities.append(velocity)

        print("Motor velocities:", velocities)

        return velocities
    
    # VELOCITY MODE
    def set_vel_goal_single(self, dxl_id: int, velocity: int):
        if (dxl_id not in self.DXL_IDS):
            raise ValueError("Invalid motor ID!")
        
        limit = self.velocity_limits[dxl_id]

        if not (-limit <= velocity <= limit):
            raise ValueError(f"Velocity out of range for motor {dxl_id}. Limit: ±{limit}")
        
        dxl_comm_result, dxl_error = self.packetHandler.write4ByteTxRx(self.portHandler, dxl_id, ADDR_GOAL_VELOCITY, velocity)

        if dxl_comm_result != COMM_SUCCESS:
            print(f"Communication failed for ID {dxl_id}")
        elif dxl_error != 0:
            print(f"Motor error for ID {dxl_id}: {dxl_error}")
        else:
            print(f"Motor {dxl_id} velocity set to {velocity}")


    def set_velocity_sync(self, velocity_list: list):

        if len(velocity_list) != len(self.DXL_IDS):
            raise ValueError("Velocity list must match motor count")

        for dxl_id, velocity in zip(self.DXL_IDS, velocity_list):
            limit = self.velocity_limits[dxl_id]

            if not (-limit <= velocity <= limit):
                raise ValueError(f"Velocity {velocity} exceeds limit {limit} for motor {dxl_id}")
            
            param_velocity = [DXL_LOBYTE(DXL_LOWORD(velocity)),DXL_HIBYTE(DXL_LOWORD(velocity)),DXL_LOBYTE(DXL_HIWORD(velocity)),DXL_HIBYTE(DXL_HIWORD(velocity))]

            self.groupSyncWriteGoalVel.addParam(dxl_id, param_velocity)

        self.groupSyncWriteGoalVel.txPacket()
        self.groupSyncWriteGoalVel.clearParam()

        print("All motors velocity updated")

    def stop_all(self):
        velocity_list = [0] * len(self.DXL_IDS)

        self.set_velocity_sync(velocity_list)

        print("All motors stopped")
    
    # TORQUE MODE
    def set_torque_single(self, dxl_id: int, torque: float):
        
        if dxl_id not in self.DXL_IDS:
            raise ValueError("Invalid motor ID")
        else:
            current = torque_to_current(dxl_id, torque)

        if not (-1193 <= current <= 1193):
            raise ValueError("Current out of range")

        dxl_comm_result, dxl_error = self.packetHandler.write2ByteTxRx(self.portHandler,dxl_id,ADDR_GOAL_CURRENT,current)

        if dxl_comm_result != COMM_SUCCESS:
            print(f"Communication failed for ID {dxl_id}")
        elif dxl_error != 0:
            print(f"Motor error for ID {dxl_id}: {dxl_error}")
        else:
            print(f"Motor {dxl_id} current set to {current}")


    def set_torque_sync(self, torque_list: list):
        if (len(torque_list) != len(self.DXL_IDS)):
            raise ValueError("Torque list must match motor count!")

        for dxl_id, torque in zip(self.DXL_IDS, torque_list):
            current = torque_to_current(dxl_id, torque)
            if not (-1193 <= current <= 1193):
                raise ValueError(f"Torque is out of range {dxl_id}")
            
            param_current = [DXL_LOBYTE(current),DXL_HIBYTE(current)]

            self.groupSyncWriteCurrent.addParam(dxl_id, param_current)

        dxl_comm_result = self.groupSyncWriteCurrent.txPacket()

        if dxl_comm_result != COMM_SUCCESS:
            print("Current sync write failed")
        else:
            print("All motors torque updated")

        self.groupSyncWriteCurrent.clearParam()

    def read_all_(self):

        currents = []
        torques = []

        for dxl_id in self.DXL_IDS:

            current, dxl_comm_result, dxl_error = self.packetHandler.read2ByteTxRx(self.portHandler,dxl_id,ADDR_PRESENT_CURRENT)

            if dxl_comm_result != COMM_SUCCESS:
                print(f"Communication failed for ID {dxl_id}")
                currents.append(None)

            elif dxl_error != 0:
                print(f"Motor error for ID {dxl_id}: {dxl_error}")
                currents.append(None)

            else:
                currents.append(current)

        for dxl_id, current in zip(self.DXL_IDS, currents):
            torques.append(current_to_torque(dxl_id, current))

            print("Motor torques:", torques) # N.m

        return torques

    def read_velocity_limit(self, dxl_id: int):
        limit, dxl_comm_result, dxl_error = self.packetHandler.read4ByteTxRx(self.portHandler,dxl_id,44)

        if dxl_comm_result != 0:
            print(f"Communication failed for ID {dxl_id}")
        elif dxl_error != 0:
            print(f"Motor error for ID {dxl_id}: {dxl_error}")
        else:
            print(f"Velocity limit of motor {dxl_id}: {limit}")
        return limit
    













        
        

    
    

    
    

