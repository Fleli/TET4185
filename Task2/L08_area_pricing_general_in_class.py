# -*- coding: utf-8 -*-
"""
Created on Thu Jan 25 12:49:11 2024

@author: kasperet
"""



#Imported packages
import pyomo.environ as pyo
from pyomo.opt import SolverFactory
import sys
"""
INPUT DATA MANAGEMENT, WHAT DO WE HAVE
"""

"""
How many consumers and producers exist
"""

Producers = ["Statkraft","Kinect","NTE"] + ["Leirfossen","HighIQ"]

Consumers = ["Tibber","AE","Agva"] +["TokTik"]

Areas = ["IN","OUT"]

#Producers_OUT = ["Leirfossen","HighIQ"]

#Consumers_OUT = ["TokTik"]

Tuple = ("Area1","Producer1")

#sys.exit()


"""
What is the production/demand quantity for each producer/consumer [MWh]
"""

Prod_capacity = {("IN","Statkraft"):200,
                 ("IN","Kinect"):400,
                 ("IN","NTE"):250,
                 ("OUT","Leirfossen"):400,
                 ("OUT","HighIQ"):400,
                 
                 ("OUT","Statkraft"):0,
                 ("OUT","Kinect"):0,
                 ("OUT","NTE"):0,
                 ("IN","Leirfossen"):0,
                 ("IN","HighIQ"):0
                 }

Cons_capacity = {("IN","Tibber"):350,
                 ("IN","AE"):300,
                 ("IN","Agva"):500,
                 ("OUT","TokTik"):600,
                 
                 ("OUT","Tibber"):0,
                 ("OUT","AE"):0,
                 ("OUT","Agva"):0,
                 ("IN","TokTik"):0
                                  
                 }


MC_prod = {("IN","Statkraft"):400,
                 ("IN","Kinect"):200,
                 ("IN","NTE"):700,
                 ("OUT","Leirfossen"):300,
                 ("OUT","HighIQ"):100,
                 
                 ("OUT","Statkraft"):0,
                 ("OUT","Kinect"):0,
                 ("OUT","NTE"):0,
                 ("IN","Leirfossen"):0,
                 ("IN","HighIQ"):0
                 }

MC_cons = {("IN","Tibber"):1000,
                 ("IN","AE"):600,
                 ("IN","Agva"):200,
                 ("OUT","TokTik"):1000,
                 
                 ("OUT","Tibber"):0,
                 ("OUT","AE"):0,
                 ("OUT","Agva"):0,
                 ("IN","TokTik"):0
                                  
                 }

# Prod_capacity_OUT = {"Leirfossen":400,
#                  "HighIQ":400}

# Cons_capacity_OUT = {"TokTik":600}


"""
What is the marginal price for production/consumption [NOK/MWh]
"""


# Prod_price_IN = {"Statkraft":400, "Kinect":200, "NTE":700}

# MC_cons_IN = {}
# MC_cons_IN["Tibber"] = 1000
# MC_cons_IN["AE"] = 600
# MC_cons_IN["Agva"] = 200

# Prod_price_OUT = {"Leirfossen":300, "HighIQ":100}

# MC_cons_OUT = {}
# MC_cons_OUT["TokTik"] = 1000

T_min = {("IN","IN"):0,
         ("IN","OUT"):-75,
         ("OUT","IN"):-75,
         ("OUT","OUT"):0}

T_max = {("IN","IN"):0,
         ("IN","OUT"):75,
         ("OUT","IN"):75,
         ("OUT","OUT"):0}


"""
Create the optimization problem
"""

"""
Define the model-variable
"""


model = pyo.ConcreteModel()


"""
Define the sets
"""


#How many consumers do we consider
model.Consumers_IN = pyo.Set(initialize = Consumers)


#How many producers do we consider
model.Producers_IN = pyo.Set(initialize = Producers)

model.Areas = pyo.Set(initialize = Areas)


# #How many consumers do we consider
# model.Consumers_OUT = pyo.Set(initialize = Consumers_OUT)


# #How many producers do we consider
# model.Producers_OUT = pyo.Set(initialize = Producers_OUT)


"""
Define the set-based parameters
"""

