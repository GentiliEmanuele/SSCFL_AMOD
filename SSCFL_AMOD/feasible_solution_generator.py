import random


def generator(problem_instance):
    x = [1 for i in range(problem_instance.num_facilities)]
    y = [[0 for i in range(problem_instance.num_customers)] for j in range(problem_instance.num_facilities)]
    available = list(range(0, problem_instance.num_customers))
    while not cond(problem_instance, y) and available:
        for u in range(problem_instance.num_facilities):
            # choose casually one customer
            if available:
                v = random.choice(available)
                available.remove(v)
                y[u][v] = 1
                if (sum(y[u][v] * problem_instance.demands[v] for v in range(problem_instance.num_customers))
                        > x[u] * problem_instance.capacities[u]):
                    y[u][v] = 0
    return (sum(x[u] * problem_instance.facilities_opening_costs[u] for u in range(problem_instance.num_facilities)) +
            sum(y[u][v] * problem_instance.transportation_costs[u][v]
                for u in range(problem_instance.num_facilities) for v in range(problem_instance.num_customers)))


def cond(problem_instance, y):
    for v in range(problem_instance.num_customers):
        if sum(y[u][v] for u in range(problem_instance.num_facilities)) < 1:
            return False
    return True


def generate(problem_instance, num_solutions):
    values = []
    for i in range(num_solutions):
        values.append(generator(problem_instance))
    return min(values)
