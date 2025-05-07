# # Implemente o Factory Pattern para inicializar objetos com diferentes
# # estratégias.
# from ..core.clustering import StayPointDetector
# from ..core.strategies import DBSCANStayPointDetection, ThresholdStayPointDetection


# class MobilityFactory:
#     @staticmethod
#     def get_stay_point_detector(method="dbscan"):
#         if method == "dbscan":
#             return StayPointDetector(DBSCANStayPointDetection())
#         elif method == "threshold":
#             return StayPointDetector(ThresholdStayPointDetection())
#         else:
#             raise ValueError("Método desconhecido para Stay Point Detection")
