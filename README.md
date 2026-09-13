# Optimisation_Techniques

# Big-M Simplex Method: Metallurgical Alloy Blending

This repository contains a Python implementation of the **Big-M Simplex Method** to solve a constrained Linear Programming Problem (LPP). 

## Case Study: The Metallurgical Alloy Blending Problem
A foundry must produce exactly **100 kg** of a specialized alloy by blending three available raw materials ($M_1, M_2, M_3$). The final alloy must meet strict elemental composition requirements while minimizing the total cost of the raw materials.

### Mathematical Formulation

**Decision Variables:**
* $x_1$: Amount of Raw Material 1 (kg)
* $x_2$: Amount of Raw Material 2 (kg)
* $x_3$: Amount of Raw Material 3 (kg)

**Objective Function (Minimize Cost):**
Minimize $Z = 30x_1 + 45x_2 + 50x_3$

**Subject to Constraints:**
1. $x_1 + x_2 + x_3 = 100$ (Total weight must be exactly 100 kg)
2. $0.04x_1 + 0.08x_2 + 0.10x_3 \ge 6$ (Minimum Carbon requirement)
3. $0.02x_1 + 0.01x_2 + 0.05x_3 \le 3$ (Maximum Manganese limit)
4. $x_1, x_2, x_3 \ge 0$ (Non-negativity)

### Standard Form Conversion
To apply the Big-M method, the problem is converted to standard form by maximizing $-Z$, adding artificial variables ($A_1, A_2$) with a large penalty ($-M$), a surplus variable ($S_1$), and a slack variable ($S_2$).

Maximize $Z^* = -30x_1 - 45x_2 - 50x_3 + 0S_1 + 0S_2 - MA_1 - MA_2$

Subject to:
1. $x_1 + x_2 + x_3 + A_1 = 100$
2. $0.04x_1 + 0.08x_2 + 0.10x_3 - S_1 + A_2 = 6$
3. $0.02x_1 + 0.01x_2 + 0.05x_3 + S_2 = 3$

## Installation and Setup

1. Clone the repository:
   ```bash
   git clone [https://github.com/krishnabansal-cp/Optimisation_Techniques.git](https://github.com/krishnabansal-cp/Optimisation_Techniques.git)
   cd alloy-simplex-solver
