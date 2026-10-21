from plotting.visualiser import Visualiser
import numpy as np
from models.frame import Frame
from models.frameelement import FrameElement
from models.loads import PointLoad
from models.node import Node
from analysis.results import Results
import pytest

def test_load_position_at_midpoint():
    node_1 = Node(1, 0, 0, [True, True, True])
    node_2 = Node(2, 1, 0, [False, False, False])

    element = FrameElement(
        node_1,
        node_2,
        E=1,
        A=1,
        I=1
    )

    load = PointLoad(
        P=10,
        x=0.5,
        element=element
    )

    frame = Frame(
        [node_1, node_2],
        [element],
        [load]
    )

    results = Results([], [], {}, {})
    visualiser = Visualiser(frame, results)

    x, y = visualiser._load_position(load)

    assert x == pytest.approx(0.5)
    assert y == pytest.approx(0.0)

def test_load_position_at_element_start():
    node_1 = Node(1, 0, 0, [True, True, True])
    node_2 = Node(2, 1, 0, [False, False, False])

    element = FrameElement(
        node_1,
        node_2,
        E=1,
        A=1,
        I=1
    )

    load = PointLoad(
        P=10,
        x=0,
        element=element
    )

    frame = Frame(
        [node_1, node_2],
        [element],
        [load]
    )

    results = Results([], [], {}, {})
    visualiser = Visualiser(frame, results)

    x, y = visualiser._load_position(load)

    assert x == pytest.approx(0)
    assert y == pytest.approx(0)

def test_load_position_at_element_end():
    node_1 = Node(1, 0, 0, [True, True, True])
    node_2 = Node(2, 1, 0, [False, False, False])

    element = FrameElement(
        node_1,
        node_2,
        E=1,
        A=1,
        I=1
    )

    load = PointLoad(
        P=10,
        x=1,
        element=element
    )

    frame = Frame(
        [node_1, node_2],
        [element],
        [load]
    )

    results = Results([], [], {}, {})
    visualiser = Visualiser(frame, results)

    x, y = visualiser._load_position(load)

    assert x == pytest.approx(1)
    assert y == pytest.approx(0)

def test_vertical_load_direction():
    node_1 = Node(1, 0, 0, [True, True, True])
    node_2 = Node(2, 1, 0, [False, False, False])

    element = FrameElement(
        node_1,
        node_2,
        E=1,
        A=1,
        I=1
    )

    load = PointLoad(
        P=10,
        x=0.5,
        element=element,
        angle=np.pi / 2
    )

    frame = Frame(
        [node_1, node_2],
        [element],
        [load]
    )

    results = Results([], [], {}, {})
    visualiser = Visualiser(frame, results)

    dx, dy = visualiser._load_direction(load)

    assert dx == pytest.approx(0)
    assert dy == pytest.approx(-1)

def test_horizontal_load_direction():
    node_1 = Node(1, 0, 0, [True, True, True])
    node_2 = Node(2, 1, 0, [False, False, False])

    element = FrameElement(
        node_1,
        node_2,
        E=1,
        A=1,
        I=1
    )

    load = PointLoad(
        P=10,
        x=0.5,
        element=element,
        angle=0
    )

    frame = Frame(
        [node_1, node_2],
        [element],
        [load]
    )

    results = Results([], [], {}, {})
    visualiser = Visualiser(frame, results)

    dx, dy = visualiser._load_direction(load)

    assert dx == pytest.approx(1)
    assert dy == pytest.approx(0)

def test_load_direction_on_inclined_element():
    node_1 = Node(1, 0, 0, [True, True, True])
    node_2 = Node(2, 1, 1, [False, False, False])

    element = FrameElement(
        node_1,
        node_2,
        E=1,
        A=1,
        I=1
    )

    load = PointLoad(
        P=10,
        x=element.length() / 2,
        element=element,
        angle=np.pi / 2
    )

    frame = Frame(
        [node_1, node_2],
        [element],
        [load]
    )

    results = Results([], [], {}, {})
    visualiser = Visualiser(frame, results)

    dx, dy = visualiser._load_direction(load)

    assert dx == pytest.approx(1 / np.sqrt(2))
    assert dy == pytest.approx(-1 / np.sqrt(2))