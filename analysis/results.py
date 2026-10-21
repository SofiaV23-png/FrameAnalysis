import numpy as np

class Results:
    def __init__(self, u: np.ndarray, R: np.ndarray, element_displacements: list, element_forces: list):
        self.u = u
        self.R = R
        self.element_displacements = element_displacements
        self.element_forces = element_forces