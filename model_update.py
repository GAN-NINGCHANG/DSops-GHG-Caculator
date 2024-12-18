import firebase_admin
from firebase_admin import credentials, firestore
import pandas as pd
from Estimation import Electricity, Water


def add_data_to_firestore(data, collection_name):
    """
    将字典作为一行数据添加到指定的 Firebase Firestore 集合中。

    参数：
    data (dict): 要添加到 Firestore 的数据，键值对表示字段名称和值。
    collection_name (str): Firestore 中集合的名称。

    返回：
    None
    """
        # 初始化 Firebase
    if not firebase_admin._apps:
        cred = credentials.Certificate("firebase_key.json")  
        firebase_admin.initialize_app(cred)

    db = firestore.client()
    try:
        # 获取集合的引用
        collection_ref = db.collection(collection_name)
        # 添加数据为新的文档
        doc_ref = collection_ref.add(data)
        print(f"Document added with ID: {doc_ref[1].id}")
    except Exception as e:
        print(f"An error occurred: {e}")

def update_models():
    """
    检查 Water 和 Electricity 数据的行数是否为 10 的倍数。
    如果满足条件，则从 Firebase Firestore 获取数据并更新模型。
    """
    # Firebase 初始化
    if not firebase_admin._apps:
        cred = credentials.Certificate("firebase_key.json")
        firebase_admin.initialize_app(cred)

    db = firestore.client()

    def fetch_and_order_firestore_data(collection_name, columns_order):
        """
        从 Firestore 获取集合数据并按指定列顺序返回 DataFrame。
        
        参数：
        collection_name (str): Firestore 中集合的名称。
        columns_order (list): 返回的 DataFrame 中列的顺序。

        返回：
        pd.DataFrame: 格式化后的 DataFrame。
        """
        documents = db.collection(collection_name).get()
        data = [doc.to_dict() for doc in documents]
        df = pd.DataFrame(data)
        return df[columns_order]

    # 读取 Electricity_data 集合，并按指定列顺序显示
    electricity_columns_order = ["Building Type", "Gross Floor Area", "2020EUI"]
    electricity_data_df = fetch_and_order_firestore_data("Electricity_data", electricity_columns_order)

    # 读取 Water_data 集合，并按指定列顺序显示
    water_columns_order = ["PBA", "TYPE", "SQFT", "NWKER", "WTCNS"]
    water_data_df = fetch_and_order_firestore_data("Water_data", water_columns_order)

    # 检查行数是否为 1000 的倍数
    if len(electricity_data_df) % 1000 == 0 or len(water_data_df) % 1000 == 0:
        # 更新 Water 模型
        Water.train_water_model(water_data_df)
        # 更新 Electricity 模型
        Electricity.train_electricity_model(electricity_data_df)
        print("Model has been updated.")

