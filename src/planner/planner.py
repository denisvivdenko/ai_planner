import numpy as np
import multiprocessing as mp
from collections import defaultdict

from src.problem.problem import Problem

class Planner:
    def __init__(self, problem: Problem, n_workers: int) -> None:
        self.problem = problem
        self.n_workers = n_workers
        self.stats = defaultdict(list)

    def solve(self, max_attempts: int, disp: bool = False) -> ...:
        with mp.Manager() as manager:
            shared_stats = manager.Queue()

            solvers = [Solver(self.problem, max_attempts, shared_stats, disp) for _ in range(self.n_workers)]
            [solver.start() for solver in solvers]
            [solver.join() for solver in solvers]

            while not shared_stats.empty():
                solver_stats = shared_stats.get()
                for stat_name, values in solver_stats.items():
                    self.stats[stat_name].extend(values)


class Solver(mp.Process):
    def __init__(self, problem: Problem, max_attempts: int, shared_stats, disp: bool = False) -> None:
        super().__init__()
        self.problem = problem
        self.max_attempts = max_attempts
        self.stats = defaultdict(list)
        self.shared_stats = shared_stats
        self.disp = disp

    def run(self) -> None:
        self.solve(self.max_attempts, disp=self.disp)
    
    def solve(self, max_attempts: int = 1000, disp: bool = False) -> None:
        for attempt in range(max_attempts):
            if disp:
                print(attempt)
            n_steps = 0
            try:
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
            if n_steps > 0:
                self.stats["n_steps_distribution"].append(n_steps)
        self.shared_stats.put(self.stats)

