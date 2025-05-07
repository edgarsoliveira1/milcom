from abc import ABC, abstractmethod
from typing import Union

import holoviews as hv
import hvplot.pandas
import numpy as np
import pandas as pd
from dask import dataframe as dd
from matplotlib import pyplot as plt

from ..utils.config import col_names


class PolarPlotStrategy(ABC):
    @abstractmethod
    def plot(self, column: pd.Series, *args, **kwargs) -> Union[hv.Element, hv.Overlay]:
        raise NotImplementedError("Subclasses should implement this method")


class HvPolarCurvePlotStrategy(PolarPlotStrategy):
    def plot(self, column: pd.Series, *args, **kwargs) -> hv.Element:
        counts, bin_edges = np.histogram(np.radians(column), bins=360)
        bin_centers = (
            bin_edges[:-1] + bin_edges[1:]
        ) / 2  # Pegando os centros dos bins

        return hv.Curve((bin_centers, counts), *args, **kwargs).options(
            backend="matplotlib", projection="polar"
        )


class HvPolarAreaPlotStrategy(PolarPlotStrategy):
    def plot(self, column: pd.Series, *args, **kwargs) -> hv.Element:
        counts, bin_edges = np.histogram(np.radians(column), bins=360)
        bin_centers = (
            bin_edges[:-1] + bin_edges[1:]
        ) / 2  # Pegando os centros dos bins

        return hv.Area((bin_centers, counts), *args, **kwargs).options(
            backend="matplotlib", projection="polar"
        )


class PyPlotPolarBarPlotStrategy(PolarPlotStrategy):
    def plot(self, column: pd.Series, *args, **kwargs) -> hv.Element:
        ax = plt.axes(projection="polar")
        plt.hist(np.radians(column), *args, **kwargs)
        ax.set_theta_zero_location("N")
        ax.set_rlabel_position(135)
        ax.set_axisbelow(True)
        return ax


class PolarPlotter:
    def __init__(self, strategy: PolarPlotStrategy):
        self._strategy = strategy

    def set_strategy(self, strategy: PolarPlotStrategy):
        self._strategy = strategy

    def plot(self, column: pd.Series, *args, **kwargs) -> Union[hv.Element, hv.Overlay]:
        return self._strategy.plot(column, *args, **kwargs)


# Example usage:
# data = pd.Series(np.random.randn(1000))
# plotter = PolarPlotter(HvPolarBarPlotStrategy())
# plot = plotter.plot(data, bins=30, color='red')
# hv.save(plot, 'polar_bar_plot.html')
