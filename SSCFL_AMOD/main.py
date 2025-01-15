import models as m
import problem_instance as pi
import models_utils as mu

# only for test
if __name__ == '__main__':
    problem_instance = pi.ProblemInstance([1, 4, 1, 3],
                                          [[10, 2, 3, 5], [20, 2, 1, 3]],
                                          [7, 2, 1, 2],
                                          [3, 1])
    original_model = m.init_original_problem(problem_instance)
    original_model.setParam('OutputFlag', 0)
    original_model.optimize()
    first_lagrangian_relaxation = m.init_first_problem_relaxation(problem_instance, [0, 0, 0, 0])
    first_lagrangian_relaxation.optimize()
    second_lagrangian_relaxation = m.init_second_problem_relaxation(problem_instance, [17, 16])
    second_lagrangian_relaxation.optimize()
    print(f"Original problem solution value {original_model.objVal}")
    print(f"First lagrangian relaxation solution value {first_lagrangian_relaxation.objVal}")
    print(f"Second lagrangian relaxation solution value {second_lagrangian_relaxation.objVal}")
