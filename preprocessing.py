import datetime
import os

import dask.dataframe as dd
import numpy as np
import pandas as pd

from moveminer.utils.config import col_names


# Define a function to calculate cosine of an angle in degrees
def cosd(degrees):
    return np.cos(np.radians(degrees))


def load_format_anglova_points(path: str) -> pd.DataFrame:
    dataset = dd.read_csv(
        path,
        sep=",",
    )
    dataset[col_names.TRAJECTORY_ID] = dataset["id"]
    # Fix Projection
    Alon = dataset["lon"]
    Alat = dataset["lat"]
    dataset[col_names.Y] = Alat + 7.9133854851
    dataset[col_names.X] = (Alon - 7.88017769562444) * cosd(Alat) / cosd(
        dataset[col_names.Y]
    ) + 23.0
    initial_datetime = datetime.datetime(2019, 9, 17)
    dataset["time"] = dataset["time"].astype("int")
    # Convert time to datetime
    dataset[col_names.T] = dd.to_datetime(
        dataset["time"],
        unit="s",
        origin=initial_datetime,
    )
    # Drop unnecessary columns
    dataset = dataset.drop(columns=["id", "lon", "lat", "time"])
    return dataset.compute()


def load_format_anglova_trajectories(path: str) -> pd.DataFrame:
    dataset = dd.read_csv(
        path,
        sep=",",
        usecols=[
            "Id",
            "Company",
            "Company type",
            "Platoon",
            "Platoon Type",
            "Vehicle function",
            "Vehicle type",
            "Command",
        ],
    )
    dataset = dataset.rename(
        columns={
            "Id": col_names.TRAJECTORY_ID,
            "Company type": "Company Type",
            "Vehicle function": "Vehicle Function",
            "Vehicle type": "Vehicle Type",
        }
    )
    dataset["Vehicle Type"] = dataset["Vehicle Type"].fillna("Unknown")
    dataset["Command"] = dataset["Command"].fillna("Unknown")
    return dataset.compute()


if __name__ == "__main__":
    # Example usage
    output_dir = "./anglova_processed"
    points_path = "./anglova/latlong.csv"
    trajectories_path = "./anglova/anglovavignette2battalion - Details.csv"
    points_processed = load_format_anglova_points(points_path)
    trajectories_processed = load_format_anglova_trajectories(
        trajectories_path
    )
    # Data Fusion
    points_processed = points_processed.merge(
        trajectories_processed,
        on=col_names.TRAJECTORY_ID,
        how="left",
    )
    # If output directory does not exist, create it
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    # Save the DataFrame to a CSV file
    points_processed.to_csv(f"{output_dir}/points_processed.csv", index=False)
    trajectories_processed.to_csv(
        f"{output_dir}/trajectories_processed.csv", index=False
    )
