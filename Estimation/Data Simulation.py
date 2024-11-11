import numpy as np
import pandas as pd
from scipy.stats import norm
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import mean_absolute_error, r2_score
import pickle
import random
import string

water_data = pd.read_csv('../data/Water.csv').iloc[:,1:-1]
water_data.columns = ['Building_Type','Gross_Floor_Area','Average_Headcount']

# Data preprocessing and split
label_encoder = LabelEncoder()
water_data['Building_Type_Encoded'] = label_encoder.fit_transform(water_data['Building_Type'])

X = water_data[['Building_Type_Encoded', 'Gross_Floor_Area']]  
y = water_data['Average_Headcount']  

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=5105)

# Train Model
rf = RandomForestRegressor(random_state=5105)

param_grid = {
    'n_estimators': [50, 100, 200],  
    'max_depth': [None, 10, 20, 30],  
    'min_samples_split': [2, 5, 10],  
    'min_samples_leaf': [1, 2, 4],    
    'max_features': [None, 'sqrt', 'log2']  
}

grid_search = GridSearchCV(estimator=rf, param_grid=param_grid, cv=5, n_jobs=-1, verbose=2)
grid_search.fit(X_train, y_train)

# Predict with optimal model
best_rf = grid_search.best_estimator_
# y_pred = best_rf.predict(X_test)

# mae = mean_absolute_error(y_test, y_pred) #544.15
# r2 = r2_score(y_test, y_pred) #0.4958

data = pd.read_csv('../data/Electricity.csv')
data['Gross_Floor_Area'] = data['Gross_Floor_Area'].str.replace(',','').astype('float') * 10.7639 
max_EUI = data['EUI'].max()
data['EUI'] = data['EUI']*data['Gross_Floor_Area'] / 10.7639
n = len(data)
data['Building_Type'] = data['Building_Type'].map(
    {'Hotel': 0, 'Mixed Development': 1, 'Office': 2, 'Retail': 3}
    ).astype('category')
data.columns = ['PBA_Encoded','SQFT','Electricity_Amount']

## Simulate the distribution of area and headcount
# Find the distribution of area and headcount
n_samples = 10000 - n  
building_type_counts = data['PBA_Encoded'].value_counts(normalize=True)
gfa_mean, gfa_std = norm.fit(data['SQFT']) 

# Synthesize building types
building_types = np.random.choice(building_type_counts.index, size=n_samples, p=building_type_counts.values)

# Synthesize area and headcount
gfa_samples = np.random.normal(gfa_mean, gfa_std, n_samples)

# Restrict the range of the data 
gfa_samples = np.clip(gfa_samples, data['SQFT'].min(), data['SQFT'].max())

# Store new data
simulated_data = pd.DataFrame({
    'PBA_Encoded': building_types,
    'SQFT': gfa_samples
})

## Electricity and renewable proportion
with open('electricity_rf_model.pkl', 'rb') as file:
    electricity_model = pickle.load(file)

X_simulated = simulated_data[['SQFT','PBA_Encoded']]
electricity_simulated = electricity_model.predict(X_simulated)
electricty_limit = max_EUI * simulated_data['SQFT'] / 10.7639 
simulated_data['Electricity_Amount'] = np.minimum(electricty_limit, electricity_simulated) / 10
data = pd.concat([data, simulated_data], ignore_index=True)

data['Renewable_Energy_Proportion'] = np.random.uniform(0, 0.05, 10000)

## Headcount
X_headcount = data[['PBA_Encoded','SQFT']]
X_headcount.columns = ['Building_Type_Encoded','Gross_Floor_Area']
headcount = best_rf.predict(X_headcount)
data['Average_Headcount'] = headcount.astype(int) 

## Water
with open('water_model.pkl', 'rb') as file:
    water_model = pickle.load(file)
# X = df[['SQFT', 'NWKER', 'PBA']]
X_water = data[['SQFT','Average_Headcount','PBA_Encoded']]
X_water.columns = ['SQFT','NWKER','PBA']
water = water_model.predict(X_water)
data['Water_Amount'] = water 

