import numpy as np
from models.frameelement import FrameElement
from models.node import Node

def test_length():
    node1 = Node(1, 0, 0)
    node2 = Node(2, 3000, 4000)

    f_element = FrameElement(node1, node2, 1, 1, 1)

    assert np.isclose(f_element.length(), 5000)

