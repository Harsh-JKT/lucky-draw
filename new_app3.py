import streamlit as st
import pandas as pd
import random
import time
from datetime import datetime
from spinner import spin_wheel_image, spin_wheel_image_org

# ----------------- Page Config -----------------
st.set_page_config(
    page_title="Lucky Draw 🎉", 
    page_icon="🎲", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# ----------------- Prize Configuration -----------------
PRIZE_BUCKETS = [
    {"name": "Milton 5L Water Bottle", "emoji": "🍶", "count": 7, "color": "#4CAF50"},
    {"name": "Premium Bags", "emoji": "👜", "count": 6, "color": "#FF9800"},
    {"name": "Seiko Clock", "emoji": "🕐", "count": 5, "color": "#2196F3"},
    {"name": "Smart Watch", "emoji": "⌚", "count": 4, "color": "#9C27B0"},
    {"name": "Boat Headphones", "emoji": "🎧", "count": 3, "color": "#607D8B"},
    {"name": "iPhone 17", "emoji": "📱", "count": 2, "color": "#FF5722"},
    {"name": "EV Scooter", "emoji": "🛴", "count": 1, "color": "#795548"},
    {"name": "Car", "emoji": "🚗", "count": 1, "color": "#FFD700"}
]

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

        /* Prize display */
        .current-prize {
            background: linear-gradient(135deg, #FFD700 0%, #FFA500 100%);
            border-radius: 20px;
            padding: 30px;
            margin: 20px auto;
            text-align: center;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            border: 3px solid white;
            animation: prizeGlow 2s ease-in-out infinite alternate;
        }

        @keyframes prizeGlow {
            from { box-shadow: 0 20px 60px rgba(255, 215, 0, 0.5); }
            to { box-shadow: 0 20px 60px rgba(255, 165, 0, 0.8); }
        }

        .current-prize h2 {
            font-size: 48px;
            margin: 0;
            color: #333;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
        }

        .current-prize p {
            font-size: 24px;
            margin: 10px 0 0 0;
            color: #555;
            font-weight: bold;
        }

        /* Winner display */
        .winner-card {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-radius: 20px;
            padding: 20px;
            margin: 10px auto;
            max-width: 600px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.3);
            border: 2px solid gold;
            animation: slideIn 0.5s ease-out;
            display: flex;
            align-items: center;
            justify-content: space-between;
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

        .winner-info {
            flex: 1;
        }

        .winner-prize {
            font-size: 18px;
            color: gold;
            margin-bottom: 5px;
            font-weight: bold;
        }

        .winner-name {
            font-size: 24px;
            color: white;
            font-weight: bold;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }

        .winner-emoji {
            font-size: 36px;
            margin-left: 20px;
        }

        /* Prize bucket display */
        .prize-bucket {
            background: rgba(255, 255, 255, 0.1);
            border-radius: 15px;
            padding: 15px;
            margin: 10px 0;
            border: 2px solid rgba(255, 255, 255, 0.3);
            backdrop-filter: blur(10px);
        }

        .prize-bucket.active {
            border-color: gold;
            background: rgba(255, 215, 0, 0.2);
            box-shadow: 0 0 20px rgba(255, 215, 0, 0.5);
        }

        .prize-bucket.completed {
            opacity: 0.6;
            border-color: #4CAF50;
            background: rgba(76, 175, 80, 0.1);
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

        /* Progress bar for bucket completion */
        .bucket-progress {
            width: 100%;
            height: 8px;
            background: rgba(255, 255, 255, 0.3);
            border-radius: 4px;
            overflow: hidden;
            margin-top: 10px;
        }

        .bucket-progress-fill {
            height: 100%;
            background: linear-gradient(90deg, #4CAF50, #8BC34A);
            transition: width 0.5s ease;
        }
    </style>
""", unsafe_allow_html=True)

# ----------------- Initialize Session State -----------------
if "names" not in st.session_state:
    st.session_state.names = []
if "all_winners" not in st.session_state:
    st.session_state.all_winners = []
if "draw_started" not in st.session_state:
    st.session_state.draw_started = False
if "current_bucket_index" not in st.session_state:
    st.session_state.current_bucket_index = 0
if "current_bucket_winners" not in st.session_state:
    st.session_state.current_bucket_winners = []
if "current_winner_index" not in st.session_state:
    st.session_state.current_winner_index = 0
if "is_spinning" not in st.session_state:
    st.session_state.is_spinning = False
if "available_names" not in st.session_state:
    st.session_state.available_names = []
if "bucket_completed" not in st.session_state:
    st.session_state.bucket_completed = [False] * len(PRIZE_BUCKETS)

# ----------------- Helper Functions -----------------
def get_current_bucket():
    return PRIZE_BUCKETS[st.session_state.current_bucket_index]

def get_total_prizes():
    return sum(bucket["count"] for bucket in PRIZE_BUCKETS)

def get_total_winners():
    return len(st.session_state.all_winners)

def is_draw_complete():
    return st.session_state.current_bucket_index >= len(PRIZE_BUCKETS)

def start_new_bucket():
    if st.session_state.current_bucket_index < len(PRIZE_BUCKETS):
        current_bucket = get_current_bucket()
        available_count = len(st.session_state.available_names)
        required_count = current_bucket["count"]
        
        if available_count >= required_count:
            st.session_state.current_bucket_winners = random.sample(
                st.session_state.available_names, 
                required_count
            )
            st.session_state.current_winner_index = 0
        else:
            st.error(f"Not enough participants left for {current_bucket['name']}! Need {required_count}, have {available_count}")

def advance_to_next_winner():
    current_bucket = get_current_bucket()
    winner = st.session_state.current_bucket_winners[st.session_state.current_winner_index]
    
    # Add to all winners with prize info
    st.session_state.all_winners.append({
        "name": winner,
        "prize": current_bucket["name"],
        "emoji": current_bucket["emoji"],
        "bucket_index": st.session_state.current_bucket_index,
        "winner_number": st.session_state.current_winner_index + 1
    })
    
    # Remove from available names
    st.session_state.available_names.remove(winner)
    st.session_state.current_winner_index += 1
    
    # Check if bucket is complete
    if st.session_state.current_winner_index >= current_bucket["count"]:
        st.session_state.bucket_completed[st.session_state.current_bucket_index] = True
        st.session_state.current_bucket_index += 1
        st.session_state.current_winner_index = 0
        
        # Start next bucket if not complete
        if not is_draw_complete():
            start_new_bucket()

# ----------------- Load Data -----------------
try:
    df = pd.read_csv("Employee list.csv")
    st.session_state.names = df["Name"].dropna().tolist()
except FileNotFoundError:
    st.error("Employee list.csv file not found!")
    st.session_state.names = ["John Doe", "Jane Smith", "Bob Johnson", "Alice Brown", "Charlie Wilson", 
                             "David Lee", "Sarah Connor", "Mike Ross", "Rachel Green", "Ross Geller"]

# Initialize available names
if not st.session_state.available_names:
    st.session_state.available_names = st.session_state.names.copy()

# Reset button
if st.button("🔄 Reset All"):
    st.session_state.all_winners = []
    st.session_state.draw_started = False
    st.session_state.current_bucket_index = 0
    st.session_state.current_bucket_winners = []
    st.session_state.current_winner_index = 0
    st.session_state.is_spinning = False
    st.session_state.available_names = st.session_state.names.copy()
    st.session_state.bucket_completed = [False] * len(PRIZE_BUCKETS)
    st.rerun()

# ----------------- Main Content -----------------
# Title
st.markdown('<h1 class="main-title">🎊 LUCKY DRAW 🎊</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Win Amazing Prizes!</p>', unsafe_allow_html=True)

# Main container
col1, col2, col3 = st.columns([1, 3, 1])

with col2:
    # Status metrics
    with st.container():
        cols = st.columns(4)
        with cols[0]:
            st.metric("🎮 Total Participants", len(st.session_state.names))
        with cols[1]:
            st.metric("🏆 Winners Selected", get_total_winners())
        with cols[2]:
            st.metric("🎁 Total Prizes", get_total_prizes())
        with cols[3]:
            remaining = len(st.session_state.available_names)
            st.metric("👥 Remaining", remaining)
    
    # Prize buckets overview in sidebar
    with st.sidebar:
        st.markdown("### 🎁 Prize Categories")
        for i, bucket in enumerate(PRIZE_BUCKETS):
            bucket_class = "completed" if st.session_state.bucket_completed[i] else ("active" if i == st.session_state.current_bucket_index else "")
            
            winners_in_bucket = len([w for w in st.session_state.all_winners if w["bucket_index"] == i])
            progress_percentage = (winners_in_bucket / bucket["count"]) * 100
            
            st.markdown(f"""
                <div class="prize-bucket {bucket_class}">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <span style="font-size: 18px; font-weight: bold; color: white;">
                            {bucket["emoji"]} {bucket["name"]}
                        </span>
                        <span style="color: gold; font-weight: bold;">
                            {winners_in_bucket}/{bucket["count"]}
                        </span>
                    </div>
                    <div class="bucket-progress">
                        <div class="bucket-progress-fill" style="width: {progress_percentage}%"></div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
    
    # Start Lucky Draw button
    if not st.session_state.draw_started:
        col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
        with col_btn2:
            total_prizes_needed = get_total_prizes()
            if st.button("🚀 START LUCKY DRAW", use_container_width=True):
                if len(st.session_state.names) < total_prizes_needed:
                    st.error(f"⚠️ Need at least {total_prizes_needed} participants!")
                else:
                    st.session_state.draw_started = True
                    start_new_bucket()
                    st.balloons()
                    st.rerun()
    
    # Draw section
    if st.session_state.draw_started and not is_draw_complete():
        current_bucket = get_current_bucket()
        
        # Current prize display
        st.markdown(f"""
            <div class="current-prize">
                <h2>{current_bucket["emoji"]} {current_bucket["name"]}</h2>
                <p>Prize {st.session_state.current_winner_index + 1} of {current_bucket["count"]}</p>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Spin button
        if not st.session_state.is_spinning:
            col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
            with col_btn2:
                winner_num = st.session_state.current_winner_index + 1
                if st.button(f"🎰 SPIN FOR {current_bucket['name']} #{winner_num}", 
                            use_container_width=True):
                    st.session_state.is_spinning = True
                    st.rerun()
        
        # Spinning animation
        if st.session_state.is_spinning:
            winner = st.session_state.current_bucket_winners[st.session_state.current_winner_index]
            
            # Spinning wheel
            try:
                spin_wheel_image_org(
                    names=st.session_state.available_names,
                    winner=winner,
                    duration_sec=2.4,
                    wheel_url=r"C:\Users\harsh.gupta\OneDrive - Jkmail\Documents\projects\lucky_draw\streamlit_app\lucky-draw\images.jpg",
                    num_slices=len(st.session_state.available_names),
                    start_angle_deg=0.0,
                    clockwise=True,
                    pointer_at="top",
                    extra_spins=5,
                    size_px=420,
                    key=f"wheel_{st.session_state.current_bucket_index}_{st.session_state.current_winner_index}"
                )
            except:
                # Fallback if wheel doesn't work
                st.info("🎲 Spinning...")
                
            # Reveal winner and advance
            time.sleep(2.5)
            st.success(f"🎉 {current_bucket['emoji']} Winner: {winner} - {current_bucket['name']}")
            st.session_state.is_spinning = False
            advance_to_next_winner()
            st.balloons()
            st.rerun()
    
    # Show completion message
    if is_draw_complete():
        st.markdown("---")
        st.success("### 🎊 All prizes have been distributed! Congratulations to all winners! 🎊")
        st.snow()
        
        # Restart option
        col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
        with col_btn2:
            if st.button("🔄 New Draw Session", use_container_width=True):
                st.session_state.draw_started = False
                st.session_state.current_bucket_index = 0
                st.session_state.all_winners = []
                st.session_state.current_bucket_winners = []
                st.session_state.current_winner_index = 0
                st.session_state.available_names = st.session_state.names.copy()
                st.session_state.bucket_completed = [False] * len(PRIZE_BUCKETS)
                st.rerun()

# Display all winners
if st.session_state.all_winners:
    st.markdown("---")
    st.markdown("### 🏆 Winners List")
    
    # Group winners by prize bucket
    for bucket_idx, bucket in enumerate(PRIZE_BUCKETS):
        bucket_winners = [w for w in st.session_state.all_winners if w["bucket_index"] == bucket_idx]
        
        if bucket_winners:
            st.markdown(f"#### {bucket['emoji']} {bucket['name']} Winners:")
            
            for winner in bucket_winners:
                st.markdown(f"""
                    <div class="winner-card">
                        <div class="winner-info">
                            <div class="winner-prize">{winner['prize']} #{winner['winner_number']}</div>
                            <div class="winner-name">{winner['name']}</div>
                        </div>
                        <div class="winner-emoji">{winner['emoji']}</div>
                    </div>
                """, unsafe_allow_html=True)