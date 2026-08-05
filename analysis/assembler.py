# obtain elemental stiffness matrix in global CSYS
# assemble global stiffness matrix
import numpy as np

class Assembler:
    def __init__(self, frame):
        self.frame = frame

    def assemble_stiffness(self):
        n_dof = len(self.frame.nodes) * 3
        K = np.zeros((n_dof, n_dof))

        for element in self.frame.elements:
            k = element.global_stiffness()
            dofs = element.map_dof()
            K[np.ix_(dofs, dofs)] += k

        return K

    def assemble_loads(self):
        pass
