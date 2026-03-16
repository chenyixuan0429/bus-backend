# 导入 FastAPI 需要的库
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import socketio
import socketio
from starlette.middleware.wsgi import WSGIMiddleware
import gps_simulator
from fastapi import FastAPI
# 创建 FastAPI 应用实例
app = FastAPI(title="公交监控系统API")

# 配置 CORS（允许前端访问）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有来源
    allow_credentials=True,
    allow_methods=["*"],  # 允许所有 HTTP 方法
    allow_headers=["*"],  # 允许所有 HTTP 头
)

# 测试接口：访问 http://localhost:8000/ 会返回这个信息
@app.get("/")
async def root():
    return {"message": "公交监控系统后端运行正常"}

# 获取所有站点的接口
@app.get("/api/stations")
async def get_stations():
    """返回所有站点信息"""
    stations = [
        {"id": 1, "name": "颐和园", "lat": 39.999, "lng": 116.272, "order": 1},
        {"id": 2, "name": "西苑", "lat": 39.992, "lng": 116.286, "order": 2},
        {"id": 3, "name": "北京大学西门", "lat": 39.987, "lng": 116.302, "order": 3},
        {"id": 4, "name": "海淀桥北", "lat": 39.981, "lng": 116.309, "order": 4},
        {"id": 5, "name": "中关村", "lat": 39.978, "lng": 116.318, "order": 5},
        {"id": 6, "name": "中关村南", "lat": 39.972, "lng": 116.324, "order": 6}
    ]
    return stations

# 启动服务器
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

# 模拟公交车位置
@app.get("/api/buses")
async def get_buses():
    buses = [
        {
            "bus_id": "BUS001",
            "lat": 39.990,
            "lng": 116.290,
            "speed": 30
        },
        {
            "bus_id": "BUS002",
            "lat": 39.985,
            "lng": 116.300,
            "speed": 25
        }
    ]
    return buses