import numpy as np

class RobotController:
    def __init__(self, type_interface):
        self.robot = type_interface
        self.start_time = None
        self.phase = 0
        self.phase_initialized = False

    def reset_timer(self, current_sim_time):
        self.start_time = current_sim_time
        self.phase = 0
        self.phase_initialized = False

    def dance(self, sim_time):
        if self.start_time is None:
            self.reset_timer(sim_time)

        elapsed = sim_time - self.start_time

        # ================= PHASE 0 =================
        if self.phase == 0:
            self.robot.go_home()

            if elapsed >= 3.0:
                self.phase = 1
                self.phase_initialized = False

        # ================= PHASE 1 =================
        elif self.phase == 1:
            duration = 3.0

            if not self.phase_initialized:
                self.start = np.array([0, 0, 0, 0, 0])
                self.target = np.array([90, 0, 0, 0, 0])
                self.phase_start_time = elapsed
                self.phase_initialized = True

            t = (elapsed - self.phase_start_time) / duration
            t = np.clip(t, 0, 1)
            t_smooth = 3*t**2 - 2*t**3

            pos = self.start + (self.target - self.start) * t_smooth
            self.robot.set_position_sync(pos)

            if t >= 1:
                self.phase = 2
                self.phase_initialized = False

        # ================= PHASE 2 =================
        elif self.phase == 2:
            duration = 1.0

            if not self.phase_initialized:
                self.start = np.array([90, 0, 0, 0, 0])
                self.target = np.array([90, 0, -90, 0, 0])
                self.phase_start_time = elapsed
                self.phase_initialized = True

            t = (elapsed - self.phase_start_time) / duration
            t = np.clip(t, 0, 1)
            t_smooth = 3*t**2 - 2*t**3

            pos = self.start + (self.target - self.start) * t_smooth
            self.robot.set_position_sync(pos)

            if t >= 1:
                self.phase = 3
                self.phase_initialized = False

        # ================= PHASE 3 =================
        elif self.phase == 3:
            if not self.phase_initialized:
                self.phase_start_time = elapsed
                self.phase_initialized = True

            t_wave = elapsed - self.phase_start_time

            T = 3.0
            w = 2 * np.pi / T

            joint2 = 45 * np.sin(w * t_wave)
            joint1 = 10 * np.sin(w * t_wave + np.pi/2)
            joint3 = -90 + 15 * np.sin(w * t_wave + np.pi)

            pos = np.array([90 + joint1, joint2, joint3, 0, 0])
            self.robot.set_position_sync(pos)

            if t_wave >= 10.0:
                self.phase = 4
                self.phase_initialized = False

        # ================= PHASE 4 =================
        elif self.phase == 4:
            duration = 2.0

            if not self.phase_initialized:
                self.start = np.array([90, 0, -90, 0, 0])
                self.target = np.array([90, 0, 0, 0, 0])
                self.phase_start_time = elapsed
                self.phase_initialized = True

            t = (elapsed - self.phase_start_time) / duration
            t = np.clip(t, 0, 1)
            t_smooth = 3*t**2 - 2*t**3

            pos = pos = self.start + (self.target - self.start) * t_smooth
            self.robot.set_position_sync(pos)

            if t >= 1:
                self.phase = 4
                self.phase_initialized = False

                self.start_time = None
                return True

            return False
        
        # ================= PHASE 5 =================
        elif self.phase == 5:
            self.robot.go_home()
            self.start_time = None


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

            self.robot.set_position_sync([joint1, 30, 0, 0, 0])
        
        elif elapsed < 17.0:
            self.robot.set_position_sync([90, 0, 0, 0, 5])

        elif elapsed < 20.0:
            self.robot.go_home()
            
        else:
            self.start_time = None
            return True

        return False

        
