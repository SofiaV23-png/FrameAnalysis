from analysis.assembler import Assembler
from analysis.solver import Solver
from analysis.results import Results
from analysis.processor import Processor


class FrameAnalysis:
    def __init__(self, frame):
        self.frame = frame

    def run(self) -> Results:
        # Assemble global stiffness matrix and load vector
        assembler = Assembler(self.frame)

        K = assembler.assemble_stiffness()
        F = assembler.assemble_loads()

        # Solve for nodal displacements
        solver = Solver(self.frame)

        u = solver.solve(K, F)

        # Calculate reactions
        R = solver.return_reactions(K, F, u)

        # Calculate element displacements and internal forces
        processor = Processor(self.frame, u)

        element_forces = processor.calculate_all_internal_forces()
        element_displacements = processor.calculate_all_element_displacements()


        # Collect outputs
        return Results(u,
                       R,
                       element_displacements,
                       element_forces)
