import gurobipy as gp
from gurobipy import GRB


# define the model
def init_first_problem_relaxation(facilities_opening_costs, transportation_costs, capacities, demands, lamb):
    # there variables are the number of the two type of decision variables
    num_facilities = len(facilities_opening_costs)
    num_customers = len(transportation_costs)
    model = gp.Model('SSCFL')
    # add the variables to the model
    x = model.addVars(num_facilities, vtype=GRB.BINARY, name='x')
    y = model.addVars(num_facilities, num_customers, vtype=GRB.BINARY, name='y')
    # add the constraint
    model.addConstrs((gp.quicksum(y[(u, v)] for u in range(num_facilities)) == 1 for v in range(num_customers)),
                     name="first_constraint")
    model.setObjective(gp.quicksum(facilities_opening_costs[u] +
                       lamb[u]*capacities[u]*x[u] for u in range(num_facilities)) +
                       gp.quicksum(transportation_costs[v][u] + lamb[u] * demands[v] for u in range(num_facilities)
                                   for v in range(num_customers)))
    model.optimize()


# only for test
if __name__ == '__main__':
    init_first_problem_relaxation([2, 1, 1, 3], [[4, 8, 12, 5], [2, 5, 1, 3]], [7, 2, 1, 2], [3, 1], [1, 2, 3, 4])
