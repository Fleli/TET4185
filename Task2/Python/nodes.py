
def find_nodes(frame):
    
    node_set = set()
    
    for y in range(len(frame)):
        row = frame.iloc[y]
        for x in [3, 11]:
            cell = row.iloc[x]
            if (type(cell) == str) and (cell.startswith("Node ")):
                node_set.add(cell)
    
    return list(node_set)
