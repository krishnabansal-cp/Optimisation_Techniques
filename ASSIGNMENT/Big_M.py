import numpy as np
import pandas as pd

def print_tableau(tableau, columns, iteration):
    """Formats and prints the Simplex tableau."""
    print(f"\n--- Iteration {iteration} ---")
    df = pd.DataFrame(tableau, columns=columns, index=["Eq1 (A1)", "Eq2 (A2)", "Eq3 (S2)", "Z-Row"])
    print(df.round(3))

def solve_big_m():
    # Define a sufficiently large number for M
    M = 100000.0
    
    # Columns: x1, x2, x3, S1, S2, A1, A2, RHS
    columns = ['x1', 'x2', 'x3', 'S1', 'S2', 'A1', 'A2', 'RHS']
    
    # Initial Matrix / Tableau Setup
    tableau = np.array([
        [1.0,   1.0,   1.0,   0.0,  0.0,  1.0,  0.0,  100.0],  # Constraint 1 (=)
        [0.04,  0.08,  0.10, -1.0,  0.0,  0.0,  1.0,  6.0],    # Constraint 2 (>=)
        [0.02,  0.01,  0.05,  0.0,  1.0,  0.0,  0.0,  3.0],    # Constraint 3 (<=)
        [30.0,  45.0,  50.0,  0.0,  0.0,   M,    M,   0.0]     # Z-Row (C_j initially)
    ])
    
    # Standardize the Z-row: Z_j - C_j = 0
    # Subtract M * (Row 1) and M * (Row 2) from the Z-row to zero out A1 and A2 columns
    tableau[3] = tableau[3] - (M * tableau[0]) - (M * tableau[1])
    
    iteration = 0
    print_tableau(tableau, columns, iteration)
    
    while True:
        # Check for optimality: If all coefficients in the Z-row (excluding RHS) are >= 0
        if np.all(tableau[3, :-1] >= -1e-6): 
            print("\nOptimal solution reached!")
            break
            
        # Find entering variable (most negative value in Z-row)
        pivot_col = np.argmin(tableau[3, :-1])
        
        # Find leaving variable (minimum positive ratio: RHS / entering column)
        ratios = []
        for i in range(3): # 3 constraints
            if tableau[i, pivot_col] > 1e-6: # Prevent division by zero or negative
                ratios.append(tableau[i, -1] / tableau[i, pivot_col])
            else:
                ratios.append(np.inf)
                
        pivot_row = np.argmin(ratios)
        
        if ratios[pivot_row] == np.inf:
            print("\nProblem is unbounded!")
            return
            
        print(f"\nEntering Variable: {columns[pivot_col]}")
        print(f"Leaving Row Index: {pivot_row}")
        
        # Perform Pivot Operations
        pivot_element = tableau[pivot_row, pivot_col]
        tableau[pivot_row] = tableau[pivot_row] / pivot_element
        
        for i in range(4):
            if i != pivot_row:
                tableau[i] = tableau[i] - (tableau[i, pivot_col] * tableau[pivot_row])
                
        iteration += 1
        print_tableau(tableau, columns, iteration)

    # Extract final values
    # A variable is basic if its column has exactly one '1' and the rest '0's
    results = {'x1': 0, 'x2': 0, 'x3': 0}
    for i, var in enumerate(['x1', 'x2', 'x3']):
        col = tableau[:, i]
        if np.count_nonzero(col[:-1]) == 1 and np.sum(col[:-1]) == 1.0:
            row_idx = np.where(col[:-1] == 1.0)[0][0]
            results[var] = tableau[row_idx, -1]

    optimal_cost = tableau[3, -1]  # Z* value

    print("\n==================================")
    print("FINAL OPTIMAL SOLUTION:")
    print(f"Raw Material 1 (x1): {results['x1']:.2f} kg")
    print(f"Raw Material 2 (x2): {results['x2']:.2f} kg")
    print(f"Raw Material 3 (x3): {results['x3']:.2f} kg")
    print(f"Minimum Total Cost: ${optimal_cost:.2f}")
    print("==================================")

if __name__ == "__main__":
    solve_big_m()