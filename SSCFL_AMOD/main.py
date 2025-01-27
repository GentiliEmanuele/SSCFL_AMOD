import instance_parser as parser
import models as m
import feasible_solution_generator as fsg

# only for test
if __name__ == '__main__':
    problem_instance = parser.parse_file("instances/capa1")
    model = m.init_original_problem(problem_instance)
    model.optimize()
    fs = fsg.generate(problem_instance, 10)
    print(f"The value of fs is {fs} and the value of objVal is " 
          f"{model.objVal} ({model.objVal < fs})")
