import instance_parser as parser
import solve_lagrangian_relaxation as slr
import models_utils as mu
import models as m

# only for test
if __name__ == '__main__':
    problem_instance = parser.parse_file("instances/cap62")
    z_u, best_x_feasible, best_y_feasible, z_l, best_x, best_y, lamb = slr.solve_lagrangian_relaxation(problem_instance)
    print(f"Upper bound: {z_u}, z_l: {z_l}"
          f"Best_x: {best_x}, best_y: {best_y}, lamb: {lamb}")
    print(f"Best_x_feasible: {best_x_feasible}")
    print("Best_y_feasible: ")
    for i in range(problem_instance.num_facilities):
        print(f"{i}: {best_y_feasible[i]}")

    print(f"Lower bound: {z_l}")
    print(f"Best_x: {best_x}")
    print("Best_y: ")
    for i in range(problem_instance.num_facilities):
        print(f"{i}: {best_y[i]}")
    print(f"Lambda: {lamb}")
    print(mu.is_feasible(problem_instance, best_x_feasible, best_y_feasible))
    model = m.init_first_problem_relaxation(problem_instance, lamb)
    model.optimize()
    print(model.objVal, z_l)
