
import numpy as np
import pytest

from analysis.frameanalysis import FrameAnalysis
from analysis.results import Results
from models.frame import Frame
from models.frameelement import FrameElement
from models.loads import PointLoad
from models.node import Node


@pytest.fixture
def cantilever_frame():
    fixed_node = Node(
        id=1,
        x=0,
        y=0,
        restraints=(True, True, True),
    )

    free_node = Node(
        id=2,
        x=1,
        y=0,
        restraints=(False, False, False),
    )

    element = FrameElement(
        start=fixed_node,
        end=free_node,
        E=1,
        A=1,
        I=1,
    )

    load = PointLoad(
        P=10,
        x=1,
        element=element,
    )

    return Frame(
        nodes=[fixed_node, free_node],
        elements=[element],
        point_loads=[load],
    )


@pytest.fixture
def analysis(cantilever_frame):
    return FrameAnalysis(cantilever_frame)


def test_run_returns_results_object(analysis):
    results = analysis.run()
    assert isinstance(results, Results)


def test_cantilever_displacements_match_theory(analysis):
    results = analysis.run()

    expected_displacements = np.array([
        [0],
        [0],
        [0],
        [0],
        [-10 / 3],
        [-5],
    ])

    assert results.u.shape == (6, 1)

    np.testing.assert_allclose(
        results.u,
        expected_displacements,
        rtol=1e-7,
        atol=1e-9,
    )


def test_support_reactions_balance_applied_load(analysis):
    results = analysis.run()

    assert results.R.shape == (6, 1)

    expected_support_reactions = np.array([0, 10, 10])

    np.testing.assert_allclose(
        results.R[[0, 1, 2], 0],
        expected_support_reactions,
        atol=1e-9,
    )

    np.testing.assert_allclose(
        results.R[[3, 4, 5], 0],
        np.zeros(3),
        atol=1e-9,
    )


def test_element_results_are_returned(analysis):
    results = analysis.run()

    assert 1 in results.element_displacements
    assert 1 in results.element_forces

    element_displacements = results.element_displacements[1]
    element_forces = results.element_forces[1]

    assert element_displacements.shape == (6, 1)
    assert element_forces.shape == (6, 1)

    np.testing.assert_allclose(
        element_displacements,
        results.u,
        atol=1e-9,
    )

    expected_element_forces = np.array([
        [0],
        [10],
        [10],
        [0],
        [0],
        [0],
    ])

    np.testing.assert_allclose(
        element_forces,
        expected_element_forces,
        atol=1e-9,
    )
