def print_solution(model):
    for var in model.getVars():
        print(f"{var.varName} = {var.x}")


def is_feasible(problem_instance, x, y):
    feasibility = True
    for v in range(problem_instance.num_customers):
        if sum(y[u][v] for u in range(problem_instance.num_facilities)) != 1:
            feasibility = False
            break
    for u in range(problem_instance.num_facilities):
        total_demands = sum(y[u][v] * problem_instance.demands[v] for v in range(problem_instance.num_customers))
        if total_demands > problem_instance.capacities[u] * x[u]:
            feasibility = False
            break
    return feasibility


def verbose_is_feasible(problem_instance, x, y):
    feasibility = True
    for v in range(problem_instance.num_customers):
        if sum(y[u][v] for u in range(problem_instance.num_facilities)) != 1:
            feasibility = False
            print(f"Assignment constraint has been violated {v}")
    for u in range(problem_instance.num_facilities):
        total_demands = sum(y[u][v] * problem_instance.demands[v] for v in range(problem_instance.num_customers))
        if total_demands > problem_instance.capacities[u] * x[u]:
            feasibility = False
            print("Capacity constraint has been violated")
            break
    return feasibility


def obj_value(problem_instance, x, y):
    return (sum(x[u] * problem_instance.facilities_opening_costs[u] for u in range(problem_instance.num_facilities)) +
            sum(y[u][v] * problem_instance.transportation_costs[u][v]
                for u in range(problem_instance.num_facilities) for v in range(problem_instance.num_customers)))
