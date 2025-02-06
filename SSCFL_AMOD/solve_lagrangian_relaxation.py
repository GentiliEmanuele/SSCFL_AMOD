import numpy as np
import models as m
import models_utils as mu
import heuristics as h


def solve_lagrangian_relaxation(problem_instance, num_executions, w, epsilon):
    marked_lamb = []
    lamb = np.zeros(problem_instance.num_facilities)
    best_lamb = lamb.copy()
    residuals_num_runs = num_executions
    it = 0
    find_feasible = False
    # Step 0: Solve (1) by the add heuristic and initialize z_u. Solve (2) with lambda_i = 0 and initialize z_l.
    # If the solution of (2) is feasible for (1) stop. Otherwise, initialize the lambda_i for the violated constraints.
    best_x_feasible, best_y_feasible, z_u, k = h.initial_add_heuristic(problem_instance)
    if not mu.is_feasible(problem_instance, best_x_feasible, best_y_feasible):
        return
    model = m.init_first_problem_relaxation(problem_instance, lamb)
    model.setParam("OutputFlag", 0)
    model.optimize()
    z_l = model.objVal
    best_x = get_x(model, problem_instance)
    best_y = get_y(model, problem_instance)
    if mu.is_feasible(problem_instance, get_x(model, problem_instance), get_y(model, problem_instance)):
        return lamb
    while True and residuals_num_runs >= 0:
        it += 1
        prev_lamb = lamb.copy()
        better_solution_found = False
        cont = False
        # Step 3: Update the multipliers, mark multipliers as necessary, and go to step 1.
        for u in range(len(lamb)):
            if u not in marked_lamb:
                y = get_y(model, problem_instance)
                x = get_x(model, problem_instance)
                update_multipliers(problem_instance, lamb, marked_lamb, w, z_u, z_l, x, y, u)
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
        if feasibility and z_u > curr_relaxed_sol >= 0:
            z_u = curr_relaxed_sol
            best_x_feasible = get_x(model, problem_instance)
            best_y_feasible = get_y(model, problem_instance)
            it = 0
            better_solution_found = True
        # Step 2: If (2) has been solved MAX times without providing another feasible solution to (1) go to step 5.
        # Otherwise, continue.
        if not better_solution_found:
            residuals_num_runs -= 1
            if residuals_num_runs == 0 and find_feasible:
                h.final_adjustment_heuristic(problem_instance, best_x, best_y, k)
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
                h.final_adjustment_heuristic(problem_instance, best_x, best_y, k)
                break
        else:
            marked_lamb = []
    return best_lamb


def get_x(model, problem_instance):
    return [int(model.getVarByName(f"x[{u}]").X) for u in range(problem_instance.num_facilities)]


def get_y(model, problem_instance):
    return [[int(model.getVarByName(f"y[{u},{v}]").X) for v in range(problem_instance.num_customers)]
            for u in range(problem_instance.num_facilities)]


def compute_den(problem_instance, marked_lamb, y):
    total = 0
    facilities_total = 0
    for i in range(problem_instance.num_facilities):
        if i not in marked_lamb:
            for j in range(problem_instance.num_customers):
                total += problem_instance.demands[j] * y[i][j]
            total -= problem_instance.capacities[i]
            facilities_total += total ** 2
    return facilities_total


def update_multipliers(problem_instance, lamb, marked_lamb, w, z_u, z_l, x, y, u):
    num = (w * (z_u - z_l) * (sum(problem_instance.demands[v] * y[u][v]
                                  for v in range(problem_instance.num_customers))) -
           problem_instance.capacities[u])
    den = compute_den(problem_instance, marked_lamb, y)
    lamb[u] = max(lamb[u] + num / den, 0)
