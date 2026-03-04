import time

from robot.franka_env import FrankaEnv
from policy.smolvla_policy import Policy
from config import INSTRUCTION, CONTROL_DT


def main():

    env = FrankaEnv()

    policy = Policy()

    try:

        while True:

            obs = env.get_observation()

            action = policy.act(obs, INSTRUCTION)

            env.step(action)

            time.sleep(CONTROL_DT)

    except KeyboardInterrupt:

        env.close()


if __name__ == "__main__":
    main()