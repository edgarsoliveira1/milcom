import math
from abc import ABC, abstractmethod

import dask.dataframe as dd
import numpy as np
import pandas as pd

from ..core.trajectory import Trajectory
from ..utils.config import col_names


class DirectionAngleCalculationStrategy(ABC):
    @abstractmethod
    def calculate(
        self,
        x1: pd.Series,
        y1: pd.Series,
        x2: pd.Series,
        y2: pd.Series,
    ) -> pd.Series:
        """
        Abstract method to calculate the turning angles for a trajectory.

        Parameters:
        trajectory (TrajectoryData): The trajectory data containing the coordinates of the points.

        Returns:
        TrajectoryData: The trajectory data with an additional column containing the calculated turning angles.
        """
        raise NotImplementedError


class EuclideanDirectionAngleCalculation(DirectionAngleCalculationStrategy):
    def calculate(
        self,
        x1: pd.Series,
        y1: pd.Series,
        x2: pd.Series,
        y2: pd.Series,
    ) -> pd.Series:
        # Calculate differences between consecutive points
        x_diff = x1 - x2
        y_diff = y1 - y2

        # Calculate angles between consecutive segments
        angles = np.arctan2(y_diff, x_diff)

        # Calculate turning angles
        turning_angle = np.diff(angles, prepend=angles[0])

        # Normalize turning angles to the range [-pi, pi]
        turning_angle = (turning_angle + np.pi) % (2 * np.pi) - np.pi

        # Add turning angles to the trajectory data
        return turning_angle


class HaversineDirectionAngleCalculation(DirectionAngleCalculationStrategy):
    def calculate(
        self,
        lat1: pd.Series,
        lon1: pd.Series,
        lat2: pd.Series,
        lon2: pd.Series,
    ) -> pd.Series:
        """
        Calcula o azimute (bearing) entre dois pontos geográficos.

        Parameters:
        lat1 (float): Latitude do primeiro ponto.
        lon1 (float): Longitude do primeiro ponto.
        lat2 (float): Latitude do segundo ponto.
        lon2 (float): Longitude do segundo ponto.

        Returns:
        float: O azimute (bearing) em graus.
        """

        lat1, lon1, lat2, lon2 = np.radians([lat1, lon1, lat2, lon2])
        lat1 = np.radians(lat1)
        lat2 = np.radians(lat2)

        delta_lon = np.radians(lon2 - lon1)

        x = np.sin(delta_lon) * np.cos(lat2)
        y = np.cos(lat1) * np.sin(lat2) - (
            np.sin(lat1) * np.cos(lat2) * np.cos(delta_lon)
        )
        bearing = np.degrees(np.arctan2(x, y))
        compass_bearing = (bearing + 360) % 360

        # Check if the points are equal
        equal_points = (lat1 == lat2) & (lon1 == lon2)

        # Set compass_bearing to NaN where points are equal
        compass_bearing = np.where(equal_points, np.nan, compass_bearing)

        return compass_bearing


class DirectionAngleCalculator:
    def __init__(self, strategy: DirectionAngleCalculationStrategy):
        self._strategy = strategy

    def set_strategy(self, strategy: DirectionAngleCalculationStrategy):
        self._strategy = strategy

    def add_direction_column(self, trajectory: Trajectory) -> Trajectory:
        trajectory[col_names.PREV_X] = trajectory.groupby(
            col_names.TRAJECTORY_ID
        )[col_names.X].shift(1)
        trajectory[col_names.PREV_Y] = trajectory.groupby(
            col_names.TRAJECTORY_ID
        )[col_names.Y].shift(1)
        trajectory = dd.from_pandas(
            trajectory, npartitions=trajectory.npartitions
        )
        trajectory[col_names.DIRECTION] = trajectory.map_partitions(
            lambda d: self._strategy.calculate(
                d[col_names.PREV_Y],
                d[col_names.PREV_X],
                d[col_names.Y],
                d[col_names.X],
            ),
            meta=(col_names.DIRECTION, "f8"),
        )
        # trajectory[col_names.DIRECTION] = trajectory.groupby(
        #     col_names.TRAJECTORY_ID
        # )[col_names.DIRECTION].apply(
        #     lambda group: group.replace(np.nan, method="ffill"),
        #     meta=(col_names.DIRECTION, "f8"),
        # )
        trajectory[col_names.DIRECTION] = trajectory[col_names.DIRECTION]
        return trajectory.compute()
