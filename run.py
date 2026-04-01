import mujoco
import mujoco.viewer
import time


from sim_interface import Mujoco_Motors  
from robot_tasks import RobotController      

model = mujoco.MjModel.from_xml_path("open_manipulator_x.xml")
data = mujoco.MjData(model)

motors = Mujoco_Motors(model, data) 
tasks = RobotController(motors) 

mission = "pick and place"

with mujoco.viewer.launch_passive(model, data) as viewer:
    while viewer.is_running():
        step_start = time.time()

        if mission == "pick and place":
            tasks.pick_and_place(data.time)

        elif mission == "dance":
            tasks.dance(data.time)

        mujoco.mj_step(model, data)
        viewer.sync()
        


        time_until_next_step = model.opt.timestep - (time.time() - step_start)

        if time_until_next_step > 0:
            time.sleep(time_until_next_step)