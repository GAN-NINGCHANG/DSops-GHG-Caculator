import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, GridSearchCV, KFold, cross_val_score
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score, mean_absolute_percentage_error, make_scorer
import pickle

def train_electricity_model(dataframe):
    """
    训练随机森林模型以预测建筑的电力消耗

    参数：
    dataframe (pd.DataFrame): 包含训练数据的 DataFrame

    返回：
    best_model: 训练好的随机森林模型
    """
    # 数据预处理：将建筑类型映射到数值编码，并转换建筑面积为数值格式
    dataframe['PBA_Encoded'] = dataframe['Building Type'].map({
        'Hotel': 0,
        'Mixed Development': 1,
        'Office': 2,
        'Retail': 3
    }).astype('category')
    
    # 将建筑面积 (SQFT) 转换为数值格式并转换为平方英尺
    dataframe['SQFT'] = dataframe['Gross Floor Area'].str.replace(',', '').astype(float) * 10.76
    
    # 选择模型所需的特征和目标变量
    X = dataframe[['SQFT', 'PBA_Encoded']]
    y = dataframe['2020EUI'] * dataframe['SQFT']

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

    # 使用最佳参数重新训练模型
    best_model = RandomForestRegressor(**best_params, random_state=21)
    kf = KFold(n_splits=5, shuffle=True, random_state=24)

    # 计算 R² 和 MAPE
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

    # 返回训练好的模型
    return best_model

# # 加载数据
# df = pd.read_csv('data/Electricity.csv')

# # 训练模型
# train_electricity_model(df)
