
# ===== IMPORTS =====


from read_data import *
import pyomo.environ as pyo
from pyomo.opt import SolverFactory as Solvers


# ===== FETCH INPUT =====


# Read data from the Excel file
nodes, lines, line_capacities, line_susceptances, producers, consumers, prod_cap, cons_cap, prod_mc = read_data()

print(prod_cap)


# ===== MODEL INITIALIZATION =====


# Create the model
model = pyo.ConcreteModel()

# Initialize Sets for nodes, lines, producers, and consumers
model.nodes = pyo.Set(initialize = nodes)
model.lines = pyo.Set(initialize = lines)
model.producers = pyo.Set(initialize = producers)
model.consumers = pyo.Set(initialize = consumers)

# Initialize Parameters (marginal costs and capacities)
model.trans_cap = pyo.Param(model.nodes, model.nodes, initialize = line_capacities)
model.cons_cap = pyo.Param(model.nodes, model.consumers, initialize = cons_cap)
model.prod_cap = pyo.Param(model.nodes, model.producers, initialize = prod_cap)
model.prod_mc = pyo.Param(model.nodes, model.producers, initialize = prod_mc)

# Decision Variables
model.prod_q = pyo.Var(model.nodes, model.producers, within = pyo.NonNegativeReals)
model.transfer = pyo.Var(model.nodes, model.nodes)


# ===== OBJECTIVE FUNCTION =====


# Objective function: minimizing production costs
model.objective = pyo.Objective (sense = pyo.minimize,
    rule = lambda model: sum (
        model.prod_q[a, p] * model.prod_mc[a, p]
            for a in model.nodes
            for p in model.producers
    )
)


# ===== CONSTRAINTS =====


# Verify that the transfer from node_a to node_b isn't too small
model.constraint_transfer_min = pyo.Constraint (model.nodes, model.nodes, 
    rule = lambda model, node_a, node_b: (
        -model.trans_cap[node_a, node_b] 
        <= model.transfer[node_a, node_b] 
    )
)

# Verify that the transfer from node_a to node_b isn't too large
model.constraint_transfer_max = pyo.Constraint (model.nodes, model.nodes, 
    rule = lambda model, node_a, node_b: (
        model.transfer[node_a, node_b] 
        <= model.trans_cap[node_a, node_b] 
    )
)

# If X flows P->Q, then -X flows Q->P
model.constraint_transfer_balance = pyo.Constraint (model.nodes, model.nodes, 
    rule = lambda model, node_a, node_b: (
        model.transfer[node_a, node_b] == -model.transfer[node_b, node_a]
    )
)

# Each producer has a given maximum production quantity
model.constraint_max_production = pyo.Constraint (model.nodes, model.producers,
    rule = lambda model, node, producer: (
        model.prod_q[node, producer] <= prod_cap[node, producer]
    )
)

# Production must equal consumption.
def _constraint_energy_balance(model, node):
    
    # Find the total production, consumption and transfer to a given node
    prod = sum ( [ model.prod_q[node, prod] for prod in model.producers ] )
    cons = sum ( [ model.cons_cap[node, cons] for cons in model.consumers ] )
    trans = sum ( [ model.transfer[node, other] for other in model.nodes ] )
    
    # Production plus transfer (positive incoming) must equal consumption at all nodes
    return prod + trans == cons

model.constraint_energy_balance = pyo.Constraint(model.nodes, rule = _constraint_energy_balance)


# ===== SOLVING THE OPTIMIZATION PROBLEM =====


solver = Solvers("glpk")

results = solver.solve(model,load_solutions = True)
    
model.display()
