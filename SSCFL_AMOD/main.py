import instance_parser as parser
import models as m
import models_utils as mu
import numpy as np

# only for test
if __name__ == '__main__':
    problem_instance = parser.parse_file("instances/cap63")
    model = m.init_first_problem_relaxation(problem_instance, np.zeros(problem_instance.num_facilities))
    model.optimize()
    print(model.ObjVal)
