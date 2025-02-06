import evaluator
import solution_parser
import instance_parser

# only for test
if __name__ == '__main__':
    num_runs = 300
    w = 0.25
    epsilon = 0.0001
    solutions = solution_parser.parse_solutions()
    instances = instance_parser.get_all_instances()
    evaluator.evaluate(instances, solutions, num_runs, w, epsilon)
