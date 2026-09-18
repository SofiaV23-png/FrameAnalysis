import numpy as np

class Processor:
    def __init__(self, frame, u):
        self.frame = frame
        self.u = u

    def calculate_element_displacement(self, element):
        dofs = element.map_dof()
        T = element.transformation()

        u_global = self.u[dofs]
        u_local = T @ u_global

        return u_local

    def calculate_element_loads(self, element):
        p_global = np.zeros((6, 1))

        for load in element.applied_point_loads:
            p_global += load.equivalent_nodal_load()

        T = element.transformation()
        p_local = T @ p_global

        return p_local

    def calculate_internal_forces(self, element):
         k_local = element.local_stiffness()

         u_local = self.calculate_element_displacement(element)
         p_local = self.calculate_element_loads(element)

         internal_forces = k_local @ u_local - p_local

         return internal_forces

    def calculate_all_internal_forces(self):
        all_element_internal_forces = {}
        
        for i, element in enumerate(self.frame.elements, start=1):
            element_internal_forces = self.calculate_internal_forces(element)
            all_element_internal_forces[i] = element_internal_forces

        return all_element_internal_forces