import models as m


# only for test
if __name__ == '__main__':
    model = m.init_second_problem_relaxation([1, 4, 1, 3],
                                             [[4, 8, 12, 5], [2, 2, 1, 3]],
                                             [7, 2, 1, 2],
                                             [3, 1],
                                             [1, 4])
    model.optimize()
