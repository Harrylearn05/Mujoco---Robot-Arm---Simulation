class DigitalTwinBridge:
    def __init__(self, mujoco_interface, hardware_interface):
        self.sim = mujoco_interface
        self.hw = hardware_interface

    def set_position_single(self, dxl_id: int, degree:float):
        self.sim.set_position_single(dxl_id, degree)
        
        self.hw.set_position_single(dxl_id, degree + 180)

    def set_position_sync(self, degree_list):
        self.sim.set_position_sync(degree_list)
        
        self.hw.set_position_sync([d + 180 for d in degree_list])

    def go_home(self):
        self.sim.go_home()
        self.hw.go_home()