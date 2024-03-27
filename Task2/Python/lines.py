
def find_lines(frame, areas):
    
    # Column P in the Excel file
    col = 15
    
    lines = []
    line_capacities = {}
    line_susceptances = {}
    
    for y in range(2, len(frame)):
        
        # Split 'Line p-q' and fetch the 'p-q' part
        s = frame.iloc[y][15].split(" ")[1]
        
        # `to`, `from` node of the line
        p, q = s.split("-")
        
        # Capacity and susceptance are found to the right of the line names
        capacity = frame.iloc[y][col + 1]
        susceptance = frame.iloc[y][col + 2]
        
        lines.append((p, q))
        lines.append((q, p))
        
        line_capacities[p, q] = capacity
        line_capacities[q, p] = capacity
        
        line_susceptances[p, q] = susceptance
        line_susceptances[q, p] = susceptance
    
    return lines, line_capacities, line_susceptances
