from Estimation import Electricity, Water

# 调用 Water.py 中的 train_water_model 函数来重新训练模型
Water.train_water_model()
Electricity.train_electricity_model()
print("Model has been updated.")

