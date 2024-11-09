import streamlit as st
import base64
import joblib  # 用于加载模型
import numpy as np  # 用于数组操作
import pandas as pd

def page_1():
    # 将图片转换为 Base64
    def get_base64_image(file_path):
        with open(file_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode()

    base64_image = get_base64_image("/workspaces/DSops-GHG-Caculator/src/background.jpg")

    # 自定义 CSS 样式
    page_bg_img = f'''
    <style>
    .stApp {{
        background: linear-gradient(rgba(0,0,0,0.2), rgba(0,0,0,0.2)), url("data:image/jpg;base64,{base64_image}");
        background-size: cover;
        background-repeat: no-repeat;
        background-attachment: fixed;
        background-position: center;
        color: black;
        font-family: 'Arial', sans-serif;
    }}
    </style>
    '''
    st.markdown(page_bg_img, unsafe_allow_html=True)

    st.title("🏢 GHG Emissions Calculator")
    st.markdown("### Calculate GHG emissions for an office building in Singapore")
    st.write("Please enter the relevant information for each activity category:")

    # 加载水消耗模型
    try:
        model_path = '/workspaces/DSops-GHG-Caculator/utils/water_model.pkl'
        water_model = joblib.load(model_path)
    except FileNotFoundError:
        st.error("Water model file not found. Please check the path to the water_model.pkl.")
        water_model = None  # 如果文件加载失败，则模型设为 None

    # 加载废物预测模型
    try:
        waste_forecast_path = '/workspaces/DSops-GHG-Caculator/utils/all_arima_models.pkl'
        waste_forecasts = joblib.load(waste_forecast_path)  # 使用 joblib 加载废物预测数据
        
        # 提取预测值
        waste_forecast_values = {}
        for waste_type, arima_result in waste_forecasts.items():
            # 确保我们获取到的是预测值而不是 ARIMA 对象
            waste_forecast_values[waste_type] = arima_result.forecast(steps=1).iloc[0]  # 使用 iloc[0] 提取第一个预测值
    except FileNotFoundError:
        st.error("Waste forecast file not found. Please check the path to waste_forecast.pkl.")
        waste_forecast_values = None  # 如果文件加载失败，则数据设为 None

    # 加载电消耗模型
    try:
        electricity_model_path = '/workspaces/DSops-GHG-Caculator/utils/electricity_rf_model.pkl'
        electricity_rf_model = joblib.load(electricity_model_path)
    except FileNotFoundError:
        st.error("Electricity model file not found. Please check the path to the electricity_rf_model.pkl.")
        electricity_rf_model = None  # 如果文件加载失败，则模型设为 None

    # 主框架，使用字典来记录每类活动及其子活动
    if 'activities' not in st.session_state:
        st.session_state.activities = {
            "Basic Information": [],
            "Electricity_consumption(kw)": [],
            "Gas(m^3)": [],
            "Refrigeration system": [],
            "Water consumption(m^3/t)": [],
            "Waste Management": [],
            "Renewable Energy": []
        }

    if 'activity_index' not in st.session_state:
        st.session_state.activity_index = 0  # 当前活动的索引

    if 'global_vars' not in st.session_state:
        st.session_state.global_vars = {}

    activity_types = list(st.session_state.activities.keys())  # 活动类型列表
    total_activities = len(activity_types)  # 总活动数
    current_activity = activity_types[st.session_state.activity_index]
    progress_percentage = (st.session_state.activity_index + 1) / total_activities

    # 显示进度条和节点
    def display_progress_bar_with_nodes(progress, nodes, current_index):
        progress_bar_html = f"""
        <div class="progress-bar-container">
            <div class="progress-bar" style="width: {progress * 100}%;"></div>
        </div>
        <div class="progress-nodes">
        """
        for i, node in enumerate(nodes):
            if i == current_index:
                progress_bar_html += f"<span style='font-weight: bold;'>⬤ {node}</span>"
            else:
                progress_bar_html += f"<span>⬤ {node}</span>"
        progress_bar_html += "</div>"
        st.markdown(progress_bar_html, unsafe_allow_html=True)

    display_progress_bar_with_nodes(progress_percentage, activity_types, st.session_state.activity_index)

    # 获取当前的活动类别
    current_activity = activity_types[st.session_state.activity_index]

    # 显示当前活动的标题
    st.subheader(f"Activity {st.session_state.activity_index + 1}: {current_activity}")

    # 编辑当前活动的内容
    if current_activity == "Basic Information":
        if len(st.session_state.activities["Basic Information"]) == 0:
            st.session_state.activities["Basic Information"].append({})

        sub_activity = st.session_state.activities["Basic Information"][0]

        # 输入员工数量
        sub_activity["Employee number"] = st.number_input(
            "Employee number", 
            min_value=0, value=sub_activity.get("Employee number", 0),
            key="operating_hours_h_Basic_Information"
        )
        st.session_state.global_vars['Average_Headcount'] = sub_activity["Employee number"]
        
        # 输入建筑面积
        sub_activity["Building area"] = st.number_input(
            "Building area", 
            min_value=0.0, value=sub_activity.get("Building area", 0.0),
            key="power_kw_h_Basic_Information"
        )
        st.session_state.global_vars['Gross_Floor_Area'] = sub_activity["Building area"]
        
        # 输入主建筑活动类型
        sub_activity["Main building activity"] = st.selectbox(
            "Select type of electricity consumption", 
            ["hotel", "office", "retail", "mixed development"],
            index=["hotel", "office", "retail", "mixed development"].index(sub_activity.get("Main building activity", "hotel")),
            key="electricity_component_Basic_Information"
        )
        st.session_state.global_vars['Building_Type'] = sub_activity["Main building activity"]
        
        # 是否使用天然气烹饪
        sub_activity["NGCOOK"] = st.selectbox(
            "Does the building use natural gas for cooking?",
            ["Yes", "No"],
            index=["Yes", "No"].index(sub_activity.get("NGCOOK", "Yes")),
            key="ngcook_input_Basic_Information"
        )
        st.session_state.global_vars['NGCOOK'] = sub_activity["NGCOOK"]

        # 用户输入的准确数据覆盖
        st.session_state.global_vars['Water_Amount'] = st.number_input(
            "Actual Water Consumption (if known, in cubic meters)",
            min_value=0.0, value=st.session_state.global_vars.get('Water_Amount', 0.0)
        )
        st.session_state.global_vars['Electricity_Amount'] = st.number_input(
            "Actual Electricity Consumption (if known, in kWh)",
            min_value=0.0, value=st.session_state.global_vars.get('Electricity_Amount', 0.0)
        )
        st.session_state.global_vars['Natural_Gas_Amount'] = st.number_input(
            "Actual Natural Gas Consumption (if known, in tons)",
            min_value=0.0, value=st.session_state.global_vars.get('Natural_Gas_Amount', 0.0)
        )

    # 转换用户输入为独立变量
    WTCNS = st.session_state.global_vars.get('Water_Amount', None)  # 水消耗量变量
    NGCNS = st.session_state.global_vars.get('Natural_Gas_Amount', None)  # 天然气消耗量变量
    ELEC_CONS = st.session_state.global_vars.get('Electricity_Amount', None)  # 电消耗量变量
    waste_forecasts_per_type = {}  # 初始化废物预测类型变量

    if current_activity == "Basic Information":
        if len(st.session_state.activities["Basic Information"]) > 0:
            basic_info = st.session_state.activities["Basic Information"][0]
            
            # 提取独立变量
            SQFT = st.session_state.global_vars['Gross_Floor_Area']
            NWKER = st.session_state.global_vars['Average_Headcount']

            # 将 "Main building activity" 转换为编码值
            activity_mapping = {
                "hotel": 0,
                "mixed development": 1,
                "office": 2,
                "retail": 3
            }
            # 使用映射将活动类型列转换为数值
            PBA_Encoded = activity_mapping.get(st.session_state.global_vars['Building_Type'], 0)

            # 使用水模型进行预测
            if SQFT > 0 and NWKER > 0 and water_model is not None and WTCNS == 0.0:
                input_data = np.array([[SQFT, NWKER, PBA_Encoded]])
                try:
                    WTCNS = water_model.predict(input_data)[0]  # 预测水消耗量并保存到 WTCNS 变量
                    st.session_state.global_vars['Water_Amount'] = WTCNS
                except Exception as e:
                    st.error(f"An error occurred during water consumption prediction: {e}")
            # 电功消耗量预测
            if SQFT > 0 and electricity_rf_model is not None and ELEC_CONS == 0.0:
                input_data = np.array([[SQFT, PBA_Encoded]])
                try:
                    ELEC_CONS = electricity_rf_model.predict(input_data)[0]
                    st.session_state.global_vars['Electricity_Amount'] = ELEC_CONS
                except Exception as e:
                    st.error(f"An error occurred during electricity consumption prediction: {e}")

            # 天然气消耗量预测
            ngcook_input = basic_info.get("NGCOOK")
            if ngcook_input == "Yes":
                ngcook_input_encoded = 1
            elif ngcook_input == "No":
                ngcook_input_encoded = 2
            else:
                ngcook_input_encoded = None
            
            if ngcook_input_encoded is not None and NGCNS == 0.0:
                total_gas_usage = SQFT * (14.79 if ngcook_input_encoded == 1 else 6.501)
                if total_gas_usage is not None:
                    NGCNS = total_gas_usage / 103.8 * 1.925 / 1000
                    st.session_state.global_vars['Natural_Gas_Amount'] = NGCNS

            # 废物量预测
            if waste_forecast_values is not None and NWKER > 0:
                for waste_type, per_capita_waste in waste_forecast_values.items():
                    individual_waste_total = per_capita_waste * NWKER
                    st.session_state.global_vars[f"{waste_type}_Amount"] = individual_waste_total

    # 计算 CO2 排放量
    electricity_conversion_factor = 0.4168
    natural_gas_conversion_factor = 2692.8
    water_conversion_factor = 1.3
    waste_conversion_factor = 3475.172

    # 电功排放量计算
    if ELEC_CONS is not None:
        electricity_emission = ELEC_CONS * electricity_conversion_factor
        st.session_state.global_vars['Electricity_GHG_Emission'] = electricity_emission

    # 天然气排放量计算
    if NGCNS is not None:
        natural_gas_emission = NGCNS * natural_gas_conversion_factor
        st.session_state.global_vars['Natural_Gas_GHG_Emission'] = natural_gas_emission

    # 水排放量计算
    if WTCNS is not None:
        water_emission = WTCNS * water_conversion_factor
        st.session_state.global_vars['Water_GHG_Emission'] = water_emission

    # 废物排放量计算
    total_waste_amount = sum(waste_forecasts_per_type.values())
    total_waste_emission = total_waste_amount * waste_conversion_factor
    st.session_state.global_vars['Waste_GHG_Emission'] = total_waste_emission

    # 计算总的 GHG 排放量
    total_ghg_emission = sum(filter(None, [
        st.session_state.global_vars.get('Electricity_GHG_Emission'),
        st.session_state.global_vars.get('Natural_Gas_GHG_Emission'),
        st.session_state.global_vars.get('Water_GHG_Emission'),
        st.session_state.global_vars.get('Waste_GHG_Emission')
    ]))
    st.session_state.global_vars['Total_GHG_Emission'] = total_ghg_emission

    # 显示水消耗、天然气消耗和废物量预测结果
    st.markdown("### Prediction Results")
    if WTCNS is not None:
        st.write(f"**Predicted Water Consumption**: {WTCNS:.2f} cubic meters")
        st.write(f"**Water GHG Emission**: {water_emission:.2f} kg CO2")

    if ELEC_CONS is not None:
        st.write(f"**Predicted Electricity Consumption**: {ELEC_CONS:.2f} kWh")
        st.write(f"**Electricity GHG Emission**: {electricity_emission:.2f} kg CO2")

    if NGCNS is not None:
        st.write(f"**Predicted Natural Gas Consumption**: {NGCNS:.2f} tons")
        st.write(f"**Natural Gas GHG Emission**: {natural_gas_emission:.2f} kg CO2")

    if waste_forecasts_per_type:
        st.markdown("**Waste Forecasts (Total for each type)**:")
        for waste_type, value in waste_forecasts_per_type.items():
            st.write(f"{waste_type}: {value:.2f} tons")
        st.write(f"**Waste GHG Emission**: {total_waste_emission:.2f} kg CO2")

    st.write(f"**Total GHG Emission**: {total_ghg_emission:.2f} kg CO2")

    # 修改 Previous 按钮逻辑，当 activity_index 为 0 时跳转到首页
    col1, _, col2 = st.columns([1, 8, 1]) 
    if col1.button("Previous"):
        if st.session_state.activity_index > 0:
            st.session_state.activity_index -= 1
        elif st.session_state.activity_index == 0:
            st.session_state.current_page = 0  # 返回首页

    # 修改 Next 按钮逻辑，当 activity_index 到达最后一个活动时跳转到下一页
    if col2.button("Next"):
        if st.session_state.activity_index < len(activity_types) - 1:
            st.session_state.activity_index += 1
        elif st.session_state.activity_index == len(activity_types) - 1:
            st.session_state.current_page = 2  # 跳转到 page_2
