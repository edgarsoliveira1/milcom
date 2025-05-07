# Funções matemáticas genéricas
import hashlib

from dask.dataframe import DataFrame
from pandas import Series

from .config import col_names


def create_index(row: Series):
    return hashlib.md5(
        f"{row[col_names.T]}_{row[col_names.TRAJECTORY_ID]}".encode()
    ).hexdigest()


def set_unique_index(ddf: DataFrame):
    ddf["index"] = ddf.apply(create_index, axis=1)
    ddf = ddf.set_index("index", sorted=False)
    return ddf
