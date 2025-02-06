import solution


def parse_solutions():
    path = "solutions/OR-Library_Solution_Values.txt"
    solutions_list = []
    f = open(path, 'r')
    if f is None:
        print("An error occurred while opening the file")
    for line in f:
        split_line = line.strip().replace(" ", "").replace("\\", "").split("&")
        sol = solution.Solution(split_line[0], int(split_line[1]), split_line[2], float(split_line[3]))
        solutions_list.append(sol)
    return solutions_list
