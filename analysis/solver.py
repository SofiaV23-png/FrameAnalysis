# Solve F = KU and return U
import numpy as np

class Solver:
    def __init__(self, frame):
        self.frame = frame

    def sort_dofs(self):
        free_dofs = []
        restrained_dofs = []

        for node in self.frame.nodes:
            dofs = node.nodal_dof()

            for dof, restraint in zip(dofs, node.restraints):
                if restraint:
                    restrained_dofs.append(dof)
                else:
                    free_dofs.append(dof)

        return free_dofs, restrained_dofs

    def reduce_system(self, K, F):
        free_dofs, restrained_dofs = self.sort_dofs()

        K_reduced = K[np.ix_(free_dofs, free_dofs)]
        F_reduced = F[free_dofs]

        return K_reduced, F_reduced, free_dofs, restrained_dofs

    def solve(self, K, F):
        K_reduced, F_reduced, free_dofs, restrained_dofs = self.reduce_system(K, F)

        try:
            u_free = np.linalg.solve(K_reduced, F_reduced)
        except np.linalg.LinAlgError:
            raise ValueError("Structure is unstable: stiffness matrix is singular.")

        u = np.zeros((len(self.frame.nodes)*3, 1))
        u[free_dofs, :] = u_free

        return u