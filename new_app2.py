import streamlit as st
import pandas as pd
import random
import secrets
import time
from datetime import datetime
from spinner import spin_wheel_image, spin_wheel_image_org
from io import BytesIO
from datetime import datetime


sysrand = random.SystemRandom()

# ----------------- Page Config -----------------
st.set_page_config(
    page_title="Lucky Draw 🎉",
    page_icon="🎲",
    layout="wide",
    initial_sidebar_state="collapsed"
)


from pathlib import Path
import mimetypes
import base64

def show_spinner_media(src: str, size_px: int = 380):
    """
    Displays a local GIF/PNG/JPG via st.image, or MP4/WebM via <video>.
    Uses extension/mimetype detection; never routes MP4 to st.image (avoids PIL errors).
    """
    p = Path(src)
    # Guess mimetype by extension
    guess, _ = mimetypes.guess_type(str(p))
    ext = p.suffix.lower()

    # ----- GIF/Static images -----
    if (guess and guess.startswith("image")) or ext in {".gif", ".png", ".jpg", ".jpeg", ".webp"}:
        st.image(str(p), use_container_width=False, width=size_px)
        return

    # ----- Video (mp4/webm/ogg) -----
    if (guess and guess.startswith("video")) or ext in {".mp4", ".webm", ".ogg", ".mov"}:
        # Using HTML5 video for consistent autoplay/loop/mute and round mask
        try:
            video_bytes = Path(src).read_bytes()
            b64 = base64.b64encode(video_bytes).decode("utf-8")
            mime = guess or "video/mp4"
            st.markdown(
                f"""
                <div style="display:flex;align-items:center;justify-content:center;width:100%;">
                  <video autoplay loop muted playsinline
                         style="width:{size_px}px;height:{size_px}px;border-radius:50%;object-fit:cover;box-shadow:0 5px 20px rgba(0,0,0,0.25);">
                    <source src="data:{mime};base64,{b64}" type="{mime}">
                  </video>
                </div>
                """,
                unsafe_allow_html=True,
            )
        except Exception:
            # Fallback to st.video if direct HTML fails for any reason
            st.video(str(p))
        return

    # ----- Unknown: show a neutral placeholder -----
    st.info("🎲 Spinning...")




# ----------------- Prize Configuration -----------------
PRIZE_BUCKETS = [
    {"name": "Milton 5L Water Bottle", "emoji": "🍶", "count": 7, "color": "#4CAF50", "image": "https://m.media-amazon.com/images/I/41VY8NO+xwL._SX300_SY300_QL70_FMwebp_.jpg"},
    {"name": "Premium Bags", "emoji": "👜", "count": 6, "color": "#FF9800", "image": "https://m.media-amazon.com/images/I/81WvA8DFu8L._SY741_.jpg"},
    {"name": "Seiko Clock", "emoji": "🕐", "count": 5, "color": "#2196F3", "image": "https://m.media-amazon.com/images/I/71dykbW7+UL._SX679_.jpg"},
    {"name": "Smart Watch", "emoji": "⌚", "count": 4, "color": "#9C27B0", "image": "https://m.media-amazon.com/images/I/61ZjlBOp+rL._SX679_.jpg"},
    {"name": "Boat Headphones", "emoji": "🎧", "count": 3, "color": "#607D8B", "image": "https://m.media-amazon.com/images/I/61fy+-qXFPL._SX679_.jpg"},
    {"name": "iPhone 17", "emoji": "📱", "count": 2, "color": "#FF5722", "image": "https://m.media-amazon.com/images/I/71657TiFeHL._SX679_.jpg"},
    {"name": "EV Scooter", "emoji": "🛴", "count": 1, "color": "#795548", "image": "https://m.media-amazon.com/images/I/61rgWe4qbXL._SX679_.jpg"},
    {"name": "Car", "emoji": "🚗", "count": 1, "color": "#FFD700", "image": "https://imgd.aeplcdn.com/664x374/n/cw/ec/139651/curvv-exterior-right-front-three-quarter.jpeg?isig=0&q=80"}
]

