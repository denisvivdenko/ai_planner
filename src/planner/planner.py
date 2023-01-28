from uuid import uuid4
import numpy as np
import multiprocessing as mp
from collections import defaultdict
from datetime import datetime
import inspect
from pathlib import Path
import os

from src.problem.problem import Problem
from src.planner.model import Model


class Planner:
    def __init__(self, problem: Problem, n_workers: int) -> None:
        self.problem = problem
        self.n_workers = n_workers
        self.stats = defaultdict(list)

    def solve(self, max_attempts: int, max_epoch: int, disp: bool = False) -> ...:
        action_model = np.random
        parameters_model = np.random
        for epoch in range(max_epoch):
            session = f"{datetime.now().timestamp()}{str(uuid4())[:5]}"
            with mp.Manager() as manager:
                shared_stats = manager.Queue()

                solvers = [Solver(id, self.problem, action_model, parameters_model, max_attempts, session, shared_stats, disp) for id in range(self.n_workers)]
                [solver.start() for solver in solvers]
                [solver.join() for solver in solvers]

                while not shared_stats.empty():
                    solver_stats = shared_stats.get()
                    for stat_name, values in solver_stats.items():
                        self.stats[stat_name].extend(values)


class Solver(mp.Process):
    def __init__(self, id: int, problem: Problem, action_model: Model, parameters_model: Model, max_attempts: int, session: str, shared_stats: mp.Queue, disp: bool = False) -> None:
        super().__init__()
        self.solver_id = id
        self.problem = problem
        self.max_attempts = max_attempts

        self.action_model = action_model
        self.parameters_model = parameters_model
        self.actions_indices = list(range(len(self.problem.actions)))
        self.parameters_indices = list(range(len(self.problem.parameters)))
        self.session = session

        self.stats = defaultdict(list)
        self.shared_stats = shared_stats
        self.disp = disp

        self.cached_action_vs_n_parameters = {action: len(inspect.signature(action).parameters) for action in self.problem.actions}
        self.max_n_parameters = max(self.cached_action_vs_n_parameters.values())

    def run(self) -> None:
        self.solve(self.max_attempts, disp=self.disp)
    
    def solve(self, max_attempts: int = 1000, disp: bool = False) -> None:
        dataset = []
        for attempt in range(max_attempts):
            if disp:
                print(attempt)
            n_steps = 0
            try:
                while True:
                    chosen_index = self.action_model.choice(self.actions_indices)
                    action = self.problem.actions[chosen_index]

                    n_parameters = self.cached_action_vs_n_parameters[action]
                    chosen_parameters_indices = self.parameters_model.choice(self.parameters_indices, size=n_parameters)
                    parameters = [self.problem.parameters[index] for index in chosen_parameters_indices]

                    action(*parameters)

                    if self.problem.has_achived_goal():
                        print("Goal has been achived!")
                        break
                    n_steps += 1
                    
                    parameters_vector = [chosen_parameters_indices[i] if i < n_parameters else 0 for i in range(self.max_n_parameters)]
                    dataset.append([attempt, chosen_index, *parameters_vector, n_steps])
            except Exception as e:
                self.problem.reset()
                if disp:
                    print(e)
                    print(f"Number of steps: {n_steps}")
            if n_steps > 0:
                self.stats["n_steps_distribution"].append(n_steps)
        self.shared_stats.put(self.stats)
        path = Path(f"log_data/{self.session}")
        path.mkdir(parents=True, exist_ok=True)
        log_file = os.path.join(path, f"logs_{self.solver_id}.npy")
        np.save(log_file, np.array(dataset))

