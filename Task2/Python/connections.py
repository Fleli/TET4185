
def find_connection_matrix(nodes, lines, line_susceptances):
    
    matrix = {}
    
    for line in lines:
        l0 = line[0]
        l1 = line[1]
        for node in nodes:
            b_ij = line_susceptances[ line[0], line[1] ]
            value = 0
            if node == line[0]:
                value = abs(b_ij)
            elif node == line[1]:
                value = -abs(b_ij)
            matrix[l0, l1, node] = value
    
    return matrix
