import streamlit as st
import base64

def home():
    # 将图片转换为 Base64
    def get_base64_image(file_path):
        with open(file_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode()

    # 获取 Base64 编码的背景图片
    base64_image = get_base64_image("/workspaces/DSops-GHG-Caculator/src/background.jpg")

    # 自定义 CSS 样式设置背景图片和导航栏样式
    page_bg_img = f'''
    <style>
    .stApp {{
        background: linear-gradient(rgba(255,255,255,0.2), rgba(255,255,255,0.2)), url("data:image/jpg;base64,{base64_image}");
        background-size: cover;
        background-repeat: no-repeat;
        background-attachment: fixed;
        background-position: center;
        color: #333;
        font-family: 'Arial', sans-serif;
    }}
    .block-container {{
        background-color: rgba(255, 255, 255, 0.25); /* 更加透明的背景 */
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0px 4px 15px rgba(0, 0, 0, 0.1);
    }}
    .banner {{
        background-color: rgba(255, 255, 255, 0.9); /* 白色背景 */
        padding: 10px 0; /* 增加高度 */
        display: flex;
        justify-content: space-around;
        align-items: center;
        margin: 0;
    }}
    .banner a {{
        text-decoration: none;
        color: #333; /* 黑色文字 */
        font-size: 30px;
        font-weight: bold;
        text-align: center;
    }}
    .banner a:hover {{
        color: #333; /* 鼠标悬停时文字颜色保持不变 */
    }}
    /* 修改后的按钮样式 */
    div.stButton > button {{
        background-color: #4CAF50;
        color: white;
        padding: 15px 32px;
        font-size: 25px;
        margin: 10px 0;
        border: none;
        border-radius: 8px;
        cursor: pointer;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 10px;
        font-weight: bold;
    }}
    div.stButton > button:hover {{
        background-color: #3e8e41; /* 鼠标悬停时变暗 */
        color: white; /* 保持文字颜色不变 */
    }}
    .button-icon {{
        margin-left: 8px;
        transition: transform 0.2s;
    }}
    div.stButton > button:hover .button-icon {{
        transform: translateX(3px);
    }}
    </style>
    '''
    st.markdown(page_bg_img, unsafe_allow_html=True)

    st.markdown(
        '''
        <div class="banner">
            <a href="#introduction">Introduction</a>
            <a href="#about_us">About us</a>
            <a href="#how_it_works">How it works</a>
            <a href="#how_can_it_help_you">Help you</a>
            <a href="#contact">Contact Us</a>
        </div>
        ''', 
        unsafe_allow_html=True
    )

    # 顶部导航栏和图片布局
    banner = st.container()
    with banner: 
        st.markdown('<div class="banner">', unsafe_allow_html=True)
        
        # 使用 st.columns 创建导航链接和图片布局
        _, _, _, _, _, col6, col7 = st.columns(7)
        with col6:
            st.image('src/nus_logo_full-vertical.png', use_column_width=True)
        with col7:
            st.image('src/DSOps_logo.png', use_column_width=True)

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
        st.markdown("<h1 style='font-size: 75px; text-align: left;'>Building Carbon Emission Calculator</h1>", unsafe_allow_html=True)
        st.markdown(
            """
            <p style="font-size:25px;">
                Welcome to our Building Carbon Emission Estimator! In a world increasingly aware of the impacts of climate change, 
                understanding and reducing carbon emissions is more crucial than ever. Our innovative application provides users with 
                an easy-to-use platform to estimate the carbon emissions of buildings based on key parameters such as floor size, 
                air conditioning usage, and geographic location. By leveraging advanced algorithms and data analytics, we aim to empower 
                individuals, businesses, and policymakers to make informed decisions that contribute to a more sustainable future. 
                Join us on this journey to reduce carbon footprints and promote eco-friendly practices in building management!
            </p>
            """,
            unsafe_allow_html=True
        )

        # "Take the Questionnaire" button

        if st.button("Start exploring !"):
            st.session_state.current_page = 1

    with col2: 
        st.markdown('<div class="large-image">', unsafe_allow_html=True)
        st.image("https://sg.centanet.com/SingaporeCMS/attachmentDownload.aspx?download/22-173-1596/5869484821_25488d66e0_b.jpg", use_column_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # Section: About us
    st.markdown('<a id="about_us"></a>', unsafe_allow_html=True)
    st.markdown(
        "<h1 style='font-size:50px;'>About us</h1>", 
        unsafe_allow_html=True
    )
    st.markdown(
        """
        <p style="font-size:25px; color:black">
            We are a dedicated group of data science students passionate about sustainability and environmental impact.
            With diverse backgrounds in statistics, machine learning, and software development, we came together to create a tool
            that not only estimates carbon emissions but also raises awareness about energy consumption in buildings.
            Our mission is to harness the power of data to facilitate better decision-making for building owners, architects, and urban planners.
            We believe that informed choices lead to sustainable practices, and our app is designed to be a step towards a greener future for all.
        </p>
        """,
        unsafe_allow_html=True
    )

    # Section: How it works
    st.markdown('<a id="how_it_works"></a>', unsafe_allow_html=True)
    st.markdown(
        "<h1 style='font-size:50px;'>How it works</h1>", 
        unsafe_allow_html=True
    )
    st.markdown(
        """
        <p style="font-size:25px; color:black">
            Our Carbon Emission Estimator utilizes a sophisticated algorithm that processes various building parameters to estimate carbon emissions accurately.
            Users simply input data such as the building's floor size, type of air conditioning system, and location.
            The app then analyzes this information against a database of emission factors and energy consumption metrics to calculate the estimated carbon footprint.
            The results are presented in an easily understandable format, allowing users to identify potential areas for improvement and make informed decisions about energy efficiency upgrades.
            Our user-friendly interface ensures a seamless experience, making it accessible for everyone, regardless of technical expertise.
        </p>
        """,
        unsafe_allow_html=True
    )

    # Section: How can it help you
    st.markdown('<a id="how_can_it_help_you"></a>', unsafe_allow_html=True)
    st.markdown(
        "<h1 style='font-size:50px;'>How can it help you</h1>", 
        unsafe_allow_html=True
    )
    st.markdown(
        """
        <p style="font-size:25px; color:black">
            Understanding the carbon emissions of your building is a vital step toward reducing your environmental impact.
            Our app can help you by providing insights that lead to actionable changes, such as optimizing air conditioning usage or redesigning spaces for energy efficiency.
            Whether you're a building owner looking to reduce operational costs, an architect seeking to design sustainable structures, or a policymaker interested in promoting eco-friendly initiatives,
            our tool offers valuable data to support your goals. By using our app, you can contribute to a sustainable future while also enhancing the comfort and efficiency of your building.
            Let's work together to create a healthier planet for generations to come!
        </p>
        """,
        unsafe_allow_html=True
    )

    # Section: Contact Us
    st.markdown('<a id="contact"></a>', unsafe_allow_html=True)
    st.markdown(
        "<h1 style='font-size:50px;'>Contact Us</h1>", 
        unsafe_allow_html=True
    )
    st.markdown(
        """
        <p style="font-size:25px; color:black">
            Feel free to reach us at xxxxs@nus.edu.sg
        </p>
        """,
        unsafe_allow_html=True
    )


