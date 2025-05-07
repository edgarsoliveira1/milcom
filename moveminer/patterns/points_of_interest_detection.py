from abc import ABC, abstractmethod

import pandas as pd
from sklearn.cluster import KMeans

from ..core.trajectory import Trajectory
from ..utils.config import col_names


class PointsOfInterestStrategy(ABC):
    @abstractmethod
    def detect(self, trajectory: Trajectory, *args, **kwargs) -> Trajectory:
        """
        Detect points of interest in the trajectory data.

        Parameters:
        trajectory (Trajectory): The trajectory data to be analyzed.

        Returns:
        Trajectory: The trajectory data with points of interest marked.
        """
        raise NotImplementedError


class KMeansCentroids(PointsOfInterestStrategy):
    def detect(
        self,
        trajectory: Trajectory,
        n_clusters: int = 8,
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

        # Apply KMeans clustering
        kmeans = KMeans(n_clusters=n_clusters, random_state=0).fit(coords)
        labels = kmeans.labels_

        # Add points of interest labels to the trajectory data
        trajectory[col_names.POI] = labels

        # Compute centroids for each POI
        centroids = trajectory.groupby(col_names.POI)[
            [col_names.X, col_names.Y]
        ].mean()
        return centroids


class PointsOfInterestDetector:
    def __init__(self, strategy: PointsOfInterestStrategy):
        self._strategy = strategy

    def set_strategy(self, strategy: PointsOfInterestStrategy):
        self._strategy = strategy

    def detect_points_of_interest(
        self, trajectory: Trajectory, *args, **kwargs
    ) -> Trajectory:
        return self._strategy.detect(trajectory, *args, **kwargs)
