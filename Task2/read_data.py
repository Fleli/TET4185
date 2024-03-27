
import pandas as pd
import pyomo.environ as pyo

# Read input data from the Excel file handed out.
def read_data():
    
    # Build a Pandas frame by reading the xlsx file.
    frame = pd.read_excel("Problem 2 data.xlsx", "Problem 2.2 - Base case")
    
    print(frame)
    
    # Define arrays for areas, lines, producers and consumers
    areas = [ (i + 1) for i in range(3) ]
    lines = [ _cell(frame, 15, i + 2) for i in range(3) ]
    producers = [ _cell(frame, 0, i + 2) for i in range(3) ]
    consumers = [ _cell(frame, 9, i + 2) for i in range(3) ]
    
    # Initialize empty matrices (dictionaries) for capacities and MC
    prod_cap = _fill_initial(areas, producers)
    cons_cap = _fill_initial(areas, consumers)
    prod_mc = _fill_initial(areas, producers)
    
    # Fill actual production capacities and marginal costs
    # These only appear on the diagonals, since there's only
    # one producer and consumer per "area"
    for i in range(3):
        a = areas[i]
        p = producers[i]
        prod_cap[a, p] = _cell(frame, 1, i + 2)
        cons_cap[a, p] = _cell(frame, 10, i + 2)
        prod_mc[a, p] = _cell(frame, 2, i + 2)
    
    
    print(prod_cap)
    print(prod_mc)
    print(cons_cap)
    
    print(areas)
    print(lines)
    print(producers)
    print(consumers)
    
    
    print("\n")
    
    
    return areas, lines, producers, consumers, prod_cap, cons_cap, prod_mc


# Fetch the data in the cell with coordinates (x, y) in the given frame.
def _cell(data, x, y):
    return data.iloc[y].iloc[x]


# Helper method to fill an empty (2D) dictionary with "blank" data
def _fill_initial(areas, participants):
    return {
        (area, participant): 0
        for area in areas
        for participant in participants
    }
