import numpy as np
from models.node import Node

def test_node_coordinates():
    node = Node(1, 1500, 3500)
    
    assert node.x == 1500
    assert node.y == 3500