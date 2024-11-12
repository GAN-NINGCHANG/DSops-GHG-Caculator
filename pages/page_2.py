import streamlit as st
import pandas as pd
import base64
import os
import sys
from commuting_function import *
import googlemaps


def page_2():
    # 将图片转换为 Base64
    def get_base64_image(file_path):
        with open(file_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode()
    uploaded_file = None
    base64_image = get_base64_image("/workspaces/DSops-GHG-Caculator/src/background.jpg")
    gmaps = googlemaps.Client(key = API_KEY)
    Average_Headcount=st.session_state.global_vars["Average_Headcount"]
    transport_emission=0
    # 自定义 CSS 样式，设置背景和进度条样式
    page_bg_img = f'''
    <style>
    .stApp {{
        background: linear-gradient(rgba(0,0,0,0.2), rgba(0,0,0,0.2)), url("data:image/jpg;base64,{base64_image}");
        background-size: cover;
        background-repeat: no-repeat;
        background-attachment: fixed;
        background-position: center;
        color: black; /* 黑色文字 */
        font-family: 'Arial', sans-serif;
    }}
    .block-container {{
        background-color: rgba(255, 255, 255, 0.7); /* 更加透明的背景 */
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0px 4px 15px rgba(0, 0, 0, 0.5);
        width: 80%; /* 设置宽度为页面的60%，呈竖直布局 */
        margin: auto; /* 居中对齐 */
    }}
    </style>
    '''
    st.markdown(page_bg_img, unsafe_allow_html=True)

    # 页面标题和描述
    st.markdown("<h1 style='text-align: center; font-size: 40px; color: #4CAF50;'>Transportation Data</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 22px;'>Upload your transportation data or enter details manually.</p>", unsafe_allow_html=True)
    st.markdown("<hr style='border-top: 3px solid #bbb;'>", unsafe_allow_html=True)

    # 显示手动输入数据的选项
    st.markdown("<h3 style='color: #4CAF50; font-size: 24px;'>Enter Details Manually</h3>", unsafe_allow_html=True)

        # 公司名称和邮政编码输入
    st.markdown("<p style='font-size: 20px;'>Please enter either the Building Name or the Postal Code (at least one is required):</p>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)

    with col1:
        company_name = st.text_input("Building Name:")
        st.session_state.global_vars['Building_Name'] = company_name
    with col2:
        postal_code = st.text_input("Postal Code:")
    #输入WFH天数
    st.markdown("<p style='font-size: 20px;'>Please enter either Work from home days</p>", unsafe_allow_html=True)
    col3 = st.columns(1)[0]
    with col3:
        WFH = st.number_input("WFH Days:", min_value=0, max_value=5, step=1)
        st.session_state.global_vars['Work_Frequency'] = 1-(WFH/5)
    
        # 校验公司名称和邮政编码的输入
    if not company_name and not postal_code:
        st.markdown("<p style='font-size: 20px; color: orange;'>Please fill in at least one of the fields: Building Name or Postal Code.</p>", unsafe_allow_html=True)
        data_ready = False
    else:
        data_ready = True
    
    

    # 提供上传 CSV 文件的选项
    if data_ready:
        sample_file_path = "./commuting_cal/data/example_input_file.csv"  # 假设文件位于项目的 data 文件夹中
        if os.path.exists(sample_file_path):
            with open(sample_file_path, "rb") as file:
                sample_data = file.read()
                b64 = base64.b64encode(sample_data).decode()
                href = f'<a href="data:file/csv;base64,{b64}" download="Random_Building_Data.csv">Download Sample CSV File</a>'
                st.markdown(href, unsafe_allow_html=True)
        uploaded_file = st.file_uploader("Upload a CSV file with transportation data", type=["csv"])
        st.markdown("<p style='font-size: 18px;'>Note: Uploading a CSV file will generate an additional professional report.</p>", unsafe_allow_html=True)
        
    if uploaded_file is not None:
        # 显示上传文件内容
        try:
            transportation_data = pd.read_csv(uploaded_file)
            st.markdown("<p style='font-size: 20px; font-weight: bold;'>Uploaded Transportation Data</p>", unsafe_allow_html=True)
            st.dataframe(transportation_data)

        except Exception as e:
            st.markdown("<p style='font-size: 20px; color: red;'>Error reading the CSV file. Please ensure it is in the correct format.</p>", unsafe_allow_html=True)
        
        if postal_code :
            transportation_data['office'] = 'singapore ' +str(postal_code)
        else:
            transportation_data['office'] = company_name
        data_ready = True

        try:
            transport_distance_data = cal_Distance(transportation_data)
            walking = transport_distance_data[0]
            transit = transport_distance_data[1]
            driving = transport_distance_data[2]
        except IndexError :
            st.markdown("<p style='font-size: 20px; color: red;'>Error reaching the building. Please ensure it is the correct address.</p>", unsafe_allow_html=True)

        
         
    else:
        if postal_code or company_name :
            sg_pop_loc = pd.read_csv('./commuting_cal/data/sg_pop_loc.csv')
            if postal_code :
                building_loc = gmaps.geocode('singapore ' +str(postal_code))
            else:
                building_loc = gmaps.geocode(company_name)
            lat ,lon =  get_location(building_loc)['lat'],get_location(building_loc)['lng']
            weighted_distances_df = weighted_distances(lat, lon, sg_pop_loc)
            mode_distribution = pd.DataFrame({
                    'Mode of Transport': ['TRANSIT', 'WALKING', 'DRIVING'],
                    'percentage': [0.577478489, 0.097777866, 0.324743646]
                    })
            mode_distribution['distance'] = mode_distribution['percentage']*weighted_distances_df
                
            walking = mode_distribution[mode_distribution['Mode of Transport']=='WALKING']['distance'].sum()
            transit = mode_distribution[mode_distribution['Mode of Transport']=='TRANSIT']['distance'].sum()
            driving = mode_distribution[mode_distribution['Mode of Transport']=='DRIVING']['distance'].sum()


    if  company_name or postal_code:
        transport_emission = (walking*0+transit*0.0431+driving*0.118)*2*250*(5-WFH)/5*Average_Headcount
        st.write(f"**Predicted commuting emission**: {transport_emission:.2f} kg CO2")
        st.session_state.global_vars["Walk_Distance"] = walking
        st.session_state.global_vars["Public_Distance"] = transit
        st.session_state.global_vars["Drive_Distance"] = driving
        st.session_state.global_vars["Commute_GHG_Emission"] = transport_emission
        st.session_state.global_vars["Postal_Code"] = postal_code
        
    # 页面底部的bui按钮布局
    col1, _, col2 = st.columns([1, 8, 1]) 
    with col1:
        if st.button("Previous"):
            st.session_state.current_page -= 1
    

    with col2:
        # 提交数据按钮
        if st.button("Submit"):
            if data_ready:
                # Ensure page navigation to the next page
                st.session_state.current_page += 1
                
                # Define flags to display messages outside the column layout
                data_submitted = True
            else:
                data_submitted = False  # Handle incomplete data submission

    # Display submission success or failure message outside the column structure
    if 'data_submitted' in locals() and data_submitted:
        st.markdown("<p style='font-size: 20px; color: green;'>Data submitted successfully!</p>", unsafe_allow_html=True)
        st.markdown("<p style='font-size: 20px;'>Submitted Details:</p>", unsafe_allow_html=True)
        
        # Displaying additional details
        if company_name:
            st.markdown(f"<p style='font-size: 20px;'><strong>Building Name:</strong> {company_name}</p>", unsafe_allow_html=True)
        if postal_code:
            st.markdown(f"<p style='font-size: 20px;'><strong>Postal Code:</strong> {postal_code}</p>", unsafe_allow_html=True)
        if uploaded_file is not None:
            st.markdown("<p style='font-size: 20px;'>Uploaded Transportation Data:</p>", unsafe_allow_html=True)
            st.dataframe(transportation_data)