## Waste
# Estimated total Ash & Sludge waste: 33.63 tons
# Estimated total Construction & Demolition waste: 3.37 tons
# Estimated total Ferrous Metal waste: 1.19 tons
# Estimated total Food waste waste: 107.54 tons
# Estimated total Glass waste: 11.40 tons
# Estimated total Horticultural Waste waste: 6.25 tons
# Estimated total Non-ferrous Metals waste: 0.15 tons
# Estimated total Others (stones, ceramics & rubber etc) waste: 39.22 tons
# Estimated total Paper/Cardboard waste: 149.93 tons
# Estimated total Plastics waste: 157.32 tons
# Estimated total Scrap Tyres waste: 0.17 tons
# Estimated total Textile/Leather waste: 34.81 tons
# Estimated total Used Slag waste: 0.56 tons
# Estimated total Wood/Timber waste: 25.18 tons
# Estimated total Total waste: 559.01 tons
waste_per = [1.19, 149.93, 3.37, 157.32, 107.54, 6.25, 25.18, 559.01, 33.63, 34.81, 0.56, 0.15, 11.4, 0.17, 39.22]

waste_df = pd.DataFrame([waste_per] * len(headcount), columns=[
    'Ferrous_Metal_Amount', 'Paper_cardboard_Amount', 'Construction_Demolition_Amount',
    'Plastics_Amount', 'Food_Amount', 'Horticultural_Amount', 'Wood_Amount', 'Waste_Amount',
    'Ash_sludge_Amount', 'Textile_Leather_Amount', 'Used_slag_Amount', 'Non_Ferrous_Metal_Amount',
    'Glass_Amount', 'Scrap_Tyres_Amount', 'Others_Amount'
])

waste_df['headcount'] = headcount
np.random.seed(5105)  
for column in waste_df.columns[:-1]:  
    waste_df[column] = waste_df[column] * waste_df['headcount']* (1 + np.random.normal(0, 0.05, len(headcount))) / 1000

data = pd.concat([data,waste_df.iloc[:,:-1]], axis=1)

## Cook and Natural Gas
# gas_data = pd.read_excel('../data/Natural Gas Data.xlsx')
# proportion = gas_data['NGCOOK'].value_counts(normalize=True)
proportion = {1:0.333126,2:0.666874}
if_cook = 0.38915055372653057
if_not_cook = 0.2166124024523721
cook = np.random.choice([1, 2], size=10000, p=[proportion[1], proportion[2]])
data['Cook'] = cook 
data['Natural_Gas_Amount'] = np.where(data['Cook'] == 1, if_cook * data['SQFT'], if_not_cook * data['SQFT'])/103.8 *1.925 / 1000

## Commute
data['Work_Frequency'] = np.random.choice([0, 0.2, 0.4, 0.6,0.8, 1.0], size=10000, p=[0.00001,0.00009,0.0001,0.0008,0.219,0.78])
commute_per = [7.66*1.3,7.66,1.3]
commute_df = pd.DataFrame([commute_per] * len(headcount), columns=[
    'Drive_Distance','Public_Distance','Walk_Distance' 
])

commute_df['headcount'] = headcount
np.random.seed(5105)  
for column in commute_df.columns[:-1]:  
    commute_df[column] = commute_df[column] * commute_df['headcount']* (1 + np.random.normal(0, 0.05, len(headcount)))

data = pd.concat([data,commute_df.iloc[:,:-1]], axis=1)

## Name and address
def generate_unique_names(count, seed=5105):
    random.seed(seed) 
    unique_names = set()  
    while len(unique_names) < count:
        random_name = ''.join(random.choices(string.ascii_letters, k=6))
        unique_names.add(random_name)  
    return list(unique_names)  

def generate_unique_address(count, seed=5105):
    unique_names = set()  
    while len(unique_names) < count:
        random_name = ''.join(random.choices('0123456789', k=6))
        unique_names.add(random_name)  
    return list(unique_names)  

unique_names_list = generate_unique_names(10000)
unique_address_list = generate_unique_address(10000)

data['Building_Name'] = unique_names_list
data['Postal_Code'] = unique_address_list

act_data = data.copy()
act_data['SQFT'] = act_data['SQFT']/10.7639 
act_data.rename(columns={'PBA_Encoded':'Building_Type','SQFT':'Gross_Floor_Area'},inplace=True)
act_data['Building_Type'] = act_data['Building_Type'].map(
    {0: 'Hotel', 1: 'Mixed Development', 2: 'Office', 3: 'Retail'}
).astype('category')

Electricity_Factor = 0.4168               # Unit: kg CO2/kWh
Natural_Gas_Factor = 2692.8               # Unit: kg CO2/t
Water_Factor = 1.3                     # Unit: kg CO2/t

