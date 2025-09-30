import streamlit as st
import pandas as pd
import random
import time
from datetime import datetime
from spinner import spin_wheel_image, spin_wheel_image_org

# import streamlit as st
# import streamlit_authenticator as stauth
# import os
# from dotenv import load_dotenv
# from yaml import safe_load

# ----------------- Page Config -----------------
st.set_page_config(
    page_title="Lucky Draw 🎉", 
    page_icon="🎲", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# with open("config.yaml") as f:
#     config = safe_load(f)

# authenticator = stauth.Authenticate(
#     credentials            = config["credentials"],
#     cookie_name            = "my_app",
#     cookie_key             = config["cookie"]["key"],
#     cookie_expiry_days     = 7
# )
# name, auth_status, username = authenticator.login('unrendered')

# try:
#     authenticator.login()
# except Exception as e:
#     st.error(e)

# if auth_status is False:
#     st.error("Incorrect username or password")
# elif auth_status is None:
#     st.warning("Please enter your username and password")
# else:
#     st.sidebar.success(f"Welcome {name}")
#     # Business logic here
#     if st.sidebar.button("Logout"):
#         authenticator.logout("Logout", "sidebar")

# ----------------- Custom CSS -----------------
st.markdown("""
    <style>
        /* Main background with animated gradient */
        .stApp {
            background: linear-gradient(-45deg, #667eea, #764ba2, #f093fb, #f5576c, #4facfe);
            background-size: 400% 400%;
            animation: gradientShift 15s ease infinite;
        }
        
        @keyframes gradientShift {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }

        /* Main title styling */
        .main-title {
            font-size: 72px !important;
            font-weight: 900;
            background: linear-gradient(45deg, #FFD700, #FFA500, #FF6347);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            text-align: center;
            text-shadow: 3px 3px 10px rgba(0,0,0,0.2);
            margin-bottom: 10px;
            animation: pulse 2s ease-in-out infinite;
        }
        
        @keyframes pulse {
            0%, 100% { transform: scale(1); }
            50% { transform: scale(1.05); }
        }

        /* Subtitle */
        .subtitle {
            text-align: center;
            font-size: 24px;
            color: white;
            margin-bottom: 30px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }

        /* Spinning wheel container */
        .wheel-container {
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 400px;
            margin: 30px auto;
            position: relative;
        }

        /* Spinning names display */
        .spinning-names {
            font-size: 48px;
            font-weight: bold;
            color: white;
            text-align: center;
            padding: 40px;
            background: rgba(0, 0, 0, 0.5);
            border-radius: 20px;
            border: 5px solid gold;
            min-width: 500px;
            min-height: 150px;
            display: flex;
            align-items: center;
            justify-content: center;
            position: relative;
            overflow: hidden;
            box-shadow: 0 10px 40px rgba(0,0,0,0.5);
        }

        .spinning-text {
            animation: slideUp 0.1s linear infinite;
        }

        @keyframes slideUp {
            0% { transform: translateY(0); opacity: 1; }
            50% { transform: translateY(-10px); opacity: 0.5; }
            100% { transform: translateY(-20px); opacity: 0; }
        }

        /* Winner display */
        .winner-card {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-radius: 20px;
            padding: 30px;
            margin: 20px auto;
            max-width: 600px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            border: 3px solid gold;
            animation: slideIn 0.5s ease-out;
        }

        @keyframes slideIn {
            from {
                transform: translateY(-50px);
                opacity: 0;
            }
            to {
                transform: translateY(0);
                opacity: 1;
            }
        }

        .winner-number {
            font-size: 24px;
            color: gold;
            text-align: center;
            margin-bottom: 10px;
            font-weight: bold;
        }

        .winner-name {
            font-size: 36px;
            color: white;
            text-align: center;
            font-weight: bold;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }

        /* Status card */
        .status-card {
            background: rgba(255, 255, 255, 0.9);
            border-radius: 15px;
            padding: 20px;
            margin: 20px 0;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        }

        /* Button styling */
        .stButton > button {
            background: linear-gradient(45deg, #f093fb 0%, #f5576c 100%);
            color: white;
            font-size: 20px;
            font-weight: bold;
            padding: 15px 30px;
            border-radius: 50px;
            border: none;
            box-shadow: 0 4px 15px rgba(0,0,0,0.2);
            transition: all 0.3s ease;
        }

        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(0,0,0,0.3);
        }

        /* Sidebar styling */
        .css-1d391kg {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        }

        /* Confetti animation */
        @keyframes confetti-fall {
            0% { transform: translateY(-100vh) rotate(0deg); opacity: 1; }
            100% { transform: translateY(100vh) rotate(720deg); opacity: 0; }
        }

        .confetti {
            position: fixed;
            width: 10px;
            height: 10px;
            background: gold;
            animation: confetti-fall 3s linear infinite;
        }

        /* Progress indicator */
        .progress-ring {
            width: 120px;
            height: 120px;
            margin: 20px auto;
        }

        .progress-ring-circle {
            stroke: gold;
            stroke-width: 4;
            fill: transparent;
            r: 52;
            cx: 60;
            cy: 60;
            stroke-dasharray: 326.73;
            stroke-dashoffset: 326.73;
            animation: progress 20s linear;
        }

        @keyframes progress {
            to {
                stroke-dashoffset: 0;
            }
        }
    </style>
""", unsafe_allow_html=True)

# ----------------- Initialize Session State -----------------
if "names" not in st.session_state:
    st.session_state.names = []
if "winners" not in st.session_state:
    st.session_state.winners = []
if "draw_started" not in st.session_state:
    st.session_state.draw_started = False
if "revealed_count" not in st.session_state:
    st.session_state.revealed_count = 0
if "is_spinning" not in st.session_state:
    st.session_state.is_spinning = False
if "current_spinning_name" not in st.session_state:
    st.session_state.current_spinning_name = ""
if "file_uploaded" not in st.session_state:
    st.session_state.file_uploaded = False
if "spin_complete" not in st.session_state:
    st.session_state.spin_complete = [False, False, False]

# ----------------- Sidebar -----------------
# with st.sidebar:
#     st.markdown("### 🎯 Lucky Draw Setup")
    
#     # Only show file uploader if file not uploaded
#     if not st.session_state.file_uploaded:
#         st.markdown("#### 📂 Upload Participants")
#         uploaded_file = st.file_uploader(
#             "Choose a CSV file with 'Name' column", 
#             type="csv"
#         )
        
#         if uploaded_file:
#             df = pd.read_csv(uploaded_file)
#             if "Name" not in df.columns:
#                 st.error("❌ CSV must have a column named 'Name'")
#             else:
#                 st.session_state.names = df["Name"].dropna().tolist()
#                 st.session_state.file_uploaded = True
#                 st.success(f"✅ {len(st.session_state.names)} participants loaded!")
#                 st.rerun()
#     # else:
    #     st.success(f"✅ File Uploaded Successfully!")
    #     st.info(f"Total Participants: {len(st.session_state.names)}")
        
    #     # Reset button
    #     if st.button("🔄 Upload New File"):
    #         st.session_state.names = []
    #         st.session_state.winners = []
    #         st.session_state.draw_started = False
    #         st.session_state.revealed_count = 0
    #         st.session_state.is_spinning = False
    #         st.session_state.file_uploaded = False
    #         st.session_state.spin_complete = [False, False, False]
    #         st.rerun()
    
    # Show statistics
    # if st.session_state.draw_started:
    #     st.markdown("---")
    #     st.markdown("### 📊 Draw Statistics")
    #     st.metric("Winners Revealed", f"{st.session_state.revealed_count}/7")
    #     # st.metric("Remaining Draws", f"{3 - st.session_state.revealed_count}")

df = pd.read_csv("Employee list.csv")
st.session_state.names = df["Name"].dropna().tolist()

if st.button("🔄 Reset"):
    st.session_state.names = []
    st.session_state.winners = []
    st.session_state.draw_started = False
    st.session_state.revealed_count = 0
    st.session_state.is_spinning = False
    st.session_state.file_uploaded = False
    st.session_state.spin_complete = [False, False, False]
    st.rerun()

# ----------------- Main Content -----------------
# Title
st.markdown('<h1 class="main-title">🎊 LUCKY DRAW 🎊</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Experience the thrill of winning!</p>', unsafe_allow_html=True)

# Main container
col1, col2, col3 = st.columns([1, 3, 1])

with col2:
    # if st.session_state.file_uploaded:
        # Status card
    with st.container():
        # st.markdown('<div class="status-card">', unsafe_allow_html=True)
        cols = st.columns(3)
        with cols[0]:
            st.metric("🎮 Total Participants", len(st.session_state.names))
        with cols[1]:
            st.metric("🏆 Winners Selected", st.session_state.revealed_count)
        with cols[2]:
            st.metric("⏱️ Status", "Active" if st.session_state.draw_started else "Ready")
        # st.markdown('</div>', unsafe_allow_html=True)
    
    # Start Lucky Draw button
    if not st.session_state.draw_started:
        col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
        with col_btn2:
            if st.button("🚀 START LUCKY DRAW", use_container_width=True):
                if len(st.session_state.names) < 7:
                    st.error("⚠️ Need at least 7 participants!")
                else:
                    st.session_state.winners = random.sample(st.session_state.names, 7)
                    st.session_state.draw_started = True
                    st.balloons()
                    st.rerun()
    
    # Draw section
    if st.session_state.draw_started:
        st.markdown("---")
        
        # Spinning wheel area
        spinning_container = st.container()
        
        # Reveal button
        if st.session_state.revealed_count < 7:
            col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
            with col_btn2:
                if not st.session_state.is_spinning:
                    if st.button(f"🎰 SPIN FOR WINNER #{st.session_state.revealed_count + 1}", 
                                use_container_width=True):
                        st.session_state.is_spinning = True
                        st.rerun()
        
        # Spinning animation
        
        if st.session_state.is_spinning:
            winner = st.session_state.winners[st.session_state.revealed_count]

            # ⚠️ Set these so they match your actual wheel graphic:
            #   - N must match the wheel's slices.
            #   - start_angle_deg: where slice 0's CENTER is relative to pointer.
            #     If your wheel's "slice 0" center is at TOP, use 0.
            #     If at RIGHT, use 90; BOTTOM 180; LEFT 270.
            #   - clockwise: True if your slice labels increment clockwise around the wheel.
            spin_wheel_image_org(
                names=st.session_state.names,
                winner=winner,
                duration_sec=2.4,
                wheel_url=r"C:\Users\harsh.gupta\OneDrive - Jkmail\Documents\projects\lucky_draw\streamlit_app\lucky-draw\images.jpg",     # your uploaded/hosted image
                num_slices=len(st.session_state.names),
                start_angle_deg=0.0,       # adjust for your art
                clockwise=True,            # adjust if your art is counter-clockwise
                pointer_at="top",          # move to "right"/"bottom"/"left" if your pointer sits elsewhere
                extra_spins=5,
                size_px=420,
                key=f"wheel_{st.session_state.revealed_count}"
            )

            # reveal and advance
            import time
            time.sleep(2.5)
            st.success(f"🎉 Winner: {winner}")
            st.session_state.is_spinning = False
            st.session_state.spin_complete[st.session_state.revealed_count] = True
            st.session_state.revealed_count += 1
            st.balloons()
            st.rerun()

        
        # Display all revealed winners
        if st.session_state.revealed_count > 0:
            st.markdown("---")
            st.markdown("### 🏆 Winners Board")
            
            for i in range(st.session_state.revealed_count):
                st.markdown(
                    f'<div class="winner-card">'
                    f'<div class="winner-number">🥇 Winner #{i+1}</div>'
                    f'<div class="winner-name">{st.session_state.winners[i]}</div>'
                    f'</div>',
                    unsafe_allow_html=True
                )
            
            if st.session_state.revealed_count == 7:
                st.markdown("---")
                st.success("### 🎊 All winners have been revealed! Congratulations to all! 🎊")
                st.snow()
                
                # Option to restart
                col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
                with col_btn2:
                    if st.button("🔄 New Draw", use_container_width=True):
                        st.session_state.draw_started = False
                        st.session_state.revealed_count = 0
                        st.session_state.winners = []
                        st.session_state.spin_complete = [False, False, False]
                        st.rerun()
# else:
        # Instructions when no file is uploaded
        # st.info("👈 Please upload a CSV file with participant names in the sidebar to get started!")
        
        # Sample format display
        # st.markdown("### 📋 CSV Format Example")
        # sample_df = pd.DataFrame({
        #     "Name": ["John Doe", "Jane Smith", "Bob Johnson", "Alice Brown", "Charlie Wilson"]
        # })
        # st.dataframe(sample_df, use_container_width=True)