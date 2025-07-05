# Enhanced AC Circuit Analyzer

## Description

The **Enhanced AC Circuit Analyzer** is a Python-based tool developed for analyzing AC electrical circuits using Modified Nodal Analysis (MNA), graph theory, and linear algebra. Created by the team "5leha 3la Allah" for the Digital Systems Design course (ECE 115), this project automates circuit analysis by modeling circuits as graphs, transforming Kirchhoff's laws into matrix equations, and solving for node voltages, component currents, and equivalent impedances. The tool features a Tkinter-based GUI for adding components (resistors, capacitors, inductors), voltage sources, current sources, and nodes, with real-time circuit visualization and analysis results. It handles complex circuits, including series and parallel configurations, and supports AC sources with configurable waveforms, frequencies, and phases.

## Project Structure

- **linear_code.py**: Main Python script implementing the Enhanced AC Circuit Analyzer with GUI, MNA solver, and circuit visualization.
- **Linear_5leha_ala_allah.pptx**: Presentation slides detailing the theoretical approach, including graph theory, MNA, and LU decomposition for circuit analysis.
- **README.md**: This file, providing an overview and instructions for the project.

## Prerequisites

- **Python 3.x**: Required to run the analyzer.
- **Python Libraries**: Install the following dependencies:
  ```bash
  pip install numpy matplotlib tkinter
  ```
- **Documentation**: Refer to `Linear_5leha_ala_allah.pptx` for theoretical background and methodology.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/enhanced-ac-circuit-analyzer.git
   ```
2. Ensure `linear_code.py` is in the project directory.
3. Install required Python libraries:
   ```bash
   pip install numpy matplotlib tkinter
   ```

## Usage

1. Run the Python script to launch the GUI:
   ```bash
   python linear_code.py
   ```
2. Use the GUI to:
   - **Add Components**: Select resistor, capacitor, or inductor, specify value (Ω, μF, mH), and choose nodes.
   - **Add Sources**: Configure voltage or current sources (sine, square, or triangle) with peak, frequency (Hz), phase (degrees), and node connections.
   - **Manage Nodes**: Add custom nodes or use automatic node assignment (GND included by default).
   - **Analyze Circuit**: Click "Analyze Circuit" to compute node voltages, component currents, and equivalent impedances.
   - **Detect Series/Parallel**: Identify series and parallel component configurations.
   - **Clear Circuit**: Reset the circuit to start a new design.
3. View results in the right panel, including:
   - Node voltages (magnitude and phase).
   - Component currents (magnitude and phase).
   - Equivalent impedances for series/parallel configurations.
4. Observe the circuit visualization, showing components (resistors in red, capacitors in blue, inductors in green, sources in purple) and node connections.
5. Refer to `Linear_5leha_ala_allah.pptx` for details on the matrix-based analysis approach.

## Key Features

- **GUI Interface**: Tkinter-based interface for intuitive circuit design and analysis.
- **Modified Nodal Analysis (MNA)**: Solves AC circuits using complex impedance matrices, modeling circuits as `[Y][V] = [I]` (admittance matrix, node voltages, current sources).
- **Component Support**: Handles resistors (Ω), capacitors (F), inductors (H), voltage sources, and current sources (sine, square, triangle waveforms).
- **Circuit Visualization**: Displays nodes and components with labels for values, frequencies, and phases.
- **Series/Parallel Detection**: Uses graph theory to identify series and parallel component configurations.
- **Impedance Analysis**: Computes equivalent impedances for series and parallel combinations.
- **Error Handling**: Detects singular matrices (e.g., floating nodes) and suggests fixes like grounding a node.
- **LU Decomposition**: Efficiently solves the MNA matrix with O(n³) factorization and O(n²) substitutions for multiple analyses.

## Example Usage

1. **Simple RC Circuit**:
   - Add a resistor (1000Ω) between nodes N1 and N2.
   - Add a capacitor (1μF) between N2 and GND.
   - Add a voltage source (10V, 60Hz, 0° phase) between N1 and GND.
   - Click "Analyze Circuit" to get:
     - Node voltages (e.g., N1: 10.0000V ∠0.00°, N2: ~7.071V ∠-45.00°).
     - Component currents (e.g., Resistor: 0.0029A ∠45.00°, Capacitor: 0.0029A ∠45.00°).
   - Visualize the circuit diagram showing the resistor, capacitor, and voltage source.

2. **Series/Parallel Detection**:
   - Add two resistors (1000Ω each) between N1 and N2.
   - Click "Detect Series/Parallel" to identify parallel configuration and compute equivalent impedance (~500Ω).

## Technical Details (from Linear_5leha_ala_allah.pptx)

- **Graph Theory**: Circuits are modeled as graphs with nodes (junctions) and edges (components/sources), represented by adjacency matrices.
- **Kirchhoff's Laws to Matrices**: MNA transforms Kirchhoff's Current Law (KCL) and Voltage Law (KVL) into a matrix equation `[Y][V] = [I]`.
- **Complex Impedances**:
  - Resistor: `Y = 1/R`
  - Capacitor: `Y = j*2πfC`
  - Inductor: `Y = 1/(j*2πfL)`
- **Challenges Addressed**:
  - Handles multi-loop and non-planar circuits.
  - Supports dependent sources (e.g., CCVS) by modifying matrix entries.
  - Reduces manual KCL/KVL errors through automation.
- **Limitations**:
  - Singular matrices from floating nodes (fix: ground a node).
  - Nonlinear components (e.g., diodes) require iterative methods.
  - High-frequency analysis may cause numerical instability.

## Contributing

Contributions are welcome! Please follow these steps:
1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make changes and commit (`git commit -m 'Add new feature'`).
4. Push to the branch (`git push origin feature-branch`).
5. Open a pull request.

## Authors

- **Team: 5leha 3la Allah**
  - Seif Haythem
  - Abdelrahman Gomaa
  - Abdelrahman Essmat
  - Ahmed Zaytoon
  - Hesham Elkateb
- **Instructor**: Dr. Hany M. Zamil
- **Teaching Assistant**: Eng. Amr Al-Iraqi

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Developed as part of the Digital Systems Design course (ECE 115).
- Thanks to Dr. Hany M. Zamil and Eng. Amr Al-Iraqi for guidance.
- The matrix-based approach and GUI design were inspired by the need to automate complex circuit analysis, as detailed in `Linear_5leha_ala_allah.pptx`.