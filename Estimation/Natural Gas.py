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

file_path_gas = './Natural Gas data.xlsx'
df_gas = pd.read_excel(file_path_gas)

df_no = df_gas.dropna()
df_no.head()
X1 = df_no[['NGCOOK', 'SQFT','NWKER']]
y1 = df_no['NGCNS']
df_filtered = df_no.dropna(subset=['NGCNS', 'NGCOOK', 'SQFT','NWKER'])
X1 = df_filtered[['NGCOOK', 'SQFT','NWKER']]
y1 = df_filtered['NGCNS']

X_train1, X_test1, y_train1, y_test1 = train_test_split(X1, y1, test_size=0.05, random_state=42)
dt_model = DecisionTreeRegressor(random_state=42)
dt_model.fit(X_train1, y_train1)
y_pred_dt1 = dt_model.predict(X_test1)
mae_dt = mean_absolute_error(y_test1, y_pred_dt1)
r2_gas = r2_score(y_test1, y_pred_dt1)
mae_dt, r2_gas


df_gas_yes = df_filtered[df_filtered['NGCOOK'] == 1]
df_gas_no = df_filtered[df_filtered['NGCOOK'] == 2]
X_yes = df_gas_yes[['SQFT', 'NWKER']]
y_yes = df_gas_yes['NGCNS']
X_no = df_gas_no[['SQFT', 'NWKER']]
y_no = df_gas_no['NGCNS']

X_train_yes, X_test_yes, y_train_yes, y_test_yes = train_test_split(X_yes, y_yes, test_size=0.05, random_state=42)
X_train_no, X_test_no, y_train_no, y_test_no = train_test_split(X_no, y_no, test_size=0.05, random_state=42)

# GridSearchCV
param_grid = {
    'n_estimators': [50, 100, 150],
    'learning_rate': [0.01, 0.1, 0.2],
    'max_depth': [3, 5, 7]
}
xgb_model = xgb.XGBRegressor(random_state=42)
grid_search = GridSearchCV(estimator=xgb_model, param_grid=param_grid, scoring='r2', cv=10)
grid_search.fit(X_train_yes, y_train_yes)
best_params = grid_search.best_params_
print("Best Parameters:", best_params)

xgb_best_model = xgb.XGBRegressor(**best_params, random_state=42)
xgb_best_model.fit(X_train_yes, y_train_yes)
y_pred_yes_best = xgb_best_model.predict(X_test_yes)
mae_yes_best = mean_absolute_error(y_test_yes, y_pred_yes_best)
r2_yes_best = r2_score(y_test_yes, y_pred_yes_best)

mae_yes_best, r2_yes_best


df_ngcook_1 = df_filtered[df_filtered['NGCOOK'] == 1]
df_ngcook_2 = df_filtered[df_filtered['NGCOOK'] == 2]

average_rate_per_sqft_1 = df_ngcook_1['NGCNS'].sum() / df_ngcook_1['SQFT'].sum()
average_rate_per_sqft_2 = df_ngcook_2['NGCNS'].sum() / df_ngcook_2['SQFT'].sum()

predicted_ngcns_1 = df_ngcook_1['SQFT'] * average_rate_per_sqft_1
predicted_ngcns_2 = df_ngcook_2['SQFT'] * average_rate_per_sqft_2

y_true_1 = df_ngcook_1['NGCNS']
y_true_2 = df_ngcook_2['NGCNS']

mae_1 = mean_absolute_error(y_true_1, predicted_ngcns_1)
mse_1 = mean_squared_error(y_true_1, predicted_ngcns_1)
r2_1 = r2_score(y_true_1, predicted_ngcns_1)

mae_2 = mean_absolute_error(y_true_2, predicted_ngcns_2)
mse_2 = mean_squared_error(y_true_2, predicted_ngcns_2)
r2_2 = r2_score(y_true_2, predicted_ngcns_2)

print(average_rate_per_sqft_1)
print(average_rate_per_sqft_2)
print(f"NGCOOK=1 - MAE: {mae_1}, MSE: {mse_1}, R²: {r2_1}")
print(f"NGCOOK=2 - MAE: {mae_2}, MSE: {mse_2}, R²: {r2_2}")

# INPUT
ngcook_input = 1
sqft_input = 20000

if ngcook_input == 1:
    total_gas_usage = sqft_input * average_rate_per_sqft_1
elif ngcook_input == 2:
    total_gas_usage = sqft_input * average_rate_per_sqft_2
else:
    total_gas_usage = None
    print("Invalid NGCOOK value. Please enter 1 or 2.")

if total_gas_usage is not None:
    print(f"Estimated total natural gas usage: {total_gas_usage:.2f} units")
