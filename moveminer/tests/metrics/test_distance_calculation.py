import datetime

import pytest
from moveminer.core.trajectory import Trajectory
from moveminer.metrics.distance_calculation import (
    DistanceCalculator,
    EuclideanDistanceCalculation,
    HaversineDistanceCalculation,
)
from moveminer.utils.config import col_names


@pytest.fixture
def trajectory_data():
    # The distance between Big Ben in London (51.5007° N, 0.1246° W) and
    # The Statue of Liberty in
    # New York (40.6892° N, 74.0445° W) is 5574.8 km.
    return Trajectory(
        {
            col_names.TRAJECTORY_ID: [1, 1],
            col_names.X: [-74.00597, -118.24368],
            col_names.Y: [40.71427, 34.05223],
            col_names.T: [
                datetime.datetime(2019, 11, 1, 0, 0, 0)
                + datetime.timedelta(seconds=i)
                for i in range(2)
            ],
        }
    )


def test_euclidean_distance_calculation(trajectory_data):
    distance_calculator = DistanceCalculator(EuclideanDistanceCalculation())
    trajectory_data_with_distances = distance_calculator.add_distance_column(
        trajectory_data
    )
    print(trajectory_data_with_distances)
    distances = trajectory_data_with_distances[col_names.DISTANCE]
    assert distances.iloc[0] == 0.0
    assert distances.iloc[1] == 44.736537226362294


def test_haversine_distance_calculation(trajectory_data):
    distance_calculator = DistanceCalculator(HaversineDistanceCalculation())
    trajectory_data_with_distances = distance_calculator.add_distance_column(
        trajectory_data
    )
    distances = trajectory_data_with_distances[col_names.DISTANCE]
    assert distances.iloc[0] == 0.0
    assert distances.iloc[1] == pytest.approx(3935735)


if __name__ == "__main__":
    pytest.main()
