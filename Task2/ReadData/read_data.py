
import pandas as pd

from ReadData.nodes import *
from ReadData.lines import *
from ReadData.params import *
from ReadData.helpers import *

# Read input data from the Excel file handed out.
def read_data(context, flexible_demand, ces, cat):
    
    # Build a Pandas frame by reading the xlsx file.
    frame = pd.read_excel("Input/Problem 2 data.xlsx", context["SHEETNAME"])
    
    # Find nodes and prod/cons parameters (capacities and MCs)
    nodes = find_nodes(frame, context)
    producers, consumers, prod_mc, prod_cap, cons_mc, cons_cap, co2 = find_params(frame, nodes, context, flexible_demand, ces, cat)
    
    print(co2)
    
    # Find line information, including the lines themselves, their capacities, and susceptances B
    lines, line_capacities, line_susceptances = find_lines(frame, nodes, context)
    
    # We interpret NAN values as being willing to pay anything it takes, so we set the WTP extremely high
    for key, value in cons_mc.items():
        if value == "NAN":
            cons_mc[key] = 5000
    
    # Return a dictionary with all the data we've extracted
    return {
        "nodes": nodes,
        "lines": lines,
        "capacities": line_capacities,
        "susceptances": line_susceptances,
        "producers": producers,
        "consumers": consumers,
        "prod_mc": prod_mc,
        "prod_cap": prod_cap,
        "cons_mc": cons_mc,
        "cons_cap": cons_cap,
        "co2": co2
    }
