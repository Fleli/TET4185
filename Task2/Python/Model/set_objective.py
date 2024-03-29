
import pyomo.environ as pyo

def set_model_objective(model, flexible_demand):
    
    # Which objective function we choose (and whether to maximize or minimize) depends
    # on the problem we're solving (is the demand flexible or not?)
    model.objective = pyo.Objective (
        sense = pyo.maximize,
        rule = _objective_maximizeSocialWelfare
    ) if flexible_demand else pyo.Objective (
        sense = pyo.minimize,
        rule = _objective_minimizeGenerationCosts
    )


# This is the objective function used if demand is flexible.
# Then, we want to maximize social welfare.
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


# If instead demand is inflexible (2.2 and 2.3), then
# our goal is just to minimize generation costs
def _objective_minimizeGenerationCosts(model):
    return sum (
        model.prod_q[node, p] * model.prod_mc[node, p] 
            for p in model.producers
            for node in model.nodes
    )
