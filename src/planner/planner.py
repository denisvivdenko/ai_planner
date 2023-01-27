import numpy as np

from src.problem.problem import Problem

class Planner:
    def __init__(self, problem: Problem) -> None:
        self.problem = problem

    def solve(self, max_attempts: int = 1000, disp: bool = False) -> None:
        for attempt in range(max_attempts):
            if disp:
                print(attempt)
            try:
                n_steps = 0
                while True:
                    action = np.random.choice(self.problem.actions)
                    parameters = np.random.choice(self.problem.parameters, size=2)
                    action(*parameters)

                    if self.problem.has_achived_goal():
                        print("Goal has been achived!")
                        break
                    n_steps += 1
            except Exception as e:
                self.problem.reset()
                if disp:
                    print(e)
                    print(f"Number of steps: {n_steps}")


    