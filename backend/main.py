# main.py

# 导入库
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

# 创建 FastAPI 应用
app = FastAPI(title="公交监控系统API")

# 允许跨域（前端能访问）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =====================
# 测试接口
# =====================
@app.get("/")
async def root():
    return {"message": "公交监控系统后端运行正常"}

# =====================
# 站点接口
# =====================
@app.get("/api/stations")
async def get_stations():
    return [
        {"id": 1, "name": "高能街广场", "lat": 38.8623, "lng": 121.5233, "order": 1},
        {"id": 2, "name": "高能街", "lat": 38.8630, "lng": 121.5220, "order": 2},
        {"id": 3, "name": "名仕智慧谷", "lat": 38.8640, "lng": 121.5200, "order": 3},
        {"id": 4, "name": "学子街", "lat": 38.8650, "lng": 121.5180, "order": 4},
        {"id": 5, "name": "敬贤街", "lat": 38.8635, "lng": 121.5250, "order": 5},
        {"id": 6, "name": "万达广场", "lat": 38.8614, "lng": 121.5285, "order": 6},
        {"id": 7, "name": "七贤岭地铁站", "lat": 38.8620, "lng": 121.5300, "order": 7},
        {"id": 8, "name": "信达街", "lat": 38.8605, "lng": 121.5350, "order": 8}
    ]

# =====================
# 公交车接口
# =====================
@app.get("/api/buses")
async def get_buses():
    return [
        {"bus_id": "BUS001", "lat": 39.990, "lng": 116.290, "speed": 30},
        {"bus_id": "BUS002", "lat": 39.985, "lng": 116.300, "speed": 25}
    ]

# =====================
# 启动服务器
# =====================
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)