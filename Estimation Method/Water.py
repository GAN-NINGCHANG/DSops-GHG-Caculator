import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import mean_squared_error
from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import GradientBoostingRegressor
from statsmodels.tsa.arima.model import ARIMA
from sklearn.metrics import r2_score
from sklearn.metrics import mean_absolute_error
import warnings
import xgboost as xgb
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import GridSearchCV

df = pd.read_csv('Water data2.csv', encoding='ISO-8859-1')
label_encoder = LabelEncoder()
df['PBA_Encoded'] = label_encoder.fit_transform(df['PBA.1'])
df['PBA_Encoded'] = pd.Categorical(df['PBA_Encoded'])
X = df[['SQFT', 'NWKER', 'PBA_Encoded']]
y = df['WTCNS']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.05, random_state=42)

# XGBoost
xgb_model = xgb.XGBRegressor(objective='reg:squarederror', enable_categorical=True, random_state=42)

param_grid = {
    'n_estimators': [50, 100, 200],
    'learning_rate': [0.01, 0.1, 0.3],
    'max_depth': [3, 5, 7]
}

# GridSearchCV
grid_search = GridSearchCV(estimator=xgb_model, param_grid=param_grid, scoring='r2', cv=5, n_jobs=-1)
grid_search.fit(X_train, y_train)
best_params = grid_search.best_params_
print("Best parameter:", best_params)

# XGBRegressor
xgb_best_model = xgb.XGBRegressor(**best_params, enable_categorical=True, random_state=42)
xgb_best_model.fit(X_train, y_train)

y_pred_best = xgb_best_model.predict(X_test)
r2_best = r2_score(y_test, y_pred_best)

print(f'R2 Score: {r2_best}')

# Input
new_data = {
    'SQFT': 30000,
    'NWKER': 180,  
    'PBA_Encoded':1
}
new_data_df = pd.DataFrame([new_data])
new_prediction = xgb_best_model.predict(new_data_df)

print(f'Predicted water usage: {new_prediction[0]}')

