class Node:
    def __init__(
            self, 
            id: int, 
            x: float, 
            y: float, 
            restraints: tuple[bool, bool, bool] = (True, True, False)
            ):
        self.id = id
        # units for x and y are mm
        self.x = x
        self.y = y
        # restraint corresponds to [ux, uy, rz] where a fixed node is [True, True, True]
        self.restraints = restraints

    def nodal_dof(self):
        dof = [
            self.id * 3 - 3,
            self.id * 3 - 2,
            self.id * 3 - 1
        ]
        return dof
