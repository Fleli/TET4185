
# ===== IMPORTS =====


from read_data import *
import pyomo.environ as pyo
from pyomo.opt import SolverFactory as Solvers


# ===== FETCH INPUT =====


# Read data from the Excel file
nodes, lines, line_capacities, line_susceptances, producers, consumers, prod_cap, cons_cap, prod_mc = read_data()


# ===== MODEL INITIALIZATION =====


# Create the model
model = pyo.ConcreteModel()

# Initialize Sets for nodes, lines, producers, and consumers
model.nodes = pyo.Set(initialize = nodes)
model.lines = pyo.Set(initialize = lines)
model.producers = pyo.Set(initialize = producers)
model.consumers = pyo.Set(initialize = consumers)

# Initialize Parameters (marginal costs and capacities)
model.susceptances = pyo.Param(model.nodes, model.nodes, initialize = line_susceptances)
model.trans_cap = pyo.Param(model.nodes, model.nodes, initialize = line_capacities)
model.cons_cap = pyo.Param(model.nodes, model.consumers, initialize = cons_cap)
model.prod_cap = pyo.Param(model.nodes, model.producers, initialize = prod_cap)
model.prod_mc = pyo.Param(model.nodes, model.producers, initialize = prod_mc)

# Decision Variables
model.prod_q = pyo.Var(model.nodes, model.producers, within = pyo.NonNegativeReals)
model.transfer = pyo.Var(model.nodes, model.nodes)
model.deltas = pyo.Var(model.nodes)


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


# Minimum flow
model.constraint_transfer_min = pyo.Constraint (
    
    model.nodes, 
    model.nodes,
    
    rule = lambda model, node_a, node_b: (
        -model.trans_cap[node_a, node_b]
        <= model.transfer[node_a, node_b]
    )
    
)

# Maximum flow
model.constraint_transfer_max = pyo.Constraint (
    
    model.nodes,
    model.nodes,
    
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
        model.prod_q[node, producer] <= model.prod_cap[node, producer]
    )
)

# Require flow A->B be equal to susceptance A->B times difference in bus phase angles
model.constraint_flow = pyo.Constraint (model.nodes, model.nodes,
    rule = lambda model, node_a, node_b: (
        model.transfer[node_a, node_b] == model.susceptances[node_a, node_b] * ( model.deltas[node_a] - model.deltas[node_b] )
    )
)

# Enforce the power flow equations P - D = B * delta
def _constraint_energy_balance(model, node):
    
    pN = sum ( model.prod_q[node, p] for p in model.producers )
    qN = sum ( model.cons_cap[node, q] for q in model.consumers )
    
    result = sum ( model.susceptances[node, other] * model.deltas[other] for other in model.nodes )
    
    return pN + result == qN

model.constraint_energy_balance = pyo.Constraint(model.nodes, rule = _constraint_energy_balance)

# Set the (deviation of the) first node to be the known, zero-valued bus.
model.ccc = pyo.Constraint(rule = lambda model: (
    model.deltas["Node 1"] == 0
))


# ===== SOLVING THE OPTIMIZATION PROBLEM =====


# Solve the model, including dual values
model.dual = pyo.Suffix(direction = pyo.Suffix.IMPORT)
results = Solvers("glpk").solve(model, load_solutions = True)

# Display the results
model.display()
model.dual.display()
