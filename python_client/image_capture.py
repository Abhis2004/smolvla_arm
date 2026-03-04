import pygame

class VisionFeed:
    def __init__(self, sim):
        self.sim = sim
        self.camera = sim.getObject('/Franka/FrankaGripper/visionSensor')
        raw, res = self.sim.getVisionSensorImg(self.camera)
        self.width, self.height = res

        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Arm camera feed")
        self.clock = pygame.time.Clock()

    # def update(self):
    #     # Clears the internal event queue to prevent OS freezing
    #     pygame.event.pump() 

    #     raw, _ = self.sim.getVisionSensorImg(self.camera)
    #     surface = pygame.image.frombuffer(raw, (self.width, self.height), "RGB")
    #     surface = pygame.transform.flip(surface, False, True)
    #     self.screen.blit(surface, (0, 0))
    #     pygame.display.update()
    #     self.clock.tick(30)
    
    # In python_client/image_capture.py
    def update(self):
        # NOTE: No pygame.event checks here anymore! The keyboard controller handles it.
        raw, _ = self.sim.getVisionSensorImg(self.camera)
        surface = pygame.image.frombuffer(raw, (self.width, self.height), "RGB")
        surface = pygame.transform.flip(surface, False, True)
        self.screen.blit(surface, (0, 0))
        pygame.display.update()
        self.clock.tick(30)

    def quit(self):
        pygame.quit()