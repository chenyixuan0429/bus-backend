import time
import random
import threading
import socketio
from math import sin, cos, sqrt, atan2, radians

# 创建Socket.IO服务器
sio = socketio.Server(cors_allowed_origins='*')

# 站点数据
STATIONS = [
    {"id": 1, "name": "万达广场", "lng": 121.788651, "lat": 39.062107},
    {"id": 2, "name": "艺术学院", "lng": 121.784879, "lat": 39.056556},
    {"id": 3, "name": "开发区安盛", "lng": 121.784519, "lat": 39.051896},
    {"id": 4, "name": "友谊商城", "lng": 121.786108, "lat": 39.048847},
    {"id": 5, "name": "盛京大连医院", "lng": 121.778239, "lat": 39.043123},
    {"id": 6, "name": "红梅小区", "lng": 121.772117, "lat": 39.048274},
    {"id": 7, "name": "翠竹南里", "lng": 121.767796, "lat": 39.044036},
    {"id": 8, "name": "东芝", "lng": 121.765627, "lat": 39.050391},
    {"id": 9, "name": "王子", "lng": 121.764896, "lat": 39.053590},
    {"id": 10, "name": "工业区", "lng": 121.764266, "lat": 39.070369},
    {"id": 11, "name": "炮台山公园", "lng": 121.771517, "lat": 39.055296},
    {"id": 12, "name": "万宝至", "lng": 121.773013, "lat": 39.059557},
    {"id": 13, "name": "佳能", "lng": 121.775888, "lat": 39.063085},
    {"id": 14, "name": "通世泰", "lng": 121.781564, "lat": 39.067109},
    {"id": 15, "name": "十里岗", "lng": 121.767873, "lat": 39.076099},
    {"id": 16, "name": "恒盛阳光美麓", "lng": 121.767331, "lat": 39.081237},
    {"id": 17, "name": "桃园", "lng": 121.765191, "lat": 39.082786},
    {"id": 18, "name": "鸿玮澜山", "lng": 121.769634, "lat": 39.083343},
    {"id": 19, "name": "八里", "lng": 121.755694, "lat": 39.087824},
    {"id": 20, "name": "左岸阳光", "lng": 121.752964, "lat": 39.087701},
    {"id": 21, "name": "金纺", "lng": 121.743834, "lat": 39.086887},
    {"id": 22, "name": "万科城", "lng": 121.739208, "lat": 39.090413},
    {"id": 23, "name": "盛滨", "lng": 121.733554, "lat": 39.094926},
    {"id": 24, "name": "金州体育场", "lng": 121.729594, "lat": 39.098697},
    {"id": 25, "name": "行政服务中心", "lng": 121.725833, "lat": 39.102469},
    {"id": 26, "name": "区一院", "lng": 121.723453, "lat": 39.104327},
    {"id": 27, "name": "向应公园北门", "lng": 121.723110, "lat": 39.106550}
]

# 提取路径
route_points = [[s["lat"], s["lng"]] for s in STATIONS]

class BusSimulator:
    def __init__(self, bus_id, start_point_index=0):
        self.bus_id = bus_id
        self.current_segment = start_point_index
        self.progress = random.random()
        self.speed = random.uniform(20, 40) / 3.6
        self.last_update = time.time()

    def get_position(self):
        start_idx = self.current_segment % len(route_points)
        end_idx = (self.current_segment + 1) % len(route_points)

        start_point = route_points[start_idx]
        end_point = route_points[end_idx]

        now = time.time()
        dt = now - self.last_update
        self.last_update = now

        distance = self.speed * dt

        lat1, lon1 = radians(start_point[0]), radians(start_point[1])
        lat2, lon2 = radians(end_point[0]), radians(end_point[1])

        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = sin(dlat/2)**2 + cos(lat1)*cos(lat2)*sin(dlon/2)**2
        c = 2 * atan2(sqrt(a), sqrt(1-a))
        segment_len = 6371000 * c

        self.progress += distance / segment_len

        while self.progress >= 1:
            self.progress -= 1
            self.current_segment = (self.current_segment + 1) % len(route_points)

        lat = start_point[0] + (end_point[0] - start_point[0]) * self.progress
        lng = start_point[1] + (end_point[1] - start_point[1]) * self.progress

        return {
            "vehicle_id": self.bus_id,
            "longitude": round(lng, 6),
            "latitude": round(lat, 6),
            "speed": round(self.speed * 3.6, 1),
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(now))
        }

# 3辆车
buses = [
    BusSimulator("bus_1", 0),
    BusSimulator("bus_2", 3),
    BusSimulator("bus_3", 6)
]

# 广播
def broadcast():
    while True:
        positions = [bus.get_position() for bus in buses]

        sio.emit('bus_update', {
            "status": "success",
            "data": positions
        })

        time.sleep(1)

threading.Thread(target=broadcast, daemon=True).start()

@sio.event
def connect(sid, environ):
    print("连接:", sid)

@sio.event
def disconnect(sid):
    print("断开:", sid)