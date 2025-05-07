# (Strategy Pattern)
from abc import ABC, abstractmethod

import dask.dataframe as dd
import pandas as pd

from ..core.trajectory import Trajectory
from ..utils.config import col_names


class AccelerationCalculationStrategy(ABC):
    @abstractmethod
    def calculate(self, delta_speed: pd.Series, time: pd.Series) -> pd.Series:
        raise NotImplementedError


class SimpleAccelerationCalculation(AccelerationCalculationStrategy):
    def calculate(self, delta_speed: pd.Series, time: pd.Series) -> pd.Series:
        time = time.replace(0, pd.NA)
        acc = delta_speed / time
        return acc.fillna(0)


class AccelerationCalculator:
    def __init__(self, strategy: AccelerationCalculationStrategy):
        self._strategy = strategy

    def set_strategy(self, strategy: AccelerationCalculationStrategy):
        self._strategy = strategy

    def add_acceleration_column(self, trajectory: Trajectory) -> Trajectory:
        if col_names.SPEED not in trajectory.columns:
            raise ValueError(
                f"Column {col_names.SPEED} is missing in trajectory_data"
            )
        if col_names.DELTA_TIME not in trajectory.columns:
            raise ValueError(
                f"Column {col_names.DELTA_TIME} is missing in trajectory_data"
            )
        trajectory[col_names.PREV_SPEED] = trajectory.groupby(
            col_names.TRAJECTORY_ID
        )[col_names.SPEED].shift(1)

        trajectory[col_names.DELTA_SPEED] = (
            trajectory[col_names.SPEED] - trajectory[col_names.PREV_SPEED]
        )

        trajectory[col_names.ACCELERATION] = self._strategy.calculate(
            trajectory[col_names.DELTA_SPEED], trajectory[col_names.DELTA_TIME]
        )
        return trajectory
