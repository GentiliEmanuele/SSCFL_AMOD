import models_utils as mu


def initial_add_heuristic(problem_instance, x, y):
    # Step 0: start with K = [] and set Z_u = inf
    k = []
    z_u = float("inf")
    # Step 1: foreach facility i not in k compute and estimate R_i of the saving that would result if i were added to K
    w = [[0 for _ in range(problem_instance.num_customers)] for _ in range(problem_instance.num_facilities)]
    omega = [0 for _ in range(problem_instance.num_customers)]
    r = [0 for _ in range(problem_instance.num_facilities)]
    j_list = [[j, 0] for j in range(problem_instance.num_customers)]
    prohibit_k = []
    while True:
        for i in range(problem_instance.num_facilities):
            if i not in k and len(k) != 0:
                for j in range(problem_instance.num_customers):
                    w[i][j] = max(compute_min(problem_instance, i, j, k), 0)
                omega[i] = sum(w[i][j] for j in range(problem_instance.num_customers))
                r[i] = omega[i] * min(problem_instance.capacities[i] /
                                      sum(problem_instance.demands[j] for j in range(problem_instance.num_customers)
                                          if w[i][j] > 0), 1) - problem_instance.facilities_opening_costs[i]
        # Step 2: open facility i' that achieves the maximum R_i for i not in K and add i' to K
        max_r = max(x for x in r if r.index(x) not in k)
        i_p = r.index(max_r)
        x[i_p] = 1
        if i_p not in prohibit_k and i_p not in k:
            k.append(i_p)
        # Step 3: if sum(capacities[i] i in K) < sum(demands[j] j in range(num_customers) return to step 1. Otherwise
        # continue
        if sum(problem_instance.capacities[i] for i in k) >= sum(
                problem_instance.demands[j] for j in range(problem_instance.num_customers)):
            # Step 4: foreach customer j, computer the cost differential between its best and second-best assignment
            # in K. Order j in order to decrease cos differential
            for j in range(problem_instance.num_customers):
                if len(k) != 0:
                    first_best = compute_minus_on_column(problem_instance, j, float("inf"), k)
                    second_best = compute_minus_on_column(problem_instance, j, first_best, k)
                    j_list[j][1] = first_best - second_best
            j_list_sorted = sorted(j_list, key=lambda j_elem: j_elem[1], reverse=True)
            # Step 5: foreach j in order assign it to the open facility with minimum assignment cost among those with
            # sufficient capacity. If for some j, no feasible assignment is possible, return to step 1. Otherwise
            # continue
            count_feasible = 0
            for j in j_list_sorted:
                feasible = []
                for i in k:
                    if ((sum(y[i][a] * problem_instance.demands[a] for a in range(problem_instance.num_customers)) +
                         problem_instance.demands[j[0]] <= problem_instance.capacities[i] * x[i]) and
                            sum(y[b][j[0]] for b in range(problem_instance.num_facilities))
                            == 0):
                        feasible.append(i)
                        count_feasible += 1
                if len(feasible) != 0:
                    index = find_min_index(problem_instance, j[0], feasible)
                    y[index][j[0]] = 1
            if count_feasible != 0:
                # Step 6: any facility with no customers assigned to it should be removed from K and not be
                # re-entered in future iterations. If the total cost TC of the last feasible solution found is less
                # than z_u, set z_u = TC and return to step (1). Otherwise stop
                for i in range(problem_instance.num_facilities):
                    if i in k and sum(y[i][j] for j in range(problem_instance.num_customers)) == 0:
                        k.remove(i)
                        prohibit_k.append(i)
                obj_val = mu.obj_value(problem_instance, x, y)
                if obj_val < z_u and mu.is_feasible(problem_instance, x, y):
                    z_u = obj_val
                    break
                else:
                    if mu.is_feasible(problem_instance, x, y):
                        break
    return x, y, z_u, k


def final_adjustment_heuristic(problem_instance, best_x, best_y, k):
    customers_list = [[j, 0] for j in range(problem_instance.num_customers)]
    for j in range(problem_instance.num_customers):
        if len(k) != 0:
            first_best = compute_minus_on_column(problem_instance, j, float("inf"), k)
            second_best = compute_minus_on_column(problem_instance, j, first_best, k)
            customers_list[j][1] = first_best - second_best
    customers_ordered = sorted(customers_list, key=lambda j_elem: j_elem[1], reverse=True)
    for j in customers_ordered:
        for i in range(problem_instance.num_facilities):
            if best_y[i][j[0]] == 1:
                best_y[i][j[0]] = 0
                if not try_another_solution(problem_instance, best_x, best_y, j[0]):
                    best_y[i][j[0]] = 1
                    break


