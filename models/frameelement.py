import numpy as np
import math

class FrameElement:
    def __init__(self, start, end, E, A, I):
        self.start = start
        self.end = end
        # Units are GPa for E, mm^2 for A, mm^4 for I
        self.E = E
        self.A = A
        self.I = I

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
        local_stiffness_matrix = np.array([[self.A, 0, 0, -self.A, 0, 0],
                                  [0, 12*self.I/(self.L)**2, 6*self.I/self.L, 0, -12*self.I/(self.L)**2, 6*self.I/self.L],
                                  [0, 6*self.I/self.L, 4*self.I, 0, -6*self.I/self.L, 2*self.I],
                                  [-self.A, 0, 0, self.A, 0, 0],
                                  [0, -12*self.I/(self.L)**2, -6*self.I/self.L, 0, 12*self.I/(self.L)**2, -6*self.I/self.L],
                                  [0, 6*self.I/self.L, 2*self.I, 0, -6*self.I/self.L, 4*self.I]])
        return local_stiffness_matrix
    
    def translation(self):
        translation_matrix = np.array([[np.cos(self.angle), np.sin(self.angle), 0, 0, 0, 0],
                              [-np.sin(self.angle), np.cos(self.angle), 0, 0, 0, 0],
                              [0, 0, 1, 0, 0, 0],
                              [0, 0, 0, np.cos(self.angle), np.sin(self.angle), 0],
                              [0, 0, 0, np.sin(self.angle), np.cos(self.angle), 0],
                              [0, 0, 0, 0, 0, 1]])
        return translation_matrix
    

