from src.problem.travel_salesman_problem import TravelSalesmanProblem
from src.planner.planner import Planner

if __name__ == "__main__":
    problem = TravelSalesmanProblem("01001", "20117", 2000, 10)
    planner = Planner(problem)
    planner.solve()
