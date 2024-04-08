
import sys as Process
Process.dont_write_bytecode = True

print(Process.path)

from ReadData.helpers import *
from ReadData.read_data import *

from Model.init_model import *
from Model.set_objective import *
from Model.set_constraints import *
from Model.solve import *

# Build a dictionary of x coordinates
cols_x, flexible_demand, ces, cat = build_x(Process.argv)

# Read data from the Excel file
data = read_data(cols_x, flexible_demand, ces, cat)

# Initialize the model with its sets, parameters and variables
model = init_model(data, flexible_demand, ces, cat)

# Set the model's objective function
set_model_objective(model, flexible_demand)

# Set the model's constraints
set_model_constraints(model, flexible_demand, ces, cat)

# Solve the model
solve_model(model)
