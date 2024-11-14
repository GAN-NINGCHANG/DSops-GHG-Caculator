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
        background: linear-gradient(rgba(255,255,255,0.2), rgba(255,255,255,0.2)), url("data:image/jpg;base64,{base64_image}");
        background-size: cover;
        background-repeat: no-repeat;
        background-attachment: fixed;
        background-position: center;
        color: #333;
        font-family: 'Arial', sans-serif;
    }}
    .block-container {{
        background-color: rgba(255, 255, 255, 0.5); /* 更加透明的背景 */
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0px 4px 15px rgba(0, 0, 0, 0.1);
        width: 80%;
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
            "Electricity": [],
            "Gas": [],
            "Water": [],
            "Waste": [],
        }

    if 'activity_index' not in st.session_state:
        st.session_state.activity_index = 0  # 当前活动的索引

    activity_types = list(st.session_state.activities.keys())  # 活动类型列表
    total_activities = len(activity_types)  # 总活动数
    current_activity = activity_types[st.session_state.activity_index]
    progress_percentage = (st.session_state.activity_index + 1) / total_activities

    # 显示进度条和节点
    def display_progress_bar_with_nodes(progress, nodes, current_index):
        progress_bar_html = f"""
        <div style="width: 100%; background-color: #e0e0e0; height: 30px; border-radius: 10px;">
            <div style="width: {progress * 100}%; background-color: #44901E; height: 100%; border-radius: 10px;"></div>
        </div>
        <div style="display: flex; justify-content: space-between; font-size: 1.5rem;">
        """
        for i, node in enumerate(nodes):
            if i == current_index:
                progress_bar_html += f"<span style='color: #44901E; font-weight: bold;'>⬤ {node}</span>"
            else:
                progress_bar_html += f"<span>⬤ {node}</span>"
        progress_bar_html += "</div>"
        
        st.markdown(progress_bar_html, unsafe_allow_html=True)

    display_progress_bar_with_nodes(progress_percentage, activity_types, st.session_state.activity_index)
    # 定义添加和删除子活动的函数
    def add_sub_activity(activity_type):
        st.session_state.activities[activity_type].append({})

    def remove_sub_activity(activity_type, index):
        if len(st.session_state.activities[activity_type]) > 0:
            st.session_state.activities[activity_type].pop(index)

    # 获取当前的活动类别
    current_activity = activity_types[st.session_state.activity_index]

    # 显示当前活动的标题
    st.subheader(f"Activity {st.session_state.activity_index + 1}: {current_activity}")

    # 添加子活动的按钮
    if current_activity != "Basic Information":
        if st.button("➕", key=f"add_{current_activity}"):
            add_sub_activity(current_activity)

    # 显示并编辑每个子活动
    if current_activity == "Basic Information":
        # 确保 "Basic Information" 只有一个子活动
        if len(st.session_state.activities["Basic Information"]) == 0:
            st.session_state.activities["Basic Information"].append({})

        sub_activity = st.session_state.activities["Basic Information"][0]

        # 输入员工数量
        st.session_state.global_vars['Average_Headcount'] = st.number_input(
            "Employee number", 
            min_value=0, value=sub_activity.get("Employee number", 0),
            key="operating_hours_h_Basic_Information"
        )
                
        # 输入建筑面积
        st.session_state.global_vars['Gross_Floor_Area'] = st.number_input(
            "Building area (Square meter)", 
            min_value=0.0, value=sub_activity.get("Building area", 0.0),
            key="power_kw_h_Basic_Information"
        )
                
        # 输入主建筑活动类型
        st.session_state.global_vars['Building_Type'] = st.selectbox(
            "Select type of electricity consumption", 
            ["hotel", "office", "retail", "mixed development"],
            index=["hotel", "office", "retail", "mixed development"].index(sub_activity.get("Main building activity", "hotel")),
            key="electricity_component_Basic_Information"
        )
                
        # 是否使用天然气烹饪
        ngcook_input = st.selectbox(
             "Does the building use natural gas for cooking?",
            ["Yes", "No"],
            index=["Yes", "No"].index(sub_activity.get("NGCOOK", "Yes")),
            key="ngcook_input_Basic_Information"
        )
         # 输入可持续能源比例
        st.session_state.global_vars['Renewable_Energy_Proportion'] = st.number_input(
            "Renewable Energy Proportion", 
            min_value=0.0, value=sub_activity.get("Renewable Energy Proportion", 0.0),
            key="Renewable_Energy_precentage_Basic_Information"
        )

        # 编辑其他活动类型的子活动
    for i, sub_activity in enumerate(st.session_state.activities[current_activity]):
        if current_activity != "Basic Information":
            st.write(f"**{current_activity} {i + 1}**")

            if current_activity == "Electricity":
                sub_activity["power_kw_h"] = st.number_input(
                    "Power (kwh)", 
                    min_value=0.0, value=0.0, key=f"power_kw_h_{current_activity}_{i}"
                )
                # 更新全局变量
                st.session_state.global_vars['Electricity_Amount'] = sub_activity["power_kw_h"]

            elif current_activity == "Gas":
                sub_activity["quantity"] = st.number_input(
                    "Quantity (tons)", 
                    min_value=0.0, value=0.0, key=f"gas_quantity_{current_activity}_{i}"
                )
                # 更新全局变量
                st.session_state.global_vars['Natural_Gas_Amount'] = sub_activity["quantity"]

            elif current_activity == "Water":
                sub_activity["quantity"] = st.number_input(
                    "Quantity (m³/t)", 
                    min_value=0.0, value=0.0, key=f"water_quantity_{current_activity}_{i}"
                )
                # 更新全局变量
                st.session_state.global_vars['Water_Amount'] = sub_activity["quantity"]

            elif current_activity == "Waste":
                sub_activity["quantity"] = st.number_input(
                    "Quantity (t)", 
                    min_value=0.0, value=0.0, key=f"waste_quantity_{current_activity}_{i}"
                )
                # 更新全局变量
                st.session_state.global_vars['Waste_Amount'] = sub_activity["quantity"]


            if st.button("➖", key=f"remove_{current_activity}_{i}"):
                remove_sub_activity(current_activity, i)
                st.rerun()

    def is_basic_information_complete():
        for sub_activity in st.session_state.activities["Basic Information"]:
            if (
                sub_activity.get("Employee number", 0) <= 0 or 
                sub_activity.get("Building area", 0.0) <= 0.0 or 
                sub_activity.get("Main building activity") or
                not sub_activity.get("NGCOOK")
            ):
                return False
        return True
    
    # 检查是否有用户输入的消耗量
    ELEC_CONS = st.session_state.global_vars.get('Electricity_Amount')
    NGCNS = st.session_state.global_vars.get('Natural_Gas_Amount')
    WTCNS = st.session_state.global_vars.get('Water_Amount')
    WASTE_AMOUNT = st.session_state.global_vars.get('Waste_Amount')

    # 电、水、天然气、废物的 CO2 转换因子
    electricity_conversion_factor = 0.4168
    natural_gas_conversion_factor = 2692.8
    water_conversion_factor = 1.3
    waste_conversion_factor = 3475.172

    # 如果用户输入了所有消耗量，直接计算排放量；否则使用模型预测
    if ELEC_CONS and NGCNS and WTCNS and WASTE_AMOUNT:
        # 直接使用用户输入的消耗量计算排放量
        st.session_state.global_vars['Electricity_GHG_Emission'] = (ELEC_CONS * electricity_conversion_factor)*(1-st.session_state.global_vars['Renewable_Energy_Proportion'])
        st.session_state.global_vars['Natural_Gas_GHG_Emission'] = NGCNS * natural_gas_conversion_factor
        st.session_state.global_vars['Water_GHG_Emission'] = WTCNS * water_conversion_factor
        st.session_state.global_vars['Waste_GHG_Emission'] = WASTE_AMOUNT * waste_conversion_factor
    else:
        # 使用模型预测消耗量
        # 如果当前活动是 Basic Information 且有输入数据
        if current_activity == "Basic Information" and len(st.session_state.activities["Basic Information"]) > 0:
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
            if SQFT > 0 and NWKER > 0 and water_model is not None:
                input_data = np.array([[SQFT, NWKER, PBA_Encoded]])
                try:
                    WTCNS = water_model.predict(input_data)[0]  # 预测水消耗量
                    st.session_state.global_vars['Water_Amount'] = WTCNS
                    st.session_state.global_vars['Water_GHG_Emission'] = WTCNS * water_conversion_factor
                except Exception as e:
                    st.error(f"An error occurred during water consumption prediction: {e}")

            # 电功消耗量预测
            if SQFT > 0 and electricity_rf_model is not None:
                input_data = np.array([[SQFT, PBA_Encoded]])
                try:
                    ELEC_CONS = electricity_rf_model.predict(input_data)[0]
                    st.session_state.global_vars['Electricity_Amount'] = ELEC_CONS
                    st.session_state.global_vars['Electricity_GHG_Emission'] = ELEC_CONS * electricity_conversion_factor
                except Exception as e:
                    st.error(f"An error occurred during electricity consumption prediction: {e}")

            # 天然气消耗量预测
            ngcook_input_encoded = 1 if ngcook_input == "Yes" else 2 if ngcook_input == "No" else None
            if ngcook_input_encoded is not None:
                total_gas_usage = SQFT * (14.79 if ngcook_input_encoded == 1 else 6.501)
                if total_gas_usage is not None:
                    NGCNS = total_gas_usage / 103.8 * 1.925 / 1000
                    st.session_state.global_vars['Natural_Gas_Amount'] = NGCNS
                    st.session_state.global_vars['Natural_Gas_GHG_Emission'] = NGCNS * natural_gas_conversion_factor

            # 废物量预测
            if waste_forecast_values is not None and NWKER > 0:
                for waste_type, per_capita_waste in waste_forecast_values.items():
                    individual_waste_total = per_capita_waste * NWKER
                    st.session_state.global_vars[f"{waste_type}_Amount"] = individual_waste_total
                    st.session_state.global_vars['Waste_Amount'] += individual_waste_total
                WASTE_AMOUNT = st.session_state.global_vars['Waste_Amount']
                st.session_state.global_vars['Waste_GHG_Emission'] = WASTE_AMOUNT * waste_conversion_factor

    # 计算总的 GHG 排放量
    total_ghg_emission = sum(filter(None, [
        st.session_state.global_vars.get('Electricity_GHG_Emission'),
        st.session_state.global_vars.get('Natural_Gas_GHG_Emission'),
        st.session_state.global_vars.get('Water_GHG_Emission'),
        st.session_state.global_vars.get('Waste_GHG_Emission')
    ]))
    st.session_state.global_vars['Total_GHG_Emission'] = total_ghg_emission

    # 设置主标题和样式
    st.markdown("<h2 style='text-align: center; color: #4CAF50;'>Prediction Results</h2>", unsafe_allow_html=True)
    
    # 添加提示文本
    st.markdown("<p style='text-align: center; color: #777777; font-size: 20px;'>Don't worry, if precise data is unavailable, we can provide estimates based on basic information.</p>", unsafe_allow_html=True)
    
    # 使用 Streamlit 的列布局，将数据分为数量和排放量两组
    col1, col2 = st.columns(2)

    # 在第一列中显示数量信息，使用卡片式背景并加入图标
    with col1:
        st.markdown("<h4 style='color: #2F4F4F;'>Consumption Quantities</h4>", unsafe_allow_html=True)
        if WTCNS is not None:
            st.markdown(f"""
                <div style="background-color: #f0f8ff; padding: 10px; border-radius: 10px; margin-bottom: 10px; display: flex; align-items: center;">
                    <span style="font-size: 24px; margin-right: 10px;">💧</span>
                    <strong>Predicted Water Consumption:</strong>
                    <span style="color: #333; font-weight: bold; font-size: 20px; margin-left: auto;">{WTCNS:.2f} cubic meters</span>
                </div>
            """, unsafe_allow_html=True)
        if ELEC_CONS is not None:
            st.markdown(f"""
                <div style="background-color: #f0f8ff; padding: 10px; border-radius: 10px; margin-bottom: 10px; display: flex; align-items: center;">
                    <span style="font-size: 24px; margin-right: 10px;">💡</span>
                    <strong>Predicted Electricity Consumption:</strong>
                    <span style="color: #333; font-weight: bold; font-size: 20px; margin-left: auto;">{ELEC_CONS:.2f} kWh</span>
                </div>
            """, unsafe_allow_html=True)
        if NGCNS is not None:
            st.markdown(f"""
                <div style="background-color: #f0f8ff; padding: 10px; border-radius: 10px; margin-bottom: 10px; display: flex; align-items: center;">
                    <span style="font-size: 24px; margin-right: 10px;">🔥</span>
                    <strong>Predicted Natural Gas Consumption:</strong>
                    <span style="color: #333; font-weight: bold; font-size: 20px; margin-left: auto;">{NGCNS:.2f} tons</span>
                </div>
            """, unsafe_allow_html=True)
        if WASTE_AMOUNT:
            st.markdown(f"""
                <div style="background-color: #f0f8ff; padding: 10px; border-radius: 10px; margin-bottom: 10px; display: flex; align-items: center;">
                    <span style="font-size: 24px; margin-right: 10px;">🗑️</span>
                    <strong>Predicted Waste Consumption:</strong>
                    <span style="color: #333; font-weight: bold; font-size: 20px; margin-left: auto;">{WASTE_AMOUNT:.2f} tons</span>
                </div>
            """, unsafe_allow_html=True)

    # 在第二列中显示排放量信息，使用卡片式背景并加入图标
    with col2:
        st.markdown("<h4 style='color: #2F4F4F;'>GHG Emissions</h4>", unsafe_allow_html=True)
        if WTCNS is not None:
            st.markdown(f"""
                <div style="background-color: #ffebcd; padding: 10px; border-radius: 10px; margin-bottom: 10px; display: flex; align-items: center;">
                    <span style="font-size: 24px; margin-right: 10px;">💧</span>
                    <strong>Water GHG Emission:</strong>
                    <span style="color: #333; font-weight: bold; font-size: 20px; margin-left: auto;">{st.session_state.global_vars['Water_GHG_Emission']:.2f} kg CO2</span>
                </div>
            """, unsafe_allow_html=True)
        if ELEC_CONS is not None:
            st.markdown(f"""
                <div style="background-color: #ffebcd; padding: 10px; border-radius: 10px; margin-bottom: 10px; display: flex; align-items: center;">
                    <span style="font-size: 24px; margin-right: 10px;">💡</span>
                    <strong>Electricity GHG Emission:</strong>
                    <span style="color: #333; font-weight: bold; font-size: 20px; margin-left: auto;">{st.session_state.global_vars['Electricity_GHG_Emission']:.2f} kg CO2</span>
                </div>
            """, unsafe_allow_html=True)
        if NGCNS is not None:
            st.markdown(f"""
                <div style="background-color: #ffebcd; padding: 10px; border-radius: 10px; margin-bottom: 10px; display: flex; align-items: center;">
                    <span style="font-size: 24px; margin-right: 10px;">🔥</span>
                    <strong>Natural Gas GHG Emission:</strong>
                    <span style="color: #333; font-weight: bold; font-size: 20px; margin-left: auto;">{st.session_state.global_vars['Natural_Gas_GHG_Emission']:.2f} kg CO2</span>
                </div>
            """, unsafe_allow_html=True)
        if WASTE_AMOUNT:
            st.markdown(f"""
                <div style="background-color: #ffebcd; padding: 10px; border-radius: 10px; margin-bottom: 10px; display: flex; align-items: center;">
                    <span style="font-size: 24px; margin-right: 10px;">🗑️</span>
                    <strong>Waste GHG Emission:</strong>
                    <span style="color: #333; font-weight: bold; font-size: 20px; margin-left: auto;">{st.session_state.global_vars['Waste_GHG_Emission']:.2f} kg CO2</span>
                </div>
            """, unsafe_allow_html=True)
        
        # 总排放量的卡片设计
        st.markdown(f"""
            <div style="background-color: #c7ccad; padding: 10px; border-radius: 10px; margin-top: 20px; margin-bottom: 40px; display: flex; align-items: center;">
                <span style="font-size: 24px; margin-right: 10px;">🌍</span>
                <strong>Total GHG Emission:</strong>
                <span style="color: #333; font-weight: bold; font-size: 24px; margin-left: auto;">{total_ghg_emission:.2f} kg CO2</span>
            </div>
        """, unsafe_allow_html=True)

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
