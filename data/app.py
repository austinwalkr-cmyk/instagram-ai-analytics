import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Instagram Analytics", page_icon="🎾", layout="wide")

st.title("🎾 Halton Tennis Centre — Instagram Dashboard")

@st.cache_data(ttl=60)
def load_data():
    df = pd.read_csv("data/sample_data.csv")
    df["date"] = pd.to_datetime(df["date"])
    return df.sort_values("date")

try:
    df = load_data()
    latest = df.iloc[-1]
    prev = df.iloc[-2] if len(df) >= 2 else latest

    # Top KPI Metrics Cards
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Followers", f"{int(latest['followers']):,}", f"{int(latest['followers'] - prev['followers']):+d}")
    c2.metric("Reach (7d)", f"{int(latest['reach']):,}", f"{((latest['reach'] - prev['reach']) / (prev['reach'] or 1))*100:+.1f}%")
    c3.metric("Views (7d)", f"{int(latest['views']):,}", f"{((latest['views'] - prev['views']) / (prev['views'] or 1))*100:+.1f}%")
    c4.metric("Profile Views (7d)", f"{int(latest['profile_views']):,}", f"{((latest['profile_views'] - prev['profile_views']) / (prev['profile_views'] or 1))*100:+.1f}%")

    st.markdown("---")

    # Trend Charts
    col_left, col_right = st.columns(2)

    with col_left:
        st.subheader("Weekly Reach & Views")
        fig_views = px.line(df, x="date", y=["reach", "views"], markers=True, color_discrete_sequence=["#1f77b4", "#ff7f0e"])
        st.plotly_chart(fig_views, use_container_width=True)

    with col_right:
        st.subheader("Follower Growth")
        fig_followers = px.line(df, x="date", y="followers", markers=True, color_discrete_sequence=["#2ca02c"])
        st.plotly_chart(fig_followers, use_container_width=True)

    st.subheader("Historical Log")
    st.dataframe(df.sort_values("date", ascending=False), use_container_width=True)

except Exception as e:
    st.error(f"Error loading analytics data: {e}")
