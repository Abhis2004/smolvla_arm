import numpy as np

class SimCamera:

    def __init__(self, sim, camera_path):

        self.sim = sim
        self.camera = sim.getObject(camera_path)

        raw, res = sim.getVisionSensorImg(self.camera)
        self.width, self.height = res


    def get_image(self):

        raw, _ = self.sim.getVisionSensorImg(self.camera)

        img = np.frombuffer(raw, dtype=np.uint8)
        img = img.reshape(self.height, self.width, 3)

        img = np.flip(img, axis=0).copy()

        return img