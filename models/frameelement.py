import numpy as np

class FrameElement:
    def __init__(self, start, end, E, A, I):
        self.start = start
        self.end = end
        # Units are GPa for E, mm^2 for A, mm^4 for I
        self.E = E
        self.A = A
        self.I = I

    def length(self):
        length = np.sqrt((self.start.x-self.end.x)**2 + (self.start.y-self.end.y)**2)
        return length
    