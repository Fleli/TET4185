
import pyomo.environ as pyo

def set_model_constraints(model, flexible_demand):
    
    
    per_unit_base = 100
    
    
    # === FLOW ===
    
    
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
    
    
    
    # === QUANTITY LIMITS ===
    
    
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
    
    
    # === FLOW-SUSCEPTANCE-PHASE RELATIONSHIP ===
    
    
    # Require flow A->B be equal to susceptance A->B times difference in bus phase angles
    model.constraint_flow = pyo.Constraint (model.nodes, model.nodes,
        rule = lambda model, node_a, node_b: (
            model.transfer[node_a, node_b] == model.susceptances[node_a, node_b] * ( model.deltas[node_a] - model.deltas[node_b] ) * per_unit_base
        )
    )
    
    
    # === ENERGY BALANCE ===
    
    
    # Enforce energy balance (production + net transfer = consumption)
    model.constraint_energy_balance = pyo.Constraint (model.nodes, 
        rule = lambda model, node: (
            sum(model.prod_q[node, p] for p in model.producers)                                                         # Local production
            + sum(model.susceptances[node, other] * model.deltas[other] * per_unit_base for other in model.nodes)       # + Transfer
            == sum( model.cons_q[node, q] for q in model.consumers)                                                     # = Consumption
        )
    )
    
    
    # === OTHER CONSTRAINTS ===
    
    
    # Set the (deviation of the) first node to be the known, zero-valued bus.
    model.ccc = pyo.Constraint(rule = lambda model: (
        model.deltas["Node 1"] == 0
    ))
    
    # If demand is inflexible, consumption equals capacity at all load entities
    if not flexible_demand:
        model.constraint_full_load_capacity = pyo.Constraint (model.nodes, model.consumers,
            rule = lambda model, node, consumer: (
                model.cons_q[node, consumer] == model.cons_cap[node, consumer]
            )
        )
