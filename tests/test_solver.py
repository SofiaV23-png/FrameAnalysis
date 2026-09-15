import numpy as np
import pytest
from models.frame import Frame
from models.frameelement import FrameElement
from models.loads import PointLoad
from models.node import Node
from analysis.solver import Solver
from analysis.assembler import Assembler


def test_solver_frame():
    frame = Frame()
    solver = Solver(frame)

    assert solver.frame is frame

def test_sort_dofs():
    frame = Frame([Node(1, 0, 0),
                   Node(2, 1, 0, (True, False, False)),
                   Node(3, 0, 1, (False, False, True))])
    solver = Solver(frame)

    free_dofs, restrained_dofs = solver.sort_dofs()

    assert free_dofs == [2, 4, 5, 6, 7]
    assert restrained_dofs == [0, 1, 3, 8]

def test_sort_dofs_all_free():
    frame = Frame([Node(1, 0, 0, (False, False, False)),
                   Node(2, 1, 0, (False, False, False)),
                   Node(3, 0, 1, (False, False, False))])

    solver = Solver(frame)

    free_dofs, restrained_dofs = solver.sort_dofs()

    assert restrained_dofs == []

def test_sort_dofs_all_restrained():
    frame = Frame([Node(1, 0, 0, (True, True, True)),
                   Node(2, 1, 0, (True, True, True)),
                   Node(3, 0, 1, (True, True, True))])

    solver = Solver(frame)

    free_dofs, restrained_dofs = solver.sort_dofs()

    assert free_dofs == []

def test_reduce_system():
    frame = Frame([Node(1, 0, 0, (False, True, False)),
                   Node(2, 1, 0, (False, False, True))])

    solver = Solver(frame)

    K = np.array([[0, 1, 2, 3, 4, 5],
                  [6, 7, 8, 9, 10, 11],
                  [12, 13, 14, 15, 16, 17],
                  [18, 19, 20, 21, 22, 23],
                  [24, 25, 26, 27, 28, 29],
                  [30, 31, 32, 33, 34, 35]])

    F = np.array([0, 1, 2, 3, 4, 5])

    K_reduced, F_reduced, free_dofs, restrained_dofs = solver.reduce_system(K, F)

    K_expected = np.array([[0, 2, 3, 4],
                  [12, 14, 15, 16],
                  [18, 20, 21, 22],
                  [24, 26, 27, 28]])

    F_expected = np.array([0, 2, 3, 4])

    np.testing.assert_array_equal(K_reduced, K_expected)
    np.testing.assert_array_equal(F_reduced, F_expected)


def test_solve_cantilever_bending():
    node_1 = Node(1, 0, 0, (True, True, True))
    node_2 = Node(2, 1, 0, (False, False, False))
    element = FrameElement(node_1, node_2, 1, 1, 1)

    frame = Frame(nodes=[node_1, node_2],
                   elements=[element],
                   point_loads=[PointLoad(10, 1, element)])

    assembler = Assembler(frame)
    K = assembler.assemble_stiffness()
    F = assembler.assemble_loads()

    solver = Solver(frame)
    u = solver.solve(K, F)

    u_expected = np.array([[0],
                           [0],
                           [0],
                           [0], 
                           [-10/3], 
                           [-5]])

    np.testing.assert_allclose(u, u_expected, atol=1e-12)

def test_solve_cantilever_axial():
    node_1 = Node(1, 0, 0, (True, True, True))
    node_2 = Node(2, 1, 0, (False, False, False))
    element = FrameElement(node_1, node_2, 1, 1, 1)

    frame = Frame(nodes=[node_1, node_2],
                   elements=[element],
                   point_loads=[PointLoad(10, 1, element, angle=np.pi)])

    assembler = Assembler(frame)
    K = assembler.assemble_stiffness()
    F = assembler.assemble_loads()

    solver = Solver(frame)
    u = solver.solve(K, F)

    u_expected = np.array([[0],
                           [0],
                           [0],
                           [-10], 
                           [0], 
                           [0]])

    np.testing.assert_allclose(u, u_expected, atol=1e-12)

def test_solve_fundamental_equilibrium_condition():
    node_1 = Node(1, 0, 0, (True, False, False))
    node_2 = Node(2, 0, 1, (True, True, True))
    node_3 = Node(3, 1, 0, (True, True, False))

    element_1 = FrameElement(node_1, node_2, 1, 1, 1)
    element_2 = FrameElement(node_2, node_3, 1, 1, 1)

    frame = Frame(nodes=[node_1, node_2, node_3],
                   elements=[element_1, element_2],
                   point_loads=[PointLoad(10, 1, element_1, angle=np.pi)])

    assembler = Assembler(frame)
    K = assembler.assemble_stiffness()
    F = assembler.assemble_loads()

    solver = Solver(frame)
    u = solver.solve(K, F)

    internal_force = K @ u
    free_dofs, restrained_dofs = solver.sort_dofs()

    np.testing.assert_allclose(internal_force[free_dofs], F[free_dofs])

def test_unstable_structure_error():
    node_1 = Node(1, 0, 0, (False, False, False))
    node_2 = Node(2, 1, 0, (False, False, False))

    element = FrameElement(node_1, node_2, 1, 1, 1)

    frame = Frame(nodes=[node_1, node_2],
                   elements=[element],
                   point_loads=[PointLoad(10, 1, element, angle=np.pi)])

    assembler = Assembler(frame)
    K = assembler.assemble_stiffness()
    F = assembler.assemble_loads()

    solver = Solver(frame)

    with pytest.raises(ValueError, match="unstable"):
                       solver.solve(K, F)