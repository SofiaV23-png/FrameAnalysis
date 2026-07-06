from models.node import Node
from models.frameelement import FrameElement

node_1 = Node(1, 0, 0)
node_2 = Node(1, 1, 0)

beam = FrameElement(node_1, node_2, 210, 100, 10e8)
print(beam.start)