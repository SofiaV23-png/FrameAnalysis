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

