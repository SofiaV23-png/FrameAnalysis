from models.node import Node
from models.frameelement import FrameElement

node_1 = Node(1, 1, 1)
node_2 = Node(2, 0, 0)

beam = FrameElement(node_1, node_2, 210, 100, 10e8)
print(beam.angle())

value = 2
print(-value)