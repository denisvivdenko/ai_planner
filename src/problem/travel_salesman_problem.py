import pandas as pd

from src.problem.problem import Problem


class TravelSalesmanProblem(Problem):
    def __init__(self, start_position: str, goal_position: str, max_distance: float, max_moves: int, data_file_path: str = "data/data.csv") -> None:
        super().__init__()
        self.position = start_position
        self.goal_position = goal_position
        self.distance_counter = 0
        self.moves_counter = 0

        self.max_distance = max_distance
        self.max_moves = max_moves
    
        self.graph = self._read_data(data_file_path)

        self.actions.extend([self.move])
        self.constraints.extend([self.check_distance_constraint, self.check_moves_constrains])

    def has_achived_goal(self) -> bool:
        for check_constraint in self.constraints:
            check_constraint()

        if self.position == self.goal_position:
            return True
        return False

    def move(self, from_node: str, to_node: str) -> None:
        distance = self.graph.get((from_node, to_node), None)
        if not distance:
            distance = self.graph.get((to_node, from_node), None)
        if not distance:
            raise Exception(f"Impossible combination of parameters. from_node = {from_node}; to_node = {to_node}.")
        self.distance_counter += self.graph[(from_node, to_node)]

    def check_distance_constraint(self) -> None:
        if self.distance_counter > self.max_distance:
            raise Exception(f"Distance constraint violation.  {self.distance_counter} > {self.max_distance}.")

    def check_moves_constrains(self) -> None:
        if self.moves_counter > self.max_moves:
            raise Exception(f"Max moves constraint violation. {self.moves_counter} > {self.max_moves}.")
    
    def _read_data(self, file_path: str) -> dict[tuple, float]:
        data = pd.read_csv(file_path).sample(5000, random_state=42)
        graph = {}
        for _, row in data.iterrows():
            graph[(row["county1"], row["county2"])] = row["mi_to_county"]
        return graph