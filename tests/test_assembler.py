from models.frameelement import FrameElement
from models.node import Node
from models.frame import Frame
from models.loads import PointLoad
from analysis.assembler import Assembler
import numpy as np

def test_assemble_single_element():
    node_1 = Node(1, 1, 1)
    node_2 = Node(2, 0, 0)

    element = FrameElement(node_1, node_2, 1, 1, 1)
    frame = Frame([node_1, node_2], [element])
    assemble = Assembler(frame)

    expected = element.global_stiffness()

    K = assemble.assemble_stiffness()

    np.testing.assert_allclose(K, expected)

def test_assemble_stiffness_dimensions():
    node_1 = Node(1, 1, 1)
    node_2 = Node(2, 0, 0)

    element = FrameElement(node_1, node_2, 1, 1, 1)
    frame = Frame([node_1, node_2], [element])
    assemble = Assembler(frame)
    
    expected = (len(frame.nodes)*3, len(frame.nodes)*3)

    K = assemble.assemble_stiffness()

    assert K.shape == expected

def test_assemble_symmetry():
    node_1 = Node(1, 1, 1)
    node_2 = Node(2, 0, 0)

    element = FrameElement(node_1, node_2, 1, 1, 1)
    frame = Frame([node_1, node_2], [element])
    assemble = Assembler(frame)
    
    K = assemble.assemble_stiffness()

    np.testing.assert_allclose(K, K.T)

def test_assemble_disconnected_elements():
    node_1 = Node(1, 0, 0)
    node_2 = Node(2, 0, 1)
    node_3 = Node(3, 1, 1)
    node_4 = Node(4, 1, 0)

    element_1 = FrameElement(node_1, node_2, 1, 1, 1)
    element_2 = FrameElement(node_3, node_4, 1, 1, 1)

    frame = Frame(
        [node_1, node_2, node_3, node_4],
        [element_1, element_2])
    assemble = Assembler(frame)

    expected = np.zeros((12, 12))
    expected[0:6, 0:6] = element_1.global_stiffness()
    expected[6:12, 6:12] = element_2.global_stiffness()

    K = assemble.assemble_stiffness()

    np.testing.assert_allclose(K, expected)

    
def test_assemble_connected_elements():
    node_1 = Node(1, 0, 0)
    node_2 = Node(2, 0, 1)
    node_3 = Node(3, 1, 1)

    element_1 = FrameElement(node_1, node_2, 1, 1, 1)
    element_2 = FrameElement(node_2, node_3, 1, 1, 1)

    frame = Frame(
        [node_1, node_2, node_3], 
        [element_1, element_2])
    assemble = Assembler(frame)

    expected = np.zeros((9, 9))

    k_1 = element_1.global_stiffness()
    dof_1 = element_1.map_dof()
    expected[np.ix_(dof_1, dof_1)] += k_1

    k_2 = element_2.global_stiffness()
    dof_2 = element_2.map_dof()
    expected[np.ix_(dof_2, dof_2)] += k_2

    K = assemble.assemble_stiffness()

    np.testing.assert_allclose(K, expected)

def test_assemble_no_load():
    node_1 = Node(1, 0, 0)
    node_2 = Node(2, 2, 0)

    element = FrameElement(node_1, node_2, 1, 1, 1)
    frame = Frame([node_1, node_2], [element])
    assemble = Assembler(frame)

    expected = np.zeros((6, 1))

    np.testing.assert_allclose(assemble.assemble_loads(), expected)


def test_assemble_single_load():
    node_1 = Node(1, 0, 0)
    node_2 = Node(2, 2, 0)

    element = FrameElement(node_1, node_2, 1, 1, 1)
    load = PointLoad(10, 1, element)
    frame = Frame([node_1, node_2], [element], [load])
    assemble = Assembler(frame)

    expected = np.array([[0],
                         [-5],
                         [-5/2],
                         [0],
                         [-5],
                         [5/2]])

    np.testing.assert_allclose(assemble.assemble_loads(), expected, atol=1e-12)  

def test_assemble_multiple_loads():
    node_1 = Node(1, 0, 0)
    node_2 = Node(2, 10, 0)

    element = FrameElement(node_1, node_2, 1, 1, 1)
    load_1 = PointLoad(10, 5, element)
    load_2 = PointLoad(5, 2, element)
    frame = Frame([node_1, node_2], [element], [load_1, load_2])
    assemble = Assembler(frame)

    expected = load_1.equivalent_nodal_load() + load_2.equivalent_nodal_load()

    np.testing.assert_allclose(assemble.assemble_loads(), expected, atol=1e-12)

def test_assemble_loads_shared_node():
    node_1 = Node(1, 0, 0)
    node_2 = Node(2, 2, 0)
    node_3 = Node(3, 0, 2)

    element_1 = FrameElement(node_1, node_2, 1, 1, 1)
    load_1 = PointLoad(10, 1, element_1)

    element_2 = FrameElement(node_2, node_3, 1, 1, 1)
    load_2 = PointLoad(10, 1, element_2)

    frame = Frame([node_1, node_2, node_3], [element_1, element_2], [load_1, load_2])
    assemble = Assembler(frame)

    expected = np.zeros((9, 1))

    expected[element_1.map_dof()] += load_1.equivalent_nodal_load()
    expected[element_2.map_dof()] += load_2.equivalent_nodal_load()

    np.testing.assert_allclose(assemble.assemble_loads(), expected, atol=1e-12)