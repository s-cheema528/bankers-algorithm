# Banker's Algorithm Simulation

## Table of Contents
1. Introduction
2. Features
3. Technologies Used
4. Algorithm Overview
5. Implementation Details
6. Test Cases

---

## Introduction
This project is a simulation of the **Banker's Algorithm**, a resource allocation and deadlock avoidance algorithm used in operating systems. The algorithm ensures that resource allocation to processes does not lead to a deadlock by checking for a safe sequence of execution.

The project is implemented using **Python** and **Tkinter** for the graphical user interface (GUI). It allows users to input the number of resources, processes, and their respective allocation and maximum needs. The program then simulates the Banker's Algorithm step-by-step and displays the safe sequence if one exists.

---

## Features
- Dynamic Input: Users can input the number of available resources and add processes dynamically.
- Step-by-Step Execution: The algorithm runs step-by-step, showing the current state of available resources and the safe sequence.
- Error Handling: The program validates user input to ensure correct data entry.
- Visualization: The GUI provides a clear and interactive way to visualize the algorithm's execution.
- Safe Sequence Detection: The program detects and displays a safe sequence if one exists, or warns of an unsafe state.

---

## Technologies Used
- Python 3.10: The core programming language used for the project.
- Tkinter: Used for creating the graphical user interface (GUI).
- NumPy: Used for matrix calculations and handling resource allocation efficiently.
- ttk: Themed widgets from Tkinter for a modern look and feel.

---

## Algorithm Overview
The Banker's Algorithm follows these key steps:
1. Input Allocation & Maximum Resources: The user provides the number of resources allocated and maximum required for each process.
2. Calculate Need Matrix**: The need matrix is computed as `Need = Max - Allocation`.
3. Check Safe Sequence:
   - Start with available resources.
   - Find a process whose need can be fulfilled.
   - Allocate resources, execute the process, and release them.
   - Repeat until all processes are executed or deadlock is detected.

---

## Implementation Details
- The GUI displays input fields for Process Number, Allocation, Max, and Available Resources.
- The **Check Safe State** button verifies the safety of resource allocation and displays the result.
- If a safe sequence exists, it is displayed; otherwise, a warning is shown.

---

## Test Cases
| Process | Allocation (R1, R2, R3) | Max (R1, R2, R3) | Available (R1, R2, R3) | Safe Sequence |
|---------|-------------------------|------------------|------------------------|---------------|
| P0      | (2, 1, 0)               | (8, 6, 3)        | (4, 3, 3)              | P3 P2   P0 P1 |
| P1      | (1, 2, 2)               | (9, 4, 3)        |                        |               |
| P2      | (0, 2, 0)               | (5, 3, 3)        |                        |               |
| P3      | (3, 0, 1)               | (4, 2, 3)        |                        |               |
