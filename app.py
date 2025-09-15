import streamlit as st
import pandas as pd
import random

st.title("🎉 Lucky Draw System 🎉")

uploaded_file = st.file_uploader("Upload a CSV file with names", type="csv")

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    if "Name" not in df.columns:
        st.error("CSV must have a column named 'Name'")
    else:
        st.write("✅ Names loaded:", df["Name"].tolist())
        
        if st.button("Pick Winners 🎲"):
            winners = random.sample(df["Name"].dropna().tolist(), 5)
            st.success("🏆 Winners:")
            for i, w in enumerate(winners, 1):
                st.write(f"{i}. {w}")
