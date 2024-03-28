
from helpers import *

def find_params(frame, nodes):
    
    # Find the number of rows. There are 2 "header rows".
    n_rows = len(frame) - 2
    
    # First column (x index) for producers and consumers
    p_x = 0
    c_x = 9
    
    producers = []
    consumers = []
    
    print(n_rows)
    
    for i in range(n_rows):
        for x, array in [(p_x, producers), (c_x, consumers)]:
            entity = cell(frame, x, i + 2)
            if type(entity) == str and entity != "":
                array.append(entity)
    
    print(producers, consumers)
    
    # Initialize empty matrices (dictionaries) for capacities and MC
    prod_mc = fill_initial(nodes, producers)
    prod_cap = fill_initial(nodes, producers)
    cons_cap = fill_initial(nodes, consumers)
    
    # Fill actual production capacities and marginal costs
    # These only appear on the diagonals, since there's only
    # one producer and consumer per "area"
    for i in range(len(producers)):
        p = producers[i]
        node = cell(frame, p_x + 3, i + 2)
        prod_mc[node, p] = cell(frame, 2, i + 2)
        prod_cap[node, p] = cell(frame, 1, i + 2)
    
    for i in range(len(consumers)):
        c = consumers[i]
        node = cell(frame, c_x + 2, i + 2)
        cons_cap[node, c] = cell(frame, 10, i + 2)
    
    return producers, consumers, prod_mc, prod_cap, cons_cap
