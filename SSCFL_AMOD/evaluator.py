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
    if not mu.verbose_is_feasible(problem_instance, x, y):
        exit(1)
    return obj_val, (end - start), mu.obj_value(problem_instance, x, y)


def solve_lagrangian_second(problem_instance, num_runs, w, eps):
    start = time.time()
    _mu, obj_val, x, y = solve_lagrangian_relaxation.solve_lagrangian_relaxation_second(problem_instance, num_runs, w,
                                                                                        eps)
    end = time.time()
    heuristics.find_feasible_second(problem_instance, x, y)
    if not mu.verbose_is_feasible(problem_instance, x, y):
        exit(1)
    return obj_val, (end - start), mu.obj_value(problem_instance, x, y)


def evaluate(instances, solutions, num_runs, w_first, w_second, eps):
    with (open("results/results_first_relaxation1.csv", "w") as first,
          open("results/results_second_relaxation1.csv", "w") as second):
        first.write("instance_name,num_facilities,num_customers,original_solution_value,original_execution_time,"
                    "first_relaxation_solution_value,"
                    "first_relaxation_solution_time,first_feasible_solution_value,"
                    "OR_Library_Solution_Value\n")
        second.write("instance_name,num_facilities,num_customers,original_solution_value,original_execution_time,"
                     "second_relaxation_solution_value,"
                     "second_relaxation_solution_time,second_feasible_solution_value,"
                     "OR_Library_Solution_Value\n")
        solve_lagrangian_second(instances[len(instances) - 1], num_runs, w_second, eps)
        for inst in instances:
            or_lib_sol_val = get_sol_value(solutions, inst.name)
            print(f"Solving for {inst.name} -> Expected {or_lib_sol_val}")
#           obj_val, execution_time = solve_original(inst)
#            print(f"Original problem has been solved execution_time={execution_time} obj_value={obj_val}")
            l_obj_val, l_execution_time, feasible_first = solve_lagrangian_first(inst, num_runs, w_first, eps)
            print(f"Relaxation has been solved execution_time={l_execution_time} obj_value={l_obj_val} "
                  f"first_feasible_solution_value={feasible_first}")
            l2_obj_val, l2_execution_time, feasible_second = solve_lagrangian_second(inst, num_runs, w_second, eps)
            print(f"Relaxation has been solved execution_time={l2_execution_time} obj_value={l2_obj_val} "
                  f"second_feasible_solution_value={feasible_second}")
#            first.write(f"{inst.name},{inst.num_facilities},{inst.num_customers},{obj_val},{execution_time},"
#                        f"{l_obj_val},{l_execution_time}, {feasible_first},{or_lib_sol_val}\n")
#            second.write(f"{inst.name},{inst.num_facilities},{inst.num_customers},{obj_val},{execution_time},"
 #                        f"{l2_obj_val},{l2_execution_time},{feasible_second},{or_lib_sol_val}\n")
