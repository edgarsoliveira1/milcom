# (Strategy Pattern)
from abc import ABC, abstractmethod

import dask.dataframe as dd
import pandas as pd

from ..utils.config import col_names


# Estratégia de cálculo de delta time entre pontos
class DeltaTimeCalculationStrategy(ABC):
    @abstractmethod
    def calculate(self, t1: pd.Series, t2: pd.Series) -> pd.Series:
        """
        Calcula a distância entre dois pontos.

        Parameters:
        point_a (pd.Series): Um ponto com colunas 'x', 'y' e 't'.
        point_b (pd.Series): Outro ponto com colunas 'x', 'y' e 't'.

        Returns:
        float: A diferença de tempo calculada entre os dois pontos em segundos.
        """
        raise NotImplementedError


class HourDeltaTimeCalculation(DeltaTimeCalculationStrategy):
    def calculate(self, t1: pd.Series, t2: pd.Series) -> pd.Series:
        t1 = pd.to_datetime(t1, errors='coerce')
        t2 = pd.to_datetime(t2, errors='coerce')
        delta_time = (t2 - t1).dt.total_seconds() / 3600.0
        return delta_time.fillna(0)


class DeltaTimeCalculator:
    def __init__(self, strategy: DeltaTimeCalculationStrategy):
        if strategy is DeltaTimeCalculationStrategy:
            self._strategy = strategy()
        else:
            self._strategy = strategy

    def set_strategy(self, strategy: DeltaTimeCalculationStrategy):
        self._strategy = strategy

    def calculate_total_time(self, trajectory: pd.DataFrame) -> float:
        return trajectory.groupby(col_names.TRAJECTORY_ID)[
            col_names.DELTA_TIME
        ].sum()

    def add_delta_time_column(self, trajectory: pd.DataFrame) -> pd.DataFrame:
        # Function to calculate time difference within each group
        trajectory[col_names.PREV_T] = trajectory.groupby(
            col_names.TRAJECTORY_ID
        )[col_names.T].shift(1)

        # Apply the function to each group
        trajectory = dd.from_pandas(
            trajectory, npartitions=trajectory.npartitions
        )
        trajectory[col_names.DELTA_TIME] = trajectory.map_partitions(
            lambda d: self._strategy.calculate(
                d[col_names.PREV_T],
                d[col_names.T],
            ),
            meta=(col_names.DELTA_TIME, "f8"),
        )
        return trajectory.compute()
