# Histogram Plotting
from abc import ABC, abstractmethod
from typing import Union

import dask.dataframe as dd
import holoviews as hv
import hvplot.dask
import pandas as pd


class HistogramPlotStrategy(ABC):
    @abstractmethod
    def plot(self):
        raise NotImplementedError("Subclasses should implement this method")


class HvHistogramPlotStrategy(HistogramPlotStrategy):
    def plot(self, column: pd.Series, **kwargs):
        return column.hvplot.hist(**kwargs)


class HvKdePlotStrategy(HistogramPlotStrategy):
    def plot(self, column: pd.Series, *args, **kwargs):
        return column.hvplot.kde(*args, **kwargs)


class HistogramPlotter:
    def __init__(self, strategy: HistogramPlotStrategy):
        self._strategy = strategy

    def set_strategy(self, strategy: HistogramPlotStrategy):
        self._strategy = strategy

    def plot(
        self, column: pd.Series, *args, **kwargs
    ) -> Union[hv.Element, hv.Overlay]:
        return self._strategy.plot(column.reset_index(), *args, **kwargs)
