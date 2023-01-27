from abc import ABC, abstractmethod


class Problem(ABC):
    def __init__(self) -> None:
        self.constraints = []
        self.actions = []
        self.parameters = []

    @abstractmethod
    def has_achived_goal(self) -> bool:
        pass

    @abstractmethod
    def reset(self) -> None:
        pass