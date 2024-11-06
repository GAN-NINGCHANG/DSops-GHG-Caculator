import streamlit as st
from pages import home, page_1, page_2, page_3

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
    if st.session_state.current_page > 0:
        if st.button("后退"):
            prev_page()
with col2:
    # 前进按钮，仅当当前页面不是最后一页时显示
    if st.session_state.current_page < 3:
        if st.button("前进"):
            next_page()
