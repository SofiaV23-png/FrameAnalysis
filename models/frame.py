from .node import Node
from .frameelement import FrameElement

class Frame:
    def __init__(self, nodes: list[Node], elements: list[FrameElement]):
        self.nodes = nodes
        self.elements = elements

    
