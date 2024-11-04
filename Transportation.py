import streamlit as st
import pandas as pd

def main():
    # Set page title and layout
    st.set_page_config(page_title="Transportation Data", layout="centered")

    # Page title and description
    st.markdown("<h1 style='text-align: center; color: #4CAF50;'>Transportation Data</h1>", unsafe_allow_html=True)
    st.write("<p style='text-align: center;'>Upload your transportation data or enter details manually if you don't have a file.</p>", unsafe_allow_html=True)
    st.markdown("<hr style='border-top: 3px solid #bbb;'>", unsafe_allow_html=True)

    # Data readiness flag
    data_ready = False

    # Upload transportation data CSV file
    uploaded_file = st.file_uploader("Upload a CSV file with transportation data", type=["csv"])

    if uploaded_file is not None:
        # Display uploaded file content
        transportation_data = pd.read_csv(uploaded_file)
        st.write("Uploaded Transportation Data")
        st.dataframe(transportation_data)
        data_ready = True  # Mark data as ready
    else:
        # If no CSV file is uploaded, show detailed data input option
        show_details = st.checkbox("I don't have detailed data")

        # If the user chooses to enter detailed data manually
        if show_details:
            st.markdown("<h3 style='color: #4CAF50;'>Enter Details Manually</h3>", unsafe_allow_html=True)
            
            # Input for the number of employees
            employee_count = st.number_input("Enter the number of employees:", min_value=1, step=1)
            st.write(f"**Number of Employees:** {employee_count}")

            # Company Name and Postal Code input in the same row
            st.markdown("**Please enter either the Company Name or the Postal Code (only one is required):**")
            col1, col2 = st.columns(2)
            
            with col1:
                company_name = st.text_input("Company Name:")
            with col2:
                postal_code = st.text_input("Postal Code:")

            # Validate that only one of the fields is filled
            if company_name and postal_code:
                st.warning("Please fill in only one of the fields: Company Name or Postal Code.")
            elif not company_name and not postal_code:
                st.warning("Please enter either the Company Name or the Postal Code.")
            else:
                data_ready = True  # Mark data as ready

    # Footer buttons (Previous and Submit Data) in the same row
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("Previous"):
            st.write("This would take you to the previous page if implemented.")
    
    with col2:
        # Submit Data button
        if st.button("Submit Data"):
            if data_ready:
                st.success("Data submitted successfully!")
                if show_details:
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

if __name__ == "__main__":
    main()
