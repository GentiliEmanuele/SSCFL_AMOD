import gurobipy as gp
from gurobipy import GRB


def init_original_problem(problem_instance):
    # unpack the object problem_instance
    facilities_opening_costs = problem_instance.facilities_opening_costs
    transportation_costs = problem_instance.transportation_costs
    capacities = problem_instance.capacities
    demands = problem_instance.demands
    num_facilities = len(facilities_opening_costs)
    num_customers = len(transportation_costs)
    model = gp.Model('sscfl')
    # add the variables to the model
    x = model.addVars(num_facilities, vtype=GRB.BINARY, name='x')
    y = model.addVars(num_facilities, num_customers, vtype=GRB.BINARY, name='y')
    model.addConstrs((gp.quicksum(y[(u, v)] for u in range(num_facilities)) == 1 for v in range(num_customers)),
                     name="first_constraints")
    model.addConstrs((gp.quicksum(y[(u, v)] * demands[v] for v in range(num_customers)) <= x[u] * capacities[u]
                     for u in range(num_facilities)), name="second_constraints")
    model.setObjective(gp.quicksum(x[u] * facilities_opening_costs[u] for u in range(num_facilities)) +
                       gp.quicksum(y[(u, v)] * demands[v] * transportation_costs[v][u] for u in range(num_facilities)
                       for v in range(num_customers)), sense=GRB.MINIMIZE)
    return model


# define the first lagrangian relaxation (relaxation of the second constraints)
def init_first_problem_relaxation(problem_instance, lamb):
    # unpack the object problem_instance
    facilities_opening_costs = problem_instance.facilities_opening_costs
    transportation_costs = problem_instance.transportation_costs
    capacities = problem_instance.capacities
    demands = problem_instance.demands
    # there variables are the number of the two type of decision variables
    num_facilities = len(facilities_opening_costs)
    num_customers = len(transportation_costs)
    model = gp.Model('first_lagrangian_relaxation')
    # add the variables to the model
    x = model.addVars(num_facilities, vtype=GRB.BINARY, name='x')
    y = model.addVars(num_facilities, num_customers, vtype=GRB.BINARY, name='y')
    # add the constraints
    model.addConstrs((gp.quicksum(y[(u, v)] for u in range(num_facilities)) == 1 for v in range(num_customers)),
                     name="first_constraints")
    model.setObjective(gp.quicksum(facilities_opening_costs[u] -
                       lamb[u]*capacities[u]*x[u] for u in range(num_facilities)) +
                       gp.quicksum((transportation_costs[v][u] * demands[v] + lamb[u] * demands[v])*y[(u, v)]
                                   for u in range(num_facilities)
                                   for v in range(num_customers)), sense=GRB.MINIMIZE)
    return model


# define the second relaxation (relaxation of the first constraints)
def init_second_problem_relaxation(problem_instance, mu):
    # unpack the object problem instance
    facilities_opening_costs = problem_instance.facilities_opening_costs
    transportation_costs = problem_instance.transportation_costs
    capacities = problem_instance.capacities
    demands = problem_instance.demands
    num_facilities = len(facilities_opening_costs)
    num_customers = len(transportation_costs)
    model = gp.Model('second_lagrangian_relaxation')
    # add the variables to the model
    x = model.addVars(num_facilities, vtype=GRB.BINARY, name='x')
    y = model.addVars(num_facilities, num_customers, vtype=GRB.BINARY, name='y')
    # add the constraints
    model.addConstrs((gp.quicksum(y[(u, v)] * demands[v] for v in range(num_customers)) <= x[u] * capacities[u]
                      for u in range(num_facilities)), name="second_constraints")
    model.setObjective(gp.quicksum(facilities_opening_costs[u] * x[u] for u in range(num_facilities)) +
                       gp.quicksum((transportation_costs[v][u] * demands[v] - mu[v]) * y[(u, v)]
                                   for u in range(num_facilities) for v in range(num_customers)) +
                       gp.quicksum(mu[v] for v in range(num_customers)), sense=GRB.MINIMIZE)
    return model
