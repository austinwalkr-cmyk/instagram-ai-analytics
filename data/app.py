import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Page configuration
st.set_page_config(page_title="Instagram Analytics", page_icon="🎾", layout="wide")

st.title("🎾 Halton Tennis Centre — Instagram Visual Dashboard")

@st.cache_data(ttl=60)
def load_data():
    df = pd.read_csv("data/sample_data.csv")
    df["date"] = pd.to_datetime(df["date"])
    return df.sort_values("date")

try:
    df = load_data()
    latest = df.iloc[-1]
    prev = df.iloc[-2] if len(df) >= 2 else latest

    # Top Visual KPI Cards
    kpi1, kpi2, kpi3, kpi4 = st.columns(4)
    kpi1.metric("Total Followers", f"{int(latest['followers']):,}", f"{int(latest['followers'] - prev['followers']):+d}")
    kpi2.metric("Weekly Reach", f"{int(latest['reach']):,}", f"{((latest['reach'] - prev['reach']) / (prev['reach'] or 1))*100:+.1f}%")
    kpi3.metric("Weekly Views", f"{int(latest['views']):,}", f"{((latest['views'] - prev['views']) / (prev['views'] or 1))*100:+.1f}%")
    kpi4.metric("Profile Visits", f"{int(latest['profile_views']):,}", f"{((latest['profile_views'] - prev['profile_views']) / (prev['profile_views'] or 1))*100:+.1f}%")

    st.markdown("---")

    # DEMOGRAPHICS SECTION
    st.header("👥 Audience Demographics")
    
    demo_col1, demo_col2, demo_col3 = st.columns(3)

    # 1. Gender Distribution Donut Chart
    with demo_col1:
        st.subheader("Gender Split")
        female_pct = float(latest.get("gender_female_pct", 61))
        male_pct = 100 - female_pct
        
        fig_gender = go.Figure(data=[go.Pie(
            labels=['Female', 'Male'], 
            values=[female_pct, male_pct], 
            hole=.5,
            marker_colors=['#e91e63', '#2196f3']
        )])
        fig_gender.update_layout(margin=dict(t=0, b=0, l=0, r=0), height=250)
        st.plotly_chart(fig_gender, use_container_width=True)

    # 2. Age Distribution Bar Chart
    with demo_col2:
        st.subheader("Top Age Brackets")
        age_data = pd.DataFrame({
            'Age Group': ['18-24', '25-34', '35-44', '45-54', '55+'],
            'Percentage': [15, 42, 28, 10, 5]
        })
        fig_age = px.bar(
            age_data, x='Percentage', y='Age Group', orientation='h',
            color='Percentage', color_continuous_scale='Blues'
        )
        fig_age.update_layout(margin=dict(t=0, b=0, l=0, r=0), height=250, coloraxis_showscale=False)
        st.plotly_chart(fig_age, use_container_width=True)

    # 3. Top Locations Donut Chart
    with demo_col3:
        st.subheader("Top Locations")
        loc_data = pd.DataFrame({
            'City': ['Aylesbury', 'Halton', 'Wendover', 'Tring', 'Other'],
            'Audience %': [45, 25, 15, 10, 5]
        })
        fig_loc = px.pie(
            loc_data, values='Audience %', names='City', 
            color_discrete_sequence=px.colors.sequential.Tealgrn
        )
        fig_loc.update_layout(margin=dict(t=0, b=0, l=0, r=0), height=250)
        st.plotly_chart(fig_loc, use_container_width=True)

    st.markdown("---")

    # PERFORMANCE TRENDS SECTION
    st.header("📈 Performance Trends")
    
    trend_col1, trend_col2 = st.columns(2)

    with trend_col1:
        st.subheader("Weekly Reach vs. Views")
        fig_performance = px.area(
            df, x="date", y=["reach", "views"], 
            labels={"value": "Count", "date": "Date"},
            color_discrete_sequence=["#008080", "#2E8B57"]
        )
        fig_performance.update_layout(height=300)
        st.plotly_chart(fig_performance, use_container_width=True)

    with trend_col2:
        st.subheader("Follower Growth Trend")
        fig_followers = px.line(
            df, x="date", y="followers", markers=True,
            color_discrete_sequence=["#2E8B57"]
        )
        fig_followers.update_layout(height=300)
        st.plotly_chart(fig_followers, use_container_width=True)

except Exception as e:
    st.error(f"Unable to render dashboard: {e}")
