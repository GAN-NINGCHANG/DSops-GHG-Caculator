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
