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