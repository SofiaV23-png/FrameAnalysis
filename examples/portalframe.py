"""
Example: Portal frame with central point load

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
    length = 3000.0 # mm
    height = 4000.0 # mm

    pin_base = Node(id=1, x=0, y=0, restraints=(True, True, False))
    left_connection = Node(id=2, x=0, y=height, restraints=(False, False, False))
    right_connection = Node(id=3, x=length, y=height, restraints=(False, False, False))
    roller_base = Node(id=4, x=length, y=0, restraints=(False, True, False))
    midspan = Node(id=5, x=length/2, y=height, restraints=(False, False, False))

    # 2. Define the beam's material and section properties.
    E = 200000.0  # MPa
    A = 1000.0    # mm^2
    I = 8000000.0  # mm^4

    # 3. Define nodes, frame elements and loads

    left_base = Node(
        id=1, x=0.0, y=0.0,
        restraints=(True, True, False),
    )
    left_joint = Node(
        id=2, x=0.0, y=height,
        restraints=(False, False, False),
    )
    midspan = Node(
        id=3, x=length/2, y=height,
        restraints=(False, False, False),
    )
    right_joint = Node(
        id=4, x=length, y=height,
        restraints=(False, False, False),
    )
    right_base = Node(
        id=5, x=length, y=0.0,
        restraints=(False, True, False),
    )


    left_column = FrameElement(
        start=left_base, end=left_joint,
        E=E, A=A, I=I,
    )
    left_beam = FrameElement(
        start=left_joint, end=midspan,
        E=E, A=A, I=I,
    )
    right_beam = FrameElement(
        start=midspan, end=right_joint,
        E=E, A=A, I=I,
    )
    right_column = FrameElement(
        start=right_base, end=right_joint,
        E=E, A=A, I=I,
    )

    load_magnitude = 10000

    load = PointLoad(
        P=load_magnitude,
        x=length/2,
        element=left_beam,
    )

    # 4. Assemble the structural model
    frame = Frame(
        nodes=[
            left_base, left_joint, midspan, right_joint, right_base
        ],
        elements=[
            left_column, left_beam, right_beam, right_column
        ],
        point_loads=[load],
    )


    # 5. Run the analysis.
    analysis = FrameAnalysis(frame)
    results = analysis.run()

    # 6. Display the results.
    print("PORTAL FRAME VALIDATION")
    print("-" * 35)

    print("\nNodal displacement vector [mm, mm, rad, ...]:")
    print(results.u)

    print("\nSupport reaction vector:")
    print(results.R)

    tip_vertical_displacement = results.u[12, 0]

    beam_midspan_moment = results.element_forces[2][5, 0]

    print(
        "\nHorizontal displacement at right base: "
        f"{tip_vertical_displacement:.6f} mm"
    )

    print(
        "\nMoment at beam midspan: "
        f"{beam_midspan_moment:.2f} N"
    )

    # Theoretical benchmarks
    expected_moment = load_magnitude * length / 4
    expected_deflection = load_magnitude * height * length**2 / (8 * E * I)

    print(f"\nExpected horizontal displacement at right base: "
          f"{expected_deflection:.6f} mm")

    print(f"\nExpected moment at beam midspan: "
          f"{expected_moment:.2f} N")

    print("\nElement internal forces:")
    for element_id, forces in results.element_forces.items():
        print(f"Element {element_id}:")
        print(forces)

if __name__ == "__main__":
    main()