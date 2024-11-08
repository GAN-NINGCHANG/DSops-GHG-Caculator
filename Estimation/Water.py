import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import r2_score
import xgboost as xgb
import pickle
# from sqlalchemy import create_engine

def train_water_model():
    #     # MySQL 数据库连接信息
    # user = 'your_username'         # 用户名
    # password = 'your_password'     # 密码
    # host = 'your_host'             # 主机（例如 'localhost' 或 IP 地址）
    # port = '3306'                  # MySQL 端口，通常为 3306
    # database = 'your_database'     # 数据库名称
    # table_name = 'your_table'      # 表名（包含水资源数据）

    # # 创建数据库连接
    # engine = create_engine(f'mysql+pymysql://{user}:{password}@{host}:{port}/{database}')
    
    # # 从数据库中读取数据
    # query = f"SELECT * FROM {table_name}"
    # df = pd.read_sql(query, engine)
    # 加载数据
    df = pd.read_csv('data/Water data2.csv', encoding='ISO-8859-1')
    
    # 将 PBA.1 列设置为类别变量
    df['PBA'] = df['PBA'].replace({1: 0, 2: 1, 3: 2, 4: 3}).astype('category')
    X = df[['SQFT', 'NWKER', 'PBA']]
    y = df['WTCNS']

    # 数据集拆分
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.05, random_state=42)

    # XGBoost 模型定义和参数网格
    xgb_model = xgb.XGBRegressor(objective='reg:squarederror', enable_categorical=True, random_state=42)
    param_grid = {
        'n_estimators': [50, 100, 200],
        'learning_rate': [0.01, 0.1, 0.3],
        'max_depth': [3, 5, 7]
    }

    # 参数优化
    grid_search = GridSearchCV(estimator=xgb_model, param_grid=param_grid, scoring='r2', cv=5, n_jobs=-1)
    grid_search.fit(X_train, y_train)
    best_params = grid_search.best_params_
    print("Best parameters:", best_params)

    # 使用最佳参数重新训练模型
    xgb_best_model = xgb.XGBRegressor(**best_params, enable_categorical=True, random_state=42)
    xgb_best_model.fit(X_train, y_train)

    # 模型评估
    y_pred_best = xgb_best_model.predict(X_test)
    r2_best = r2_score(y_test, y_pred_best)
    print(f'R2 Score: {r2_best}')

    # 保存模型
    model_path = 'utils/water_model.pkl'
    with open(model_path, 'wb') as f:
        pickle.dump(xgb_best_model, f)

    print("Water model has been saved to:", model_path)

    # 返回训练好的模型
    return xgb_best_model

# 调用函数以训练和保存模型
train_water_model()
