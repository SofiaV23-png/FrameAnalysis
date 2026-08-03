class Node:
    def __init__(self, id, x, y):
        self.id = id
        # units for x and y are mm
        self.x = x
        self.y = y

    def nodal_dof(self):
        dof = [
            self.id * 3 - 3,
            self.id * 3 - 2,
            self.id * 3 - 1
        ]
        return dof
