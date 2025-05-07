# from ..core.metrics import MetricsCalculator
# from ..core.preprocessing import NoiseFilter
# from ..core.visualization import PointPlotter


# class MobilityAnalysisBuilder:
#     def __init__(self, trajectory_data):
#         self.trajectory_data = trajectory_data
#         self.pipeline = []

#     def add_noise_filter(self):
#         self.pipeline.append(NoiseFilter())
#         return self

#     def add_distance_calculator(self):
#         self.pipeline.append(MetricsCalculator())
#         return self

#     def add_visualizer(self):
#         self.pipeline.append(PointPlotter())
#         return self

#     def run(self):
#         data = self.trajectory_data
#         for step in self.pipeline:
#             data = step.process(data)
#         return data
