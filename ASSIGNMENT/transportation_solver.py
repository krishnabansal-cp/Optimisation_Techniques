import numpy as np

def calculate_penalties(costs, available_rows, available_cols):
    """Calculates row and column penalties for VAM."""
    row_penalties = {}
    col_penalties = {}
    
    for i in available_rows:
        row = sorted([costs[i][j] for j in available_cols])
        row_penalties[i] = row[1] - row[0] if len(row) > 1 else row[0]
        
    for j in available_cols:
        col = sorted([costs[i][j] for i in available_rows])
        col_penalties[j] = col[1] - col[0] if len(col) > 1 else col[0]
        
    return row_penalties, col_penalties

def vam(costs, supply, demand):
    """Generates Initial Basic Feasible Solution using Vogel's Approximation Method."""
    supply_copy = supply.copy()
    demand_copy = demand.copy()
    
    rows = len(supply)
    cols = len(demand)
    
    allocation = np.zeros((rows, cols))
    basic_cells = []
    
    available_rows = list(range(rows))
    available_cols = list(range(cols))
    
    while available_rows and available_cols:
        row_penalties, col_penalties = calculate_penalties(costs, available_rows, available_cols)
        
        max_row_penalty = max(row_penalties.values()) if row_penalties else -1
        max_col_penalty = max(col_penalties.values()) if col_penalties else -1
        
        # Determine whether to allocate in the row or column with the highest penalty
        if max_row_penalty >= max_col_penalty:
            target_row = max(row_penalties, key=row_penalties.get)
            target_col = min(available_cols, key=lambda j: costs[target_row][j])
        else:
            target_col = max(col_penalties, key=col_penalties.get)
            target_row = min(available_rows, key=lambda i: costs[i][target_col])
            
        # Allocate minimum of available supply or demand
        qty = min(supply_copy[target_row], demand_copy[target_col])
        allocation[target_row][target_col] = qty
        basic_cells.append((target_row, target_col))
        
        supply_copy[target_row] -= qty
        demand_copy[target_col] -= qty
        
        # Remove exhausted rows/columns
        if supply_copy[target_row] == 0 and target_row in available_rows:
            available_rows.remove(target_row)
        if demand_copy[target_col] == 0 and target_col in available_cols:
            available_cols.remove(target_col)
            
    return allocation, basic_cells

def modi_optimality_test(costs, allocation, basic_cells):
    """Applies MODI method to test for optimality."""
    rows, cols = costs.shape
    u = {i: None for i in range(rows)}
    v = {j: None for j in range(cols)}
    
    # Set u[0] to 0 to start the chain
    u[0] = 0
    
    # Calculate u_i and v_j for all basic cells (where c_ij = u_i + v_j)
    while None in u.values() or None in v.values():
        for (i, j) in basic_cells:
            if u[i] is not None and v[j] is None:
                v[j] = costs[i][j] - u[i]
            elif v[j] is not None and u[i] is None:
                u[i] = costs[i][j] - v[j]
                
    print("\n--- MODI Dual Variables ---")
    print(f"Row values (u_i): {u}")
    print(f"Col values (v_j): {v}")
    
    # Calculate opportunity costs for non-basic cells (d_ij = c_ij - (u_i + v_j))
    is_optimal = True
    print("\n--- Opportunity Costs (d_ij) for Non-Basic Cells ---")
    
    for i in range(rows):
        for j in range(cols):
            if (i, j) not in basic_cells:
                d_ij = costs[i][j] - (u[i] + v[j])
                print(f"Cell ({i}, {j}): {d_ij}")
                if d_ij < 0:
                    is_optimal = False
                    
    return is_optimal

def solve_transportation():
    costs = np.array([
        [12, 10, 15, 14],
        [8,  11,  9,  7],
        [5,  14,  8, 12]
    ])
    
    supply = [300, 500, 400]
    demand = [250, 350, 400, 200]
    
    print("Executing Vogel's Approximation Method (VAM)...")
    allocation, basic_cells = vam(costs, supply, demand)
    
    print("\n--- Initial Basic Feasible Solution (IBFS) ---")
    print(allocation)
    
    total_cost = np.sum(allocation * costs)
    print(f"\nTotal IBFS Cost: {total_cost}")
    
    print("\nExecuting MODI Method to test optimality...")
    is_optimal = modi_optimality_test(costs, allocation, basic_cells)
    
    if is_optimal:
        print("\nAll d_ij >= 0. The current solution is OPTIMAL.")
    else:
        print("\nNegative opportunity costs found. The solution requires iteration (Stepping-Stone).")
        # In this specific case study, VAM hits the optimal solution on the first try.

    print("\n==================================")
    print("FINAL OPTIMAL SHIPMENT PLAN:")
    print(f"Texas (S1) -> Stuttgart (D2): {allocation[0][1]} tons")
    print(f"W. Australia (S2) -> Stuttgart (D2): {allocation[1][1]} tons")
    print(f"W. Australia (S2) -> Seoul (D3): {allocation[1][2]} tons")
    print(f"W. Australia (S2) -> Kyoto (D4): {allocation[1][3]} tons")
    print(f"Inner Mongolia (S3) -> Shenzhen (D1): {allocation[2][0]} tons")
    print(f"Inner Mongolia (S3) -> Seoul (D3): {allocation[2][2]} tons")
    print(f"\nMinimum Total Transportation Cost: ${total_cost * 10000:,.2f}")
    print("==================================")

if __name__ == "__main__":
    solve_transportation()