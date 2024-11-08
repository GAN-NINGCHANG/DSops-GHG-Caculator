import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, GridSearchCV, KFold, cross_val_score
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score, mean_absolute_percentage_error, make_scorer
import pickle
# from sqlalchemy import create_engine

def train_electricity_model():
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
    # 数据读取与预处理
    df = pd.read_excel('data/Listing of Building Energy Performance Data for 2020.xlsx').iloc[:, 3:]
    df.columns = ['PBA_Encoded', 'size', 'Beginning Year', 'green mark rating', 'green mark year',
                  'green mark type', 'SQFT', 'AC percent', 'monthly occupation rate', 'number of hotel rooms',
                  'AC Type', 'age of chiller', 'AC Efficiency', 'last chiller check year', 'LED percent',
                  'Use of PV', '2017EUI', '2018EUI', '2019EUI', '2020EUI']
    df = df.loc[:, ['SQFT', 'PBA_Encoded', '2020EUI']].dropna()
    df['SQFT'] = df['SQFT'] * 10.76
    df['PBA_Encoded'] = df['PBA_Encoded'].map({'Hotel': 0, 'Mixed Development': 1, 'Office': 2, 'Retail': 3}).astype('category')

    # 模型特征和目标变量
    X = df.drop('2020EUI', axis=1)
    y = df['2020EUI'] * df['SQFT']

    # 定义评分器
    r2_scorer = make_scorer(r2_score, greater_is_better=True)
    mape_scorer = make_scorer(mean_absolute_percentage_error, greater_is_better=False)

    # 超参数调优
    param_grid = {
        'n_estimators': [50, 100, 200],
        'max_depth': [None, 10, 20, 30],
        'min_samples_split': [2, 5, 10],
        'min_samples_leaf': [1, 2, 4],
        'max_features': [None, 'sqrt', 'log2']
    }

    model = RandomForestRegressor(random_state=5105)
    grid_search = GridSearchCV(
        estimator=model,
        param_grid=param_grid,
        scoring=r2_scorer,
        cv=2,
        n_jobs=-1,
        verbose=2
    )
    grid_search.fit(X, y)
    best_params = grid_search.best_params_
    print("Best parameters:", best_params)

    # 用最佳参数重新训练模型
    best_model = RandomForestRegressor(**best_params, random_state=21)
    k = 5
    kf = KFold(n_splits=k, shuffle=True, random_state=24)

    # 计算 R^2 和 MAPE
    r2_scores = cross_val_score(best_model, X, y, cv=kf, scoring=r2_scorer)
    mean_r2 = np.mean(r2_scores)
    print("R^2 scores:", r2_scores)
    print("Mean R^2:", mean_r2)

    mape_scores = -cross_val_score(best_model, X, y, cv=kf, scoring=mape_scorer)
    mean_mape = np.mean(mape_scores)
    print("MAPE scores:", mape_scores)
    print("Mean MAPE:", mean_mape)

    # 分割数据集并训练模型
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=5202)
    best_model.fit(X_train, y_train)

    # 保存模型
    model_path = 'utils/electricity_rf_model.pkl'
    with open(model_path, 'wb') as file:
        pickle.dump(best_model, file)
    print("Model has been saved to:", model_path)

    # 输出模型和评价指标
    print("Training complete. Model and evaluation metrics are available.")
