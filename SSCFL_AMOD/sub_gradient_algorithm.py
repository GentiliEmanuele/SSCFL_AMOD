import models as m
import models_utils as utils


def sub_gradient_algorithm(problem_instance, initial_lambda, initial_mu, initial_rho, max_num_iterations, min_rho):
    k = 0
    current_lambda = initial_lambda
    current_mu = initial_mu
    current_rho = initial_rho
    while k < max_num_iterations:
        # solve the sub-problem in x and y obtaining a solution (x_k, y_k) of value w_k
        actual_first_lagrangian_relaxation = m.init_first_problem_relaxation(problem_instance, current_lambda)
        actual_first_lagrangian_relaxation.setParam('OutputFlag', 0)
        actual_first_lagrangian_relaxation.optimize()
        w_k = actual_first_lagrangian_relaxation.objVal

        # compute the subgradient
        delta_h_j_k = compute_first_gradient(actual_first_lagrangian_relaxation,
                                             len(problem_instance.facilities_opening_costs),
                                             len(problem_instance.transportation_costs))
        delta_g_i_k = compute_second_gradient(actual_first_lagrangian_relaxation,
                                              len(problem_instance.facilities_opening_costs),
                                              len(problem_instance.transportation_costs), problem_instance.capacities,
                                              problem_instance.demands)
        ub = 200  # todo(compute real upper bound)
        alpha_k = current_rho * (ub - w_k) / (sum_vector_square(delta_g_i_k, len(delta_g_i_k)) +
                                              sum_vector_square(delta_h_j_k, len(delta_h_j_k)))
        current_rho = 0.5 * current_rho
        for i in range(0, len(delta_g_i_k)):
            current_lambda_i = current_lambda[i] + alpha_k * delta_g_i_k[i]
            if current_lambda_i < 0:
                current_lambda[i] = 0
            else:
                current_lambda[i] = current_lambda_i

        for j in range(0, len(delta_h_j_k)):
            current_mu_j = current_mu[j] + alpha_k * delta_h_j_k[j]
            if current_mu_j < 0:
                current_mu[j] = 0
            else:
                current_mu[j] = current_mu_j
        if k % 10 == 0:
            current_sol = actual_first_lagrangian_relaxation.objVal
            print(f"iteration {k} solution value{actual_first_lagrangian_relaxation.objVal} alpha {alpha_k} rho{current_rho}")
        k = k + 1


def compute_first_gradient(model, num_facilities, num_customers):
    delta_h = []
    for j in range(num_customers):
        current_sum = 0
        for i in range(num_facilities):
            current_sum += model.getVarByName(f"y[{i},{j}]").x
        delta_h.append(current_sum)
    return delta_h


def compute_second_gradient(model, num_facilities, num_customers, capacities, demands):
    delta_g = []
    for i in range(num_facilities):
        current_sum = 0
        for j in range(num_customers):
            current_sum += model.getVarByName(f"y[{i},{j}]").x * demands[j]
        current_sum -= model.getVarByName(f"x[{i}]").x * capacities[i]
        delta_g.append(current_sum)
    return delta_g


def sum_vector_square(v, size):
    accumulator = 0
    for i in range(size):
        accumulator += v[i] * v[i]
    return accumulator
