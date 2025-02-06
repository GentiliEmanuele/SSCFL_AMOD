import os

import problem_instance as pi


def parse_file(path, name):
    line_counter = 0
    opening_costs = []
    transportation_cost = []
    num_costumers = 0
    num_facilities = 0
    demands = []
    capacities = []
    f = open(path, 'r')
    if f is None:
        print("An error occurred while opening the file")
    for line in f:
        if line_counter == 0:
            split_line = line.strip().split(" ")
            num_facilities = int(split_line[0])
            num_costumers = int(split_line[1])
        if 0 < line_counter <= num_facilities:
            split_line = line.strip().split(" ")
            capacities.append(float(split_line[0]))
            opening_costs.append(float(split_line[1]))
        if line_counter == num_facilities + 1:
            demands = [float(x) for x in line.strip().split(" ")]
        if num_facilities + 1 < line_counter:
            transportation_cost.append([float(x) for x in line.strip().split(" ")])
        line_counter += 1
    return pi.ProblemInstance(name, num_facilities, num_costumers, opening_costs, transportation_cost, capacities,
                              demands)


def get_all_instances():
    problem_instances = []
    for filename in os.listdir("instances"):
        file_path = os.path.join("instances", filename)
        if os.path.isfile(file_path):
            problem_instance = parse_file(file_path, filename)
            problem_instances.append(problem_instance)
    return problem_instances
