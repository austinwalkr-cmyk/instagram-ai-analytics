import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# 1. Page Configuration
st.set_page_config(
    page_title="Halton Tennis Centre — Analytics",
    page_icon="🎾",
    layout="wide"
)

# 2. Halton Brand Styling (Custom CSS)
st.markdown("""
    <style>
    /* Main Background & Accent Styling */
    .stApp {
        background-color: #f8fafc;
    }
    .halton-header {
        background: linear-gradient(135deg, #1a365d 0%, #0d9488 100%);
        padding: 24px;
        border-radius: 12px;
        color: white;
        margin-bottom: 25px;
    }
    .halton-header h1 {
        color: #ffffff !important;
        margin: 0;
        font-weight: 700;
    }
    .halton-header p {
        color: #e2e8f0;
        margin: 5px 0 0 0;
        font-size: 15px;
    }
    div[data-testid="stMetric"] {
        background-color: #ffffff;
        padding: 16px;
        border-radius: 10px;
        border-left: 5px solid #0d9488;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
    </style>
""", unsafe_allow_html=True)

# 3. Custom Header Banner
st.markdown("""
    <div class="halton-header">
        <h1>🎾 Halton Tennis Centre</h1>
        <p>Instagram Performance & Audience Intelligence Dashboard</p>
    </div>
""", unsafe_allow_html=True)

@st.cache_data(ttl=60)
def load_data():
    df = pd.read_csv("data/sample_data.csv")
    df["date"] = pd.to_datetime(df["date"])
    return df.sort_values("date")

try:
    df = load_data()
    latest = df.iloc[-1]
    prev = df.iloc[-2] if len(df) >= 2 else latest

    # Brand Colors
    NAVY = "#1a365d"
    TEAL = "#0d9488"
    GREEN = "#16a34a"
    LIGHT_BG = "#f1f5f9"

    # KPI Summary Row
    kpi1, kpi2, kpi3, kpi4 = st.columns(4)
    kpi1.metric("Total Followers", f"{int(latest['followers']):,}", f"{int(latest['followers'] - prev['followers']):+d}")
    kpi2.metric("Weekly Reach", f"{int(latest['reach']):,}", f"{((latest['reach'] - prev['reach']) / (prev['reach'] or 1))*100:+.1f}%")
    kpi3.metric("Weekly Views", f"{int(latest['views']):,}", f"{((latest['views'] - prev['views']) / (prev['views'] or 1))*100:+.1f}%")
    kpi4.metric("Profile Visits", f"{int(latest['profile_views']):,}", f"{((latest['profile_views'] - prev['profile_views']) / (prev['profile_views'] or 1))*100:+.1f}%")

    st.write("")
    st.write("")

    # AUDIENCE DEMOGRAPHICS
    st.markdown("<h3 style='color: #1a365d;'>👥 Community Demographics</h3>", unsafe_allow_html=True)
    
    demo_col1, demo_col2, demo_col3 = st.columns(3)

    # 1. Gender Split
    with demo_col1:
        st.subheader("Gender Split")
        female_pct = float(latest.get("gender_female_pct", 61))
        male_pct = 100 - female_pct
        
        fig_gender = go.Figure(data=[go.Pie(
            labels=['Female', 'Male'], 
            values=[female_pct, male_pct], 
            hole=.55,
            marker_colors=[TEAL, NAVY]
        )])
        fig_gender.update_layout(margin=dict(t=10, b=10, l=10, r=10), height=240, showlegend=True)
        st.plotly_chart(fig_gender, use_container_width=True)

    # 2. Age Distribution Bar Chart
    with demo_col2:
        st.subheader("Age Breakdown")
        age_data = pd.DataFrame({
            'Age Bracket': ['18-24', '25-34', '35-44', '45-54', '55+'],
            'Audience %': [15, 42, 28, 10, 5]
        })
        fig_age = px.bar(
            age_data, x='Audience %', y='Age Bracket', orientation='h',
            color_discrete_sequence=[TEAL]
        )
        fig_age.update_layout(margin=dict(t=10, b=10, l=10, r=10), height=240)
        st.plotly_chart(fig_age, use_container_width=True)

    # 3. Local Towns Map/Chart
    with demo_col3:
        st.subheader("Local Reach")
        loc_data = pd.DataFrame({
            'Town': ['Aylesbury', 'Halton', 'Wendover', 'Tring', 'Other'],
            'Share %': [45, 25, 15, 10, 5]
        })
        fig_loc = px.pie(
            loc_data, values='Share %', names='Town', 
            color_discrete_sequence=[NAVY, TEAL, GREEN, "#64748b", "#cbd5e1"]
        )
        fig_loc.update_layout(margin=dict(t=10, b=10, l=10, r=10), height=240)
        st.plotly_chart(fig_loc, use_container_width=True)

    st.write("")

    # PERFORMANCE TRENDS SECTION
    st.markdown("<h3 style='color: #1a365d;'>📈 Growth & Engagement Trends</h3>", unsafe_allow_html=True)
    
    trend_col1, trend_col2 = st.columns(2)

    with trend_col1:
        st.subheader("Weekly Reach vs. Views")
        fig_performance = px.line(
            df, x="date", y=["reach", "views"], markers=True,
            labels={"value": "Count", "date": "Date", "variable": "Metric"},
            color_discrete_map={"reach": TEAL, "views": NAVY}
        )
        fig_performance.update_layout(height=300, legend=dict(orientation="h", y=1.1, x=0))
        st.plotly_chart(fig_performance, use_container_width=True)

    with trend_col2:
        st.subheader("Total Follower Growth")
        fig_followers = px.area(
            df, x="date", y="followers",
            color_discrete_sequence=[GREEN]
        )
        fig_followers.update_layout(height=300)
        st.plotly_chart(fig_followers, use_container_width=True)

except Exception as e:
    st.error(f"Unable to load Halton Tennis Centre dashboard: {e}")
