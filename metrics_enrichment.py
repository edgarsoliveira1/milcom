import os

import dask.dataframe as dd
import pandas as pd

from moveminer.core.trajectory import Trajectory
from moveminer.metrics.acceleration_calculation import (
    AccelerationCalculator,
    SimpleAccelerationCalculation,
)

from moveminer.metrics.direction_calculation import (
    DirectionAngleCalculator,
    HaversineDirectionAngleCalculation,
)
from moveminer.metrics.distance_calculation import (
    DistanceCalculator,
    HaversineDistanceCalculation,
)
from moveminer.metrics.radius_gyration import (
    HaversineRadiusGyrationCalculation,
    RadiusGyrationCalculator,
)
from moveminer.metrics.speed_calculation import (
    SimpleSpeedCalculation,
    SpeedCalculator,
)
from moveminer.metrics.time_diff_calculation import (
    DeltaTimeCalculator,
    HourDeltaTimeCalculation,
)
from moveminer.preprocessing.stop_detection import (
    SpeedStopDetection,
    StopDetector,
)
from moveminer.utils.config import col_names


def enrich_points_with_metrics(points_df: pd.DataFrame) -> pd.DataFrame:
    """
    Enrich points with metrics.
    Args:
        points_df (pd.DataFrame): DataFrame containing points data.
    Returns:
        pd.DataFrame: DataFrame with enriched metrics.
    """
    # Create a Trajectory object from the points DataFrame
    points_tr = Trajectory(points_df)

    # Sort the points DataFrame by trajectory ID and time
    points_tr = points_tr.sort_values([col_names.TRAJECTORY_ID, col_names.T])
    # Distance calculation
    distance_calculator = DistanceCalculator(HaversineDistanceCalculation())
    points_tr = distance_calculator.add_distance_column(points_tr)
    # Delta Time calculation
    delta_time_calculator = DeltaTimeCalculator(HourDeltaTimeCalculation())
    points_tr = delta_time_calculator.add_delta_time_column(points_tr)
    # Direction calculation
    diretion_calculator = DirectionAngleCalculator(
        HaversineDirectionAngleCalculation()
    )
    points_tr = diretion_calculator.add_direction_column(points_tr)
    # Speed calculation
    speed_calculator = SpeedCalculator(SimpleSpeedCalculation())
    points_tr = speed_calculator.add_speed_column(points_tr)
    # Acceleration calculation
    acceleration_calculator = AccelerationCalculator(
        SimpleAccelerationCalculation()
    )
    points_tr = acceleration_calculator.add_acceleration_column(points_tr)
    # Stop detection
    stop_detector = StopDetector(SpeedStopDetection())
    points_tr = stop_detector.add_stop_column(points_tr)
    # TODO Turn Angle calculation
    # turning_angle_calculator = TurningAngleCalculator(
    #     TurningAngleCalculation()
    # )
    # points_tr = turning_angle_calculator.add_turning_angle_column(points_tr)
    return points_tr


def enrich_trajectories_with_metrics(
    trajectories_df: pd.DataFrame,
    enriched_points_tr: Trajectory,
) -> pd.DataFrame:
    """
    Enrich trajectories with metrics.
    Args:
        trajectories_df (pd.DataFrame): DataFrame containing trajectories data.
    Returns:
        pd.DataFrame: DataFrame with enriched metrics.
    """
    # Create a Trajectory object from the points DataFrame
    trajectories_tr = Trajectory(trajectories_df)

    # Sort the points DataFrame by trajectory ID and time
    enriched_points_tr = enriched_points_tr.reset_index(drop=True).sort_values(
        [col_names.TRAJECTORY_ID, col_names.T]
    )
    trajectories_tr = trajectories_tr.sort_values([col_names.TRAJECTORY_ID])
    # Total distance calculation
    distance_calculator = DistanceCalculator(HaversineDistanceCalculation())
    trajectories_tr[col_names.TOTAL_DISTANCE] = (
        distance_calculator.calculate_total_distance(enriched_points_tr)
        .to_frame(name=col_names.TOTAL_DISTANCE)
        .reset_index()[col_names.TOTAL_DISTANCE]
    )
    # Straight line distance calculation
    trajectories_tr[col_names.STRAIGHT_LINE_DISTANCE] = (
        distance_calculator.calculate_straight_line_distance(
            enriched_points_tr
        ).reset_index()[col_names.STRAIGHT_LINE_DISTANCE]
    )
    # Path Tortuosity calculation
    trajectories_tr[col_names.PATH_TORTUOSITY] = (
        trajectories_tr[col_names.TOTAL_DISTANCE]
        / trajectories_tr[col_names.STRAIGHT_LINE_DISTANCE]
    )
    # Radius of Gyration calculation
    radius_gyration_calculator = RadiusGyrationCalculator(
        HaversineRadiusGyrationCalculation()
    )
    trajectories_tr[col_names.RADIUS_GYRATION] = (
        radius_gyration_calculator.calculate_radius_of_gyration(
            enriched_points_tr
        )
        .to_frame(name=col_names.RADIUS_GYRATION)
        .reset_index()[col_names.RADIUS_GYRATION]
    )
    # Time Stopped calculation
    trajectories_tr[col_names.TIME_STOPPED] = (
        enriched_points_tr[col_names.STOP]
        .groupby(enriched_points_tr[col_names.TRAJECTORY_ID])
        .sum()
    )
    # Destine Arrive Time

    return trajectories_tr


if __name__ == "__main__":
    output_dir = "./anglova_metrics_enriched"
    # Load the processed points
    points_path = "./anglova_processed/points_processed.csv"
    trajectories_path = "./anglova_processed/trajectories_processed.csv"
    points_processed_df = dd.read_csv(
        points_path,
        sep=",",
    ).compute()
    trajectories_processed_df = dd.read_csv(
        trajectories_path,
        sep=",",
    ).compute()
    # Enrich the points with metrics
    enriched_points_tr = enrich_points_with_metrics(points_processed_df)
    # Enrich the trajectories with metrics
    enriched_trajectories_df = enrich_trajectories_with_metrics(
        trajectories_processed_df, enriched_points_tr
    )
    # If output directory does not exist, create it
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    # Save the DataFrame to a CSV file
    enriched_points_tr.to_csv(
        f"{output_dir}/points_enriched_metrics.csv",
        index=False,
    )
    enriched_trajectories_df.to_csv(
        f"{output_dir}/trajectories_enriched_metrics.csv",
        index=False,
    )
    print("Enriched points and trajectories saved successfully.")
