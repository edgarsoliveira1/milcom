from abc import ABC, abstractmethod

import numpy as np
import pandas as pd

from ..core.trajectory import Trajectory
from ..utils.config import col_names


class OutlierDetectionStrategy(ABC):
    @abstractmethod
    def detect(self, trajectory: Trajectory, *args, **kwargs) -> Trajectory:
        """
        Detect outliers in the trajectory data.

        Parameters:
        trajectory (TrajectoryData): The trajectory data to be analyzed.

        Returns:
        TrajectoryData: The trajectory data with outliers marked or removed.
        """
        raise NotImplementedError


class ZScoreOutlierDetection(OutlierDetectionStrategy):
    def detect(self, trajectory: Trajectory, threshold: float = 3.0) -> pd.DataFrame:
        # Calculate Z-scores for each column
        z_scores = np.abs((trajectory - trajectory.mean()) / trajectory.std())
        # Mark outliers
        outliers = (z_scores > threshold).any(axis=1)
        trajectory[col_names.OUTLIER] = outliers
        return trajectory


class IQRBasedOutlierDetection(OutlierDetectionStrategy):
    def detect(self, trajectory: Trajectory) -> pd.DataFrame:
        # Calculate IQR for each column
        Q1 = trajectory.quantile(0.25)
        Q3 = trajectory.quantile(0.75)
        IQR = Q3 - Q1
        # Mark outliers
        outliers = (
            (trajectory < (Q1 - 1.5 * IQR)) | (trajectory > (Q3 + 1.5 * IQR))
        ).any(axis=1)
        trajectory[col_names.OUTLIER] = outliers
        return trajectory


class SpeedOutlierDetector(OutlierDetectionStrategy):
    def detect(self, trajectory: Trajectory, max_speed_ms: float) -> Trajectory:
        # Mark outliers
        trajectory[col_names.OUTLIER] = trajectory[col_names.SPEED].apply(
            lambda x: x > max_speed_ms
        )
        return trajectory


class OutlierDetector:
    def __init__(self, strategy: OutlierDetectionStrategy):
        self._strategy = strategy

    def set_strategy(self, strategy: OutlierDetectionStrategy):
        self._strategy = strategy

    def detect_outliers(self, trajectory: Trajectory, *args, **kwargs) -> Trajectory:
        # Apply the function to each group
        trajectory = trajectory.groupby(col_names.TRAJECTORY_ID).apply(
            lambda t: self._strategy.detect(t, *args, **kwargs)
        )
        return trajectory
