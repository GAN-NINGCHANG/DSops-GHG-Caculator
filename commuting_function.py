#设置环境
import pandas as pd
import numpy as np
import googlemaps
import requests
import re
import matplotlib.pyplot as plt
import seaborn as sns
from plotnine import *
import geopandas as gpd
import googlemaps

from math import radians, sin, cos, sqrt, atan2

API_KEY = "AIzaSyC10VMZks3BC9xaLESq5fDYb1dFG749xfM"
gmaps = googlemaps.Client(key = API_KEY)

#对buidling_loc函数返回值的解析，用于找到经纬度
def get_location(x):
    if len(x) == 0:
        return np.NAN
    return x[0]['geometry']['location']

#解析distance文本，并统一单位为KM ， 例： the input text example is "1.04 km"
def clarify_unit(text):
    if text.split()[-1] == 'km':
        return float(text.split()[0])
    else :
        return float(text.split()[0]) / 1000
    
#对于gmaps.directions返回值的解析，用于得到两点间各段出行方式的距离加总
def get_mode_distance(df):
    list = []
    for j in df[0]['legs'][0]['steps']:
            distance = clarify_unit(j['distance']['text'])
            mode = j['travel_mode']
            list.append([mode,distance])
    df1=pd.DataFrame(list)
    df1.columns=['mode','distance']
    return df1.groupby('mode').agg('sum').reset_index()

#计算两个地点的距离，需要提供经纬度
def haversine(lat1, lon1, lat2, lon2):
    R = 6371  
    phi1, phi2 = np.radians(lat1), np.radians(lat2)
    delta_phi = np.radians(lat2 - lat1)
    delta_lambda = np.radians(lon2 - lon1)
    
    a = np.sin(delta_phi / 2) ** 2 + np.cos(phi1) * np.cos(phi2) * np.sin(delta_lambda / 2) ** 2
    c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))
    
    return R * c


#得到两个地点的通勤距离（没有具体步骤的版本，矩阵获得，速度更快）结果返回距离的DATAFRAME
def get_distance_list(origins,destinations, mode = None ):
    distance_data = gmaps.distance_matrix(origins = origins , destinations = destinations , mode = mode)
    distance_list = []
    for i in range(len(distance_data['rows'])):
        distance_list.append(distance_data['rows'][i]["elements"][0]['distance']["text"])
    return pd.DataFrame(distance_list)

#调整家庭地址，修改为“singapore +postcode"格式
def change_home_address_format(commuting_data):
    def find_post_code(text):
        match = re.findall(r'\d{6}', text)
        return match[0] if match else None
    commuting_data['post_code']=commuting_data['home'].apply(find_post_code)
    commuting_data['home']="Singapore" +' '+commuting_data['post_code']
    return commuting_data

#得到地点的经纬度，用API得到，为废案
def extract_lat_lng(address , data_type = "json"):
    endpoint = f"https://maps.googleapis.com/maps/api/geocode/{data_type}"
    params = {"address" : address , "key": API_KEY}
    url_params = urlencode(params)
    url = f"{endpoint}?{url_params}"
    r = requests.get(url)
    if r.status_code not in range(200,299):
        return {}
    return r.json()['results'][0]

#给详细版的文档，计算距离,返回DATAFRAME
def cal_Distance(df):
    df['mode_distance']=[np.nan]*len(df)
    for i in range(len(df)):
        data = gmaps.directions(df['home'][i],df['office'][i],mode=df['trans_mode'][i])
        df['mode_distance'][i] = get_mode_distance(data)
    walking = 0
    transit = 0
    driving = 0
    for i in df['mode_distance']:
        walking += i[i['mode'] == "WALKING"]['distance'].sum()
        transit += i[i['mode'] == "TRANSIT"]['distance'].sum()
        driving += i[i['mode'] == "DRIVING"]['distance'].sum()
    return [walking,transit,driving]

#算得该点到各个PA的加权距离，权重为各个planning area 的人口比例
def weighted_distances(lat, lon, df):
    distances = haversine(lat, lon, df['centroid_lat'], df['centroid_lon'])
    weighted_distances = distances * df['pop_per']
    return weighted_distances.sum()

#寻找最近地铁站
def find_nearest_station(row):
    office_location = (row['latitude'], row['longitude'])
    nearest_station = None
    min_distance = float('inf')
    
    for _, station_row in mrt.iterrows():
        station_location = (station_row['latitude'], station_row['longitude'])
        distance = geodesic(office_location, station_location).kilometers
        if distance < min_distance:
            min_distance = distance
            nearest_station = station_row['station_name']
    
    return pd.Series([nearest_station, min_distance], index=['NearestStation', 'DistanceToStation'])

#寻找最近的公交车站
def find_nearest_stop(row):
    office_location = (row['latitude'], row['longitude'])
    nearest_station = None
    min_distance = float('inf')
    
    for _, station_row in bus_stops.iterrows():
        station_location = (station_row['latitude'], station_row['longitude'])
        distance = geodesic(office_location, station_location).kilometers
        if distance < min_distance:
            min_distance = distance
            nearest_stop = station_row['stop_name']
            nearest_road_to_stop = station_row['road']
    
    return pd.Series([nearest_stop, min_distance,nearest_road_to_stop], index=['NearestStop', 'DistanceToStop','NeareastRoadToStop'])