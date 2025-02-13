import instance_parser
import solution_parser
import evaluator


# only for test
if __name__ == '__main__':
    num_runs = 300
    w_first = 10
    w_second = 0.1
    epsilon = 0.01
    solutions = solution_parser.parse_solutions()
    instances = instance_parser.get_all_instances()
    evaluator.evaluate(instances, solutions, num_runs, w_first, w_second, epsilon)
