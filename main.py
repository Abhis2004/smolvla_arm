import sys
from coppeliasim_zmqremoteapi_client import RemoteAPIClient
from python_client.image_capture import VisionFeed
from python_client.keyboard_control import FrankaKeyboardController


def main():
    print("Connecting to CoppeliaSim...")
    client = RemoteAPIClient()
    sim = client.require('sim')
    print("Connected!!")

    sim.startSimulation()

    vision = VisionFeed(sim)
    keyboard = FrankaKeyboardController(sim)

    print("Controls:")
    print("Q/A W/S E/D R/F T/G Y/H U/J -> Move joints 1-7")
    print("O -> Open gripper")
    print("P -> Close gripper")
    print("ESC -> Quit")

    running = True
    while running:
        running = keyboard.handle()
        vision.update()

    vision.quit()
    sim.stopSimulation()
    sys.exit()


if __name__ == "__main__":
    main()