# (Strategy Pattern)
from abc import ABC, abstractmethod

import dask.dataframe as dd
import pandas as pd

from ..core.trajectory import Trajectory
from ..utils.config import col_names


class SpeedCalculationStrategy(ABC):
    @abstractmethod
    def calculate(self, distance: pd.Series, time: pd.Series) -> pd.Series:
        raise NotImplementedError


class SimpleSpeedCalculation(SpeedCalculationStrategy):
    def calculate(self, distance: pd.Series, time: pd.Series) -> pd.Series:
        time = time.replace(0, pd.NA)
        speed = distance / time
        return speed.fillna(0)


class SpeedCalculator:
    def __init__(self, strategy: SpeedCalculationStrategy):
        self._strategy = strategy

    def set_strategy(self, strategy: SpeedCalculationStrategy):
        self._strategy = strategy

    def add_speed_column(self, trajectory: Trajectory) -> Trajectory:
        # Ensure that the distance and time difference columns are present
        if col_names.DISTANCE not in trajectory.columns:
            raise ValueError(
                f"Column {col_names.DISTANCE} is missing in trajectory_data"
            )
        if col_names.DELTA_TIME not in trajectory.columns:
            raise ValueError(
                f"Column {col_names.DELTA_TIME} is missing in trajectory_data"
            )
        trajectory = dd.from_pandas(
            trajectory, npartitions=trajectory.npartitions
        )
        trajectory[col_names.SPEED] = trajectory.map_partitions(
            lambda t: self._strategy.calculate(
                t[col_names.DISTANCE],
                t[col_names.DELTA_TIME],
            ),
            meta=(col_names.SPEED, "f8"),
        )
        return trajectory.compute()
