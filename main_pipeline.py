import dask.dataframe as dd
import pandas as pd

import cde_plot_pyplot
import spatial_plot_geopandas_pyplot
from moveminer.utils.config import col_names

if __name__ == "__main__":
    anglova_categories = [
        "Company",
        "Company Type",
        "Platoon",
        "Platoon Type",
        "Vehicle Function",
        "Vehicle Type",
        "Command",
    ]
    point_metrics = [
        {"column": col_names.SPEED, "label": "Speed (km/h)"},
        {"column": col_names.ACCELERATION, "label": "Acceleration (km/h²)"},
        {"column": col_names.DISTANCE, "label": "Distance (km)"},
        {"column": col_names.DELTA_TIME, "label": "Delta Time (h)"},
    ]
    trajectory_metrics = [
        {"column": col_names.TOTAL_DISTANCE, "label": "Total Distance (km)"},
        {
            "column": col_names.STRAIGHT_LINE_DISTANCE,
            "label": "Straight Line Distance (km)",
        },
        {"column": col_names.PATH_TORTUOSITY, "label": "Path Tortuosity (km)"},
        {
            "column": col_names.RADIUS_GYRATION,
            "label": "Radius of Gyration (km)",
        },
    ]
    # Carrega os dados
    enriched_points = dd.read_csv(
        "./anglova_metrics_enriched/points_enriched_metrics.csv",
    ).compute()
    enriched_trajectories_df = pd.read_csv(
        "./anglova_metrics_enriched/trajectories_enriched_metrics.csv",
    )
    # Generate spatial plots
    # spatial_plot_geopandas_pyplot.main(enriched_points, anglova_categories)
    # Generate CDE plot by points
    cde_plot_pyplot.main(
        enriched_points,
        anglova_categories,
        point_metrics,
    )
    # Generate CDE plot by trajectories
    cde_plot_pyplot.main(
        enriched_trajectories_df,
        anglova_categories,
        trajectory_metrics,
    )