#A parameter dependent on multiple keys can be defined by saying it depends on a set with the same elements in the list as keys in a dictionary
#The parameter will then have multiple values, locked behind a key for each of them (similar to how dictionaries work!)

#Parameter for all prices set by the producers
model.Prod_price_IN = pyo.Param(model.Areas, model.Producers_IN, initialize = MC_prod)

#Parameter for all prices set by the consumer
model.Cons_price_IN = pyo.Param(model.Areas, model.Consumers_IN, initialize = MC_cons)

#Parameter for all production capacities for each producer
model.Prod_capacity_IN = pyo.Param(model.Areas, model.Producers_IN, initialize = Prod_capacity)

#Parameter for all consumption capacities for each consumer
model.Cons_capacity_IN = pyo.Param(model.Areas, model.Consumers_IN, initialize = Cons_capacity)

model.T_min = pyo.Param(model.Areas,model.Areas, initialize = T_min)
model.T_max = pyo.Param(model.Areas,model.Areas, initialize = T_max)


"""
Define the set-based variables
"""

#The only variables we have are how much each producer/consumer produces/consumes
# in a market clearing

#Thus, we have to create variables for each producer/consumer,
#using sets like for parameters

#What is the production quantity for each producer
model.producer_quantity_IN = pyo.Var(model.Areas,model.Producers_IN, within = pyo.NonNegativeReals)

#What is the consumption quantity for each consumer
model.consumer_quantity_IN = pyo.Var(model.Areas,model.Consumers_IN, within = pyo.NonNegativeReals)

model.T = pyo.Var(model.Areas, model.Areas)


"""
Define the objective function
"""

def OBJ(model):
    
    
    Production_cost = 0
    for a in model.Areas:
        for p in model.Producers_IN:
            Production_cost += model.producer_quantity_IN[a,p]*model.Prod_price_IN[a,p]
    
    Value_of_electricity = 0
    for a in model.Areas:
        for p in model.Consumers_IN:
            Value_of_electricity += model.consumer_quantity_IN[a,p]*model.Cons_price_IN[a,p]
    
    
    return(Value_of_electricity-Production_cost)
model.OBJ = pyo.Objective(rule = OBJ, sense = pyo.maximize)


"""
Define the constraints
"""

#Each producer has production limitation equal to capacity
def Prod_limit_IN(model,a,p):
    return(model.producer_quantity_IN[a,p] <= model.Prod_capacity_IN[a,p])
model.Prod_limit_IN_const = pyo.Constraint(model.Areas, model.Producers_IN, rule = Prod_limit_IN)

#Each consumer has consumer limitation equal to capacity
def Cons_limit_IN(model,a,c):
    return(model.consumer_quantity_IN[a,c] <= model.Cons_capacity_IN[a,c])
model.Cons_limit_IN_const = pyo.Constraint(model.Areas, model.Consumers_IN, rule = Cons_limit_IN)

#Production must equal consumption
def Energy_balance_IN(model,a):
    Production = sum(model.producer_quantity_IN[a,p] for p in model.Producers_IN) 
    Consumption = sum(model.consumer_quantity_IN[a,c] for c in model.Consumers_IN)
    
    Transfer = sum(model.T[a,a2] for a2 in model.Areas)
    
    return(Production + Transfer == Consumption)
model.Energy_balance_IN_const = pyo.Constraint(model.Areas, rule = Energy_balance_IN)


def Lower_T(model,a,a2):
    return(model.T_min[a,a2] <= model.T[a,a2])
model.Lower_T_constraint = pyo.Constraint(model.Areas, model.Areas, rule = Lower_T)

def Upper_T(model,a,a2):
    return(model.T_max[a,a2] >= model.T[a,a2])
model.Upper_T_constraint = pyo.Constraint(model.Areas, model.Areas, rule = Upper_T)

def Transfer_couple(model,a,a2):
    return(model.T[a,a2] == -model.T[a2,a])
model.C = pyo.Constraint(model.Areas, model.Areas, rule = Transfer_couple)


#Define solver
opt = SolverFactory("glpk")


#Enable extraction of dual solution
model.dual = pyo.Suffix(direction=pyo.Suffix.IMPORT)

"""
Solve the problem
"""

results = opt.solve(model,load_solutions = True)
    
model.display()
model.dual.display()












