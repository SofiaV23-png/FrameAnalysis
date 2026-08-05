from models.node import Node
from models.frameelement import FrameElement


node1 = Node(1, 0, 0)
node2 = Node(2, 1000, 0)

f_element = FrameElement(
    node1,
    node2,
    E=200000,
    A=2000,
    I=1e6
    )

print(f_element.local_stiffness())
print(f_element.transformation())
print(f_element.angle())
print(f_element.global_stiffness())