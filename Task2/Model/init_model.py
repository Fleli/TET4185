
import pyomo.environ as pyo

# Note regarding some dual values:
# I've decided to store marginal costs in dictionaries with [node, producer] as key and mc as value. An
# artifact of this design is that some dual values, for example that of constraint_max_production[Node 1, Gen 2],
# appear when solving the model. However, these have no practical interpretation, since Gen 2 isn't located at Node 1.
# The reason its value is (e.g.) -300 when solving T=2, is that the solver thinks [Node 1, Gen 2] could produce at MC = 0
# instead of [Node 1, Gen 1] at MC = 300, had it only had the capacity.

# This function initializes and returns a concrete model with the given data.
def init_model(data: dict, ces: bool, cat: bool):
    
    # Create the model
    model = pyo.ConcreteModel()
    
    # Initialize Sets for nodes, lines, producers, and consumers
    model.nodes = pyo.Set(initialize = data["nodes"])
    model.lines = pyo.Set(initialize = data["lines"])
    model.producers = pyo.Set(initialize = data["producers"])
    model.consumers = pyo.Set(initialize = data["consumers"])
    
    # Initialize Parameters (marginal costs and capacities)
    model.susceptances = pyo.Param(model.nodes, model.nodes, initialize = data["susceptances"])
    model.trans_cap = pyo.Param(model.nodes, model.nodes, initialize = data["capacities"])
    model.cons_cap = pyo.Param(model.nodes, model.consumers, initialize = data["cons_cap"])
    model.prod_cap = pyo.Param(model.nodes, model.producers, initialize = data["prod_cap"])
    model.prod_mc = pyo.Param(model.nodes, model.producers, initialize = data["prod_mc"])
    model.cons_mc = pyo.Param(model.nodes, model.consumers, initialize = data["cons_mc"])
    
    # Decision Variables
    model.prod_q = pyo.Var(model.nodes, model.producers, within = pyo.NonNegativeReals)
    model.cons_q = pyo.Var(model.nodes, model.consumers, within = pyo.NonNegativeReals)
    model.deltas = pyo.Var(model.nodes)
    
    # Optionally include the CO2 emissions as a parameter if we're in CES or CAT mode
    # (Clean energy standard or Cap-and-trade)
    if ces or cat:
        model.co2 = pyo.Param(model.nodes, model.producers, initialize = data["co2"])
    
    return model
    