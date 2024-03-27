
from helpers import *

def find_params(frame, nodes):
    
    # Find the number of rows. There are 2 "header rows".
    n_rows = len(frame) - 2
    
    producers = [ _cell(frame, 0, i + 2) for i in range(n_rows) ]
    consumers = [ _cell(frame, 9, i + 2) for i in range(n_rows) ]
    
    # Initialize empty matrices (dictionaries) for capacities and MC
    prod_mc = fill_initial(nodes, producers)
    prod_cap = fill_initial(nodes, producers)
    cons_cap = fill_initial(nodes, consumers)
    
    # Fill actual production capacities and marginal costs
    # These only appear on the diagonals, since there's only
    # one producer and consumer per "area"
    for i in range(n_rows):
        p = producers[i]
        c = consumers[i]
        node = _cell(frame, 3, i + 2)
        prod_mc[node, p] = _cell(frame, 2, i + 2)
        prod_cap[node, p] = _cell(frame, 1, i + 2)
        cons_cap[node, c] = _cell(frame, 10, i + 2)
    
    return producers, consumers, prod_mc, prod_cap, cons_cap


# Fetch the data in the cell with coordinates (x, y) in the given frame.
def _cell(data, x, y):
    return data.iloc[y].iloc[x]

