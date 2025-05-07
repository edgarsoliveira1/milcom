import datetime
from math import radians

import pytest
from moveminer.core.trajectory import Trajectory
from moveminer.metrics.direction_calculation import (
    HaversineDirectionAngleCalculation,
    DirectionAngleCalculator,
)
from moveminer.utils.config import col_names


def test_haversine_turning_angle_east():
    trajectory_data = Trajectory(
        {
            col_names.TRAJECTORY_ID: [1, 1],
            col_names.X: [0, 1],
            col_names.Y: [0, 0],
            col_names.T: [
                datetime.datetime(2019, 11, 1, 0, 0, 0)
                + datetime.timedelta(seconds=i)
                for i in range(2)
            ],
        }
    )
    turning_angle_calculation = DirectionAngleCalculator(
        HaversineDirectionAngleCalculation()
    )
    trajectory_data_with_distances = (
        turning_angle_calculation.add_direction_column(trajectory_data)
    )
    distances = trajectory_data_with_distances[col_names.DIRECTION]
    assert distances.iloc[0] == 0
    assert distances.iloc[1] == 90.0


def test_haversine_turning_angle_west():
    trajectory_data = Trajectory(
        {
            col_names.TRAJECTORY_ID: [1, 1],
            col_names.X: [0, -10],
            col_names.Y: [0, 0],
            col_names.T: [
                datetime.datetime(2019, 11, 1, 0, 0, 0)
                + datetime.timedelta(seconds=i)
                for i in range(2)
            ],
        }
    )
    turning_angle_calculation = DirectionAngleCalculator(
        HaversineDirectionAngleCalculation()
    )
    trajectory_data_with_distances = (
        turning_angle_calculation.add_direction_column(trajectory_data)
    )
    distances = trajectory_data_with_distances[col_names.DIRECTION]
    assert distances.iloc[0] == 0
    assert distances.iloc[1] == 270


def test_haversine_turning_angle_north():
    trajectory_data = Trajectory(
        {
            col_names.TRAJECTORY_ID: [1, 1],
            col_names.X: [0, 0],
            col_names.Y: [0, 10],
            col_names.T: [
                datetime.datetime(2019, 11, 1, 0, 0, 0)
                + datetime.timedelta(seconds=i)
                for i in range(2)
            ],
        }
    )
    turning_angle_calculation = DirectionAngleCalculator(
        HaversineDirectionAngleCalculation()
    )
    trajectory_data_with_distances = (
        turning_angle_calculation.add_direction_column(trajectory_data)
    )
    distances = trajectory_data_with_distances[col_names.DIRECTION]
    assert distances.iloc[0] == 0
    assert distances.iloc[1] == 0


def test_haversine_turning_angle_south():
    trajectory_data = Trajectory(
        {
            col_names.TRAJECTORY_ID: [1, 1],
            col_names.X: [0, 0],
            col_names.Y: [0, -10],
            col_names.T: [
                datetime.datetime(2019, 11, 1, 0, 0, 0)
                + datetime.timedelta(seconds=i)
                for i in range(2)
            ],
        }
    )
    turning_angle_calculation = DirectionAngleCalculator(
        HaversineDirectionAngleCalculation()
    )
    trajectory_data_with_distances = (
        turning_angle_calculation.add_direction_column(trajectory_data)
    )
    distances = trajectory_data_with_distances[col_names.DIRECTION]
    assert distances.iloc[0] == 0
    assert distances.iloc[1] == 180


def test_haversine_turning_angle_north_east():
    trajectory_data = Trajectory(
        {
            col_names.TRAJECTORY_ID: [1, 1],
            col_names.X: [0, 10],
            col_names.Y: [0, 10],
            col_names.T: [
                datetime.datetime(2019, 11, 1, 0, 0, 0)
                + datetime.timedelta(seconds=i)
                for i in range(2)
            ],
        }
    )
    turning_angle_calculation = DirectionAngleCalculator(
        HaversineDirectionAngleCalculation()
    )
    trajectory_data_with_distances = (
        turning_angle_calculation.add_direction_column(trajectory_data)
    )
    distances = trajectory_data_with_distances[col_names.DIRECTION]
    assert distances.iloc[0] == 0
    assert round(distances.iloc[1]) == 45


if __name__ == "__main__":
    pytest.main()
