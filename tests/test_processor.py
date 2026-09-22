import numpy as np
from models.frame import Frame
from models.frameelement import FrameElement
from models.loads import PointLoad
from models.node import Node
from analysis.solver import Solver
from analysis.assembler import Assembler
from analysis.processor import Processor
import pytest

def test_calculate_element_displacement():
    node_1 = Node(1, 0, 0)
    node_2 = Node(2, 1, 0)
    element = FrameElement(node_1, node_2, 1, 1, 1)
    frame = Frame(nodes=[node_1, node_2], elements=[element])

    u = np.array([[0.01],
                  [0.02],
                  [0.03],
                  [0.04],
                  [0.05],
                  [0.06]])

    processor = Processor(frame, u)

    u_result = processor.calculate_element_displacement(element)
    u_expected = element.transformation() @ u

    assert np.allclose(u_result, u_expected)

def test_calculate_element_multiple_loads():
    node_1 = Node(1, 0, 0)
    node_2 = Node(2, 1, 0)

    element = FrameElement(node_1, node_2, 1, 1, 1)

    load_1 = PointLoad(10, 1/3, element)
    load_2 = PointLoad(5, 2/3, element)

    frame = Frame(
        nodes=[node_1, node_2],
        elements=[element],
        point_loads=[load_1, load_2]
    )

    frame.connect_point_loads_to_elements()
    
    u = np.array([[0.01],
                  [0.02],
                  [0.03],
                  [0.04],
                  [0.05],
                  [0.06]])

    processor = Processor(frame, u)
    
    expected_global_loads = (
        load_1.equivalent_nodal_load()
        + load_2.equivalent_nodal_load()
        )

    local_loads_expected = element.transformation() @ expected_global_loads
    local_loads_result = processor.calculate_element_loads(element)

    np.testing.assert_allclose(local_loads_result, local_loads_expected)

def test_calculate_element_no_loads():
    node_1 = Node(1, 0, 0)
    node_2 = Node(2, 1, 0)

    element = FrameElement(node_1, node_2, 1, 1, 1)

    frame = Frame(
        nodes=[node_1, node_2],
        elements=[element]
    )

    frame.connect_point_loads_to_elements()

    u = np.array([[0.01],
                  [0.02],
                  [0.03],
                  [0.04],
                  [0.05],
                  [0.06]])

    processor = Processor(frame, u)

    local_loads_result = processor.calculate_element_loads(element)

    np.testing.assert_allclose(local_loads_result, np.zeros((6, 1)))

def test_calculate_internal_forces():
    node_1 = Node(1, 0, 0)
    node_2 = Node(2, 1, 0)

    element = FrameElement(node_1, node_2, 1, 1, 1)
    load = PointLoad(10, 1/3, element)

    frame = Frame(
        nodes=[node_1, node_2],
        elements=[element],
        point_loads=[load]
    )

    assembler = Assembler(frame)
    K = assembler.assemble_stiffness()
    F = assembler.assemble_loads()

    solver = Solver(frame)
    u = solver.solve(K, F)
    
    u_local = element.transformation() @ u
    p_global = load.equivalent_nodal_load()
    p_local = element.transformation() @ p_global

    forces_expected = (
        element.local_stiffness() @ u_local
        - p_local
    )

    frame.connect_point_loads_to_elements()
    processor = Processor(frame, u)
    forces_result = processor.calculate_internal_forces(element)

    np.testing.assert_allclose(forces_result, forces_expected)

@pytest.fixture
def frame_with_point_loads():
    node_1 = Node(1, 0, 0)
    node_2 = Node(2, 1, 0)
    node_3 = Node(3, 1, 1)

    element_1 = FrameElement(node_1, node_2, 1, 1, 1)
    element_2 = FrameElement(node_2, node_3, 1, 1, 1)

    load_1 = PointLoad(10, 1/3, element_1)
    load_2 = PointLoad(5, 2/3, element_1)

    frame = Frame(
        nodes=[node_1, node_2, node_3],
        elements=[element_1, element_2],
        point_loads=[load_1, load_2]
    )

    frame.connect_point_loads_to_elements()

    u = np.array([[0.01],
                  [0.02],
                  [0.03],
                  [0.04],
                  [0.05],
                  [0.06],
                  [0.07],
                  [0.08],
                  [0.09]])

    processor = Processor(frame, u)

    return element_1, element_2, processor

def test_calculate_all_internal_forces(frame_with_point_loads):
    element_1, element_2, processor = frame_with_point_loads

    all_forces_result = processor.calculate_all_internal_forces()

    assert set(all_forces_result.keys()) == {1, 2}

    assert np.allclose(
        all_forces_result[1],
        processor.calculate_internal_forces(element_1)
    )

    assert np.allclose(
        all_forces_result[2],
        processor.calculate_internal_forces(element_2)
    )

def test_calculate_all_element_displacements(frame_with_point_loads):
    element_1, element_2, processor = frame_with_point_loads

    all_displacements_result = processor.calculate_all_element_displacements()

    assert set(all_displacements_result.keys()) == {1, 2}

    assert np.allclose(
        all_displacements_result[1],
        processor.calculate_element_displacement(element_1)
    )

    assert np.allclose(
        all_displacements_result[2],
        processor.calculate_element_displacement(element_2)
    )

def test_internal_forces_cantilever():
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

    frame.connect_point_loads_to_elements()

    processor = Processor(frame, u)

    displacement_result = processor.calculate_element_displacement(element)
    forces_result = processor.calculate_internal_forces(element)

    forces_expected = np.array([[0],
                                [10],
                                [10],
                                [0],
                                [0],
                                [0]])

    displacement_expected = np.array([[0],
                                      [0],
                                      [0],
                                      [0],
                                      [-10/3],
                                      [-5]])

    np.testing.assert_allclose(forces_result, forces_expected, atol=1e-12)
    np.testing.assert_allclose(displacement_result, displacement_expected, atol=1e-12)