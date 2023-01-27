from src.problem.travel_salesman_problem import TravelSalesmanProblem


if __name__ == "__main__":
    problem = TravelSalesmanProblem("01001", "20117", 2000, 10)
    problem.actions[0]("01001", "20117")