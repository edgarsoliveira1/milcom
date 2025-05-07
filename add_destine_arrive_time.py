import dask.dataframe as dd
import pandas as pd

from moveminer.metrics.distance_calculation import (
    HaversineDistanceCalculation,
)

if __name__ == "__main__":
    # Carrega os dados
    enriched_points = dd.read_csv(
        "./anglova_metrics_enriched/points_enriched_metrics.csv",
    ).compute()
    enriched_trajectories_df = pd.read_csv(
        "./anglova_metrics_enriched/trajectories_enriched_metrics.csv",
    )
    # Quando cada veiculo chega a seu destino?
    t = enriched_points.copy()
    t["t"] = pd.to_datetime(t["t"])
    t = t.sort_values(by=["trajectory_id", "t"])
    # Get the last point for each trajectory_id
    last_points = t.groupby("trajectory_id").last().reset_index()

    # Add new columns for the last point coordinates
    t["last_x"] = t["trajectory_id"].map(
        last_points.set_index("trajectory_id")["x"]
    )
    t["last_y"] = t["trajectory_id"].map(
        last_points.set_index("trajectory_id")["y"]
    )

    haversine = HaversineDistanceCalculation()
    t["destine_distance"] = t.apply(
        lambda row: haversine.calculate(
            row["y"],
            row["x"],
            row["last_y"],
            row["last_x"],
        ),
        axis=1,
    )
    threshold = 0.001  # 100 metres
    # Define a threshold for distance (in degrees, approx 100 meters)
    t["destine_arrive"] = t["destine_distance"] < threshold
    destine_arrive_time = (
        t[t["destine_arrive"]]
        .groupby("trajectory_id")["t"]
        .min()
        .reset_index()
        .rename(columns={"t": "destine_arrive_time"})
    )

    destine_arrive_time.sort_values(by="destine_arrive_time").reset_index(
        drop=True
    )
    enriched_trajectories_df = enriched_trajectories_df.merge(
        destine_arrive_time, on="trajectory_id", how="left"
    )
    enriched_points.to_csv(
        "./anglova_metrics_enriched/points_enriched_metrics.csv",
        index=False,
    )
    enriched_trajectories_df.to_csv(
        "./anglova_metrics_enriched/trajectories_enriched_metrics.csv",
        index=False,
    )
