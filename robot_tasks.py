import numpy as np
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
            t = (elapsed - 3.0) / 3.0
            t_smooth = 3*t**2 - 2*t**3

            joint1 = 90 * t_smooth

            self.robot.set_position_sync([joint1, 0, 0, 0, 0])

        elif elapsed < 7.0:
            t = (elapsed - 6.0) / 1.0
            t_smooth = 3*t**2 - 2*t**3

            joint3 = -90 * t_smooth

            self.robot.set_position_sync([90, 0, joint3, 0, 0])

        elif elapsed < 15.0:
            t_wave = elapsed - 7.0

            T = 3.0
            w = 2 * np.pi / T

            joint2 = 45 * np.sin(w * t_wave) 
            joint1 = 10 * np.sin(w * t_wave + np.pi/2)
            joint3 = -90 + 15 * np.sin(w * t_wave + np.pi) 

            self.robot.set_position_sync([90 + joint1, joint2, joint3, 0, 0])

        elif elapsed < 17.0:
            t = (elapsed - 15.0) / 2.0
            t_smooth = 3*t**2 - 2*t**3

            joint1 = 90 * t_smooth
            joint3 = -90 * (1 - t_smooth)

            self.robot.set_position_sync([joint1, 0, joint3, 0, 0])

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
            t = (elapsed - 3.0) / 3.0
            t_smooth = 3*t**2 - 2*t**3

            joint3 = -30 * t_smooth

            self.robot.set_position_sync([0, 0, joint3, 0, 5])

        elif elapsed < 9.0:
            t = (elapsed - 6.0) / 3.0
            t_smooth = 3*t**2 - 2*t**3

            joint2 = 30 * t_smooth

            self.robot.set_position_sync([0, joint2, -30, 0, 5])

        elif elapsed < 11.0:
            self.robot.set_position_sync([0, 30, -30, 0, 0])

        elif elapsed < 14.0:
            t = (elapsed - 11.0) / 3.0 
            t_smooth = 3*t**2 - 2*t**3

            joint1 = 90 * t_smooth

            self.robot.set_position_sync([joint1, 0, 0, 0, 0])
        
        elif elapsed < 17.0:
            self.robot.set_position_sync([90, 0, 0, 0, 5])

        elif elapsed < 20.0:
            self.robot.go_home()
            
        else:
            self.start_time = None
            return True

        return False

        
