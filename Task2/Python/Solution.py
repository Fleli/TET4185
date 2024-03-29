
# ===== IMPORTS =====


import sys
from helpers import *
from read_data import *
import pyomo.environ as pyo
from pyomo.opt import SolverFactory as Solvers


# ===== FETCH INPUT =====


# Build a dictionary of x coordinates
cols_x, flexible_demand, co2_emissions = build_x(sys.argv)

# Read data from the Excel file
nodes, lines, line_capacities, line_susceptances, producers, consumers, prod_mc, prod_cap, cons_mc, cons_cap = read_data(cols_x, flexible_demand, co2_emissions)

# We interpret NAN values as being willing to pay anything it takes, so we set the WTP extremely high
for key, value in cons_mc.items():
    if value == "NAN":
        cons_mc[key] = 100000

print(flexible_demand)

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

# Optionally include additional parameters and variables if demand is flexible
if flexible_demand:
    model.cons_mc = pyo.Param(model.nodes, model.consumers, initialize = cons_mc)
    model.cons_q = pyo.Var(model.nodes, model.consumers, within = pyo.NonNegativeReals)


# ===== OBJECTIVE FUNCTION =====


def _objective_maximizeSocialWelfare(model):
    
    consumer_value = sum (
        model.cons_mc[node, c] * model.cons_q[node, c]
            for c in model.consumers
            for node in model.nodes
    )
    
    producer_costs = sum (
        model.prod_mc[node, p] * model.prod_q[node, p]
            for p in model.producers
            for node in model.nodes
    )
    
    return consumer_value - producer_costs


def _objective_minimizeGenerationCosts(model):
    return sum (
        model.prod_q[node, p] * model.prod_mc[node, p] 
            for p in model.producers
            for node in model.nodes
    )


# Which objective function we choose (and whether to maximize or minimize) depends
# on the problem we're solving.
model.objective = pyo.Objective (
    sense = pyo.maximize,
    rule = _objective_maximizeSocialWelfare
) if flexible_demand else pyo.Objective (
    sense = pyo.minimize,
    rule = _objective_minimizeGenerationCosts
)


# ===== CONSTRAINTS =====


# Minimum flow
model.constraint_transfer_min = pyo.Constraint (model.nodes, model.nodes,
    rule = lambda model, node_a, node_b: (
        -model.trans_cap[node_a, node_b]
        <= model.transfer[node_a, node_b]
    )
)

# Maximum flow
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
        model.prod_q[node, producer] <= model.prod_cap[node, producer]
    )
)

# Require flow A->B be equal to susceptance A->B times difference in bus phase angles
model.constraint_flow = pyo.Constraint (model.nodes, model.nodes,
    rule = lambda model, node_a, node_b: (
        model.transfer[node_a, node_b] == model.susceptances[node_a, node_b] * ( model.deltas[node_a] - model.deltas[node_b] )
    )
)

# Enforce energy balance (production + net transfer = consumption)
model.constraint_energy_balance = pyo.Constraint (model.nodes, 
    rule = lambda model, node: (
        sum(model.prod_q[node, p] for p in model.producers)                                         # Local production
        + sum(model.susceptances[node, other] * model.deltas[other] for other in model.nodes)       # + Transfer (into)
        == (                                                                                        # = Consumption
            sum(model.cons_q[node, q] for q in model.consumers)
            if flexible_demand else                                                                 # Either fixed or flexible consumption
            sum(model.cons_cap[node, q] for q in model.consumers)
        )
    )
)

if flexible_demand:
    model.constraint_max_consumption = pyo.Constraint (model.nodes, model.consumers,
        rule = lambda model, node, consumer: (
            model.cons_q[node, consumer] <= model.cons_cap[node, consumer]
        )
    )

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