def try_another_solution(problem_instance, x, y, j):
    find_best_feasible = False
    best_value = float("inf")
    for i in range(problem_instance.num_facilities):
        y[i][j] = 1
        if mu.is_feasible(problem_instance, x, y):
            feasible_value = mu.obj_value(problem_instance, x, y)
            if feasible_value < best_value:
                find_best_feasible = True
                break
    return find_best_feasible


def compute_min(problem_instance, i, j, k):
    res = float("inf")
    c = problem_instance.transportation_costs
    for s in k:
        if c[s][j] - c[i][j] < res:
            res = c[s][j] - c[i][j]
    return res


def compute_minus_on_column(problem_instance, j, div, k):
    res = float("inf")
    for i in k:
        x = problem_instance.transportation_costs[i][j]
        if x < res and x != div:
            res = problem_instance.transportation_costs[i][j]
    return res


def find_min_index(problem_instance, j, feasible):
    index = 0
    res = float("inf")
    for i in feasible:
        if problem_instance.transportation_costs[i][j] < res:
            res = problem_instance.transportation_costs[i][j]
            index = i
    return index


def find_feasible_first(problem_instance, x, y):
    migrate = []
    for u in range(problem_instance.num_facilities):
        # if the facilities is closed but there are customers assigned open the facilities
        if x[u] == 0 and sum(y[u][j] for j in range(problem_instance.num_customers)) > 0:
            x[u] = 1
            # check if the assignment respect the capacity
            while (sum(y[u][j] * problem_instance.demands[j] for j in range(problem_instance.num_customers)) >
                   problem_instance.capacities[u]):
                v_p = max_transportation_cost(problem_instance, x, y)
                migrate.append([v_p])
                y[v_p] = 0
    if len(migrate) != 0:
        for u in range(problem_instance.num_facilities):
            for v in migrate:
                u_p = min_transportation_cost(problem_instance, v, x, y)
                if u_p == -1:
                    u_p = min_opening_costs(problem_instance, x)
                    x[u] = 1
                    y[u_p][v] = 1
    for u in range(problem_instance.num_facilities):
        if sum(y[u][v] for v in range(problem_instance.num_customers)) == 0:
            x[u] = 0


def find_feasible_second(problem_instance, x, y):
    removed = []
    for u in range(problem_instance.num_facilities):
        if sum(y[u][v] for v in range(problem_instance.num_customers)) >= 1:
            x[u] = 1
    for v in range(problem_instance.num_customers):
        if sum(y[i][v] for i in range(problem_instance.num_facilities)) == 0:
            removed.append(v)
        while sum(y[i][v] for i in range(problem_instance.num_facilities)) > 1:
            for u in range(problem_instance.num_facilities):
                v_p = max_transportation_cost(problem_instance, y, u)
                y[u][v_p] = 0
                removed.append(v_p)
    for v in removed:
        while sum(y[u][v] for u in range(problem_instance.num_facilities)) < 1:
            u_p = min_transportation_cost(problem_instance, v, x, y)
            if u_p == -1:
                u_p = min_opening_costs(problem_instance, x)
                x[u_p] = 1
                y[u_p][v] = 1
            else:
                y[u_p][v] = 1


def min_opening_costs(problem_instance, x):
    low = float("inf")
    min_index = -1
    for u in range(problem_instance.num_facilities):
        if problem_instance.facilities_opening_costs[u] < low and x[u] == 0:
            min_index = u
            low = problem_instance.facilities_opening_costs[u]
    return min_index


def max_transportation_cost(problem_instance, y, u):
    up = 0
    max_index = -1
    for v in range(problem_instance.num_customers):
        if problem_instance.transportation_costs[u][v] > up and y[u][v] == 1:
            up = problem_instance.transportation_costs[u][v]
            max_index = v
    return max_index


def min_transportation_cost(problem_instance, v, x, y):
    low = float("inf")
    min_index = -1
    for u in range(problem_instance.num_facilities):
        if x[u] == 1 and problem_instance.transportation_costs[u][v] < low and sum(problem_instance.demands[j] * y[u][j] for j in range(problem_instance.num_customers)) + problem_instance.demands[v] <= problem_instance.capacities[u]:
            min_index = u
            low = problem_instance.transportation_costs[u][v]
    return min_index
