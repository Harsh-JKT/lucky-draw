import streamlit as st
import pandas as pd
import random

# ----------------- Page Config -----------------
st.set_page_config(page_title="Lucky Draw 🎉", page_icon="🎲", layout="centered")

# ----------------- Custom CSS -----------------
st.markdown("""
    <style>
        /* Background color (yellow + black theme) */
        .stApp {
            background-color: #FFD700; /* Yellow */
            background-image: linear-gradient(to bottom right, #FFD700, #000000);
            color: #000000;
            font-family: 'Arial Black', sans-serif;
        }

        /* Title styling */
        .big-title {
            font-size: 48px !important;
            font-weight: 900;
            color: #000000;
            text-align: center;
        }

        /* Subtitle */
        .subtext {
            text-align: center;
            font-size: 20px;
            color: #333333;
            margin-bottom: 20px;
        }

        /* Winner text */
        .winner {
            font-size: 32px !important;
            font-weight: bold;
            color: #e60000; /* Bold Red */
            text-align: center;
            margin: 20px 0;
            background: #fff;
            padding: 10px;
            border-radius: 10px;
            border: 3px solid black;
        }

        /* Footer */
        .footer {
            position: fixed;
            left: 0;
            bottom: 0;
            width: 100%;
            background-color: black;
            color: yellow;
            text-align: center;
            padding: 8px;
            font-size: 14px;
        }
    </style>
""", unsafe_allow_html=True)

# # ----------------- Logo + Title -----------------
# logo_path = "jktyre_logo.svg"  # <-- Change this to your local SVG path
# with open(logo_path, "r") as f:
#     svg_logo = f.read()
# st.markdown(f"<div class='logo'>{svg_logo}</div>", unsafe_allow_html=True)

st.markdown('<p class="big-title">🎉 Lucky Draw 🎉</p>', unsafe_allow_html=True)
st.markdown('<p class="subtext">Upload participant list and reveal winners one by one!</p>', unsafe_allow_html=True)

# ----------------- Session State -----------------
if "names" not in st.session_state:
    st.session_state.names = []
if "winners" not in st.session_state:
    st.session_state.winners = []
if "draw_started" not in st.session_state:
    st.session_state.draw_started = False
if "revealed_count" not in st.session_state:
    st.session_state.revealed_count = 0

# ----------------- File Upload -----------------
uploaded_file = st.file_uploader("📂 Upload a CSV file with a 'Name' column", type="csv")

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    if "Name" not in df.columns:
        st.error("❌ CSV must have a column named 'Name'")
    else:
        st.session_state.names = df["Name"].dropna().tolist()
        st.success(f"✅ {len(st.session_state.names)} names loaded!")

        # Start Lucky Draw
        if st.button("🚀 Start Lucky Draw") and not st.session_state.draw_started:
            if len(st.session_state.names) < 3:
                st.error("⚠️ Need at least 3 participants!")
            else:
                st.session_state.winners = random.sample(st.session_state.names, 3)
                st.session_state.draw_started = True
                st.session_state.revealed_count = 1   # Show first winner immediately
                st.balloons()

        # Reveal winners section
        if st.session_state.draw_started:
            st.markdown("### 🏆 Winners Reveal")

            if st.session_state.revealed_count < len(st.session_state.winners):
                if st.button("🎲 Reveal Next Winner"):
                    st.session_state.revealed_count += 1

            # Display revealed winners
            for i in range(st.session_state.revealed_count):
                st.markdown(f'<p class="winner">🥳 Winner #{i+1}: {st.session_state.winners[i]}</p>', unsafe_allow_html=True)

            if st.session_state.revealed_count == 3:
                st.success("🎊 All 3 winners revealed! Congratulations! 🎊")
                st.snow()

# ----------------- Footer -----------------
# st.markdown('<div class="footer">© JK Tyre & Industries Limited</div>', unsafe_allow_html=True)
