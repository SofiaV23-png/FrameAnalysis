class Beam:
    def __init__(self, length, E, I):
        # Length in m
        self.length = length
        # E units are GPa
        self.E = E
        # I units are mm^4
        self.I = I

        self.point_loads = []
        self.uniform_loads = []
        self.supports = []

    def add_point_load(self, P, x):
        # P in kN and x in m
        self.point_loads.append(
            (P, x)
        )
    
    def add_uniform_load(self, w, start, end):
        # w in kN/m and a and b in m
        self.uniform_loads.append(
            (w, start, end)
        )

    def add_support(self, type, x):
        # types are "roller", "pinned", "fixed" and x in m
        self.supports.append(
            (type, x)
        )
