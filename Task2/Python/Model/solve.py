
import pyomo.environ as pyo
from pyomo.opt import SolverFactory as Solvers

def solve_model(model):
    
    # Define the model's dual values
    model.dual = pyo.Suffix(direction = pyo.Suffix.IMPORT)
    
    # Solve the model and load solutions
    Solvers("glpk").solve(model, load_solutions = True)
    
    # Display the results, including dual values
    model.display()
    model.dual.display()
