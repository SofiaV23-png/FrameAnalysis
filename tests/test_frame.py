from models.frame import Frame
from models.loads import PointLoad
from models.frameelement import FrameElement
from models.node import Node
import numpy as np
import pytest


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

    return frame, element_1, element_2, load_1, load_2

def test_load_connection_method(frame_with_point_loads):
    frame, element_1, element_2, load_1, load_2 = frame_with_point_loads

    assert element_1.applied_point_loads == []
    assert element_2.applied_point_loads == []

    frame.connect_point_loads_to_elements()

    assert element_1.applied_point_loads == [load_1, load_2]
    assert element_2.applied_point_loads == []

def test_load_connection_method_called_twice(frame_with_point_loads):
    frame, element_1, element_2, load_1, load_2 = frame_with_point_loads

    frame.connect_point_loads_to_elements()
    frame.connect_point_loads_to_elements()

    assert element_1.applied_point_loads == [load_1, load_2]
    assert element_2.applied_point_loads == []