import firebase_admin
from firebase_admin import credentials, firestore
import pandas as pd

# Firebase 初始化
if not firebase_admin._apps:
    cred = credentials.Certificate("firebase_key.json")
    firebase_admin.initialize_app(cred)

db = firestore.client()

# # 文件路径
# csv_file_path = "data/Electricity_data.csv"

# # 读取 CSV 文件
# data = pd.read_csv(csv_file_path)

# # 遍历 DataFrame 的每一行，将每一行作为一个文档上传
# for index, row in data.iterrows():
#     # 使用索引生成唯一文档 ID
#     doc_id = f"row_{index}"  # 可以使用其他唯一标识符
#     # 定义文档参考路径
#     doc_ref = db.collection("Electricity_data").document(doc_id)
#     # 将行数据转换为字典并上传
#     doc_ref.set(row.to_dict())

# print("CSV 文件中的数据已成功批量上传到 Firestore！")

# 文件路径
csv_file_path = "data/Water_data.csv"

# 读取 CSV 文件
data = pd.read_csv(csv_file_path)

# 遍历 DataFrame 的每一行，将每一行作为一个文档上传
for index, row in data.iterrows():
    # 使用索引生成唯一文档 ID
    doc_id = f"row_{index}"  # 可以使用其他唯一标识符
    # 定义文档参考路径
    doc_ref = db.collection("Water_data").document(doc_id)
    # 将行数据转换为字典并上传
    doc_ref.set(row.to_dict())

print("CSV 文件中的数据已成功批量上传到 Firestore！")

