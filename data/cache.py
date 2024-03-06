import redis
from utils.config import REDIS_HOST, REDIS_PORT

cache = redis.Redis(host=REDIS_HOST, port=REDIS_PORT)

def get_risk_data(vehicle_id, action):
    key = f'risk:{vehicle_id}:{action}'
    risk_level = cache.get(key)
    if risk_level is None:
        # 從數據庫獲取並緩存
        session = Session()
        risk_data = session.query(RiskData).get((vehicle_id, action))
        if risk_data:
            risk_level = risk_data.risk_level
            cache.set(key, risk_level, ex=3600)  # 緩存1小時
        session.close()
    return risk_level