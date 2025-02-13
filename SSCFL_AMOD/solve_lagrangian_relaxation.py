import models as m
import models_utils as mu
import heuristics as h
import random


def solve_lagrangian_relaxation_first(problem_instance, num_executions, w, epsilon):
    marked_lamb = []
    x = [0 for _ in range(problem_instance.num_facilities)]
    y = [[0 for _ in range(problem_instance.num_customers)] for _ in range(problem_instance.num_facilities)]
    lamb = [0 for _ in range(problem_instance.num_facilities)]
    best_lamb = lamb.copy()
    residuals_num_runs = num_executions
    find_feasible = False
    # Step 0: Solve (1) by the add heuristic and initialize z_u. Solve (2) with lambda_i = 0 and initialize z_l.
    # If the solution of (2) is feasible for (1) stop. Otherwise, initialize the lambda_i for the violated constraints.
    best_x_feasible, best_y_feasible, z_u, k = h.initial_add_heuristic(problem_instance, x, y)
    if not mu.is_feasible(problem_instance, best_x_feasible, best_y_feasible):
        return
    model = m.init_first_problem_relaxation(problem_instance, lamb)
    model.setParam("OutputFlag", 0)
    model.optimize()
    best_x = get_x(model, problem_instance)
    best_y = get_y(model, problem_instance)
    z_l = model.objVal
    if mu.is_feasible(problem_instance, get_x(model, problem_instance), get_y(model, problem_instance)):
        return lamb, z_l
    while residuals_num_runs >= 0:
        prev_lamb = lamb.copy()
        better_solution_found = False
        cont = False
        y = get_y(model, problem_instance)
        # Step 3: Update the multipliers, mark multipliers as necessary, and go to step 1.
        for u in range(problem_instance.num_facilities):
            if u not in marked_lamb:
                update_multipliers_first(problem_instance, lamb, marked_lamb, w, z_u, z_l, y, u)
            if prev_lamb[u] > lamb[u]:
                marked_lamb.append(u)
            else:
                if prev_lamb[u] < lamb[u] and u in marked_lamb:
                    marked_lamb.remove(u)
        # Step 1: Solve (2) and update z_l if necessary. If the solution is feasible for (1), update z_u if necessary
        # and go to step 4. Otherwise, continue.
        model = m.init_first_problem_relaxation(problem_instance, lamb)
        model.setParam("OutputFlag", 0)
        model.optimize()
        curr_relaxed_sol = model.objVal
        feasibility = mu.is_feasible(problem_instance, get_x(model, problem_instance), get_y(model, problem_instance))
        if feasibility:
            find_feasible = True
        if curr_relaxed_sol > z_l >= 0:
            z_l = curr_relaxed_sol
            best_x = get_x(model, problem_instance)
            best_y = get_y(model, problem_instance)
            best_lamb = lamb.copy()
        else:
            break
        if feasibility and z_u > curr_relaxed_sol >= 0:
            z_u = curr_relaxed_sol
            # best_x_feasible = get_x(model, problem_instance)
            # best_y_feasible = get_y(model, problem_instance)
            residuals_num_runs = num_executions
            better_solution_found = True
        # Step 2: If (2) has been solved MAX times without providing another feasible solution to (1) go to step 5.
        # Otherwise, continue.
        if not better_solution_found:
            residuals_num_runs -= 1
            if residuals_num_runs == 0 and find_feasible:
                h.final_adjustment_heuristic(problem_instance, get_x(model, problem_instance),
                                             get_y(model, problem_instance), k)
                break
            if residuals_num_runs > 0:
                cont = True
        # Step 4: if z_u/z_l <= 1 + eps or if a better solution of (1) was previously found by (2) go to step (5).
        # Otherwise, record the solution, cont multipliers, and go to step (3).
        if (better_solution_found or z_u / z_l <= 1 + epsilon) and not cont:
            # Step 5: If the lagrangian relaxation have not found any feasible solutions for (1), stop, Otherwise,
            # execute the final adjustment heuristic, and stop.
            if not find_feasible:
                break
            else:
                h.final_adjustment_heuristic(problem_instance, get_x(model, problem_instance),
                                             get_y(model, problem_instance), k)
                break
        else:
            marked_lamb = []
    return best_lamb, z_l, best_x, best_y


