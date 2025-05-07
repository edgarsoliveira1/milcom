from abc import ABC, abstractmethod

import pandas as pd
from ..core.trajectory import Trajectory
from ..utils.config import col_names


class MovingTogetherDetectionStrategy(ABC):
    @abstractmethod
    def detect(self, trajectory: Trajectory, **kwargs) -> pd.DataFrame:
        pass


class Encounter(MovingTogetherDetectionStrategy):
    """
    A group of at least n objects that will arrive simultaneously in a disc with radius r (meters)
    """

    def detect(self, trajectory: Trajectory, n: int, r_m: float):
        t = trajectory.copy()
        last_points = t.groupby(col_names.TRAJECTORY_ID).tail(1)
        return t


class Convergence(MovingTogetherDetectionStrategy):
    """
    A group of at least m objects that will pass through a disc with radius r (not necessarily at the same time).
    """

    def __init__(self, m, r):
        super().__init__(m, r)

    def detect(self, traj: Trajectory):
        # TODO: Implement the Convergence pattern logic
        pass


class PatternContext:
    def __init__(self, strategy: MovingTogetherDetectionStrategy):
        self._strategy = strategy

    def set_strategy(self, strategy: MovingTogetherDetectionStrategy):
        self._strategy = strategy

    def execute_strategy(self, traj: Trajectory):
        return self._strategy.detect(traj)
