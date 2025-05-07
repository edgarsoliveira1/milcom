import dask.dataframe as dd
import pandas as pd

from ..utils.config import col_names, projections


class Trajectory(pd.DataFrame):
    @property
    def _constructor(self):
        return Trajectory

    def __init__(
        self,
        *args,
        crs=projections.WGS84,
        is_geo=True,
        npartitions=1,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.crs = crs
        self.is_geo = is_geo
        self.npartitions = npartitions
        # TODO: Verify if the input dataframe has the X, Y and T columns
        # TODO: Map the input dataframe column names
        # TODO: Set indeces

    def set_crs(self, crs):
        self.crs = crs

    def set_is_geo(self, is_geo):
        self.is_geo = is_geo

    @property
    def essential_columns(self):
        return [
            col_names.X,
            col_names.Y,
            col_names.T,
        ]

    @property
    def all_columns(self):
        return {
            attr: getattr(col_names, attr)
            for attr in dir(col_names)
            if not attr.startswith("__")
        }

    def get_essential_info(self):
        return {
            "crs": self.crs,
            "is_geo": self.is_geo,
            "columns": self.essential_columns,
            "head": self[self.essential_columns].head(),
        }
