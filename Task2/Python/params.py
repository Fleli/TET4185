
from helpers import *

def find_params(frame, nodes, cols_x, flexible_demand):
    
    # Find the number of rows. There are 2 "header rows".
    n_rows = len(frame) - 2
    
    # Arrays for producers and consumers (names)
    producers = []
    consumers = []
    
    # Fill the lists of producers and consumers
    for i in range(n_rows):
        for x, array in [(cols_x["name prod"], producers), (cols_x["name cons"], consumers)]:
            entity = cell(frame, x, i + 2)
            if (type(entity) == str) and (entity != ""):
                array.append(entity)
    
    # Initialize empty matrices (dictionaries) for capacities and MC
    prod_mc = fill_initial(nodes, producers)
    prod_cap = fill_initial(nodes, producers)
    cons_mc = fill_initial(nodes, consumers)
    cons_cap = fill_initial(nodes, consumers)
    
    # Fill actual production capacities and marginal costs
    for i in range(len(producers)):
        p = producers[i]
        node = cell(frame, cols_x["node prod"], i + 2)
        prod_mc[node, p] = cell(frame, cols_x["mc prod"], i + 2)
        prod_cap[node, p] = cell(frame, cols_x["cap prod"], i + 2)
    
    # Fill actual consumption capacities and marginal costs
    for i in range(len(consumers)):
        c = consumers[i]
        node = cell(frame, cols_x["node cons"], i + 2)
        if flexible_demand:
            cons_mc[node, c] = cell(frame, cols_x["mc cons"], i + 2)
        cons_cap[node, c] = cell(frame, cols_x["cap cons"], i + 2)
    
    # Return the data we've found
    return producers, consumers, prod_mc, prod_cap, cons_mc, cons_cap
