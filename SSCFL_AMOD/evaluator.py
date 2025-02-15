import models
import time
import solve_lagrangian_relaxation
import heuristics

import models_utils as mu


def get_sol_value(solutions, name):
    for s in solutions:
        if s.name == name:
            return s.optimal_value
    return -1


def solve_original(problem_instance):
    model = models.init_original_problem(problem_instance)
    model.setParam("OutputFlag", 0)
    start = time.time()
    model.optimize()
    end = time.time()
    obj_val = model.objVal
    return obj_val, end - start


def solve_lagrangian_first(problem_instance, num_runs, w, eps):
    start = time.time()
    lamb, obj_val, x, y = solve_lagrangian_relaxation.solve_lagrangian_relaxation_first(problem_instance, num_runs, w,
                                                                                        eps)
    heuristics.find_feasible_first(problem_instance, x, y)
    end = time.time()
    if not mu.is_feasible(problem_instance, x, y):
        exit(1)
    return obj_val, (end - start), mu.obj_value(problem_instance, x, y)


def solve_lagrangian_second(problem_instance, num_runs, w, eps):
    start = time.time()
    _mu, obj_val, x, y = solve_lagrangian_relaxation.solve_lagrangian_relaxation_second(problem_instance, num_runs, w,
                                                                                        eps)
    end = time.time()
    heuristics.find_feasible_second(problem_instance, x, y)
    if not mu.is_feasible(problem_instance, x, y):
        exit(1)
    return obj_val, (end - start), mu.obj_value(problem_instance, x, y)


def evaluate(instances, solutions, num_runs, eps):
    with (open("results/results_original_problem.csv", "w") as original,
          open("results/results_first_relaxation.csv", "w") as first,
          open("results/results_second_relaxation.csv", "w") as second):
        # original.write("name,N,M,value,execution_time,ref_value\n")
        first.write("name,value,execution_time,feasible_solution_value\n")
        second.write("name,value,execution_time,feasible_solution_value\n")
        for inst in instances:
            if inst.num_facilities >= 100 and inst.num_customers >= 1000:
                w_first = 10
                w_second = 0.1
            else:
                w_first = 0.25
                w_second = 0.05
            or_lib_sol_val = get_sol_value(solutions, inst.name)
            print(f"Solving for {inst.name} -> Expected {or_lib_sol_val}")
            obj_val, execution_time = solve_original(inst)
            print(f"Original problem has been solved execution_time={execution_time} obj_value={obj_val}")
            l_obj_val, l_execution_time, feasible_first = solve_lagrangian_first(inst, num_runs, w_first, eps)
            print(f"Relaxation has been solved execution_time={l_execution_time} obj_value={l_obj_val} "
                  f"first_feasible_solution_value={feasible_first}")
            l2_obj_val, l2_execution_time, feasible_second = solve_lagrangian_second(inst, num_runs, w_second, eps)
            print(f"Relaxation has been solved execution_time={l2_execution_time} obj_value={l2_obj_val} "
                  f"second_feasible_solution_value={feasible_second}")
            original.write(f"{inst.name},{inst.num_facilities},{inst.num_customers},{obj_val},{execution_time},"
                           f"{or_lib_sol_val}\n")
            first.write(f"{inst.name},{l_obj_val},{l_execution_time},{feasible_first}\n")
            second.write(f"{inst.name},{l2_obj_val},{l2_execution_time},{feasible_second}\n")
