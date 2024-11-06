import streamlit as st
import pandas as pd
import altair as alt
import numpy as np
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import base64
from reportlab.platypus import Table, TableStyle
from reportlab.lib import colors
from reportlab.graphics.shapes import Drawing
from reportlab.graphics.charts.barcharts import VerticalBarChart


def page_3():
    # 设置网页标题和图标

    # 将图片转换为 Base64
    def get_base64_image(file_path):
        with open(file_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode()

    # 获取 Base64 编码的图片
    base64_image = get_base64_image("/workspaces/DSops-GHG-Caculator/src/istockphoto.jpg")

    # 自定义 CSS 样式设置背景图片
    page_bg_img = f'''
    <style>
    .stApp {{
        background-image: url("data:image/jpg;base64,{base64_image}");
        background-size: cover;
        background-repeat: no-repeat;
        background-attachment: fixed;
        background-position: center;
        color: #333;
        font-family: 'Arial', sans-serif;
    }}
    .block-container {{
        background-color: rgba(255, 255, 255, 0.8);
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0px 4px 15px rgba(0, 0, 0, 0.1);
    }}
    .sidebar .sidebar-content {{
        background: rgba(255, 255, 255, 0.9);
        padding: 1rem;
        border-radius: 10px;
    }}
    .css-1q8dd3e p {{
        font-size: 1.1rem;
    }}
    </style>
    '''
    st.markdown(page_bg_img, unsafe_allow_html=True)

    # 应用标题和描述
    st.title("🌍 Company GHG Emissions Dashboard")
    st.markdown("""
    Welcome to the Company GHG Emissions Dashboard! Here, you can upload a CSV file containing data on greenhouse gas (GHG) emissions.
    Select a company to view its GHG emission profile and compare it with other companies. Discover insights into emission factors
    and identify companies with similar profiles.
    """)

    # 上传数据
    uploaded_file = st.file_uploader("Upload your GHG emissions CSV file", type=['csv'])

    if uploaded_file is not None:
        # 读取上传的CSV文件
        df = pd.read_csv(uploaded_file)

        # 检查数据是否包含所需的列
        required_columns = ['BuildingName', 'AC', 'GAS', 'COLDING', 'COMMUTE', 'RENEWABLE']
        if all(col in df.columns for col in required_columns):

            # 添加分隔符
            st.markdown("---")

            # 用户选择自己的公司
            st.sidebar.header("Select a Company")
            companies = df['BuildingName'].unique()
            user_company = st.sidebar.selectbox(
                '🏢 Choose a company:', 
                companies
            )

            if user_company:
                # 计算与用户公司消耗量最接近的五个公司（使用欧氏距离）
                def calculate_euclidean_distance(df, user_company):
                    user_row = df[df['BuildingName'] == user_company].iloc[:, 1:].values
                    other_rows = df[df['BuildingName'] != user_company].iloc[:, 1:].values
                    distances = np.linalg.norm(other_rows - user_row, axis=1)
                    closest_indices = np.argsort(distances)[:5]
                    closest_companies = df['BuildingName'].iloc[closest_indices].values
                    return closest_companies

                closest_companies = calculate_euclidean_distance(df, user_company)

                # 显示与用户公司最接近的5个公司
                st.markdown("### 🌐 Top 5 Companies with Similar GHG Profiles")
                st.info(
                    f"Based on GHG emissions, here are the companies most similar to **{user_company}**. "
                    "This comparison can help you understand where your company stands in relation to others."
                )
                st.markdown(", ".join([f"🏢 **{company}**" for company in closest_companies]))

                # 展示公司 GHG 消耗数据
                st.markdown("### 📊 GHG Emissions Overview")
                st.info(f"Detailed GHG emissions data for **{user_company}**.")
                user_data = df[df['BuildingName'] == user_company].iloc[0, 1:]
                max_consumption = user_data.idxmax()

                cols = st.columns(5)
                for i, col_name in enumerate(user_data.index):
                    cols[i].metric(
                        label=col_name,
                        value=f"{user_data[col_name]:.2f} tons",
                        delta=f"Top Emission" if col_name == max_consumption else None
                    )

                st.warning(f"🚨 The largest GHG emission factor for **{user_company}** is **{max_consumption}**.")

                # 绘制用户公司及其五个最接近公司的堆叠柱状图
                st.markdown("### 📈 GHG Emissions Comparison")
                closest_df = df[df['BuildingName'].isin([user_company] + list(closest_companies))]

                closest_melted_df = closest_df.melt(id_vars='BuildingName', 
                                                    value_vars=['AC', 'GAS', 'COLDING', 'COMMUTE', 'RENEWABLE'],
                                                    var_name='Emission Type', 
                                                    value_name='Emissions (tons)')

                if not closest_melted_df.empty:
                    closest_stacked_bar = alt.Chart(closest_melted_df).mark_bar().encode(
                        x=alt.X('BuildingName:N', title='Company Name'),
                        y=alt.Y('sum(Emissions (tons)):Q', title='Total GHG Emissions (tons)'),
                        color='Emission Type:N',
                        tooltip=['BuildingName', 'Emission Type', 'Emissions (tons)']
                    ).properties(
                        width=800,
                        height=400
                    ).interactive()

                    st.altair_chart(closest_stacked_bar, use_container_width=True)
                else:
                    st.write("No data available for the selected companies.")

                # 添加生成 PDF 的功能
                st.markdown("### 📝 Download Emission Report")
                st.info("Generate a PDF report to save or share the GHG emissions data.")
                if st.button("Generate PDF"):
                    pdf_buffer = BytesIO()
                    c = canvas.Canvas(pdf_buffer, pagesize=letter)

                    # 添加标题
                    c.setFont("Helvetica-Bold", 16)
                    c.drawString(100, 800, "GHG Emissions Report")

                    # 添加段落
                    c.setFont("Helvetica", 12)
                    c.drawString(100, 780, f"Company: {user_company}")
                    c.drawString(100, 760, f"Largest GHG emission factor: {max_consumption}")

                    # 准备数据
                    data = [['Company', 'AC', 'GAS', 'COLDING', 'COMMUTE', 'RENEWABLE']]
                    for company in closest_companies:
                        row = [company] + df[df['BuildingName'] == company].iloc[0, 1:].tolist()
                        data.append(row)

                    # 创建表格
                    table = Table(data)
                    table.setStyle(TableStyle([
                        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                        ('GRID', (0, 0), (-1, -1), 1, colors.black),
                    ]))

                    # 绘制表格和图表
                    table.wrapOn(c, 100, 580)
                    table.drawOn(c, 100, 580)

                    # 绘制边框和背景
                    c.setStrokeColor(colors.grey)
                    c.setLineWidth(1)
                    c.rect(50, 50, 500, 700, stroke=1, fill=0)

                    c.save()
                    pdf_buffer.seek(0)

                    # 提供 PDF 下载链接
                    st.download_button(
                        label="Download PDF",
                        data=pdf_buffer,
                        file_name="ghg_emission_report.pdf",
                        mime="application/pdf"
                    )

        else:
            st.error("The uploaded CSV file does not contain the required columns: 'BuildingName', 'AC', 'GAS', 'COLDING', 'COMMUTE', 'RENEWABLE'.")
