from models.node import Node
from models.frameelement import FrameElement

node_1 = Node(1, 0, 0)
node_2 = Node(2, 3000, 0)

beam = FrameElement(node_1, node_2, 200000, 2000, 1e6)
print(beam.local_stiffness())