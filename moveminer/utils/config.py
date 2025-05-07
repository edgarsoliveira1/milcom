# (Singleton Pattern)
from pyproj import Proj


class _Constants:
    def __init__(self):
        self.R = 6371  # Radius of the Earth in km


class _Projections:
    def __init__(self):
        self.WGS84 = Proj(init="epsg:4326")  # WGS84
        self.WEB_MERCATOR = Proj(init="epsg:3857")  # Web Mercator


class _ColumnNames:
    TRAJECTORY_ID = "trajectory_id"
    X = "x"
    Y = "y"
    T = "t"
    PREV_X = "prev_x"
    PREV_Y = "prev_y"
    PREV_T = "prev_t"
    FIRST_X = "first_x"
    FIRST_Y = "first_y"
    FIRST_T = "first_t"
    LAST_X = "last_x"
    LAST_Y = "last_y"
    LAST_T = "last_t"
    DELTA_TIME = "delta_time"
    DISTANCE = "distance"
    STRAIGHT_LINE_DISTANCE = "straight_line_distance"
    TOTAL_DISTANCE = "total_distance"
    SPEED = "speed"
    PREV_SPEED = "prev_speed"
    DELTA_SPEED = "delta_speed"
    ACCELERATION = "acceleration"
    STOP = "stop"
    SEGMENT_ID = "segment_id"
    OUTLIER = "outlier"
    CLUSTER = "cluster"
    POI = "poi"
    DIRECTION = "direction"
    PREV_DIRECTION = "prev_direction"
    TURNING_ANGLE = "turning_angle"
    ANOMALY_SCORE = "anomaly_score"
    PATH_TORTUOSITY = "path_tortuosity"
    TOTAL_DURATION = "total_duration"
    AVERAGE_SPEED = "average_speed"
    AVERAGE_ACCELERATION = "average_acceleration"
    RADIUS_GYRATION = "radius_gyration"
    TIME_STOPPED = "time_stopped"
    DESTINE_ARRIVE_TIME = "destine_arrive_time"
    DESTINE_DISTANCE = "destine_distance"


# Acesso às variáveis globais
projections = _Projections()
col_names = _ColumnNames()
constants = _Constants()
