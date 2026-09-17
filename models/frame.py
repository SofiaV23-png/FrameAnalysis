from .node import Node
from .frameelement import FrameElement
from .loads import PointLoad

class Frame:
    def __init__(self, nodes: list[Node] = [], elements: list[FrameElement] = [], point_loads: list[PointLoad] = []):
        self.nodes = nodes
        self.elements = elements
        self.point_loads = point_loads

    def connect_point_loads_to_elements(self):
        for load in self.point_loads:
            if load not in load.element.applied_point_loads:
                load.element.applied_point_loads.append(load)
