
# ===== IMPORTS =====


import sys; sys.dont_write_bytecode = True

from read_data import *
import pyomo.environ as pyo


# ===== FETCH INPUT =====


# Read data from the Excel file
areas, lines, line_capacities, line_susceptances, producers, consumers, prod_cap, cons_cap, prod_mc = read_data()


# ===== MODEL INITIALIZATION =====


# Create the model
model = pyo.ConcreteModel()

# Initialize Sets for areas, lines, producers, and consumers
model.areas = pyo.Set(initialize = areas)
model.lines = pyo.Set(initialize = lines)
model.producers = pyo.Set(initialize = producers)
model.consumers = pyo.Set(initialize = consumers)

# Initialize Parameters (marginal costs and capacities)
model.trans_cap = pyo.Param(model.areas, model.areas, initialize = line_capacities)
model.cons_cap = pyo.Param(model.areas, model.consumers, initialize = cons_cap)
model.prod_cap = pyo.Param(model.areas, model.producers, initialize = prod_cap)
model.prod_mc = pyo.Param(model.areas, model.producers, initialize = prod_mc)

# Decision Variables
model.prod_q = pyo.Var(model.areas, model.producers, within = pyo.NonNegativeReals)
model.transfer = pyo.Var(model.areas, model.areas)


# ===== OBJECTIVE FUNCTION =====


# Objective function
model.objective = pyo.Objective (
    
    # We want to minimize the production costs
    rule = lambda model: sum (
        model.prod_q[a, p] * model.prod_mc[a, p]
            for a in model.areas
            for p in model.producers
    ),
    
    sense = pyo.minimize
    
)


# ===== CONSTRAINTS =====


# Verify that the transfer from node_a to node_b isn't too small
model.constraint_transfer_min = pyo.Constraint (
    
    model.areas, 
    model.areas, 
    
    # Transfer must be at least -T for transfer capacity T
    rule = lambda model, node_a, node_b: (
        -model.trans_cap[node_a, node_b] 
        <= model.transfer[node_a, node_b] 
    )
    
)


# Verify that the transfer from node_a to node_b isn't too small
model.constraint_transfer_max = pyo.Constraint (
    
    model.areas, 
    model.areas, 
    
    # Transfer must be maximum T for transfer capacity T
    rule = lambda model, node_a, node_b: (
        model.transfer[node_a, node_b] 
        <= model.trans_cap[node_a, node_b] 
    )
    
)


# If X flows P->Q, then -X flows Q->P
model.constraint_transfer_balance = pyo.Constraint(
    
    model.areas,
    model.areas,
    
    rule = lambda model, node_a, node_b: (
        model.transfer[node_a, node_b] == -model.transfer[node_b, node_a]
    )
    
)
