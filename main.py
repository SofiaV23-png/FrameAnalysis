from models.node import Node
from models.frameelement import FrameElement
from models.frame import Frame
from models.loads import PointLoad
from analysis.assembler import Assembler
import numpy as np

node_1 = Node(1, 0, 0)
node_2 = Node(2, 10, 0)

element = FrameElement(node_1, node_2, 1, 1, 1)
load_1 = PointLoad(10, 5, element)
load_2 = PointLoad(5, 2, element)
frame = Frame([node_1, node_2], [element], [load_1, load_2])
assemble = Assembler(frame)
dofs = element.map_dof()
expected = load_1.equivalent_nodal_load() + load_2.equivalent_nodal_load()

print(dofs)
f = load_1.equivalent_nodal_load()
print(f, f.shape)
F = np.zeros((6, 1))
print(F.shape)