import streamlit as st
import pandas as pd

def page_2():
    

    # 页面标题和描述
    st.markdown("<h1 style='text-align: center; color: #4CAF50;'>Transportation Data</h1>", unsafe_allow_html=True)
    st.write("<p style='text-align: center;'>Upload your transportation data or enter details manually.</p>", unsafe_allow_html=True)
    st.markdown("<hr style='border-top: 3px solid #bbb;'>", unsafe_allow_html=True)

    # 上传示例文件的下载链接
    st.markdown("[Download Sample CSV File](https://example.com/sample.csv)", unsafe_allow_html=True)  # 替换为实际的示例文件链接

    # 提供上传 CSV 文件的选项
    data_ready = False
    uploaded_file = st.file_uploader("Upload a CSV file with transportation data", type=["csv"])
    st.info("Note: Uploading a CSV file will generate an additional professional report.")

    if uploaded_file is not None:
        # 显示上传文件内容
        try:
            transportation_data = pd.read_csv(uploaded_file)
            st.write("Uploaded Transportation Data")
            st.dataframe(transportation_data)
            data_ready = True  # 标记数据已准备好
        except Exception as e:
            st.error("Error reading the CSV file. Please ensure it is in the correct format.")
    else:
        # 显示手动输入数据的选项
        st.markdown("<h3 style='color: #4CAF50;'>Enter Details Manually</h3>", unsafe_allow_html=True)
        
        # 输入员工数量
        employee_count = st.number_input("Enter the number of employees:", min_value=1, step=1)
        st.write(f"**Number of Employees:** {employee_count}")

        # 公司名称和邮政编码输入
        st.markdown("**Please enter either the Company Name or the Postal Code (at least one is required):**")
        col1, col2 = st.columns(2)

        with col1:
            company_name = st.text_input("Company Name:")
        with col2:
            postal_code = st.text_input("Postal Code:")

        # 校验公司名称和邮政编码的输入
        if not company_name and not postal_code:
            st.warning("Please fill in at least one of the fields: Company Name or Postal Code.")
            data_ready = False
        else:
            data_ready = True  # 标记数据已准备好

    # 页面底部的按钮布局
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("Previous"):
            st.write("This would take you to the previous page if implemented.")

    with col2:
        # 提交数据按钮
        if st.button("Submit Data"):
            if data_ready:
                st.success("Data submitted successfully!")
                st.write("Submitted Details:")
                st.write(f"**Employee Count:** {employee_count}")
                if company_name:
                    st.write(f"**Company Name:** {company_name}")
                if postal_code:
                    st.write(f"**Postal Code:** {postal_code}")
                if uploaded_file is not None:
                    st.write("Uploaded Transportation Data:")
                    st.dataframe(transportation_data)
            else:
                st.error("Please either upload a CSV file or fill in the detailed data.")

# 调用 show 函数来显示页面内容
