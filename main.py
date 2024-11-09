import streamlit as st
from pages import home, page_1, page_2, page_3
from commuting_function import *

st.set_page_config(layout="wide")  # 设置页面为宽屏布局

# 初始化页面状态
if 'current_page' not in st.session_state:
    st.session_state.current_page = 0  # 0 代表主页

# 定义前进和后退按钮的函数
def next_page():
    if st.session_state.current_page < 3:
        st.session_state.current_page += 1

def prev_page():
    if st.session_state.current_page > 0:
        st.session_state.current_page -= 1

# 根据当前页面状态渲染对应页面
if st.session_state.current_page == 0:
    home.home()
elif st.session_state.current_page == 1:
    page_1.page_1()
elif st.session_state.current_page == 2:
    page_2.page_2()
elif st.session_state.current_page == 3:
    page_3.page_3()

# 在页面底部添加“前进”和“后退”按钮
col1, col2 = st.columns(2)
with col1:
    # 后退按钮，仅当当前页面不是主页时显示
    if st.session_state.current_page > 2:
        if st.button("Back"):
            prev_page()

# 初始化全局变量键
if 'global_vars' not in st.session_state:
    st.session_state.global_vars = {
    'Building_Name': None,
    'Postal_code': None,
    'Gross_Floor_Area': None,
    'Average_Headcount': None,
    'Building_Type': None,
    'Cook': None,
    'Electricity_Amount': None,
    'Waste_Amount':0,
    'Renewable_Energy_Proportion': None,
    'Natural_Gas_Amount': None,
    'Water_Amount': None,
    'Ferrous_Metal_Amount': None,
    'Paper_cardboard_Amount': None,
    'Construction_Demolition_Amount': None,
    'Plastics_Amount': None,
    'Food_Amount': None,
    'Horticultural_Amount': None,
    'Wood_Amount': None,
    'Waste_Amount': None,
    'Ash_sludge_Amount': None,
    'Textile_Leather_Amount': None,
    'Used_slag_Amount': None,
    'Non_Ferrous_Metal_Amount': None,
    'Glass_Amount': None,
    'Scrap_Tyres_Amount': None,
    'Others_Amount': None,
    'Drive_Distance': None,
    'Public_Distance': None,
    'Walk_Distance': None,
    'Work_Frequency': None,
    'Electricity_GHG_Emission': None,
    'Natural_Gas_GHG_Emission': None,
    'Water_GHG_Emission': None,
    'Waste_GHG_Emission': None,
    'Commute_GHG_Emission': None,
    'Total_GHG_Emission': None
<<<<<<< HEAD
    }



# 初始化全局变量键
if 'global_vars' not in st.session_state:
    st.session_state.global_vars = {
        'Building Name': None,
        'Postal code': None,
        'Gross Floor Area': None,
        'Average Headcount': None,
        'Building Type': None,
        'Cook': None,
        'Electricy Amount': None,
        'Renewable Energy Proportion': None,
        'Natural Gas Amount': None,
        'Water Amount': None,
        'Ferrous Metal Amount': None,
        'Waste_Amount':0,
        'Paper/cardboard Amount': None,
        'Construction & Demolition Amount': None,
        'Plastics Amount': None,
        'Food Amount': None,
        'Horticultural Amount': None,
        'Wood Amount': None,
        'Ash & sludge Amount': None,
        'Textile/Leather Amount': None,
        'Used slag Amount': None,
        'Non-Ferrous Metal Amount': None,
        'Glass Amount': None,
        'Scrap Tyres Amount': None,
        'Others Amount': None,
        'Drive Distance': None,
        'Public Distance': None,
        'Walk Distance': None,
        'Electricity GHG Emission': None,
        'Natural Gas GHG Emission': None,
        'Water GHG Emission': None,
        'Waste GHG Emission': None,
        'Commute GHG Emission': None,
        'Total GHG Emission': None
=======
>>>>>>> 6917b88 (Co-authored-by: Liu Anjie <e1351237@u.nus.edu>)
    }