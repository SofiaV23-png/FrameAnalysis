import numpy as np
import math
from node import Node

class FrameElement:
    def __init__(self, start: Node, end: Node, E: float, A: float, I: float):
        self.start = start
        self.end = end
        # Units are MPa for E, mm^2 for A, mm^4 for I
        self.E = E
        self.A = A
        self.I = I

    def map_dof(self):
        dofs = self.start.nodal_dof() + self.end.nodal_dof()
        return dofs

    def length(self):
        length = np.sqrt((self.end.x-self.start.x)**2 + (self.end.y-self.start.y)**2)
        return length
    
    def angle(self):
        x_dif = self.end.x-self.start.x
        y_dif = self.end.y-self.start.y
        angle = math.atan2(y_dif, x_dif)
        return angle
    
    def local_stiffness(self):
        # in elemental coordinate system
        # stiffness matrix is in N/mm
        L = self.length()
        local_stiffness_matrix = (self.E / L) * np.array([[self.A, 0, 0, -self.A, 0, 0],
                                  [0, 12*self.I/(L)**2, 6*self.I/L, 0, -12*self.I/(L)**2, 6*self.I/L],
                                  [0, 6*self.I/L, 4*self.I, 0, -6*self.I/L, 2*self.I],
                                  [-self.A, 0, 0, self.A, 0, 0],
                                  [0, -12*self.I/(L)**2, -6*self.I/L, 0, 12*self.I/(L)**2, -6*self.I/L],
                                  [0, 6*self.I/L, 2*self.I, 0, -6*self.I/L, 4*self.I]])
        return local_stiffness_matrix
    
    def transformation(self):
        theta = self.angle()
        transformation_matrix = np.array([[np.cos(theta), np.sin(theta), 0, 0, 0, 0],
                              [-np.sin(theta), np.cos(theta), 0, 0, 0, 0],
                              [0, 0, 1, 0, 0, 0],
                              [0, 0, 0, np.cos(theta), np.sin(theta), 0],
                              [0, 0, 0, -np.sin(theta), np.cos(theta), 0],
                              [0, 0, 0, 0, 0, 1]])
        return transformation_matrix
    
    def global_stiffness(self):
        T = self.transformation()
        k_local = self.local_stiffness()
        global_stiffness_matrix = T.T @ k_local @ T
        return global_stiffness_matrix
    