Ferrous_Metal_Factor = -707.3592663       # Unit: kg CO2/t
Paper_Cardboard_Factor = 5985.56917       # Unit: kg CO2/t
Construction_Demolition_Factor = 97.79380174 # Unit: kg CO2/t
Plastics_Factor = 2905.710927            # Unit: kg CO2/t
Food_Factor = 3585.89118                  # Unit: kg CO2/t
Horticultural_Factor = -28.46620278      # Unit: kg CO2/t
Wood_Factor = 1395.634268                # Unit: kg CO2/t
Ash_Sludge_Factor = 86.9761              # Unit: kg CO2/t
Textile_Leather_Factor = 4605.975149     # Unit: kg CO2/t
Used_Slag_Factor = -6.342589587         # Unit: kg CO2/t
Non_Ferrous_Metal_Factor = -707.3592663  # Unit: kg CO2/t
Glass_Factor = 532.8208748               # Unit: kg CO2/t
Scrap_Tyres_Factor = 3963.915656         # Unit: kg CO2/t
Others_Factor = 38.17394179             # Unit: kg CO2/t

Drive_Factor = 0.118                      # Unit: kg CO2/km
Public_Factor = 0.0431                     # Unit: kg CO2/km
Walk_Factor = 0.0                         

act_data['Electricity_GHG_Emission'] = (
    act_data['Electricity_Amount'] * Electricity_Factor * 
    (1 - act_data['Renewable_Energy_Proportion'])
)

act_data['Natural_Gas_GHG_Emission'] = (
    act_data['Natural_Gas_Amount'] * Natural_Gas_Factor
)

act_data['Water_GHG_Emission'] = (
    act_data['Water_Amount'] * Water_Factor
)

act_data['Waste_GHG_Emission'] = (
    act_data['Ferrous_Metal_Amount'] * Ferrous_Metal_Factor +
    act_data['Paper_cardboard_Amount'] * Paper_Cardboard_Factor +
    act_data['Construction_Demolition_Amount'] * Construction_Demolition_Factor +
    act_data['Plastics_Amount'] * Plastics_Factor +
    act_data['Food_Amount'] * Food_Factor +
    act_data['Horticultural_Amount'] * Horticultural_Factor +
    act_data['Wood_Amount'] * Wood_Factor +
    act_data['Ash_sludge_Amount'] * Ash_Sludge_Factor +
    act_data['Textile_Leather_Amount'] * Textile_Leather_Factor +
    act_data['Used_slag_Amount'] * Used_Slag_Factor +
    act_data['Non_Ferrous_Metal_Amount'] * Non_Ferrous_Metal_Factor +
    act_data['Glass_Amount'] * Glass_Factor +
    act_data['Scrap_Tyres_Amount'] * Scrap_Tyres_Factor +
    act_data['Others_Amount'] * Others_Factor
)

act_data['Commute_GHG_Emission'] = (
    (act_data['Drive_Distance'] * Drive_Factor +
    act_data['Public_Distance'] * Public_Factor +
    act_data['Walk_Distance'] * Walk_Factor) *
    act_data['Work_Frequency']
)

act_data['Total_GHG_Emission'] = (
    act_data['Electricity_GHG_Emission'] +
    act_data['Natural_Gas_GHG_Emission'] +
    act_data['Water_GHG_Emission'] +
    act_data['Waste_GHG_Emission'] +
    act_data['Commute_GHG_Emission']
)

act_data['GHG_Unit_Intensity'] = act_data['Total_GHG_Emission']/act_data['Gross_Floor_Area']

new_column_order = [
    'Building_Name', 'Postal_Code', 'Gross_Floor_Area', 'Average_Headcount', 'Building_Type', 'Cook',
    'Electricity_Amount', 'Renewable_Energy_Proportion', 'Natural_Gas_Amount', 'Water_Amount',
    'Ferrous_Metal_Amount', 'Paper_cardboard_Amount', 'Construction_Demolition_Amount', 'Plastics_Amount',
    'Food_Amount', 'Horticultural_Amount', 'Wood_Amount', 'Waste_Amount', 'Ash_sludge_Amount',
    'Textile_Leather_Amount', 'Used_slag_Amount', 'Non_Ferrous_Metal_Amount', 'Glass_Amount', 'Scrap_Tyres_Amount',
    'Others_Amount', 'Drive_Distance', 'Public_Distance', 'Walk_Distance', 'Work_Frequency', 
    'Electricity_GHG_Emission', 'Natural_Gas_GHG_Emission', 'Water_GHG_Emission', 'Waste_GHG_Emission',
    'Commute_GHG_Emission', 'Total_GHG_Emission', 'GHG_Unit_Intensity'
]

final_df = act_data[new_column_order]
final_df.to_csv('Full_table.csv', index=False)