new_data = {
    'SQFT': 10000,
    'NWKER': 80,  
    'PBA_Encoded':3,
    'ngcook_input': 2,
    'air_conditioning' : 256500,
    'lighting' : 3032,
    'office_equipment' : 5043,
    'elevator' : 10234,
    'electricity' : 274809
}

connection = pymysql.connect(
        host='127.0.0.1',
        user='root',
        password='011225',
        database='user_data'
)

###creat database

try:
    cursor = connection.cursor()

    id_value = None 
    company = "Example Company"
    activity = new_data['PBA_Encoded']
    area_in_sqft = new_data['SQFT']
    worker = new_data['NWKER']
    cook = ngcook_input
    air_conditioning = new_data['air_conditioning']
    lighting = new_data['lighting']
    office_equipment = new_data['office_equipment']
    elevator = new_data['elevator']
    electricity = new_data['electricity']
    water = new_prediction[0]
    waste = total_waste
    natrual_gas = total_gas_usage

    insert_query = """
    INSERT INTO DATA (id, company, activity, area_in_sqft, worker, cook, air_conditioning, lighting, 
                            office_equipment, elevator, electricity, water, waste, natrual_gas) 
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    cursor.execute(insert_query, (id_value, company,activity, area_in_sqft, worker, cook, 
                                  air_conditioning, lighting, office_equipment, 
                                  elevator, electricity, water, waste, natrual_gas))

    connection.commit()
    print("Data inserted successfully.")

except Exception as e:
    print("An error occurred:", e)

finally:
    connection.close()

### Insert data
df = pd.read_csv('Water data2.csv', encoding='ISO-8859-1',usecols=['PBA', 'SQFT', 'NWKER', 'WTCNS'])
connection1 = pymysql.connect(
    host='127.0.0.1',
    user='root', 
    password='011225', 
    database='user_data'
)
try:
    cursor = connection1.cursor()
    
    for _, row in df.iterrows():
        insert_query = """
        INSERT INTO DATA (activity, area_in_sqft, worker, water)
        VALUES (%s, %s, %s, %s)
        """
        cursor.execute(insert_query, (row['PBA'], row['SQFT'], row['NWKER'], row['WTCNS']))
    
    connection1.commit()
    print("Data imported successfully.")

except Exception as e:
    print("An error occurred:", e)

finally:
    cursor.close()
    connection1.close()

## Retrain Model
def get_new_data_from_mysql():
    connection = pymysql.connect(
        host='127.0.0.1',
        user='root',
        password='011225',
        database='user_data'
    )
    
    query = """
    SELECT activity, area_in_sqft, worker, water
    FROM DATA
    """
    new_data1 = pd.read_sql(query, connection)
    connection.close()
    return new_data1

def update_xgb_model_with_grid_search():
    new_data1 = get_new_data_from_mysql()
    
    if new_data1.empty:
        print("No new data found.")
        return

    X = new_data1[['activity', 'area_in_sqft', 'worker']]
    y = new_data1['water']
    
    param_grid = {
        'n_estimators': [50, 100, 200],
        'learning_rate': [0.01, 0.1, 0.3],
        'max_depth': [3, 5, 7]
    }
    
    model = xgb.XGBRegressor(objective='reg:squarederror', random_state=42)
    grid_search = GridSearchCV(estimator=model, param_grid=param_grid, scoring='r2', cv=5, n_jobs=-1)
    
    grid_search.fit(X, y)
    best_params = grid_search.best_params_
    print("Best parameters found by grid search:", best_params)
    
    best_model = xgb.XGBRegressor(**best_params, objective='reg:squarederror', random_state=42)
    best_model.fit(X, y)

    joblib.dump(best_model, 'water_model_updated.pkl')
    print("XGBoost model updated with best parameters and saved successfully.")

    predictions = best_model.predict(X)
    mse = mean_squared_error(y, predictions)
    r2 = r2_score(y, predictions)
    print(f'Updated Model MSE: {mse}')
    print(f'Updated Model R²: {r2}')
    os.replace('water_model_updated.pkl', 'water_model.pkl')

def automated_model_update(interval=86400):

    while True:
        print("Checking for new data and updating model if necessary...")
        update_xgb_model_with_grid_search()
        print("Waiting for the next update cycle...")
        time.sleep(interval)

def main():
    automated_model_update(interval=86400)

if __name__ == "__main__":
    main()

