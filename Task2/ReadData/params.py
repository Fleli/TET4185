
from ReadData.helpers import *

def find_params(frame, nodes, cols_x, flexible_demand, ces, cat):
    
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
    co2 = fill_initial(nodes, producers)
    prod_mc = fill_initial(nodes, producers)
    prod_cap = fill_initial(nodes, producers)
    cons_mc = fill_initial(nodes, consumers)
    cons_cap = fill_initial(nodes, consumers)
    
    # Fetch data from a column at a given y offset (table index). We add 2 to the offset since the first two rows are headers.
    def data(col, offset):
        return cell(frame, cols_x[col], offset + 2)
    
    # Fill actual production capacities, marginal costs, and CO2 emissions
    for i in range(len(producers)):
        p = producers[i]
        node = data("node prod", i)
        prod_mc[node, p] = data("mc prod", i)
        prod_cap[node, p] = data("cap prod", i)
        if ces or cat:
            co2[node, p] = data("co2", i)
    
    # Fill actual consumption capacities and marginal costs
    for i in range(len(consumers)):
        c = consumers[i]
        node = data("node cons", i)
        cons_mc[node, c] = data("mc cons", i) if flexible_demand else 0
        cons_cap[node, c] = data("cap cons", i)
    
    # Return the data we've found
    return producers, consumers, prod_mc, prod_cap, cons_mc, cons_cap, co2
