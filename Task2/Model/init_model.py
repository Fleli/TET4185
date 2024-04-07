
import pyomo.environ as pyo

def init_model(data: dict, flexible_demand: bool, co2_emissions: bool):
    
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
    
    # Decision Variables
    model.prod_q = pyo.Var(model.nodes, model.producers, within = pyo.NonNegativeReals)
    model.cons_q = pyo.Var(model.nodes, model.consumers, within = pyo.NonNegativeReals)
    model.transfer = pyo.Var(model.nodes, model.nodes)
    model.deltas = pyo.Var(model.nodes)
    
    # Optionally include additional parameters and variables if demand is flexible
    if flexible_demand:
        model.cons_mc = pyo.Param(model.nodes, model.consumers, initialize = data["cons_mc"])
    
    # Optionally include the CO2 emissions as a parameter
    if co2_emissions:
        model.co2 = pyo.Param(model.nodes, model.producers, initialize = data["co2"])
    
    return model
    