
# Helper method to fill an empty (2D) dictionary with "blank" data
def fill_initial(a, b):
    return {
        (an, bn): 0
            for an in a
            for bn in b
    }


# Fetch the data in the cell with coordinates (x, y) in the given frame.
def cell(data, x, y):
    return data.iloc[y].iloc[x]


# Build a dictionary of column name -> x coodinate based on argv
def build_x(argv: list[str]) -> dict[str, int]:
    
    x = {
        
        "name prod": 0,
        "cap prod": 1,
        "mc prod": 2,
        "node prod": 3,
        
        "name cons": 9,
        "cap cons": 10,
        "mc cons": 11,
        "node cons": 11,
        
        "lines": 15,
        "capacities": 16,
        "susceptances": 17
        
    }
    
    task = int(argv[1])
    
    flexible_demand = (task >= 4)
    include_CO2_column = (task == 5)
    
    if flexible_demand:
        x["node cons"] += 1
    
    return x
