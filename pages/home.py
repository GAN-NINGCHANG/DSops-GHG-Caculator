import streamlit as st 

def home():
    # 添加CSS样式
    st.markdown(
        """
        <style>
            body {
                background-image: url('https://kaizenaire.com/wp-content/uploads/2024/06/singapore-botanic-gardens-map.jpg');
                background-size: cover;
                background-position: center;
                background-repeat: no-repeat;
                color: #333;
            }
            .banner {
                background-color: #e4e2dd;
                padding: 5px 0;
                display: flex;
                justify-content: space-around;
                align-items: center;
                min-height: 0px;
                margin: 0;
            }
            .banner a {
                background-color: #e4e2dd;
                text-decoration: none;
                color: #333;
                font-size: 18px;
                font-weight: bold;
                padding: 0 0;
                margin: 0 0;
                line-height: 1;
            }
            .banner a:hover {
                color: #e4e2dd;
            }
            .banner img {
                max-width: 50px;
                height: auto;
                margin: 0;
            }
        </style>
        """,
        unsafe_allow_html=True
    )

    # 页面顶部的横幅导航栏
    banner = st.container()
    with banner: 
        st.markdown('<div class="banner">', unsafe_allow_html=True)
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
    st.markdown(
        """
        <style>
        .large-image img {
            width: 100%;
            max-width: 600px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    col1, col2 = st.columns([1, 1.2])
    with col1: 
        st.markdown("<h1 style='font-size: 50px; text-align: left;'>Building Carbon Emission Calculator</h1>", unsafe_allow_html=True)
        st.write("Welcome to our Building Carbon Emission Estimator! In a world increasingly aware of the impacts of climate change, understanding and reducing carbon emissions is more crucial than ever...")
        if st.button("Start estimating"):
            st.write("Loading the next step")

    with col2: 
        st.markdown('<div class="large-image">', unsafe_allow_html=True)
        st.image("https://sg.centanet.com/SingaporeCMS/attachmentDownload.aspx?download/22-173-1596/5869484821_25488d66e0_b.jpg", use_column_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # Section: About us
    st.markdown('<a id="about_us"></a>', unsafe_allow_html=True)
    st.header("About us")
    st.write("We are a dedicated group of data science students passionate about sustainability and environmental impact...")

    # Section: How it works
    st.markdown('<a id="how_it_works"></a>', unsafe_allow_html=True)
    st.header("How it works")
    st.write("Our Carbon Emission Estimator utilizes a sophisticated algorithm that processes various building parameters to estimate carbon emissions accurately...")

    # Section: How can it help you
    st.markdown('<a id="how_can_it_help_you"></a>', unsafe_allow_html=True)
    st.header("How can it help you")
    st.write("Understanding the carbon emissions of your building is a vital step toward reducing your environmental impact...")

    # Section: Contact Us
    st.markdown('<a id="contact"></a>', unsafe_allow_html=True)
    st.header("Contact Us")
    st.write("Feel free to reach us at xxxxs@nus.edu.sg")
