
def find_nodes(frame, cols_x):
    
    node_set = set()
    
    for y in range(len(frame)):
        row = frame.iloc[y]
        for x in [ cols_x["node prod"], cols_x["node cons"] ]:
            cell = row.iloc[x]
            if (type(cell) == str) and (cell.startswith("Node ")):
                node_set.add(cell)
    
    return list(node_set)
