import numpy as np
from models.node import Node

def test_node_coordinates():
    node = Node(1, 1500, 3500)
    
    assert node.x == 1500
    assert node.y == 3500

def test_node_dofs():
    node = Node(3, 1, 1)

    assert node.nodal_dof() == [6, 7, 8]