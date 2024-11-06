import streamlit as st
from pages import home, page_1, page_2, page_3  # 导入页面模块

# 创建一个页面选择框
page = st.sidebar.selectbox("选择页面", ("主页", "页面 1", "页面 2", "页面 3"))

# 根据选择调用不同的页面模块中的显示函数
if page == "主页":
    home.show()  # 调用主页的显示函数
elif page == "页面 1":
    page_1.show()  # 调用页面 1 的显示函数
elif page == "页面 2":
    page_2.show()  # 调用页面 2 的显示函数
elif page == "页面 3":
    page_3.show()  # 调用页面 3 的显示函数
