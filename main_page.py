import streamlit as st

# Set up the page configuration with a title
st.set_page_config(page_title="Building Carbon Emission Calculator", layout="wide")

# Add the CSS for the page background and banner
st.markdown(
    """
    <style>
        body {
            background-image: url('https://kaizenaire.com/wp-content/uploads/2024/06/singapore-botanic-gardens-map.jpg'); /* Set your background image URL */
            background-size: cover; /* Cover the entire screen */
            background-position: center; /* Center the background image */
            background-repeat: no-repeat; /* Do not repeat the image */
            color: #333; /* Text color */
        }
        .banner {
            background-color: #e4e2dd;
            padding: 5px 0; /* Padding to ensure some space inside */
            display: flex; /* Use flexbox layout */
            justify-content: space-around; /* Space elements evenly */
            align-items: center; /* Center items vertically */
            min-height: 0px; /* Set a minimum height for the banner */
            margin: 0; /* Remove default margins */
        }
        .banner a {
            background-color: #e4e2dd;
            text-decoration: none; /* Remove underline from links */
            color: #333; /* Link color */
            font-size: 18px;
            font-weight: bold;
            padding: 0 0; /* Add padding to links */
            margin: 0 0; /* Remove any default margin */
            line-height: 1; /* Reduce line height to minimize space */
        }
        .banner a:hover {
            color: #e4e2dd; /* Change link color on hover */
        }
        .banner img {
            max-width: 50px; /* Set maximum width for banner images */
            height: auto; /* Keep the aspect ratio */
            margin: 0; /* Remove any default margin around images */
        }
    </style>
    """,
    unsafe_allow_html=True
)


banner = st.container()
with banner: 
    st.markdown('<div class="banner">', unsafe_allow_html=True)
    # Banner content with links to different sections
    col1, col2, col3, col4, col5, col6, col7 = st.columns(7)
    with col1:
        st.markdown('<div class="banner"><a href="#introduction">Introduction</a></div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="banner"><a href="#about_us">About us</a></div>', unsafe_allow_html=True)
    with col3:
        st.markdown('<div class="banner"><a href="#how_it_works">How it works</a></div>', unsafe_allow_html=True)
    with col4:
        st.markdown('<div class="banner"><a href="#how_can_it_help_you">How can it help you</a></div>', unsafe_allow_html=True)
    with col5:
        st.markdown('<div class="banner"><a href="#contact">Contact Us</a></div>', unsafe_allow_html=True)
    with col7:
        st.image('src/DSOps_logo.png', use_column_width=True)
    with col6: 
        st.image('src/nus_logo_full-vertical.png', use_column_width=True)

        st.markdown("</div>", unsafe_allow_html=True)

    

# Section: Introduction
st.markdown('<a id="introduction"></a>', unsafe_allow_html=True)

# Custom CSS for image size
st.markdown(
    """
    <style>
    .large-image img {
        width: 100%;
        max-width: 600px; /* Adjust this value to control the maximum width of the image */
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Create two columns for the title and the image
col1, col2 = st.columns([1, 1.2])  # Adjust column widths to control space allocation

with col1: 
    # Main title and description
    st.markdown("<h1 style='font-size: 50px; text-align: left;'>Building Carbon Emission Calculator</h1>", unsafe_allow_html=True)
    st.write("Welcome to our Building Carbon Emission Estimator! In a world increasingly aware of the impacts of climate change, understanding and reducing carbon emissions is more crucial than ever. Our innovative application provides users with an easy-to-use platform to estimate the carbon emissions of buildings based on key parameters such as floor size, air conditioning usage, and geographic location. By leveraging advanced algorithms and data analytics, we aim to empower individuals, businesses, and policymakers to make informed decisions that contribute to a more sustainable future. Join us on this journey to reduce carbon footprints and promote eco-friendly practices in building management!")
    # "Take the Questionnaire" button
    if st.button("Start estimating"):
        st.write("Loading the next step")

with col2: 
    st.markdown('<div class="large-image">', unsafe_allow_html=True)
    st.image("https://sg.centanet.com/SingaporeCMS/attachmentDownload.aspx?download/22-173-1596/5869484821_25488d66e0_b.jpg", use_column_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
  


# Section: About us
st.markdown('<a id="about_us"></a>', unsafe_allow_html=True)
st.header("About us")
st.write("We are a dedicated group of data science students passionate about sustainability and environmental impact. With diverse backgrounds in statistics, machine learning, and software development, we came together to create a tool that not only estimates carbon emissions but also raises awareness about energy consumption in buildings. Our mission is to harness the power of data to facilitate better decision-making for building owners, architects, and urban planners. We believe that informed choices lead to sustainable practices, and our app is designed to be a step towards a greener future for all.")

# Section: How it works
st.markdown('<a id="how_it_works"></a>', unsafe_allow_html=True)
st.header("How it works")
st.write("Our Carbon Emission Estimator utilizes a sophisticated algorithm that processes various building parameters to estimate carbon emissions accurately. Users simply input data such as the building's floor size, type of air conditioning system, and location. The app then analyzes this information against a database of emission factors and energy consumption metrics to calculate the estimated carbon footprint. The results are presented in an easily understandable format, allowing users to identify potential areas for improvement and make informed decisions about energy efficiency upgrades. Our user-friendly interface ensures a seamless experience, making it accessible for everyone, regardless of technical expertise.")

# Section: How can it help you
st.markdown('<a id="how_can_it_help_you"></a>', unsafe_allow_html=True)
st.header("How can it help you")
st.write("Understanding the carbon emissions of your building is a vital step toward reducing your environmental impact. Our app can help you by providing insights that lead to actionable changes, such as optimizing air conditioning usage or redesigning spaces for energy efficiency. Whether you're a building owner looking to reduce operational costs, an architect seeking to design sustainable structures, or a policymaker interested in promoting eco-friendly initiatives, our tool offers valuable data to support your goals. By using our app, you can contribute to a sustainable future while also enhancing the comfort and efficiency of your building. Let's work together to create a healthier planet for generations to come!")

# Section: Contact Us
st.markdown('<a id="contact"></a>', unsafe_allow_html=True)
st.header("Contact Us")
st.write("Feel free to reach us at xxxxs@nus.edu.sg")
