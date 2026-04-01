import numpy as np
from config import (deg2rad, rad2deg)


class Mujoco_Motors:
    def __init__(self, model, data):
        self.model = model
        self.data = data
        self.n_actuators = model.nu

        print("MuJoCo interface ready!")
        print(f"Number of actuators: {self.n_actuators}")

    # =========================
    # POSITION MODE (MAIN)
    # =========================
    def set_position_single(self, dxl_id: int, degree: float):
        self.data.ctrl[dxl_id-1] = deg2rad(degree)

    def set_position_sync(self, degree_list: list):
        if len(degree_list) != self.n_actuators:
            raise ValueError("Input size mismatch with actuators")

        for i, deg in enumerate(degree_list):
            self.data.ctrl[i] = deg2rad(deg)

    # =========================
    # GO HOME
    # =========================
    def go_home(self):
        for i in range(self.n_actuators):
            self.data.ctrl[i] = 0


    
    
    

 


