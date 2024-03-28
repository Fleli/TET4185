
import pandas as pd

from nodes import *
from lines import *
from params import *
from helpers import *
from connections import *

# Read input data from the Excel file handed out.
def read_data():
    
    # Build a Pandas frame by reading the xlsx file.
    frame = pd.read_excel("Input/Problem 2 data.xlsx", "Problem 2.2 - Base case")
    
    # Find nodes and prod/cons parameters (capacities and MCs)
    nodes = find_nodes(frame)
    producers, consumers, prod_mc, prod_cap, cons_cap = find_params(frame, nodes)
    
    # Find line information, including the lines themselves, their capacities, and susceptances B
    lines, line_capacities, line_susceptances = find_lines(frame, nodes)
    
    # Find connection matrix F
    connection_matrix = find_connection_matrix(nodes, lines, line_susceptances)
    
    # Return the values we've found
    return nodes, lines, line_capacities, line_susceptances, producers, consumers, prod_cap, cons_cap, prod_mc, connection_matrix
