# (Strategy Pattern)
from abc import ABC, abstractmethod

from ..core.trajectory import Trajectory
from ..utils.config import col_names


# Estraégia de detecção de stay points
class StopDetectionStrategy(ABC):
    @abstractmethod
    def detect(self, trajectory: Trajectory, **kwargs) -> Trajectory:
        raise NotImplementedError


class SpeedStopDetection(StopDetectionStrategy):
    def detect(self, trajectory, speed_threshold=0):
        # Ensure that the distance and time difference columns are present
        if col_names.SPEED not in trajectory.columns:
            raise ValueError(f"Column {col_names.SPEED} is missing in trajectory")
        trajectory[col_names.STOP] = trajectory[col_names.SPEED].apply(
            lambda speed: speed <= speed_threshold
        )
        return trajectory


class StopDetector:
    def __init__(self, strategy: StopDetectionStrategy):
        if strategy is StopDetectionStrategy:
            self._strategy = strategy()
        else:
            self._strategy = strategy

    def set_strategy(self, strategy: StopDetectionStrategy):
        self._strategy = strategy

    def add_stop_column(self, trajectory: Trajectory, **kwargs) -> Trajectory:
        # Apply the function to each group
        trajectory = trajectory.groupby(col_names.TRAJECTORY_ID).apply(
            lambda t: self._strategy.detect(t, **kwargs)
        )
        return trajectory
