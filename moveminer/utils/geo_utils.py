# Adapter Patterns
# Funções relacionadas à manipulação de coordenadas geográficas
from pyproj import transform

from ..core.trajectory import Trajectory
from .config import projections


class TrajectoryAdapter:
    def __init__(self, trajectory_data: Trajectory):
        self.trajectory_data = trajectory_data

    def get_projected_data(self):
        if not self.trajectory_data.is_geo:
            raise ValueError("Data must be in geographic coordinates")
        x, y = transform(
            self.trajectory_data.crs,
            projections.WEB_MERCATOR,
            self.trajectory_data.x.values,
            self.trajectory_data.y.values,
        )
        self.trajectory_data.x = x
        self.trajectory_data.y = y
        return self.trajectory_data


# Function to project coordinates
def project_to_web_mercator(trajectory_data: Trajectory) -> Trajectory:
    adapter = TrajectoryAdapter(trajectory_data)
    return adapter.get_projected_data()
