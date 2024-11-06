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

try:
    cursor = connection.cursor()

    id_value = None 
    company = "Example Company"
    activity = new_data['PBA_Encoded']
    area_in_sqft = new_data['SQFT']
    worker = new_data['NWKER']
    cook = new_data['ngcook_input']
    air_conditioning = new_data['air_conditioning']
    lighting = new_data['lighting']
    office_equipment = new_data['office_equipment']
    elevator = new_data['elevator']
    electricity = new_data['electricity']
    water = new_prediction[0]
    waste = total_waste

    insert_query = """
    INSERT INTO DATA (id, company, activity, area_in_sqft, worker, cook, air_conditioning, lighting, 
                            office_equipment, elevator, electricity, water, waste) 
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    cursor.execute(insert_query, (id_value, company,activity, area_in_sqft, worker, cook, 
                                  air_conditioning, lighting, office_equipment, 
                                  elevator, electricity, water, waste))

    connection.commit()
    print("Data inserted successfully.")

except Exception as e:
    print("An error occurred:", e)

finally:
    connection.close()
