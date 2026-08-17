import numpy as np
import pytest

from models.frameelement import FrameElement
from models.node import Node
from models.loads import PointLoad

def test_point_load_properties():
    node1 = Node(1, 0, 0)
    node2 = Node(2, 2, 0)
    f_element = FrameElement(node1, node2, 1, 1, 1)

    load = PointLoad(10, 1, f_element)

    assert load.P == 10
    assert load.a == 1
    assert load.element == f_element
    assert load.angle == np.pi/2

def test_point_load_start():
    node1 = Node(1, 0, 0)
    node2 = Node(2, 10, 0)
    f_element = FrameElement(node1, node2, 1, 1, 1)

    load = PointLoad(10, 0, f_element)

    assert load.a == 0

def test_point_load_middle():
    node1 = Node(1, 0, 0)
    node2 = Node(2, 10, 0)
    f_element = FrameElement(node1, node2, 1, 1, 1)

    load = PointLoad(10, 5, f_element)

    assert load.a == 5

def test_point_load_end():
    node1 = Node(1, 0, 0)
    node2 = Node(2, 10, 0)
    f_element = FrameElement(node1, node2, 1, 1, 1)

    load = PointLoad(10, 10, f_element)

    assert load.a == 10

def test_point_load_outside():
    node1 = Node(1, 0, 0)
    node2 = Node(2, 10, 0)
    f_element = FrameElement(node1, node2, 1, 1, 1)

    with pytest.raises(
        ValueError,
        match="Point load position must lie within the element."
    ):
        PointLoad(10, 15, f_element)

def test_point_load_negative():
    node1 = Node(1, 10, 0)
    node2 = Node(2, 20, 0)
    f_element = FrameElement(node1, node2, 1, 1, 1)

    with pytest.raises(
        ValueError,
        match="Point load position must lie within the element."
    ):
        PointLoad(10, -5, f_element)

def test_vertical_point_load_midspan():
    node1 = Node(1, 0, 0)
    node2 = Node(2, 2, 0)
    f_element = FrameElement(node1, node2, 1, 1, 1)
    
    load = PointLoad(10, 1, f_element)

    expected = np.array([0,
                         -5,
                         -5/2,
                         0,
                         -5,
                         5/2])

    np.testing.assert_allclose(load.equivalent_nodal_load(), expected, atol=1e-12)

def test_vertical_point_load_start_node():
    node1 = Node(1, 0, 0)
    node2 = Node(2, 2, 0)
    f_element = FrameElement(node1, node2, 1, 1, 1)
    
    load = PointLoad(10, 0, f_element)

    expected = np.array([0,
                         -10,
                         0,
                         0,
                         0,
                         0])

    np.testing.assert_allclose(load.equivalent_nodal_load(), expected, atol=1e-12)

def test_vertical_point_load_end_node():
    node1 = Node(1, 0, 0)
    node2 = Node(2, 2, 0)
    f_element = FrameElement(node1, node2, 1, 1, 1)
    
    load = PointLoad(10, 2, f_element)

    expected = np.array([0,
                         0,
                         0,
                         0,
                         -10,
                         0])

    np.testing.assert_allclose(load.equivalent_nodal_load(), expected, atol=1e-12)

def test_axial_point_load():
    node1 = Node(1, 0, 0)
    node2 = Node(2, 10, 0)
    f_element = FrameElement(node1, node2, 1, 1, 1)
    
    load = PointLoad(10, 4, f_element, angle=0.0)

    expected = np.array([6,
                         0,
                         0,
                         4,
                         0,
                         0])

    np.testing.assert_allclose(load.equivalent_nodal_load(), expected, atol=1e-12)

@pytest.mark.parametrize("a", [0.0, 1.0, 3.0, 5.0, 7.0, 9.0, 10.0])

def test_point_load_equilibrium(a):
    node1 = Node(1, 0, 0)
    node2 = Node(2, 10, 0)
    f_element = FrameElement(node1, node2, 1, 1, 1)

    L = f_element.length()
    P = 10

    load = PointLoad(P, a, f_element)

    f = load.equivalent_nodal_load()

    # Force equilibrium
    equivalent_force = f[1] + f[4]
    assert equivalent_force == pytest.approx(-P)

    # Moment equilibrium about start node
    equivalent_moment = f[2] + f[5] + f[4] * L
    applied_moment = -P * a
    assert equivalent_moment == pytest.approx(applied_moment)

def test_point_load_magnitude_linearity():
    node1 = Node(1, 0, 0)
    node2 = Node(2, 10, 0)
    f_element = FrameElement(node1, node2, 1, 1, 1)

    load1 = PointLoad(100, 4, f_element)
    load2 = PointLoad(200, 4, f_element)

    np.testing.assert_allclose(
        load2.equivalent_nodal_load(),
        2 * load1.equivalent_nodal_load()
    )

def test_point_load_rotated_element():
    node1 = Node(1, 0, 0)
    node2 = Node(2, 10, 10)
    f_element = FrameElement(node1, node2, 1, 1, 1)

    P = 100.0
    a = f_element.length() / 2

    load = PointLoad(
        P=P,
        x=a,
        element=f_element,
        angle=0.0,
    )

    actual = load.equivalent_nodal_load()

    expected = np.array([
        P / 2 * np.cos(np.pi / 4),
        P / 2 * np.sin(np.pi / 4),
        0.0,
        P / 2 * np.cos(np.pi / 4),
        P / 2 * np.sin(np.pi / 4),
        0.0,
    ])

    np.testing.assert_allclose(actual, expected, atol=1e-12)