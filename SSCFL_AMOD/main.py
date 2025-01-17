import instance_parser as parser
import models as m

# only for test
if __name__ == '__main__':
    problem_instance = parser.parse_file("instances/cap62")
    model = m.init_original_problem(problem_instance)
    model.optimize()
