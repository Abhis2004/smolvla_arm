import pygame


class FrankaKeyboardController:
    def __init__(self, sim):
        self.sim = sim
        pygame.init()

        # Get Franka base
        franka_base = self.sim.getObject('/Franka')

        # Get all joints under Franka
        all_joints = self.sim.getObjectsInTree(
            franka_base,
            self.sim.sceneobject_joint
        )

        # First 7 joints = arm
        self.arm_joints = all_joints[:7]

        # Gripper control
        self.gripper_velocity = 0.04

        self.arm_step = 0.05

    def handle(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False

        keys = pygame.key.get_pressed()

        # ---- ARM CONTROL ----
        keymap = [
            (pygame.K_q, pygame.K_a),
            (pygame.K_w, pygame.K_s),
            (pygame.K_e, pygame.K_d),
            (pygame.K_r, pygame.K_f),
            (pygame.K_t, pygame.K_g),
            (pygame.K_y, pygame.K_h),
            (pygame.K_u, pygame.K_j),
        ]

        for i, (pos_key, neg_key) in enumerate(keymap):
            if keys[pos_key]:
                self.move_arm_joint(i, self.arm_step)
            if keys[neg_key]:
                self.move_arm_joint(i, -self.arm_step)

        # ---- GRIPPER CONTROL (Velocity via signal) ----
        if keys[pygame.K_o]:
            self.sim.setFloatSignal('gripperVel', -self.gripper_velocity)

        elif keys[pygame.K_p]:
            self.sim.setFloatSignal('gripperVel', self.gripper_velocity)

        else:
            self.sim.setFloatSignal('gripperVel', 0)

        return True

    def move_arm_joint(self, joint_idx, delta):
        if joint_idx < len(self.arm_joints):
            joint = self.arm_joints[joint_idx]
            current = self.sim.getJointPosition(joint)
            self.sim.setJointTargetPosition(joint, current + delta)