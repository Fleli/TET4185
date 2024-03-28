
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
