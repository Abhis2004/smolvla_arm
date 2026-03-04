import numpy as np


def apply_joint_delta(sim, joints, action):

    action = action.squeeze()

    for i in range(min(len(joints), len(action))):

        joint = joints[i]

        current = sim.getJointPosition(joint)

        sim.setJointTargetPosition(joint, current + float(action[i]))