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


def page_3():
    # 将图片转换为 Base64
    def get_base64_image(file_path):
        with open(file_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode()

    # 使用指定的背景图
    base64_image = get_base64_image("/workspaces/DSops-GHG-Caculator/src/background.jpg")

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
        background-color: rgba(255, 255, 255, 0.25);
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0px 4px 15px rgba(0, 0, 0, 0.1);
    }}
    </style>
    '''
    st.markdown(page_bg_img, unsafe_allow_html=True)

    # 页面标题和描述
    st.title("🌍 Company GHG Emissions Results")
    st.markdown("""
    Welcome to the Company GHG Emissions Results! Enter a company name to view its GHG emission profile.
    """)

    # 读取本地 CSV 数据
    data_file_path = "/workspaces/DSops-GHG-Caculator/data/Random_Building_Data.csv"
    df = pd.read_csv(data_file_path)

    # 检查数据是否包含所需的列
    required_columns = ['BuildingName', 'AC', 'GAS', 'COLDING', 'COMMUTE', 'RENEWABLE']
    if not all(col in df.columns for col in required_columns):
        st.error("The data file does not contain the required columns.")
        return

    # 顶部公司名称输入框
    company_name = st.text_input("Enter the company name for analysis:")

    # 检查公司名称并分析数据
    if company_name and company_name in df['BuildingName'].values:
        
        # 计算与指定公司消耗量最接近的五个公司（使用欧氏距离）
        def calculate_euclidean_distance(df, company_name):
            user_row = df[df['BuildingName'] == company_name].iloc[:, 1:].values
            other_rows = df[df['BuildingName'] != company_name].iloc[:, 1:].values
            distances = np.linalg.norm(other_rows - user_row, axis=1)
            closest_indices = np.argsort(distances)[:5]
            closest_companies = df['BuildingName'].iloc[closest_indices].values
            return closest_companies

        closest_companies = calculate_euclidean_distance(df, company_name)

        # 展示公司 GHG 消耗数据
        st.markdown("### 📊 GHG Emissions Overview")
        st.info(f"Detailed GHG emissions data for **{company_name}**.")
        user_data = df[df['BuildingName'] == company_name].iloc[0, 1:]
        max_consumption = user_data.idxmax()

        cols = st.columns(5)
        for i, col_name in enumerate(user_data.index):
            cols[i].metric(
                label=col_name,
                value=f"{user_data[col_name]:.2f} tons",
                delta=f"Top Emission" if col_name == max_consumption else None
            )

        st.warning(f"🚨 The largest GHG emission factor for **{company_name}** is **{max_consumption}**.")

        # 计算所有公司 GHG 排放的平均值
        df['TotalEmissions'] = df[['AC', 'GAS', 'COLDING', 'COMMUTE', 'RENEWABLE']].sum(axis=1)
        overall_average = df['TotalEmissions'].mean()

        # 绘制公司及最接近的5个公司的堆叠柱状图，隐藏公司名，仅显示输入的公司名
        st.markdown("### 📈 GHG Emissions Comparison (with Average)")
        selected_df = df[df['BuildingName'].isin([company_name] + list(closest_companies))].copy()

        # 为相似公司设置匿名标签（例如 Anonymous1234、Anonymous5678）
        for i, company in enumerate(closest_companies, start=1):
            selected_df.loc[selected_df['BuildingName'] == company, 'DisplayName'] = f"Anonymous{i}"
        
        # 将输入的公司名称保持不变
        selected_df.loc[selected_df['BuildingName'] == company_name, 'DisplayName'] = company_name

        # 数据转换为适合绘图的格式
        selected_melted_df = selected_df.melt(id_vars='DisplayName', 
                                              value_vars=['AC', 'GAS', 'COLDING', 'COMMUTE', 'RENEWABLE'],
                                              var_name='Emission Type', 
                                              value_name='Emissions (tons)')

        # 绘制柱状图，仅标注用户输入的公司名称
        stacked_bar = alt.Chart(selected_melted_df).mark_bar().encode(
            x=alt.X('DisplayName:N', title='Company Name', axis=alt.Axis(labelAngle=0)),  # 将公司名称横置
            y=alt.Y('sum(Emissions (tons)):Q', title='Total GHG Emissions (tons)'),
            color='Emission Type:N',
            tooltip=['DisplayName', 'Emission Type', 'Emissions (tons)']
        ).properties(
            width=800,
            height=400
        )

        # 添加虚线标注所有公司总排放的平均值
        mean_line = alt.Chart(pd.DataFrame({'y': [overall_average]})).mark_rule(
            strokeDash=[5, 5],
            color='red'
        ).encode(y='y:Q')

        st.altair_chart(stacked_bar + mean_line, use_container_width=True)

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
            c.drawString(100, 780, f"Company: {company_name}")
            c.drawString(100, 760, f"Largest GHG emission factor: {max_consumption}")

            # 准备数据
            data = [['Company', 'AC', 'GAS', 'COLDING', 'COMMUTE', 'RENEWABLE']]
            row = [company_name] + df[df['BuildingName'] == company_name].iloc[0, 1:].tolist()
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
        st.warning("Please enter a valid company name.")
