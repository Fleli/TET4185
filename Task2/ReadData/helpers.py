
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
def build_x(argv):
    
    x = { }
    
    task = int(argv[1])
    
    match task:
        case 2:
            x["SHEETNAME"] = "Problem 2.2 - Base case"
        case 3:
            x["SHEETNAME"] = "Problem 2.3 - Generators"
        case 4:
            x["SHEETNAME"] = "Problem 2.4 - Loads"
        case 5:
            x["SHEETNAME"] = "Problem 2.5 - Environmental"
        case _:
            print("Unrecognized task number", task)
            exit(1)
    
    flexible_demand = (task >= 4)
    include_CO2_column = (task == 5)
    
    # Start index of 0
    index = 0
    
    # Find index for each of the generation related columns
    for name in ["name prod", "cap prod", "mc prod", "node prod"] + ( ["co2"] if include_CO2_column else [] ) + ["slack prod"]:
        x[name] = index
        index += 1
    
    # ... then 4 blank spaces
    index += 4
    
    # ... then consumer (load) data
    for name in ["name cons", "cap cons"] + ( ["mc cons"] if flexible_demand else [] ) + ["node cons"]:
        x[name] = index
        index += 1
    
    # ... then 2 or 3 blank spaces (see the Excel file)
    index += (2 if (task == 4) else 3)
    
    # ... then line information (names, capacities and susceptances)
    for name in ["lines", "capacities", "susceptances"]:
        x[name] = index
        index += 1
    
    print()
    print("x =")
    for it in x.items():
        print(" ", it)
    print()
    
    return x, flexible_demand, include_CO2_column
