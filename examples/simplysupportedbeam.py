"""
Example: simply supported beam with a downward point load at its midspan

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
    length = 4000.0 # mm

    node_1 = Node(id=1, x=0, y=0, restraints=(True, True, False))
    node_2 = Node(id=2, x=length/2, y=0, restraints=(False, False, False))
    node_3 = Node(id=3, x=length, y=0, restraints=(False, True, False))

    # 2. Define the beam's material and section properties.
    E = 200000.0  # MPa
    A = 1000.0    # mm^2
    I = 8000000.0  # mm^4

    element_1 = FrameElement(start=node_1, end=node_2, E=E, A=A, I=I)
    element_2 = FrameElement(start=node_2, end=node_3, E=E, A=A, I=I)

    # 3. Apply a 10,000 N downward point load at midspan.
    load = PointLoad(P=10000.0, x=length/2, element=element_1)

    # 4. Assemble the complete structural model.
    frame = Frame(nodes=[node_1, node_2, node_3], elements=[element_1, element_2], point_loads=[load])

    # 5. Run the analysis.
    analysis = FrameAnalysis(frame)
    results = analysis.run()

    # 6. Display the results.
    print("SIMPLY SUPPORTED BEAM VALIDATION")
    print("-" * 35)

    print("\nNodal displacement vector [mm, mm, rad, ...]:")
    print(results.u)

    print("\nSupport reaction vector:")
    print(results.R)

    tip_vertical_displacement = results.u[4, 0]

    print(
        "\nVertical displacement at midspan: "
        f"{tip_vertical_displacement:.6f} mm"
    )

    # Theoretical benchmarks
    expected_reaction = 10000 / 2
    expected_deflection = -10000 * length**3 / (48 * E * I)

    print(f"\nExpected vertical reaction at each support: "
          f"{expected_reaction:.6f} N")
    print(f"Expected midspan vertical displacement: "
          f"{expected_deflection:.6f} mm")


if __name__ == "__main__":
    main()