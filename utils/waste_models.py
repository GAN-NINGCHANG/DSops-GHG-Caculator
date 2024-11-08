import joblib

# 确定路径
file_path = '/workspaces/DSops-GHG-Caculator/utils/all_arima_models.pkl'

# 加载 pkl 文件
try:
    waste_forecast = joblib.load(file_path)
    print("Model loaded successfully.")
except FileNotFoundError:
    print("File not found. Please check the path.")
except Exception as e:
    print(f"An error occurred: {e}")
