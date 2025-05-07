from abc import ABC, abstractmethod

import pandas as pd

from ..core.trajectory import Trajectory
from ..utils.config import col_names


class CompressionStrategy(ABC):
    @abstractmethod
    def compress(self, trajectory: Trajectory, *args, **kwargs) -> Trajectory:
        """
        Compress the trajectory data.

        Parameters:
        trajectory (TrajectoryData): The trajectory data to be compressed.

        Returns:
        TrajectoryData: The compressed trajectory data.
        """
        pass


class TimeCompression(CompressionStrategy):
    def compress(
        self, trajectory: Trajectory, max_timediff_s: float
    ) -> pd.DataFrame:
        # Keep only the points where the time difference exceeds the threshold
        mask = trajectory[col_names.DELTA_TIME] > max_timediff_s
        compressed_data = trajectory[mask]
        return compressed_data


class DistanceCompression(CompressionStrategy):
    def compress(
        self, trajectory: Trajectory, max_distance_m: float
    ) -> pd.DataFrame:
        # Keep only the points where the distance exceeds the threshold
        mask = trajectory[col_names.DISTANCE] > max_distance_m
        compressed_data = trajectory[mask]
        return compressed_data


class SpeedCompression(CompressionStrategy):
    def compress(
        self, trajectory: Trajectory, max_speed_ms: float
    ) -> pd.DataFrame:
        # Keep only the points where the speed exceeds the threshold
        mask = trajectory[col_names.SPEED] > max_speed_ms
        compressed_data = trajectory[mask]
        return compressed_data


class StopCompression(CompressionStrategy):
    def compress(self, trajectory: Trajectory) -> pd.DataFrame:
        return trajectory[trajectory[col_names.STOP]]


class TrajectoryCompressor:
    def __init__(self, strategy: CompressionStrategy):
        self._strategy = strategy

    def set_strategy(self, strategy: CompressionStrategy):
        self._strategy = strategy

    def compress_trajectory(
        self, trajectory: Trajectory, *args, **kwargs
    ) -> Trajectory:
        return self._strategy.compress(trajectory, *args, **kwargs)
