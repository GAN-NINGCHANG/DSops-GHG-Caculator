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

warnings.filterwarnings("ignore")
file_path_gas = 'data/Waste.xlsx'
df_waste = pd.read_excel(file_path_gas)

def forecast_per_capita_waste_arima(waste_type, steps=5):
    waste_data = df_waste[df_waste['waste_type'] == waste_type][['year', 'per_capita_waste']]
    waste_data['year'] = pd.to_datetime(waste_data['year'], format='%Y')
    waste_data = waste_data.set_index('year')
    
    # ARIMA
    arima_model = ARIMA(waste_data['per_capita_waste'], order=(1, 1, 1))
    arima_fit = arima_model.fit()

    forecast = arima_fit.forecast(steps=steps)
    future_years = [waste_data.index.max().year + i for i in range(1, steps + 1)]
    return pd.DataFrame({'year': future_years, 'waste_type': waste_type, 'forecasted_per_capita_waste': forecast})

waste_types = df_waste['waste_type'].unique()
forecast_dfs = [forecast_per_capita_waste_arima(waste_type) for waste_type in waste_types]

forecast_all_waste_types = pd.concat(forecast_dfs).reset_index(drop=True)
print(forecast_all_waste_types)

# INPUT
num_people = 1000

total_waste = 0
for waste_type in waste_types:
    forecasted_per_capita_waste = forecast_all_waste_types[
        forecast_all_waste_types['waste_type'] == waste_type
    ]['forecasted_per_capita_waste'].iloc[0]

    total_waste_amount = forecasted_per_capita_waste * num_people
    total_waste += total_waste_amount

    print(f"Estimated total {waste_type} waste: {total_waste_amount:.2f} tons")

print(f"Total estimated waste for all types: {total_waste:.2f} tons")
