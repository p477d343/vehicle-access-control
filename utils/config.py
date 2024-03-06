import os
from dotenv import load_dotenv

# 從 .env 文件加載環境變數
load_dotenv()

# 從環境變數中獲取配置
DB_PATH = os.environ.get('RISK_DB_PATH', 'data/risk_data.db')
SERVER_HOST = os.environ.get('SERVER_HOST', '0.0.0.0')
SERVER_PORT = int(os.environ.get('SERVER_PORT', 8000))
SECRET_KEY = os.environ.get('SECRET_KEY', 'your-secret-key')