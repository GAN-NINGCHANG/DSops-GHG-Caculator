import streamlit as st

# Define a function to show different sections
def show_section(section):
    st.session_state['current_section'] = section

# Initialize session state for navigation
if 'current_section' not in st.session_state:
    st.session_state['current_section'] = 'mainPage'

# Define the sections
def main_page():
    st.title("欢迎来到碳足迹计算器")
    st.write("帮助您计算碳足迹并提供可持续生活建议")

    st.button("开始计算", on_click=lambda: show_section('calculatorPage'))

    st.subheader("碳排放的全球统计")
    st.write("每年约有 510 亿吨二氧化碳排放……")

    st.subheader("环保小贴士")
    st.write("减少食物浪费、选择公共交通、减少塑料使用……")

def calculator_page():
    st.title("碳计算器")
    st.write("在此输入您的日常生活数据以计算碳排放量。")

    electricity = st.number_input("电力使用量 (kWh):", min_value=0.0, step=0.1)
    gas = st.number_input("天然气使用量 (立方米):", min_value=0.0, step=0.1)
    transport = st.number_input("交通（公里数）:", min_value=0.0, step=0.1)

    if st.button("计算"):
        # Simple formula for demonstration, you can replace with actual calculation logic
        carbon_footprint = electricity * 0.5 + gas * 1.2 + transport * 0.3
        st.write(f"您的碳足迹估算为: {carbon_footprint:.2f} kg CO₂")

def education_page():
    st.title("环保教育")
    st.write("了解碳排放和气候变化的影响，并获得日常生活中降低碳足迹的技巧。")

def history_page():
    st.title("历史数据")
    st.write("查看您的碳排放历史记录，跟踪您的环保进步。")

def contact_page():
    st.title("联系我们")
    st.write("如有任何疑问或建议，请通过以下方式联系我们。")

    name = st.text_input("姓名")
    email = st.text_input("邮箱")
    message = st.text_area("消息")

    if st.button("发送"):
        st.write("感谢您的反馈！我们会尽快回复您。")

# Navigation bar at the top
st.sidebar.title("导航栏")
st.sidebar.button("主页", on_click=lambda: show_section('mainPage'))
st.sidebar.button("碳计算器", on_click=lambda: show_section('calculatorPage'))
st.sidebar.button("环保教育", on_click=lambda: show_section('educationPage'))
st.sidebar.button("历史数据", on_click=lambda: show_section('historyPage'))
st.sidebar.button("联系我们", on_click=lambda: show_section('contactPage'))

# Display the selected section
if st.session_state['current_section'] == 'mainPage':
    main_page()
elif st.session_state['current_section'] == 'calculatorPage':
    calculator_page()
elif st.session_state['current_section'] == 'educationPage':
    education_page()
elif st.session_state['current_section'] == 'historyPage':
    history_page()
elif st.session_state['current_section'] == 'contactPage':
    contact_page()
