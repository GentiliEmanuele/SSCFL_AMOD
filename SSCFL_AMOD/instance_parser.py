import problem_instance as pi
def parse_file(path):
    line_counter = 0
    opening_costs = []
    transportation_cost = []
    num_costumers = 0
    num_facility = 0
    demands = []
    capacities = []
    f = open(path, 'r')
    if f is None:
        print("An error occurred while opening the file")
    for line in f:
        if line_counter == 0:
            split_line = line.strip().split(" ")
            num_facility = int(split_line[0])
            num_costumers = int(split_line[1])
        if 0 < line_counter <= num_facility:
            split_line = line.strip().split(" ")
            capacities.append(float(split_line[0]))
            opening_costs.append(float(split_line[1]))
        if line_counter == num_facility + 1:
            demands = [float(x) for x in line.strip().split(" ")]
        if num_facility + 1 < line_counter <= num_costumers:
            transportation_cost.append([float(x) for x in line.strip().split(" ")])
        line_counter += 1
    return pi.ProblemInstance(opening_costs, transportation_cost, capacities, demands)
