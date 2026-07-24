import numpy as np
from models.frameelement import FrameElement
from models.node import Node

def test_length():
    node1 = Node(1, 0, 0)
    node2 = Node(2, 3000, 4000)

    f_element = FrameElement(node1, node2, 1, 1, 1)

    assert np.isclose(f_element.length(), 5000)

def test_angle_135():
    node1 = Node(1, 0, 0)
    node2 = Node(2, -3000, 3000)

    f_element = FrameElement(node1, node2, 1, 1, 1)

    assert np.isclose(f_element.angle(), 3*np.pi/4)

def test_angle_vertical():
    node1 = Node(1, 0, 0)
    node2 = Node(2, 0, 1000)

    f_element1 = FrameElement(node1, node2, 1, 1, 1)
    f_element2 = FrameElement(node2, node1, 1, 1, 1)

    assert np.isclose(f_element1.angle(), np.pi/2)
    assert np.isclose(f_element2.angle(), -np.pi/2)

def test_angle_horizontal():
    node1 = Node(1, 0, 0)
    node2 = Node(2, 1000, 0)

    f_element1 = FrameElement(node1, node2, 1, 1, 1)
    f_element2 = FrameElement(node2, node1, 1, 1, 1)

    assert np.isclose(f_element1.angle(), 0)
    assert np.isclose(f_element2.angle(), np.pi)

def test_local_stiffness():
    node1 = Node(1, 0, 0)
    node2 = Node(2, 3000, 0)

    f_element = FrameElement(
        node1,
        node2,
        E=200000,
        A=2000,
        I=1e6
    )

    expected = np.array([
        [1.333333e5, 0, 0, -1.333333e5, 0, 0],
        [0, 88.8889, 133333.333, 0, -88.8889, 133333.333],
        [0, 133333.333, 2.666667e8, 0, -133333.333, 1.333333e8],
        [-1.333333e5, 0, 0, 1.333333e5, 0, 0],
        [0, -88.8889, -133333.333, 0, 88.8889, -133333.333],
        [0, 133333.333, 1.333333e8, 0, -133333.333, 2.666667e8]
    ])

    np.testing.assert_allclose(
        f_element.local_stiffness(),
        expected,
        rtol=1e-5,
        atol=1e-5
    )

def test_stiffness_symmetry():
    node1 = Node(1, 0, 0)
    node2 = Node(2, 1000, 0)

    f_element = FrameElement(
        node1,
        node2,
        E=200000,
        A=2000,
        I=1e6
    )
    k = f_element.local_stiffness()

    np.testing.assert_allclose(k, k.T)

def test_stiffness_rigid_body_modes():
    node1 = Node(1, 0, 0)
    node2 = Node(2, 1000, 0)

    f_element = FrameElement(
        node1,
        node2,
        E=200000,
        A=2000,
        I=1e6
    )
    k = f_element.local_stiffness()
    eig = np.linalg.eigvals(k)
    
    assert np.all(eig > -1e-8)

# def test_transformation_matrix() against known result

def test_transformation_orthogonality():
    node1 = Node(1, 0, 0)
    node2 = Node(2, 1000, 0)

    f_element = FrameElement(
        node1,
        node2,
        E=200000,
        A=2000,
        I=1e6
    )

    T = f_element.transformation()
    np.testing.assert_allclose(T @ T.T, np.eye(6))

def test_global_stiffness_horizontal():
    node1 = Node(1, 0, 0)
    node2 = Node(2, 1000, 0)

    f_element = FrameElement(
        node1,
        node2,
        E=200000,
        A=2000,
        I=1e6
    )
    k = f_element.local_stiffness()
    k_global = f_element.global_stiffness()

    np.testing.assert_allclose(k_global, k)

# def test_global_stiffness_vertical() against known result
