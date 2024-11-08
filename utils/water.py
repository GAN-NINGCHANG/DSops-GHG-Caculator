from flask import Flask, request, jsonify
import joblib
import pandas as pd
import xgboost as xgb

# 创建 Flask 应用
app = Flask(__name__)

# 加载模型
model = joblib.load('/workspaces/DSops-GHG-Caculator/utils/water_model.pkl')

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    SQFT = data.get('SQFT')
    NWKER = data.get('NWKER')
    PBA_Encoded = data.get('PBA_Encoded')

    # 构建 DataFrame 用于模型预测
    input_data = pd.DataFrame([[sqft, nwker, pba_encoded]], columns=['SQFT', 'NWKER', 'PBA_Encoded'])
    prediction = model.predict(input_data)

    return jsonify({'prediction': prediction[0]})

if __name__ == '__main__':
    app.run(debug=False)
