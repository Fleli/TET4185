
from ReadData.helpers import *

def find_lines(frame, nodes, cols_x):
    
    # Initialize everything with blank data
    lines = []
    line_capacities = fill_initial(nodes, nodes)
    line_susceptances = fill_initial(nodes, nodes)
    
    # Find all node pairs
    for n1 in nodes:
        for n2 in nodes:
            lines.append((n1, n2))
    
    # Go through each line
    for y in range(2, len(frame)):
        
        # Find the value of the cell
        data = cell(frame, cols_x["lines"], y)
        
        # There's no line here if the data isn't a string.
        if (not type(data) == str):
            continue
        
        # Split 'Line p-q' and fetch the 'p-q' part
        s = data.split(" ")[1]
        
        # `to`, `from` node of the line
        p, q = s.split("-")
        
        # Node `x` is named `Node x`, by my own convention ...
        p = "Node " + p
        q = "Node " + q
        
        # Capacity and susceptance are found to the right of the line names
        capacity = frame.iloc[y].iloc[cols_x["capacities"]]
        susceptance = frame.iloc[y].iloc[cols_x["susceptances"]]
        
        # The line has the same capacity in both directions
        line_capacities[p, q] = capacity
        line_capacities[q, p] = capacity
        
        # ... and the same susceptance in both directions
        line_susceptances[p, q] = susceptance
        line_susceptances[q, p] = susceptance
    
    # Diagonal values are the positive sum of the (rest of) the corresponding row in the susceptance matrix
    for node in nodes:
        pos_sum = 0
        for other in nodes:
            if node == other:
                continue
            pos_sum -= line_susceptances[node, other]
        line_susceptances[node, node] = pos_sum
    
    # Return the line data we've found
    return lines, line_capacities, line_susceptances
