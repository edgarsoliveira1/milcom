# Heatmap Plotting
from abc import ABC, abstractmethod
from typing import Union

import holoviews as hv
import pandas as pd


class HeatmapPlotStrategy(ABC):
    @abstractmethod
    def plot(self):
        raise NotImplementedError("Subclasses should implement this method")


class HvHeatmapPlotStrategy(HeatmapPlotStrategy):
    def plot(self, od_df: pd.DataFrame, *args, **kwargs):
        heatmap = list(od_df.itertuples(index=False, name=None))
        return hv.HeatMap(heatmap).opts(*args, **kwargs)


class HeatmapPlotter:
    def __init__(self, strategy: HeatmapPlotStrategy):
        self._strategy = strategy

    def set_strategy(self, strategy: HeatmapPlotStrategy):
        self._strategy = strategy

    def plot(
        self, od_df: pd.DataFrame, *args, **kwargs
    ) -> Union[hv.Element, hv.Overlay]:
        return self._strategy.plot(od_df, *args, **kwargs)
