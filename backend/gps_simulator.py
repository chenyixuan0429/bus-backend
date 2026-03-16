import time
import random
import threading
import socketio
from math import sin, cos, sqrt, atan2, radians

# 创建Socket.IO服务器
sio = socketio.Server(cors_allowed_origins='*')

# 线路数据（从main.py复制过来）
STATIONS = [
    {"id": 1, "name": "颐和园", "lat": 39.999, "lng": 116.272, "order": 1},
    {"id": 2, "name": "西苑", "lat": 39.992, "lng": 116.286, "order": 2},
    {"id": 3, "name": "北京大学西门", "lat": 39.987, "lng": 116.302, "order": 3},
    {"id": 4, "name": "海淀桥北", "lat": 39.981, "lng": 116.309, "order": 4},
    {"id": 5, "name": "中关村", "lat": 39.978, "lng": 116.318, "order": 5},
    {"id": 6, "name": "中关村南", "lat": 39.972, "lng": 116.324, "order": 6}
]

# 提取坐标点用于路径规划
route_points = [[s["lat"], s["lng"]] for s in STATIONS]

class BusSimulator:
    """公交车模拟器"""
    def __init__(self, bus_id, start_point_index=0):
        self.bus_id = bus_id
        self.current_segment = start_point_index
        self.progress = random.random()
        self.speed = random.uniform(20, 40) / 3.6  # 转换为 m/s
        self.last_update = time.time()

    def get_position(self):
        """计算当前位置"""
        start_idx = self.current_segment % len(route_points)
        end_idx = (self.current_segment + 1) % len(route_points)
        start_point = route_points[start_idx]
        end_point = route_points[end_idx]
        now = time.time()
        time_diff = now - self.last_update
        self.last_update = now
        distance_moved = self.speed * time_diff  # 米
        lat1, lon1 = radians(start_point[0]), radians(start_point[1])
        lat2, lon2 = radians(end_point[0]), radians(end_point[1])
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))
        segment_length = 6371000 * c  # 地球半径6371km，转为米
        self.progress += distance_moved / segment_length
        while self.progress >= 1.0 and self.current_segment < len(route_points) * 2:
            self.progress -= 1.0
            self.current_segment += 1
            if self.current_segment >= len(route_points):
                self.current_segment = 0
        lat = start_point[0] + (end_point[0] - start_point[0]) * self.progress
        lng = start_point[1] + (end_point[1] - start_point[1]) * self.progress
        return {
            "bus_id": self.bus_id,
            "lat": round(lat, 6),
            "lng": round(lng, 6),
            "speed": round(self.speed * 3.6, 1),  # 转回km/h
            "timestamp": now
        }

# 创建3辆公交车
buses = [
    BusSimulator("BUS001", 0),
    BusSimulator("BUS002", 2),
    BusSimulator("BUS003", 4)
]

# 广播公交车位置
def broadcast_positions():
    """定时广播所有公交车位置"""
    while True:
        positions = []
        for bus in buses:
            pos = bus.get_position()
            positions.append(pos)
            sio.emit('bus_update', pos)
        sio.emit('all_buses', positions)
        time.sleep(1)  # 每秒更新一次

# 在新线程中启动广播
threading.Thread(target=broadcast_positions, daemon=True).start()

# 客户端连接事件
@sio.event
def connect(sid, environ):
    print(f"客户端 {sid} 已连接")

@sio.event
def disconnect(sid):
    print(f"客户端 {sid} 已断开")