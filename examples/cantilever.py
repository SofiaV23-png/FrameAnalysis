"""
Example: cantilever beam with a downward point load at its free end.

Units:
    Length: mm
    Force: N
    Young's modulus: MPa (N/mm^2)
    Area: mm^2
    Second moment of area: mm^4
"""

from models.node import Node
from models.frameelement import FrameElement
from models.loads import PointLoad
from models.frame import Frame
from analysis.frameanalysis import FrameAnalysis


def main():
    # 1. Define the beam geometry and boundary conditions.
    length = 1000.0 # mm

    fixed_node = Node(id=1, x=0, y=0, restraints=(True, True, True))
    free_node = Node(id=2, x=length, y=0, restraints=(False, False, False))

    # 2. Define the beam's material and section properties.
    E = 200000.0  # MPa
    A = 1000.0    # mm^2
    I = 8000000.0  # mm^4

    beam = FrameElement(start=fixed_node, end=free_node, E=E, A=A, I=I)

    # 3. Apply a 1000 N downward point load at the free end.
    load = PointLoad(P=1000.0, x=length, element=beam)

    # 4. Assemble the complete structural model.
    frame = Frame(nodes=[fixed_node, free_node], elements=[beam], point_loads=[load])

    # 5. Run the analysis.
    analysis = FrameAnalysis(frame)
    results = analysis.run()

    # 6. Display the results.
    print("CANTILEVER BEAM ANALYSIS")
    print("-" * 35)

    print("\nNodal displacement vector [mm, mm, rad, ...]:")
    print(results.u)

    print("\nSupport reaction vector:")
    print(results.R)

    tip_vertical_displacement = results.u[4, 0]

    print(
        "\nVertical displacement at the free end: "
        f"{tip_vertical_displacement:.6f} mm"
    )

    # 7. Compare with the Euler-Bernoulli analytical solution.
    theoretical_deflection = (
        -1000.0 * length**3 / (3 * E * I)
    )

    print(
        "Theoretical tip deflection: "
        f"{theoretical_deflection:.6f} mm"
    )


if __name__ == "__main__":
    main()
