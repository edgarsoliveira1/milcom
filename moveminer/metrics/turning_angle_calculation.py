from abc import ABC, abstractmethod

import numpy as np
import pandas as pd

from ..core.trajectory import Trajectory
from ..utils.config import col_names


class TurningAngleCalculationStrategy(ABC):
    @abstractmethod
    def calculate(
        self,
        angle1: pd.Series,
        angle2: pd.Series,
    ) -> pd.Series:
        raise NotImplementedError


class TurningAngleCalculation(TurningAngleCalculationStrategy):
    def calculate(self, angle1, angle2) -> pd.Series:
        diff = np.abs(angle1 - angle2)
        diff = diff.where(~(angle1.isna() | angle2.isna()), np.nan)
        diff = diff.apply(lambda x: x if x <= 180 else np.abs(x - 360))
        return diff


class TurningAngleCalculator:
    def __init__(self, strategy: TurningAngleCalculationStrategy):
        self._strategy = strategy

    def set_strategy(self, strategy: TurningAngleCalculationStrategy):
        self._strategy = strategy

    def add_turning_angle_column(
        self, trajectory: Trajectory, **kwargs
    ) -> Trajectory:
        trajectory[col_names.PREV_DIRECTION] = trajectory.groupby(
            col_names.TRAJECTORY_ID
        )[col_names.DIRECTION].shift(1).fillna(np.nan)

        trajectory[col_names.TURNING_ANGLE] = (
            trajectory.groupby(col_names.TRAJECTORY_ID)
            .transform(lambda t: self._strategy.calculate(
                t[col_names.PREV_DIRECTION],
                t[col_names.DIRECTION],
            ))
        )

        return trajectory