def solve_lagrangian_relaxation_second(problem_instance, num_executions, w, epsilon):
    marked_mu = []
    x = [0 for _ in range(problem_instance.num_facilities)]
    y = [[0 for _ in range(problem_instance.num_customers)] for _ in range(problem_instance.num_facilities)]
    _mu = [0 for _ in range(problem_instance.num_customers)]
    best_mu = _mu.copy()
    residuals_num_runs = num_executions
    find_feasible = False
    # Step 0: Solve (1) by the add heuristic and initialize z_u. Solve (2) with lambda_i = 0 and initialize z_l.
    # If the solution of (2) is feasible for (1) stop. Otherwise, initialize the lambda_i for the violated constraints.
    best_x_feasible, best_y_feasible, z_u, k = h.initial_add_heuristic(problem_instance, x, y)
    if not mu.is_feasible(problem_instance, best_x_feasible, best_y_feasible):
        return
    model = m.init_second_problem_relaxation(problem_instance, _mu)
    model.setParam("OutputFlag", 0)
    model.optimize()
    best_x = get_x(model, problem_instance)
    best_y = get_y(model, problem_instance)
    z_l = model.objVal
    if mu.is_feasible(problem_instance, get_x(model, problem_instance), get_y(model, problem_instance)):
        return _mu, z_l
    while residuals_num_runs >= 0:
        prev_mu = _mu.copy()
        better_solution_found = False
        cont = False
        y = get_y(model, problem_instance)
        # Step 3: Update the multipliers, mark multipliers as necessary, and go to step 1.
        for v in range(problem_instance.num_customers):
            if v not in marked_mu:
                update_multipliers_second(problem_instance, _mu, marked_mu, w, z_u, z_l, y, v)
            if prev_mu[v] > _mu[v]:
                marked_mu.append(v)
            else:
                if prev_mu[v] < _mu[v] and v in marked_mu:
                    marked_mu.remove(v)
        # Step 1: Solve (2) and update z_l if necessary. If the solution is feasible for (1), update z_u if necessary
        # and go to step 4. Otherwise, continue.
        model = m.init_second_problem_relaxation(problem_instance, _mu)
        model.setParam("OutputFlag", 0)
        model.optimize()
        curr_relaxed_sol = model.objVal
        feasibility = mu.is_feasible(problem_instance, get_x(model, problem_instance), get_y(model, problem_instance))
        if feasibility:
            find_feasible = True
        if curr_relaxed_sol > z_l >= 0:
            z_l = curr_relaxed_sol
            best_x = get_x(model, problem_instance)
            best_y = get_y(model, problem_instance)
            best_mu = _mu.copy()
        else:
            break
        if feasibility and z_u > curr_relaxed_sol >= 0:
            z_u = curr_relaxed_sol
            # best_x_feasible = get_x(model, problem_instance)
            # best_y_feasible = get_y(model, problem_instance)
            residuals_num_runs = num_executions
            better_solution_found = True
        # Step 2: If (2) has been solved MAX times without providing another feasible solution to (1) go to step 5.
        # Otherwise, continue.
        if not better_solution_found:
            residuals_num_runs -= 1
            if residuals_num_runs == 0 and find_feasible:
                h.final_adjustment_heuristic(problem_instance, get_x(model, problem_instance),
                                             get_y(model, problem_instance), k)
                break
            if residuals_num_runs > 0:
                cont = True
        # Step 4: if z_u/z_l <= 1 + eps or if a better solution of (1) was previously found by (2) go to step (5).
        # Otherwise, record the solution, cont multipliers, and go to step (3).
        if (better_solution_found or z_u / z_l <= 1 + epsilon) and not cont:
            # Step 5: If the lagrangian relaxation have not found any feasible solutions for (1), stop, Otherwise,
            # execute the final adjustment heuristic, and stop.
            if not find_feasible:
                break
            else:
                h.final_adjustment_heuristic(problem_instance, get_x(model, problem_instance),
                                             get_y(model, problem_instance), k)
                break
        else:
            marked_mu = []
    return best_mu, z_l, best_x, best_y


def get_x(model, problem_instance):
    return [int(model.getVarByName(f"x[{u}]").X) for u in range(problem_instance.num_facilities)]


def get_y(model, problem_instance):
    return [[int(model.getVarByName(f"y[{u},{v}]").X) for v in range(problem_instance.num_customers)]
            for u in range(problem_instance.num_facilities)]


def compute_den_first(problem_instance, marked_lamb, y):
    facilities_total = 0
    for i in range(problem_instance.num_facilities):
        total = 0
        if i not in marked_lamb:
            for j in range(problem_instance.num_customers):
                total += problem_instance.demands[j] * y[i][j]
            total -= problem_instance.capacities[i]
            facilities_total += total ** 2
    return facilities_total


def compute_den_second(problem_instance, marked_mu, y):
    global_total = 0
    for j in range(problem_instance.num_customers):
        total = 0
        if j not in marked_mu:
            for i in range(problem_instance.num_facilities):
                total += y[i][j]
            global_total += (1 - total) ** 2
    return global_total


def update_multipliers_first(problem_instance, lamb, marked_lamb, w, z_u, z_l, y, u):
    num = (w * (z_u - z_l) * (sum(problem_instance.demands[v] * y[u][v]
                                  for v in range(problem_instance.num_customers))) -
           problem_instance.capacities[u])
    den = compute_den_first(problem_instance, marked_lamb, y)
    lamb[u] = max(lamb[u] + num / den, 0)


def update_multipliers_second(problem_instance, _mu, marked_mu, w, z_u, z_l, y, v):
    num = w * (z_u - z_l) * (1 - sum(y[u][v] for u in range(problem_instance.num_facilities)))
    den = compute_den_second(problem_instance, marked_mu, y)
    _mu[v] = max(_mu[v] + num / den, 0)
