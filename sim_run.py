import mujoco
import mujoco.viewer
import time

from robot_tasks import RobotController 
from sim_interface import Mujoco_Motors  

model = mujoco.MjModel.from_xml_path("open_manipulator_x.xml")
data = mujoco.MjData(model)

sim_motors = Mujoco_Motors(model, data)
tasks = RobotController(sim_motors)
mission = "pick and place"

with mujoco.viewer.launch_passive(model, data) as viewer:
    while viewer.is_running():
        step_start = time.time()
        mujoco.mj_step(model, data)
        viewer.sync()
        
        if mission == "pick and place":
            tasks.pick_and_place(data.time)

        elif mission == "dance":
            tasks.dance(data.time)


        time_until_next_step = model.opt.timestep - (time.time() - step_start)

        if time_until_next_step > 0:
            time.sleep(time_until_next_step)