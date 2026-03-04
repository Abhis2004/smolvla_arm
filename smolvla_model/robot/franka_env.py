from coppeliasim_zmqremoteapi_client import RemoteAPIClient
import torch

from perception.camera import SimCamera
from config import CAMERA_PATH


class FrankaEnv:

    def __init__(self):

        client = RemoteAPIClient()
        self.sim = client.require("sim")

        self.sim.startSimulation()

        self.camera = SimCamera(self.sim, CAMERA_PATH)

        franka = self.sim.getObject("/Franka")

        joints = self.sim.getObjectsInTree(
            franka,
            self.sim.sceneobject_joint
        )

        self.arm_joints = joints[:7]


    def get_observation(self):

        image = self.camera.get_image()

        joint_state = [
            self.sim.getJointPosition(j) for j in self.arm_joints
        ]

        image = torch.tensor(image).float() / 255.0
        image = image.permute(2,0,1).unsqueeze(0)

        state = torch.tensor(joint_state).float().unsqueeze(0)

        obs = {
            "observation.state": state,
            "observation.images.camera1": image,
            "task": ["pick up the red cube"],
            }

        return obs


    def step(self, action):

        from robot.actions import apply_joint_delta

        apply_joint_delta(self.sim, self.arm_joints, action)


    def close(self):

        self.sim.stopSimulation()