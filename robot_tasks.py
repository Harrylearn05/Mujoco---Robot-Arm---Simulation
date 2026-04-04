import numpy as np
from interpolator import Interpolator

class RobotController:
    def __init__(self, type_interface):
        self.robot = type_interface
        self.start_time = None

    def reset_timer(self, current_sim_time):
        self.start_time = current_sim_time

    def dance(self, sim_time):
        if self.start_time is None: 
            self.reset_timer(sim_time)
            
        elapsed = sim_time - self.start_time

        if elapsed < 3.0:
            self.robot.go_home()

        elif elapsed < 6.0:
            START_ANGLE = 0
            TARGET_ANGLE = 90
            DURATION = 3.0
            START_TIME = 3.0
            
            t = Interpolator.get_t(elapsed, DURATION, START_TIME)
            joint_val_smooth = Interpolator.smoothstep(START_ANGLE, TARGET_ANGLE, t)
            
            self.robot.set_position_sync([joint_val_smooth, 0, 0, 0, 0])

        elif elapsed < 7.0:
            START_ANGLE = 0
            TARGET_ANGLE = -90
            DURATION = 1.0
            START_TIME = 6.0
            
            t = Interpolator.get_t(elapsed, DURATION, START_TIME)
            joint_val_smooth = Interpolator.smoothstep(START_ANGLE, TARGET_ANGLE, t)
            
            self.robot.set_position_sync([90, 0, joint_val_smooth, 0, 0])

        elif elapsed < 15.0:
            t_wave = elapsed - 7.0

            T = 3.0
            w = 2 * np.pi / T

            joint2 = 45 * np.sin(w * t_wave) 
            joint1 = 10 * np.sin(w * t_wave + np.pi/2)
            joint3 = -90 + 15 * np.sin(w * t_wave + np.pi) 

            self.robot.set_position_sync([90 + joint1, joint2, joint3, 0, 0])

        elif elapsed < 17.0:
            START_ANGLE = -90
            TARGET_ANGLE = 0
            DURATION = 2.0
            START_TIME = 15.0
            
            t = Interpolator.get_t(elapsed, DURATION, START_TIME)
            joint_val_smooth = Interpolator.smoothstep(START_ANGLE, TARGET_ANGLE, t)
            
            self.robot.set_position_sync([90, 0, joint_val_smooth, 0, 0])

        else:
            self.start_time = None
            return True

        return False

    def pick_and_place(self, sim_time):
        if self.start_time is None: 
            self.reset_timer(sim_time)

        elapsed = sim_time - self.start_time

        if elapsed < 3.0:
            self.robot.go_home()

        elif elapsed < 6.0:
            START_ANGLE = 0
            TARGET_ANGLE = -30
            DURATION = 3.0
            START_TIME = 3.0
            
            t = Interpolator.get_t(elapsed, DURATION, START_TIME)
            joint_val_smooth = Interpolator.smoothstep(START_ANGLE, TARGET_ANGLE, t)
            
            self.robot.set_position_sync([0, 0, joint_val_smooth, 0, 5])

        elif elapsed < 9.0:
            START_ANGLE = 0
            TARGET_ANGLE = 30
            DURATION = 3.0
            START_TIME = 6.0
            
            t = Interpolator.get_t(elapsed, DURATION, START_TIME)
            joint_val_smooth = Interpolator.smoothstep(START_ANGLE, TARGET_ANGLE, t)
            
            self.robot.set_position_sync([0, joint_val_smooth, -30, 0, 5])

        elif elapsed < 11.0:
            self.robot.set_position_sync([0, 30, -30, 0, 0])

        elif elapsed < 14.0:
            START_ANGLE = 0
            TARGET_ANGLE = 90
            DURATION = 3.0
            START_TIME = 11.0
            
            t = Interpolator.get_t(elapsed, DURATION, START_TIME)
            joint_val_smooth = Interpolator.smoothstep(START_ANGLE, TARGET_ANGLE, t)
            
            self.robot.set_position_sync([joint_val_smooth, 0, 0, 0, 0])
        
        elif elapsed < 17.0:
            self.robot.set_position_sync([90, 0, 0, 0, 5])

        elif elapsed < 20.0:
            self.robot.go_home()
            
        else:
            self.start_time = None
            return True

        return False

        
