import streamlit as st


def page_1():
    st.title("🏢 GHG Emissions Calculator")
    st.markdown("### Calculate GHG emissions for an office building in Singapore")
    st.write("Please enter the relevant information for each activity category:")

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

    activity_types = list(st.session_state.activities.keys())  # 活动类型列表
    total_activities = len(activity_types)  # 总活动数
    current_activity = activity_types[st.session_state.activity_index]
    progress_percentage = (st.session_state.activity_index + 1) / total_activities

    # 显示进度条和节点
    def display_progress_bar_with_nodes(progress, nodes, current_index):
        progress_bar_html = f"""
        <div style="width: 100%; background-color: #e0e0e0; height: 20px; border-radius: 10px;">
            <div style="width: {progress * 100}%; background-color: #add8e6; height: 100%; border-radius: 10px;"></div>
        </div>
        <div style="display: flex; justify-content: space-between; font-size: 0.6rem;">
        """
        for i, node in enumerate(nodes):
            if i == current_index:
                progress_bar_html += f"<span style='color: #add8e6; font-weight: bold;'>⬤ {node}</span>"
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
    if st.button("➕", key=f"add_{current_activity}"):
        add_sub_activity(current_activity)

    # 显示并编辑每个子活动
    for i, sub_activity in enumerate(st.session_state.activities[current_activity]):
        st.write(f"**{current_activity} {i + 1}**")

        if current_activity == "Basic Information":
            st.markdown("<span style='color: red;'>*</span> Employee number", unsafe_allow_html=True)
            sub_activity["Employee number"] = st.number_input(
                "Employee number", 
                min_value=0, value=0, key=f"operating_hours_h_{current_activity}_{i}"
            )
            st.markdown("<span style='color: red;'>*</span> Building area (m²)", unsafe_allow_html=True)
            sub_activity["Building area"] = st.number_input(
                "Building area", 
                min_value=0.0, value=0.0, key=f"power_kw_h_{current_activity}_{i}"
            )
            st.markdown("<span style='color: red;'>*</span> Main building activity", unsafe_allow_html=True)
            sub_activity["Main building activity"] = st.selectbox(
                "Select type of electricity consumption", 
                ["hotel", "office", "retail", "mixed development"],
                key=f"electricity_component_{current_activity}_{i}"
            )

        elif current_activity == "Electricity_consumption(kw)":
            sub_activity["component"] = st.selectbox(
                "Select type of electricity consumption", 
                ["Lighting electricity consumption", "Office equipment electricity consumption", "Elevator electricity consumption(kw)"],
                key=f"electricity_component_{current_activity}_{i}"
            )
            sub_activity["operating_hours_h"] = st.number_input(
                "Operating hours (hours)", 
                min_value=0.0, value=0.0, key=f"operating_hours_h_{current_activity}_{i}"
            )
            sub_activity["power_kw_h"] = st.number_input(
                "Power (kw/h)", 
                min_value=0.0, value=0.0, key=f"power_kw_h_{current_activity}_{i}"
            )

        elif current_activity == "Gas(m^3)":
            sub_activity["quantity"] = st.number_input(
                "Quantity (m³)", 
                min_value=0.0, value=0.0, key=f"gas_quantity_{current_activity}_{i}"
            )

        elif current_activity == "Refrigeration system":
            sub_activity["component"] = st.selectbox(
                "Select refrigeration system",
                ["Fluorinated compound emissions (kg)", "Refrigerant usage (kg)"],
                key=f"refrigeration_component_{current_activity}_{i}"
            )
            sub_activity["quantity"] = st.number_input(
                "Quantity (kg)", 
                min_value=0.0, value=0.0, key=f"refrigeration_quantity_{current_activity}_{i}"
            )

        elif current_activity == "Water consumption(m^3/t)":
            sub_activity["quantity"] = st.number_input(
                "Quantity (m³/t)", 
                min_value=0.0, value=0.0, key=f"water_quantity_{current_activity}_{i}"
            )

        elif current_activity == "Waste Management":
            sub_activity["component"] = st.selectbox(
                "Select waste management type",
                ["Solid waste disposal volume (t)", "Wastewater discharge volume (m³/t)"],
                key=f"waste_component_{current_activity}_{i}"
            )
            if sub_activity["component"] == "Solid waste disposal volume (t)":
                sub_activity["waste_type"] = st.selectbox(
                    "Solid waste type",
                    ["Food (t)", "Paper (t)", "Plastic (t)", "Wood (t)", "Others (t)"],
                    key=f"waste_type_{current_activity}_{i}"
                )
            sub_activity["quantity"] = st.number_input(
                "Quantity (t)", 
                min_value=0.0, value=0.0, key=f"waste_quantity_{current_activity}_{i}"
            )

        elif current_activity == "Renewable Energy":
            sub_activity["quantity"] = st.number_input(
                "Quantity (kw/h)", 
                min_value=0.0, value=0.0, key=f"renewable_energy_quantity_{current_activity}_{i}"
            )

        if st.button("➖", key=f"remove_{current_activity}_{i}"):
            remove_sub_activity(current_activity, i)
            st.rerun()

    def is_basic_information_complete():
        for sub_activity in st.session_state.activities["Basic Information"]:
            if (
                sub_activity.get("Employee number", 0) <= 0 or 
                sub_activity.get("Building area", 0.0) <= 0.0 or 
                not sub_activity.get("Main building activity")
            ):
                return False
        return True

    # 下一步和上一步按钮
    col1, col2 = st.columns(2)
    if col1.button("⬅️ Previous") and st.session_state.activity_index > 0:
        st.session_state.activity_index -= 1

    if col2.button("Next ➡️"):
        if st.session_state.activity_index == 0:  # 如果当前活动是第一个必填项
            if is_basic_information_complete():
                st.session_state.activity_index += 1
            else:
                st.warning("Please complete all required fields before continuing.")
        elif st.session_state.activity_index < len(activity_types) - 1:
            st.session_state.activity_index += 1
