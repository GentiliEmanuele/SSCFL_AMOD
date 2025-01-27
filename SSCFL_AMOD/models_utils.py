def print_solution(model):
    for var in model.getVars():
        print(f"{var.varName} = {var.x}")

