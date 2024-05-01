
import pyomo.environ as pyo

def set_model_constraints(model, flexible_demand, ces, cat):
    
    
    per_unit_base = 1
    
    
    # === FLOW ===
    
    
    # Minimum flow
    model.constraint_transfer_min = pyo.Constraint (model.nodes, model.nodes,
        rule = lambda model, node_a, node_b: (
            -model.trans_cap[node_a, node_b]
            <= model.susceptances[node_a, node_b] * ( model.deltas[node_a] - model.deltas[node_b] ) * per_unit_base
        )
    )
    
    # Maximum flow
    model.constraint_transfer_max = pyo.Constraint (model.nodes, model.nodes,
        rule = lambda model, node_a, node_b: (
            model.susceptances[node_a, node_b] * ( model.deltas[node_a] - model.deltas[node_b] ) * per_unit_base
            <= model.trans_cap[node_a, node_b]
        )
    )
    
    
    # === QUANTITIES ===
    
    
    # Each producer has a given maximum production quantity
    model.constraint_max_production = pyo.Constraint (model.nodes, model.producers,
        rule = lambda model, node, producer: (
            model.prod_q[node, producer] <= model.prod_cap[node, producer]
        )
    )
    
    # If demand is flexible, we enforce consumption <= maximum
    model.constraint_max_consumption = pyo.Constraint (model.nodes, model.consumers,
        rule = lambda model, node, consumer: (
            model.cons_q[node, consumer] <= model.cons_cap[node, consumer]
        )
    )
    
    
    # === ENERGY BALANCE ===
    
    
    # Enforce energy balance (production + net transfer = consumption)
    model.constraint_energy_balance = pyo.Constraint (model.nodes, 
        rule = lambda model, node: (
            (sum(model.cons_q[node, q] for q in model.consumers)
            - sum(model.prod_q[node, p] for p in model.producers)
            + sum(model.susceptances[node, other] * (model.deltas[node] - model.deltas[other]) * per_unit_base for other in model.nodes)
            ) * (1 if flexible_demand else -1)
            == 0
        )
    )
    
    
    # === ENVIRONMENTAL CONSIDERATIONS ===
    
    
    def constraint_ces(model):
        
        total = 0
        clean = 0
        
        for node in model.nodes:
            for producer in model.producers:
                prod = model.prod_q[node, producer]
                total += prod
                if model.co2[node, producer] == 0:
                    clean += prod
        
        return 0.2 * total - clean <= 0
    
    # Require 20% of produced energy to be zero-emission
    if ces:
        model.constraint_ces = pyo.Constraint(rule = constraint_ces)
        
        # Convenience variable that makes reading out total emissions easier
        model.emissions = pyo.Var(within = pyo.Reals)
        model.find_emissions = pyo.Constraint(
            rule = lambda model: (
                model.emissions == sum( model.prod_q[node, p] * model.co2[node, p] for node in model.nodes for p in model.producers )
            )
        )
    
    
    def constraint_cat(model):
        
        total = sum(
            model.prod_q[node, producer] * model.co2[node, producer]
                for producer in model.producers
                for node in model.nodes
        )
        
        return total <= 950_000
    
    # Require emissions less than 950 000 (the result from CES)
    if cat:
        model.constraint_cat = pyo.Constraint(rule = constraint_cat)
    
    
    # === OTHER CONSTRAINTS ===
    
    
    # Set the (deviation of the) first node to be the known, zero-valued bus.
    model.constraint_slack = pyo.Constraint(rule = lambda model: (
        model.deltas["Node 1"] == 0
    ))
    
    
    def _constraint_min_load(model, node, consumer):
        if model.cons_mc[node, consumer] == 0:
            return model.cons_q[node, consumer] >= model.cons_cap[node, consumer]
        return model.cons_q[node, consumer] >= 0
    
    model.constraint_required_load = pyo.Constraint(model.nodes, model.consumers, rule = _constraint_min_load)
    
    
    
