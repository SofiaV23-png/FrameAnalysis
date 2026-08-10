from .frameelement import FrameElement
import numpy as np

class PointLoad:
    def __init__(self, P: float, x: float, element: FrameElement, angle: float = np.pi/2):
        self.P = P
        self.a = x
        self.element = element
        # angle is from negative horizontal axis
        self.angle = angle

        if not 0 <= self.a <= element.length():
            raise ValueError("Point load position must lie within the element.")

    def equivalent_nodal_load(self):
        L = self.element.length()
        b = L - self.a
        T = self.element.transformation()

        local_load_vector = np.array([self.P * b / L * np.cos(self.angle), 
                                      -self.P * b**2 / L**3 * (3*self.a + b) * np.sin(self.angle),
                                      -self.P * self.a * b**2 / L**2 * np.sin(self.angle),
                                      self.P * self.a / L * np.cos(self.angle),
                                      -self.P * self.a**2 / L**3 * (self.a + 3*b) * np.sin(self.angle),
                                      self.P * self.a**2 * b / L**2 * np.sin(self.angle)])
        
        global_load_vector = T.T @ local_load_vector

        return global_load_vector

    