# ----------------- Custom CSS (kept colors; narrowed button) -----------------
st.markdown("""
    <style>
        /* Main background with animated gradient (same colors) */
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

        /* Title */
        .main-title {
            font-size: 56px !important;
            font-weight: 900;
            background: linear-gradient(45deg, #FFD700, #FFA500, #FF6347);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            text-align: center;
            text-shadow: 3px 3px 10px rgba(0,0,0,0.2);
            margin-bottom: 10px;
            animation: pulse 2s ease-in-out infinite;
        }
        @keyframes pulse { 0%,100%{transform:scale(1);} 50%{transform:scale(1.05);} }

        /* Stats bar (kept look) */
        .stats-mini {
            background: rgba(0, 0, 0, 0.4);
            border-radius: 10px;
            padding: 10px 20px;
            color: white;
            display: flex;
            justify-content: space-around;
            margin: 10px 0;
        }
        .stat-item-mini { text-align: center; }
        .stat-label-mini { font-size: 12px; color: #ccc; }
        .stat-value-mini { font-size: 20px; color: #FFD700; font-weight: bold; }

        /* Wheel + container */
        .wheel-area {
            background: rgba(0, 0, 0, 0.3);
            border-radius: 15px;
            padding: 20px;
            min-height: 420px;
            display: flex;
            align-items: center;
            justify-content: center;
            border: 2px solid rgba(255, 255, 255, 0.2);
        }
        .wheel-placeholder {
            text-align: center; color: white; font-size: 48px;
        }

        /* Winners right panel (vertical cards) */
        .winners-section-right {
            background: rgba(0, 0, 0, 0.3);
            border-radius: 15px;
            padding: 20px;
            border: 2px solid rgba(255, 255, 255, 0.2);
        }
        .section-title { color: white; font-size: 22px; font-weight: bold; margin-bottom: 15px; text-align: center; text-shadow: 2px 2px 4px rgba(0,0,0,0.3); }
        .winner-card-v {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-radius: 12px;
            padding: 14px;
            margin-bottom: 10px;
            border: 3px solid gold;
            color: white;
        }
        .winner-card-v.placeholder {
            background: rgba(255,255,255,0.1);
            border: 3px dashed rgba(255,255,255,0.3);
            color: rgba(255,255,255,0.6);
        }
        .winner-position { font-size: 14px; color: gold; font-weight: bold; }
        .winner-name { font-size: 16px; font-weight: bold; }

        /* Left sidebar categories (kept your style) */
        .sidebar-mini {
            background: rgba(0, 0, 0, 0.3);
            border-radius: 10px;
            padding: 15px;
            margin-top: 10px;
            max-height: 520px;
            overflow-y: auto;
        }
        .prize-mini-item {
            background: rgba(255, 255, 255, 0.1);
            border-radius: 8px;
            padding: 10px;
            margin: 8px 0;
            border: 2px solid rgba(255, 255, 255, 0.2);
            font-size: 13px;
            color: white;
        }
        .prize-mini-item.active { border-color: gold; background: rgba(255, 215, 0, 0.2); box-shadow: 0 0 15px rgba(255, 215, 0, 0.4); }
        .prize-mini-item.completed { opacity: 0.5; border-color: #4CAF50; }
        .mini-progress { width: 100%; height: 4px; background: rgba(255, 255, 255, 0.2); border-radius: 2px; overflow: hidden; margin-top: 5px; }
        .mini-progress-fill { height: 100%; background: linear-gradient(90deg, #4CAF50, #8BC34A); transition: width 0.5s ease; }

        /* Buttons: narrower (not 100% width) */
        .stButton > button {
            background: linear-gradient(45deg, #f093fb 0%, #f5576c 100%);
            color: white;
            font-size: 18px;
            font-weight: 700;
            padding: 12px 26px;
            border-radius: 30px;
            border: none;
            box-shadow: 0 5px 20px rgba(0,0,0,0.3);
            transition: all 0.3s ease;
            width: auto;          /* <— NOT full width */
        }
        .stButton > button:hover { transform: translateY(-3px); box-shadow: 0 8px 25px rgba(0,0,0,0.4); }

        /* Small helper to center the spin button under wheel */
        .center-btn { display: flex; justify-content: center; margin-top: 12px; }
        
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
            # sysrand.sample(participants, k)
            st.session_state.current_bucket_winners = sysrand.sample(
                st.session_state.available_names, required_count
            )
            
            # st.session_state.current_bucket_winners = secrets.choice(
            #     st.session_state.available_names
            # )
            
            st.session_state.current_winner_index = 0
        else:
            st.error(f"Not enough participants left for {current_bucket['name']}! Need {required_count}, have {available_count}")

def advance_to_next_winner():
    current_bucket = get_current_bucket()
    winner = st.session_state.current_bucket_winners[st.session_state.current_winner_index]
    st.session_state.all_winners.append({
        "name": winner,
        "prize": current_bucket["name"],
        "emoji": current_bucket["emoji"],
        "bucket_index": st.session_state.current_bucket_index,
        "winner_number": st.session_state.current_winner_index + 1
    })
    st.session_state.available_names.remove(winner)
    st.session_state.current_winner_index += 1
    if st.session_state.current_winner_index >= current_bucket["count"]:
        st.session_state.bucket_completed[st.session_state.current_bucket_index] = True
        st.session_state.current_bucket_index += 1
        st.session_state.current_winner_index = 0
        if not is_draw_complete():
            start_new_bucket()

# ----------------- Load Data -----------------
try:
    df = pd.read_csv("Employee list.csv")
    st.session_state.names = df["Name"].dropna().tolist()
except FileNotFoundError:
    st.error("Employee list.csv file not found! Using demo names.")
    st.session_state.names = [
        "John Doe","Jane Smith","Bob Johnson","Alice Brown","Charlie Wilson",
        "David Lee","Sarah Connor","Mike Ross","Rachel Green","Ross Geller",
        "Monica Geller","Chandler Bing","Phoebe Buffay","Joey Tribbiani",
        "Harsh Gupta","Lakshita Jain","Sanyam Mehta"
    ]

if not st.session_state.available_names:
    st.session_state.available_names = st.session_state.names.copy()

# ----------------- Title & Stats -----------------
st.markdown('<h1 class="main-title">🎊 DIWALI LUCKY DRAW 🎊</h1>', unsafe_allow_html=True)
st.markdown(f"""
    <div class="stats-mini">
        <div class="stat-item-mini">
            <div class="stat-label-mini">Participants</div>
            <div class="stat-value-mini">{len(st.session_state.names)}</div>
        </div>
        <div class="stat-item-mini">
            <div class="stat-label-mini">Winners</div>
            <div class="stat-value-mini">{get_total_winners()}/{get_total_prizes()}</div>
        </div>
        <div class="stat-item-mini">
            <div class="stat-label-mini">Remaining</div>
            <div class="stat-value-mini">{len(st.session_state.available_names)}</div>
        </div>
        <div class="stat-item-mini">
            <div class="stat-label-mini">Current</div>
            <div class="stat-value-mini">{"Done!" if is_draw_complete() else f"{st.session_state.current_winner_index + 1}/{get_current_bucket()['count']}"}</div>
        </div>
    </div>
""", unsafe_allow_html=True)

# ----------------- Main 3-column layout -----------------
col_left, col_center, col_right = st.columns([1, 2, 1])

# LEFT: Prize categories list (same style, progress on left)
with col_left:
    st.markdown('<div style="color: white; font-size: 18px; font-weight: bold; margin-bottom: 10px;">🎁 Prize Categories</div>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-mini">', unsafe_allow_html=True)
    for i, bucket in enumerate(PRIZE_BUCKETS):
        bucket_class = "completed" if st.session_state.bucket_completed[i] else ("active" if i == st.session_state.current_bucket_index else "")
        winners_in_bucket = len([w for w in st.session_state.all_winners if w["bucket_index"] == i])
        progress_percentage = (winners_in_bucket / bucket["count"]) * 100 if bucket["count"] else 0
        st.markdown(f"""
            <div class="prize-mini-item {bucket_class}">
                <div style="display: flex; justify-content: space-between; margin-bottom: 5px;">
                    <span>{bucket["emoji"]} {bucket["name"][:20]}...</span>
                    <span style="color: gold; font-weight: bold;">{winners_in_bucket}/{bucket["count"]}</span>
                </div>
                <div class="mini-progress">
                    <div class="mini-progress-fill" style="width: {progress_percentage}%"></div>
                </div>
            </div>
        """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # if st.button("🔄 Reset All"):
    #     st.session_state.all_winners = []
    #     st.session_state.draw_started = False
    #     st.session_state.current_bucket_index = 0
    #     st.session_state.current_bucket_winners = []
    #     st.session_state.current_winner_index = 0
    #     st.session_state.is_spinning = False
    #     st.session_state.available_names = st.session_state.names.copy()
    #     st.session_state.bucket_completed = [False] * len(PRIZE_BUCKETS)
    #     st.rerun()

# CENTER: Wheel + Spin button just below it
with col_center:
    if st.session_state.draw_started and not is_draw_complete():
        current_bucket = get_current_bucket()

        # st.markdown('<div class="wheel-area">', unsafe_allow_html=True)
        if st.session_state.is_spinning:
            # Winner preselected for this slot
            winner = st.session_state.current_bucket_winners[st.session_state.current_winner_index]
            # try:
                # ---- Fixed spin duration: 5 seconds ----
            SPINNER_SRC = "tyre_gif.mp4"  # or a .gif if you have one

            # st.markdown('<div class="wheel-area">', unsafe_allow_html=True)
            # Show the spinner media in the circle
            show_spinner_media(SPINNER_SRC, size_px=380)
            # st.markdown('</div>', unsafe_allow_html=True)

            # Keep the reveal perfectly synced to 5 seconds
            time.sleep(5.0)
            st.success(f"🎉 Winner: {winner}")
            st.session_state.is_spinning = False
            advance_to_next_winner()
            st.balloons()
            st.rerun()

        else:
            # Placeholder before spin
            st.markdown(f"""
                <div class="wheel-placeholder">
                    🎯<br>
                    <div style="font-size: 20px; margin-top: 20px; line-height: 1.5;">
                        Ready to spin for<br>
                        <strong>{current_bucket["name"]}</strong>
                    </div>
                </div>
            """, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        # Spin button (centered, not wide)
        st.markdown('<div class="center-btn">', unsafe_allow_html=True)
        winner_num = st.session_state.current_winner_index + 1
        if st.button(f"🎰 Spin #{winner_num}"):
            st.session_state.is_spinning = True
            st.rerun()
        # st.markdown('</div>', unsafe_allow_html=True)

    elif not st.session_state.draw_started:
        col_center_inner = st.columns([1, 2, 1])[1]
        with col_center_inner:
            st.markdown(f"""
                <div style="text-align: center; background: rgba(255,255,255,0.1); padding: 60px; border-radius: 20px; margin: 40px 0;">
                    <h2 style="color: white; font-size: 36px; margin-bottom: 20px;">🎮 Ready to Start?</h2>
                    <p style="color: white; font-size: 20px;">
                        {len(st.session_state.names)} participants ready<br>
                        {get_total_prizes()} amazing prizes to win!
                    </p>
                </div>
            """, unsafe_allow_html=True)

            total_prizes_needed = get_total_prizes()
            if len(st.session_state.names) < total_prizes_needed:
                st.error(f"⚠️ Need at least {total_prizes_needed} participants!")
            else:
                if st.button("🚀 START LUCKY DRAW"):
                    st.session_state.draw_started = True
                    start_new_bucket()
                    st.balloons()
                    st.rerun()
    else:
        st.markdown("""
            <div style="text-align: center; background: rgba(255,255,255,0.1); padding: 40px; border-radius: 20px; margin: 40px 0;">
                <h2 style="color: white; font-size: 36px; margin-bottom: 20px;">🎊 All Prizes Distributed! 🎊</h2>
                <p style="color: white; font-size: 20px;">Congratulations to all our winners!</p>
            </div>
        """, unsafe_allow_html=True)
        # if st.button("🔄 New Draw Session"):
        #     st.session_state.draw_started = False
        #     st.session_state.current_bucket_index = 0
        #     st.session_state.all_winners = []
        #     st.session_state.current_bucket_winners = []
        #     st.session_state.current_winner_index = 0
        #     st.session_state.available_names = st.session_state.names.copy()
        #     st.session_state.bucket_completed = [False] * len(PRIZE_BUCKETS)
        #     st.rerun()
        st.snow()

# RIGHT: Current prize winners (vertical list)
with col_right:
    if st.session_state.draw_started and not is_draw_complete():
        current_bucket = get_current_bucket()
        st.markdown(f"""
            <div class="winners-section-right">
                <div class="section-title">🏆 {current_bucket["emoji"]} {current_bucket["name"]} Winners</div>
        """, unsafe_allow_html=True)

        # Winners filled so far in the CURRENT bucket
        current_idx = st.session_state.current_bucket_index
        current_bucket_winner_list = [w for w in st.session_state.all_winners if w["bucket_index"] == current_idx]

        for winner in current_bucket_winner_list:
            st.markdown(f"""
                <div class="winner-card-v">
                    <div class="winner-position">Winner #{winner['winner_number']}</div>
                    <div class="winner-name">{winner['name']}</div>
                </div>
            """, unsafe_allow_html=True)

        # Placeholders for remaining
        remaining_spots = current_bucket["count"] - len(current_bucket_winner_list)
        for i in range(remaining_spots):
            st.markdown(f"""
                <div class="winner-card-v placeholder">
                    <div class="winner-position">Winner #{len(current_bucket_winner_list) + i + 1}</div>
                    <div class="winner-name">To Be Revealed</div>
                </div>
            """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

# ----------------- Completed buckets list (previous categories) -----------------
if st.session_state.all_winners and st.session_state.draw_started:
    for bucket_idx, bucket in enumerate(PRIZE_BUCKETS):
        if st.session_state.bucket_completed[bucket_idx]:
            bucket_winners = [w for w in st.session_state.all_winners if w["bucket_index"] == bucket_idx]
            if bucket_winners:
                st.markdown(f"""
                    <div class="winners-section-right" style="margin-top: 16px;">
                        <div class="section-title">✅ {bucket['emoji']} {bucket['name']} - Complete</div>
                """, unsafe_allow_html=True)
                for winner in bucket_winners:
                    st.markdown(f"""
                        <div class="winner-card-v">
                            <div class="winner-position">Winner #{winner["winner_number"]}</div>
                            <div class="winner-name">{winner["name"]}</div>
                        </div>
                    """, unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)

def get_winners_dataframe() -> pd.DataFrame:
    """Return a tidy table of all winners (shown only when draw completes)."""
    rows = []
    for w in st.session_state.all_winners:
        rows.append({
            "Category": w["prize"],
            "Winner #": w["winner_number"],
            "Name": w["name"],
            "Emoji": w["emoji"],
        })
    df = pd.DataFrame(rows)
    if not df.empty:
        df = df.sort_values(["Category", "Winner #"], kind="stable").reset_index(drop=True)
    return df


# ---------- SHOW ALL WINNERS & EXPORTS ONLY WHEN DRAW IS COMPLETE ----------
if is_draw_complete() and st.session_state.all_winners:
    df_winners = get_winners_dataframe()

    st.markdown("<br/>", unsafe_allow_html=True)
    st.markdown("""
    <div style="
      background: rgba(0,0,0,0.35);
      border: 1px solid rgba(255,255,255,0.2);
      border-radius: 12px; padding: 16px; margin-top: 8px;">
      <h3 style="margin:0 0 10px 0; color:white; text-align:center;">
        🗂️ All Winners Summary & Export
      </h3>
    </div>
    """, unsafe_allow_html=True)

    # Pretty table of final winners
    st.dataframe(
        df_winners,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Category": st.column_config.TextColumn("Category"),
            "Name": st.column_config.TextColumn("Winner Name"),
            "Emoji": st.column_config.TextColumn(""),
        }
    )

    # Build CSV & Excel bytes
    csv_bytes = df_winners.to_csv(index=False).encode("utf-8-sig")


    # Timestamped filenames
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    csv_name  = f"winners_{ts}.csv"

    # Download buttons centered
    c1, c2, _ = st.columns([1,1,2])
    with c1:
        st.download_button(
            "⬇️ Download CSV",
            data=csv_bytes,
            file_name=csv_name,
            mime="text/csv",
            type="primary",
        )


