
# ===== IMPORTS =====


from read_data import *
import pyomo.environ as pyo


# ===== FETCH INPUT =====


# Read data from the Excel file
areas, lines, producers, consumers, prod_cap, cons_cap, prod_mc = read_data()


# ===== MODEL INITIALIZATION =====


# Create the model
model = pyo.ConcreteModel()

# Initialize Sets for areas, lines, producers, and consumers
model.areas = pyo.Set(areas)
model.lines = pyo.Set(lines)
model.producers = pyo.Set(initialize = producers)
model.consumers = pyo.Set(initialize = consumers)

# Initialize Parameters (marginal costs and capacities)
model.cons_cap = pyo.Param(model.areas, model.consumers, initialize = cons_cap)
model.prod_cap = pyo.Param(model.areas, model.producers, initialize = prod_cap)
model.prod_mc = pyo.Param(model.areas, model.producers, initialize = prod_mc)

# Decision Variables
model.prod_q = pyo.Var(model.areas, model.Producers, within = pyo.NonNegativeReals)
model.transfer = pyo.Var(model.areas, model.areas)


# ===== OBJECTIVE FUNCTION =====


# Objective function
model.objective = pyo.Objective(
    
    rule = lambda model: sum (
        model.prod_q[a, p] * model.prod_mc[a, p]
        for a in model.areas
        for p in model.producers
    ),
    
    sense = pyo.minimize
    
)


# ===== CONSTRAINTS =====


