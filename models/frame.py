<<<<<<< Updated upstream
class Frame:
    def __init__(self, nodes, elements):
=======
from .node import Node
from .frameelement import FrameElement
from .loads import PointLoad

class Frame:
    def __init__(self, nodes: list[Node] = [], elements: list[FrameElement] = [], point_loads: list[PointLoad] = []):
>>>>>>> Stashed changes
        self.nodes = nodes
        self.elements = elements
        self.point_loads = point_loads

    
