
import pandas as pd

from nodes import *
from lines import *
from helpers import *

# Read input data from the Excel file handed out.
def read_data():
    
    # Build a Pandas frame by reading the xlsx file.
    frame = pd.read_excel("Input/Problem 2 data.xlsx", "Problem 2.2 - Base case")
    
    # Find the number of rows. There are 2 "header rows".
    n_rows = len(frame) - 2
    
    # Define arrays for areas, lines, producers and consumers
    areas = find_nodes(frame)
    producers = [ _cell(frame, 0, i + 2) for i in range(n_rows) ]
    consumers = [ _cell(frame, 9, i + 2) for i in range(n_rows) ]
    
    # Initialize empty matrices (dictionaries) for capacities and MC
    prod_cap = fill_initial(areas, producers)
    cons_cap = fill_initial(areas, consumers)
    prod_mc = fill_initial(areas, producers)
    
    lines, line_capacities, line_susceptances = find_lines(frame, areas)
    
    # Fill actual production capacities and marginal costs
    # These only appear on the diagonals, since there's only
    # one producer and consumer per "area"
    for i in range(n_rows):
        a = areas[i]
        p = producers[i]
        c = consumers[i]
        prod_cap[a, p] = _cell(frame, 1, i + 2)
        cons_cap[a, c] = _cell(frame, 10, i + 2)
        prod_mc[a, p] = _cell(frame, 2, i + 2)
    
    return areas, lines, line_capacities, line_susceptances, producers, consumers, prod_cap, cons_cap, prod_mc


# Fetch the data in the cell with coordinates (x, y) in the given frame.
def _cell(data, x, y):
    return data.iloc[y].iloc[x]

