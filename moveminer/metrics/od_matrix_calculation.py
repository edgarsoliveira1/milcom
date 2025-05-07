from abc import ABC, abstractmethod

import pandas as pd

from ..core.trajectory import Trajectory
from ..utils.config import col_names


class ODMatrixCalculationStrategy(ABC):
    @abstractmethod
    def calculate(self, trajectory: Trajectory) -> pd.DataFrame:
        """
        Abstract method to calculate the origin-destination matrix for a trajectory.

        Parameters:
        trajectory (pd.DataFrame): The trajectory data containing the coordinates of the points.

        Returns:
        pd.DataFrame: The calculated origin-destination matrix.
        """
        raise NotImplementedError


# class ClusterODMatrixCalculation(ODMatrixCalculationStrategy):
#     def calculate(self, trajectory: Trajectory) -> pd.DataFrame:
#         # Sort the trajectory by time
#         # trajectory = trajectory.sort_values(col_names.T)

#         # Get the unique clusters
#         clusters = trajectory[col_names.CLUSTER].unique()
#         # n_clusters = len(clusters)

#         # Initialize the OD matrix with zeros
#         od_matrix = pd.DataFrame(0, index=clusters, columns=clusters)

#         # Group by trajectory ID and calculate the OD pairs
#         grouped = trajectory.groupby(col_names.TRAJECTORY_ID)
#         for _, group in grouped:
#             origin = group.iloc[0][col_names.CLUSTER]
#             destination = group.iloc[-1][col_names.CLUSTER]
#             od_matrix.at[origin, destination] += 1

#         return od_matrix


class ClusterODMatrixCalculation(ODMatrixCalculationStrategy):
    def calculate(self, trajectory: Trajectory) -> pd.DataFrame:
        # Initialize a dictionary to store the OD pairs and their counts
        od_dict = {}

        # Group by trajectory ID and calculate the OD pairs
        grouped = trajectory.groupby(col_names.TRAJECTORY_ID)
        for _, group in grouped:
            origin = group.iloc[0][col_names.CLUSTER]
            destination = group.iloc[-1][col_names.CLUSTER]
            if (origin, destination) in od_dict:
                od_dict[(origin, destination)] += 1
            else:
                od_dict[(origin, destination)] = 1

        # Convert the dictionary to a DataFrame
        od_matrix = pd.DataFrame(
            [
                (origin, destination, flow)
                for (origin, destination), flow in od_dict.items()
            ],
            columns=["Origin", "Destination", "Flow"],
        )

        return od_matrix


class ODMatrixCalculator:
    def __init__(self, strategy: ODMatrixCalculationStrategy):
        self._strategy = strategy

    def set_strategy(self, strategy: ODMatrixCalculationStrategy):
        self._strategy = strategy

    def calculate_od_matrix(
        self, trajectory: Trajectory, *args, **kwargs
    ) -> pd.DataFrame:
        return self._strategy.calculate(trajectory, *args, **kwargs)
