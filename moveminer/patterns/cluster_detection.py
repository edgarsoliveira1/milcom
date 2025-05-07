from abc import ABC, abstractmethod

import pandas as pd
from sklearn.cluster import DBSCAN, KMeans

from ..core.trajectory import Trajectory
from ..utils.config import col_names


class ClusterDetectionStrategy(ABC):
    @abstractmethod
    def detect(self, trajectory: Trajectory, *args, **kwargs) -> Trajectory:
        """
        Detect clusters in the trajectory data.

        Parameters:
        trajectory (TrajectoryData): The trajectory data to be analyzed.

        Returns:
        TrajectoryData: The trajectory data with clusters marked.
        """
        raise NotImplementedError


class DBSCANClusterDetection(ClusterDetectionStrategy):
    def detect(
        self,
        trajectory: Trajectory,
        eps: float = 0.1,
        min_samples: int = 1,
        columns: list = [col_names.X, col_names.Y],
    ) -> pd.DataFrame:
        # Ensure that the necessary columns are present
        if (
            col_names.X not in trajectory.columns
            or col_names.Y not in trajectory.columns
        ):
            raise ValueError(
                f"Columns {col_names.X} and {col_names.Y} are required in trajectory"
            )

        # Extract coordinates
        coords = trajectory[columns].values

        # Apply DBSCAN clustering
        db = DBSCAN(
            eps=eps,
            min_samples=min_samples,
            metric="haversine",
            algorithm="ball_tree",
        ).fit(coords)
        labels = db.labels_

        # Add cluster labels to the trajectory data
        trajectory[col_names.CLUSTER] = labels
        return trajectory


class KMeansClusterDetection(ClusterDetectionStrategy):
    def detect(
        self, trajectory: Trajectory, n_clusters: int = 8, **kwargs
    ) -> pd.DataFrame:
        # Extract columns from kwargs or use default
        columns = kwargs.get('columns', [col_names.X, col_names.Y])
        
        # Ensure that the necessary columns are present
        if (
            col_names.X not in trajectory.columns
            or col_names.Y not in trajectory.columns
        ):
            raise ValueError(
                f"Columns {col_names.X} and {col_names.Y} are required in trajectory"
            )

        # Extract coordinates
        coords = trajectory[columns].values

        # Apply KMeans clustering
        kmeans = KMeans(n_clusters=n_clusters, random_state=0).fit(coords)
        labels = kmeans.labels_

        # Add cluster labels to the trajectory data
        trajectory[col_names.CLUSTER] = labels
        return trajectory


class ClusterDetector:
    def __init__(self, strategy: ClusterDetectionStrategy):
        self._strategy = strategy

    def set_strategy(self, strategy: ClusterDetectionStrategy):
        self._strategy = strategy

    def detect_clusters(self, trajectory: Trajectory, *args, **kwargs) -> Trajectory:
        return self._strategy.detect(trajectory, *args, **kwargs)