def print_solution(model):
    for var in model.getVars():
        print(f"{var.varName} = {var.x}")


def get_unidimensional_vars_by_name(model, name, number):
    variables = []
    for i in range(number):
        variables.append(model.getVarByName(f"{name}[{i}]"))
    return variables


def get_bidimensional_vars_by_name(model, name, num_facilities, prod_customer_facilities):
    variables = []
    for i in range(num_facilities):
        for j in range(prod_customer_facilities):
            variables.append(model.getVarByName(f"{name}[{i},{j}]"))
    return variables
