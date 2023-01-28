import matplotlib.pyplot as plt

from src.problem.travel_salesman_problem import TravelSalesmanProblem
from src.planner.planner import Planner

if __name__ == "__main__":
    problem = TravelSalesmanProblem("01001", "20117", 2000, 10)
    planner = Planner(problem, n_workers=6)
    planner.solve(max_attempts=2000000)
    # print(planner.stats)
    plt.hist(planner.stats["n_steps_distribution"], bins=10)
    plt.show()
    
