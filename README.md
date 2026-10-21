# 2D Frame Analysis Solver

A Python-based structural analysis tool for analysing two-dimensional beams and frame structures using the direct stiffness method.

This project explores the implementation of a structural solver from first principles, covering structural modelling, element stiffness, load application, global system assembly and the calculation of nodal displacements, support reactions and element forces.

## Features

- **Structural modelling:** Define nodes, frame elements, support restraints and material and cross-sectional properties.
- **Frame analysis:** Solve the assembled structural system to obtain nodal displacements and support reactions.
- **Element force recovery:** Retrieve element force results for further structural assessment.
- **Loading:** Apply point loads using the project's load modelling interface.
- **Example models:** Explore cantilever beams, simply supported beams and portal frames.
- **Validation:** Develop automated tests comparing numerical results against analytical solutions and structural equilibrium checks.

## Structural Model

The solver represents structures using two-dimensional frame elements, with three degrees of freedom per node:

- Horizontal displacement, \(u_x\)
- Vertical displacement, \(u_y\)
- Rotation, \(\theta_z\)

Each element is defined by its end nodes, Young's modulus \(E\), cross-sectional area \(A\) and second moment of area \(I\).

The analysis follows the direct stiffness method:

1. Define the structural geometry, element properties and boundary conditions.
2. Form the element stiffness matrices.
3. Assemble the global stiffness matrix and load vector.
4. Apply support restraints and solve for nodal displacements.
5. Calculate support reactions and recover element forces.

## Sign Conventions

The solver uses the following sign conventions:

- **Local x-axis:** Positive from the element's start node (*i*) to its end node (*j*).
- **Local y-axis:** Positive perpendicular to the local x-axis, following the element's local coordinate system.
- **Axial force:** Positive in tension and negative in compression.
- **Shear force:** Positive in the direction of the positive local y-axis, subject to the element end-force convention.
- **Bending moment:** Positive counter-clockwise about the out-of-plane \(z\)-axis, subject to the element end-force convention.
- **Displacements:** Positive in the direction of the corresponding global or local coordinate axis.
- **Rotations:** Positive counter-clockwise.

The sign of reported element end forces depends on the local coordinate system and the force-recovery convention used by the solver.


## Getting Started

### Requirements

- Python 3.12 or a compatible Python version
- NumPy
- pytest (for running the test suite)

Install the dependencies listed in `requirements.txt`.

### Installation

Clone the repository and navigate into the project directory:

```bash
git clone https://github.com/SofiaV23-png/FrameAnalysis.git
cd FrameAnalysis
```

Create and activate a virtual environment:

```bash
python3 -m venv FA_venv
source FA_venv/bin/activate
```

Install the project dependencies:

```bash
python -m pip install -r requirements.txt
```

### Running an Example

Run an example from the repository root using Python's module syntax. For example:

```bash
python -m examples.cantilever
```

Other available examples include:

```bash
python -m examples.simply_supported_beam
python -m examples.portal_frame
```

Each example defines a structural model, runs the analysis and displays the resulting displacements, reactions and element forces.

## Project Structure

```text
FrameAnalysis/
├── analysis/       # Analysis and solution procedures
├── models/         # Nodes, elements, loads and frame models
├── examples/       # Demonstration structural models
├── tests/          # Automated tests
├── main.py         
├── requirements.txt
├── .gitignore
└── README.md
```

## Testing and Validation

Run the automated test suite from the repository root:

```bash
pytest
```

The aim of the validation suite is to check solver behaviour against known analytical solutions for simple structural systems, alongside checks on boundary conditions, support reactions and equilibrium.

For meaningful validation, expected values should be derived independently of the solver. Tests should also account for the sign conventions and degree-of-freedom ordering used by the implementation.

## Development Roadmap

### Currently in Development

Features and improvements actively being worked on:

- Expanding the validation suite to cover additional structural configurations and loading cases.
- Improving the presentation and visualisation of analysis results.
- Refining the handling of element forces and support reactions.

### Planned Future Improvements

Potential extensions to explore after the current development work:

- Support for distributed loads and more complex loading conditions.
- Visualisation of bending moment, shear force and axial force diagrams.
- Improved input validation, error handling and numerical robustness.
- Automated calculation of second moments of area for standard cross-sections and a library of predefined material properties.


## Motivation

This project combines structural engineering theory with software development to explore how numerical methods can be translated into practical engineering tools. It provides a foundation for further work in computational structural analysis and engineering software.




