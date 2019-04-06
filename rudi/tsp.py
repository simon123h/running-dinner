try:
    import tspy
except ImportError:
    raise ImportError(
        'Module \'tspy\' required.\nPlease install it via \'pip install tspy\'')
try:
    import numpy as np
except ImportError:
    raise ImportError(
        'Module \'numpy\' required.\nPlease install it via \'pip install numpy\'')


def tsp(matrix):
    # solve the traveling salesman problem from a weight matrix
    tsp = tspy.TSP(matrix)
    solver = tspy.solvers.TwoOpt_solver(initial_tour='NN', iter_num=100)
    solution = tsp.get_approx_solution(solver)
