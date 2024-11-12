import streamlit as st
import pandas as pd
import numpy as np
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
import matplotlib.pyplot as plt
import io
import base64
import altair as alt
from utils import sensitivity_analysis
import re
import model_update
import os


def page_3():
    # Change graph to Base64
    def get_base64_image(file_path):
        with open(file_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode()

    # Background photo
    base64_image = get_base64_image("/workspaces/DSops-GHG-Caculator/src/background.jpg")
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
    
    # Extract value in former pages
    waste_amounts = {
        'Ferrous_Metal_Amount': 0.00119,
        'Paper_cardboard_Amount': 0.14993,
        'Construction_Demolition_Amount': 0.00337,
        'Plastics_Amount': 0.15732,
        'Food_Amount': 0.10754,
        'Horticultural_Amount': 0.00625,
        'Wood_Amount': 0.02518,
        'Ash_sludge_Amount': 0.03363,
        'Textile_Leather_Amount': 0.03481,
        'Used_slag_Amount': 0.00056,
        'Non_Ferrous_Metal_Amount': 0.00015,
        'Glass_Amount': 0.01140,
        'Scrap_Tyres_Amount': 0.00017,
        'Others_Amount': 0.03922
    }
    
    building_name = st.session_state.global_vars.get('Building_Name')
    postal_code = st.session_state.global_vars.get('Postal_Code')
    gross_floor_area = st.session_state.global_vars.get('Gross_Floor_Area')
    average_headcount = st.session_state.global_vars.get('Average_Headcount')
    building_type = st.session_state.global_vars.get('Building_Type')
    cook = st.session_state.global_vars.get('Cook')
    electricity_amount = st.session_state.global_vars.get('Electricity_Amount')
    waste_amount = st.session_state.global_vars.get('Waste_Amount', 0)
    renewable_energy_proportion = st.session_state.global_vars.get('Renewable_Energy_Proportion')
    natural_gas_amount = st.session_state.global_vars.get('Natural_Gas_Amount')
    water_amount = st.session_state.global_vars.get('Water_Amount')
    st.session_state.global_vars['Ferrous_Metal_Amount'] = waste_amounts['Ferrous_Metal_Amount'] * average_headcount
    ferrous_metal_amount = st.session_state.global_vars.get('Ferrous_Metal_Amount')
    st.session_state.global_vars['Paper_cardboard_Amount'] = waste_amounts['Paper_cardboard_Amount'] * average_headcount
    paper_cardboard_amount = st.session_state.global_vars.get('Paper_cardboard_Amount')
    st.session_state.global_vars['Construction_Demolition_Amount'] = waste_amounts['Construction_Demolition_Amount'] * average_headcount
    construction_demolition_amount = st.session_state.global_vars.get('Construction_Demolition_Amount')
    st.session_state.global_vars['Plastics_Amount'] = waste_amounts['Plastics_Amount'] * average_headcount
    plastics_amount = st.session_state.global_vars.get('Plastics_Amount')
    st.session_state.global_vars['Food_Amount'] = waste_amounts['Food_Amount'] * average_headcount
    food_amount = st.session_state.global_vars.get('Food_Amount')
    st.session_state.global_vars['Horticultural_Amount'] = waste_amounts['Horticultural_Amount'] * average_headcount
    horticultural_amount = st.session_state.global_vars.get('Horticultural_Amount')
    st.session_state.global_vars['Wood_Amount'] = waste_amounts['Wood_Amount'] * average_headcount
    wood_amount = st.session_state.global_vars.get('Wood_Amount')
    st.session_state.global_vars['Ash_sludge_Amount'] = waste_amounts['Ash_sludge_Amount'] * average_headcount
    ash_sludge_amount = st.session_state.global_vars.get('Ash_sludge_Amount')
    st.session_state.global_vars['Textile_Leather_Amount'] = waste_amounts['Textile_Leather_Amount'] * average_headcount
    textile_leather_amount = st.session_state.global_vars.get('Textile_Leather_Amount')
    st.session_state.global_vars['Used_slag_Amount'] = waste_amounts['Used_slag_Amount'] * average_headcount
    used_slag_amount = st.session_state.global_vars.get('Used_slag_Amount')
    st.session_state.global_vars['Non_Ferrous_Metal_Amount'] = waste_amounts['Non_Ferrous_Metal_Amount'] * average_headcount
    non_ferrous_metal_amount = st.session_state.global_vars.get('Non_Ferrous_Metal_Amount')
    st.session_state.global_vars['Glass_Amount'] = waste_amounts['Glass_Amount'] * average_headcount
    glass_amount = st.session_state.global_vars.get('Glass_Amount')
    st.session_state.global_vars['Scrap_Tyres_Amount'] = waste_amounts['Scrap_Tyres_Amount'] * average_headcount
    scrap_tyres_amount = st.session_state.global_vars.get('Scrap_Tyres_Amount')
    st.session_state.global_vars['Others_Amount'] = waste_amounts['Others_Amount'] * average_headcount
    others_amount = st.session_state.global_vars.get('Others_Amount')
    drive_distance = st.session_state.global_vars.get('Drive_Distance')
    public_distance = st.session_state.global_vars.get('Public_Distance')
    walk_distance = st.session_state.global_vars.get('Walk_Distance')
    work_frequency = st.session_state.global_vars.get('Work_Frequency')
    electricity_ghg_emission = st.session_state.global_vars.get('Electricity_GHG_Emission')
    natural_gas_ghg_emission = st.session_state.global_vars.get('Natural_Gas_GHG_Emission')
    water_ghg_emission = st.session_state.global_vars.get('Water_GHG_Emission')
    waste_ghg_emission = st.session_state.global_vars.get('Waste_GHG_Emission')
    commute_ghg_emission = st.session_state.global_vars.get('Commute_GHG_Emission')
    total_ghg_emission = st.session_state.global_vars.get('Total_GHG_Emission')
    st.session_state.global_vars['GHG_Unit_Intensity'] = total_ghg_emission / gross_floor_area
    ghg_unit_intensity = st.session_state.global_vars.get('GHG_Unit_Intensity')

    mapping = {
    'Hotel': 0,
    'Mixed Development': 1,
    'Office': 2,
    'Retail': 3
    }

    PBA = mapping.get(building_type, -1)  
    PBA = pd.Categorical([PBA])  

    # Save value in former pages
    data = {
        'Building_Name': building_name,
        'Postal_Code': postal_code,
        'Gross_Floor_Area': gross_floor_area,
        'Average_Headcount': average_headcount,
        'Building_Type': building_type,
        'Cook': cook,
        'Electricity_Amount': electricity_amount,
        'Waste_Amount': waste_amount,
        'Renewable_Energy_Proportion': renewable_energy_proportion,
        'Natural_Gas_Amount': natural_gas_amount,
        'Water_Amount': water_amount,
        'Ferrous_Metal_Amount': ferrous_metal_amount,
        'Paper_cardboard_Amount': paper_cardboard_amount,
        'Construction_Demolition_Amount': construction_demolition_amount,
        'Plastics_Amount': plastics_amount,
        'Food_Amount': food_amount,
        'Horticultural_Amount': horticultural_amount,
        'Wood_Amount': wood_amount,
        'Ash_sludge_Amount': ash_sludge_amount,
        'Textile_Leather_Amount': textile_leather_amount,
        'Used_slag_Amount': used_slag_amount,
        'Non_Ferrous_Metal_Amount': non_ferrous_metal_amount,
        'Glass_Amount': glass_amount,
        'Scrap_Tyres_Amount': scrap_tyres_amount,
        'Others_Amount': others_amount,
        'Drive_Distance': drive_distance,
        'Public_Distance': public_distance,
        'Walk_Distance': walk_distance,
        'Work_Frequency': work_frequency,
        'Electricity_GHG_Emission': electricity_ghg_emission,
        'Natural_Gas_GHG_Emission': natural_gas_ghg_emission,
        'Water_GHG_Emission': water_ghg_emission,
        'Waste_GHG_Emission': waste_ghg_emission,
        'Commute_GHG_Emission': commute_ghg_emission,
        'Total_GHG_Emission': total_ghg_emission,
        'GHG_Unit_Intensity':ghg_unit_intensity
    }
    
    data_for_water = {
        'PBA': PBA,
        'SQFT': gross_floor_area,
        'NWKER': average_headcount,
        'TYPE': building_type,
        'WTCNS': water_amount,
    }

    data_for_electricity = {
        'Gross_Floor_Area': gross_floor_area,
        'Building Type': building_type,
        '2020EUI': electricity_amount/gross_floor_area,
    }    
    
    # Add data to database
    model_update.add_data_to_firestore(data,"Full_table")
    model_update.add_data_to_firestore(data_for_water,"Water_data")
    model_update.add_data_to_firestore(data_for_electricity,"Electricity_data")
    model_update.update_models()

    # Read file
    df_new = pd.DataFrame([data])
    file_path = "/workspaces/DSops-GHG-Caculator/data/Full_table.csv"

    # Title and description
    st.title("🌍 Building GHG Emissions Results")
    st.markdown("""
    Welcome to the Building GHG Emissions Results!
    """)

    # Read full table data
    df = pd.read_csv(file_path)
    df = pd.concat([df,df_new],axis=0,ignore_index=True)

    # Find most similar 5 buildings
    def calculate_euclidean_distance(df, building_name):
        user_row = df[df['Building_Name'] == building_name].iloc[:, -7:-2].values
        other_rows = df[df['Building_Name'] != building_name].iloc[:, -7:-2].values
        distances = np.linalg.norm(other_rows - user_row, axis=1)
        closest_indices = np.argsort(distances)[:5]
        closest_companies = df['Building_Name'].iloc[closest_indices].values
        return closest_companies

    closest_companies = calculate_euclidean_distance(df, building_name)

    # Show GHG emissions of the building
    st.markdown("### 📊 GHG Emissions Overview")
    st.info(f"Detailed GHG emissions data for **{building_name}**.")
    user_data = df[df['Building_Name'] == building_name].iloc[0, -7:-2]
    max_consumption = user_data.idxmax()
    
    def extract_name(s):
        match = re.match(r"([A-Za-z]+(?:_[A-Za-z]+)*)_GHG_Emission", s)
        if match:
            return match.group(1).replace('_', ' ')  
        return None
    
    cols = st.columns(5)
    for i, col_name in enumerate(user_data.index):
        cols[i].metric(
            label= extract_name(col_name),
            value=f"{user_data[col_name]:.2f} kgs",
            delta=f"Top Emission" if col_name == max_consumption else None
        )

    st.warning(f"🚨 The largest GHG emission factor for **{building_name}** is **{max_consumption}**.")

    # Plot the barplot
    overall_average = df['Total_GHG_Emission'].mean()

    st.markdown("### 📈 GHG Emissions Comparison (with Average)")
    selected_df = df[df['Building_Name'].isin([building_name] + list(closest_companies))].copy()

    # Set anoynymous label for similar company
    for i, building in enumerate(closest_companies, start=1):
        selected_df.loc[selected_df['Building_Name'] == building, 'DisplayName'] = f"Anonymous{i}"

    selected_df.loc[selected_df['Building_Name'] == building_name, 'DisplayName'] = building_name

    # Change the format of the data to make plots
    selected_melted_df = selected_df.melt(id_vars='DisplayName', 
                                        value_vars=[
                                            'Electricity_GHG_Emission', 
                                            'Natural_Gas_GHG_Emission',
                                            'Water_GHG_Emission', 
                                            'Waste_GHG_Emission', 
                                            'Commute_GHG_Emission'
                                            ],
                                        var_name='Emission Type', 
                                        value_name='Emissions (kgs)')

    stacked_bar = alt.Chart(selected_melted_df).mark_bar().encode(
        x=alt.X('DisplayName:N', title='Building Name', axis=alt.Axis(labelAngle=0)), 
        y=alt.Y('sum(Emissions (kgs)):Q', title='Total GHG Emissions (kgs)'),
        color='Emission Type:N',
        tooltip=['DisplayName', 'Emission Type', 'Emissions (kgs)']
    ).properties(
        width=800,
        height=400
    )

    # Add the line for average total emissions
    mean_line = alt.Chart(pd.DataFrame({'y': [overall_average]})).mark_rule(
        strokeDash=[5, 5],
        color='red'
    ).encode(y='y:Q')
    
    st.altair_chart(stacked_bar + mean_line, use_container_width=True)
    
    ## Sensitivity Analysis
    st.markdown("### 🔍 Sensitivity Analysis")
    base_values = {
        'Electricity_Amount': electricity_amount,
        'Renewable_Energy_Proportion': renewable_energy_proportion,
        'Natural_Gas_Amount': natural_gas_amount,
        'Water_Amount': water_amount,
        'Ferrous_Metal_Amount': ferrous_metal_amount,
        'Paper_cardboard_Amount': paper_cardboard_amount,
        'Construction_Demolition_Amount': construction_demolition_amount,
        'Plastics_Amount': plastics_amount,
        'Food_Amount': food_amount,
        'Horticultural_Amount': horticultural_amount,
        'Wood_Amount': wood_amount,
        'Ash_sludge_Amount': ash_sludge_amount,
        'Textile_Leather_Amount': textile_leather_amount,
        'Used_Slag_Amount': used_slag_amount,
        'Non_Ferrous_Metal_Amount': non_ferrous_metal_amount,
        'Glass_Amount': glass_amount,
        'Scrap_Tyres_Amount': scrap_tyres_amount,
        'Others_Amount': others_amount,
        'Drive_Distance': drive_distance,
        'Public_Distance': public_distance,
        'Walk_Distance': walk_distance,
        'Work_Frequency': work_frequency
    }

    analyzer = sensitivity_analysis.EmissionsSensitivityAnalyzer(base_values)
    analyzer.perform_sensitivity_analysis()

    # Plot tornado graph
    plt = analyzer.plot_tornado_diagram()
    st.pyplot(plt)

    # Give suggestions
    improvements = analyzer.analyze_top_3_impact(base_values)
    for i, (var, details) in enumerate(improvements.items(), start=1):
        st.markdown(f"### Top {i} Influencing Factor: {var}")
        st.markdown(f"**GHG Emissions Reduction with 10% Improvement**: {details['reduction_amount']} kg CO2e")
        st.markdown(f"**Suggested Improvement**: {details['suggestion']}")
        st.markdown("---")  # A separator line for clarity between entries
    
    ## Generate PDF 
    st.markdown("### 📝 Download Emission Report")
    st.info("Generate a PDF report to save or share the GHG emissions data.")
    if st.button("Generate PDF"):
        # Prepare content
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4)
        styles = getSampleStyleSheet()
        story = []

        # Add title
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            spaceAfter=30
        )
        story.append(Paragraph(f"Building GHG Emissions Report - {building_name}", title_style))
        story.append(Spacer(1, 20))

        # Basic infomation graph
        basic_info = [
            ["Building Information", "Value"],
            ["Building Name", building_name],
            ["Postal Code", postal_code],
            ["Gross Floor Area", f"{gross_floor_area} sqm"],
            ["Average Headcount", str(average_headcount)],
            ["Building Type", building_type]
        ]
        basic_table = Table(basic_info, colWidths=[200, 200])
        basic_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 14),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        story.append(basic_table)
        story.append(Spacer(1, 20))

        # GHG emissions graph
        story.append(Paragraph("GHG Emissions Breakdown", styles['Heading2']))
        emissions_data = [
            ["Emission Source", "Amount (kg CO2e)"],
            ["Electricity", f"{electricity_ghg_emission:.2f}"],
            ["Natural Gas", f"{natural_gas_ghg_emission:.2f}"],
            ["Water", f"{water_ghg_emission:.2f}"],
            ["Waste", f"{waste_ghg_emission:.2f}"],
            ["Commute", f"{commute_ghg_emission:.2f}"],
            ["Total", f"{total_ghg_emission:.2f}"]
        ]
        emissions_table = Table(emissions_data, colWidths=[200, 200])
        emissions_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        story.append(emissions_table)
        story.append(Spacer(1, 20))

        # Save the compared graphs to PDF
        chart_path = "temp_chart.png"
        stacked_bar.save(chart_path)
        story.append(PageBreak())
        story.append(Paragraph("Emissions Comparison with Similar Buildings", styles['Heading2']))
        story.append(Image(chart_path, width=400, height=300))
        story.append(Spacer(1, 20))

        # Add sensitivity analysis result
        story.append(Paragraph("Sensitivity Analysis Results", styles['Heading2']))
        improvements = analyzer.analyze_top_3_impact(base_values)
        for i, (var, details) in enumerate(improvements.items(), start=1):
            story.append(Paragraph(f"Top {i} Influencing Factor: {var}", styles['Heading3']))
            story.append(Paragraph(f"Potential GHG Reduction: {details['reduction_amount']} kg CO2e", styles['Normal']))
            story.append(Paragraph(f"Suggestion: {details['suggestion']}", styles['Normal']))
            story.append(Spacer(1, 10))

        # Generate PDF
        doc.build(story)
        buffer.seek(0)

        # Add download button
        st.download_button(
            label="📥 Download PDF Report",
            data=buffer,
            file_name=f"GHG_Report_{building_name}.pdf",
            mime="application/pdf",
        )
        # Remove temp file
        if os.path.exists(chart_path):
            os.remove(chart_path)
