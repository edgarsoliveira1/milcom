from abc import ABC, abstractmethod

import pandas as pd

from ..core.trajectory import Trajectory
from ..utils.config import col_names


class SegmentationStrategy(ABC):
    @abstractmethod
    def segment(self, trajectory: Trajectory, **kwargs) -> Trajectory:
        """
        Segmenta a trajetória em partes menores.

        Parameters:
        trajectory (TrajectoryData): Os dados da trajetória a serem segmentados.

        Returns:
        TrajectoryData: Os dados da trajetória segmentados.
        """
        pass


class TimeDiffSegmentation(SegmentationStrategy):
    def segment(
        self, trajectory: Trajectory, max_timediff_s: float
    ) -> pd.DataFrame:
        trajectory[col_names.SEGMENT_ID] = (
            trajectory[col_names.DELTA_TIME].diff() > max_timediff_s
        ).cumsum()
        return trajectory


class DistanceSegmentation(SegmentationStrategy):
    def segment(
        self, trajectory: Trajectory, max_distance_m: float
    ) -> pd.DataFrame:
        trajectory[col_names.SEGMENT_ID] = (
            trajectory[col_names.DISTANCE] > max_distance_m
        ).cumsum()
        return trajectory


class SpeedSegmentation(SegmentationStrategy):
    def __init__(self, speed_threshold: float):
        self.speed_threshold = speed_threshold

    def segment(self, trajectory: Trajectory) -> pd.DataFrame:
        trajectory[col_names.SEGMENT_ID] = (
            trajectory[col_names.SPEED] > self.speed_threshold
        ).cumsum()
        return trajectory


class StopSegmentation(SegmentationStrategy):
    def segment(self, trajectory: Trajectory) -> pd.DataFrame:
        trajectory[col_names.SEGMENT_ID] = (
            trajectory[col_names.STOP]
            & ~trajectory[col_names.STOP].shift().fillna(False)
        ).cumsum()
        return trajectory


class TrajectorySegmenter:
    def __init__(self, strategy: SegmentationStrategy):
        self._strategy = strategy

    def set_strategy(self, strategy: SegmentationStrategy):
        self._strategy = strategy

    def segment_trajectory(
        self, trajectory: Trajectory, **kwargs
    ) -> pd.DataFrame:
        return trajectory.groupby(col_names.TRAJECTORY_ID).apply(
            lambda t: self._strategy.segment(t, **kwargs)
        )
