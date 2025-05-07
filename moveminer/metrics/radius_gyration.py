from abc import ABC, abstractmethod

import numpy as np
import pandas as pd

from ..core.trajectory import Trajectory
from ..utils.config import col_names, constants


class RadiusGyrationCalculationStrategy(ABC):
    @abstractmethod
    def calculate(self, trajectory: Trajectory) -> float:
        """
        Abstract method to calculate the radius of gyration for a trajectory.

        Parameters:
        trajectory (TrajectoryData): The trajectory data containing the coordinates of the points.

        Returns:
        float: The calculated radius of gyration.
        """
        raise NotImplementedError


class EuclideanRadiusGyrationCalculation(RadiusGyrationCalculationStrategy):
    def calculate(self, trajectory: Trajectory) -> float:
        # Calculate the center of mass
        x_mean = trajectory[col_names.X].mean()
        y_mean = trajectory[col_names.Y].mean()

        # Calculate the squared distances from the center of mass
        squared_distances = (trajectory[col_names.X] - x_mean) ** 2 + (
            trajectory[col_names.Y] - y_mean
        ) ** 2

        # Calculate the radius of gyration
        radius_of_gyration = np.sqrt(squared_distances.mean())
        return radius_of_gyration


class HaversineRadiusGyrationCalculation(RadiusGyrationCalculationStrategy):
    def calculate(self, trajectory: Trajectory) -> float:
        # Radius of the Earth in kilometers
        R = constants.R

        # Convert latitude and longitude to radians
        lat = np.radians(trajectory[col_names.Y])
        lon = np.radians(trajectory[col_names.X])

        # Calculate the center of mass in radians
        lat_mean = np.radians(trajectory[col_names.Y].mean())
        lon_mean = np.radians(trajectory[col_names.X].mean())

        # Calculate the squared Haversine distances from the center of mass
        dlat = lat - lat_mean
        dlon = lon - lon_mean
        a = (
            np.sin(dlat / 2.0) ** 2
            + np.cos(lat_mean) * np.cos(lat) * np.sin(dlon / 2.0) ** 2
        )
        c = 2 * np.arcsin(np.sqrt(a))
        squared_distances = (R * c) ** 2

        # Calculate the radius of gyration
        radius_of_gyration = np.sqrt(squared_distances.mean())
        return radius_of_gyration


class RadiusGyrationCalculator:
    def __init__(self, strategy: RadiusGyrationCalculationStrategy):
        self._strategy = strategy

    def set_strategy(self, strategy: RadiusGyrationCalculationStrategy):
        self._strategy = strategy

    def calculate_radius_of_gyration(self, trajectory_data: Trajectory) -> pd.DataFrame:
        return trajectory_data.groupby(col_names.TRAJECTORY_ID).apply(
            self._strategy.calculate
        )
