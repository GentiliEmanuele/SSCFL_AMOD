import models
import time
import solve_lagrangian_relaxation


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
    return obj_val, end-start


def solve_lagrangian(problem_instance, num_runs, w, eps):
    start_mult = time.time()
    lamb = solve_lagrangian_relaxation.solve_lagrangian_relaxation(problem_instance, num_runs, w, eps)
    end_mult = time.time()
    model = models.init_first_problem_relaxation(problem_instance, lamb)
    model.setParam("OutputFlag", 0)
    start = time.time()
    model.optimize()
    end = time.time()
    obj_val = model.objVal
    return obj_val, (end-start) + (end_mult-start_mult)


def evaluate(instances, solutions, num_runs, w, eps):
    with open("results/results.csv", "w") as csvfile:
        csvfile.write("instance_name,original_solution_value,original_execution_time,relaxation_solution_value,"
                      "relaxation_solution_time,OR_Library_Solution_Value\n")
        for inst in instances:
            print(f"Solving for {inst.name}")
            obj_val, execution_time = solve_original(inst)
            l_obj_val, l_execution_time = solve_lagrangian(inst, num_runs, w, eps)
            or_lib_sol_val = get_sol_value(solutions, inst.name)
            csvfile.write(f"{inst.name},{obj_val},{execution_time},{l_obj_val},{l_execution_time},{or_lib_sol_val}\n")
