import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
from sklearn.metrics import r2_score
from sklearn.model_selection import GridSearchCV, KFold, cross_val_score
from sklearn.metrics import make_scorer, mean_absolute_percentage_error
from xgboost import XGBRegressor
from sklearn.preprocessing import StandardScaler
import pickle

## Data Preprocessing
df = pd.read_excel('../data/Listing of Building Energy Performance Data for 2020.xlsx').iloc[:,3:] # Delete the first three columns about name and address of the building
df.columns = ['Building Type','size','Beginning Year','green mark rating','green mark year',
                'green mark type','Gross Floor Area','AC percent','monthly occupation rate','number of hotel rooms',
                'AC Type','age of chiller','AC Efficiency','last chiller check year','LED percent',
                'Use of PV','2017EUI','2018EUI','2019EUI','2020EUI']
df = df.loc[:,['Building Type','Gross Floor Area','2020EUI']].dropna()
df['Building Type'] = df['Building Type'].map({'Hotel':0,'Mixed Development':1,'Office':2,'Retail':3}).astype('category')

## Model Construction
X = df.drop('2020EUI',axis=1)
y = df['2020EUI']*df['Gross Floor Area']
scaler = StandardScaler()
X = scaler.fit_transform(X)

# Define scorer
r2_scorer = make_scorer(r2_score,greater_is_better=True)
mape_scorer = make_scorer(mean_absolute_percentage_error, greater_is_better=False)

# Hyperparameter tuning
param_grid = {
    'n_estimators': [50, 100, 200],
    'max_depth': [None, 10, 20, 30],
    'min_samples_split': [2, 5, 10],
    'min_samples_leaf': [1, 2, 4],
    'max_features': [None,'sqrt', 'log2']
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

# Train model by K-folding
best_model = RandomForestRegressor(**best_params, random_state=21)

k = 5
kf = KFold(n_splits=k, shuffle=True, random_state=24)

# Calculate adjusted r2 and MAPE
r2_scores = cross_val_score(best_model, X, y, cv=kf, scoring=r2_scorer)
print("R^2 scores:", r2_scores)
print("Mean R^2:", np.mean(r2_scores))

mape_scores = -cross_val_score(best_model, X, y, cv=kf, scoring=mape_scorer) 
print("MAPE scores:", mape_scores)
print("Mean MAPE:", np.mean(mape_scores))

with open('electricity_rf_model.pkl', 'wb') as file:
    pickle.dump(model, file)