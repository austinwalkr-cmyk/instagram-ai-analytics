import pandas as pd
import streamlit as st

st.set_page_config(page_title="Instagram Analytics", layout="wide")

st.title("📈 Instagram Performance Dashboard")
st.caption("Powered by Custom GitHub Data Pipeline & AI Engine")

# Load data
df = pd.read_csv("data/sample_data.csv")

# Top KPI metrics
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Followers", f"{df['followers'].iloc[-1]:,}", delta=int(df['followers'].iloc[-1] - df['followers'].iloc[0]))
col2.metric("Total Reach", f"{df['reach'].sum():,}")
col3.metric("Profile Views", f"{df['profile_views'].sum():,}")
col4.metric("Avg Engagement Rate", f"{df['engagement_rate'].mean():.2f}%")

st.markdown("---")

# Data Visualization
st.subheader("Reach & Impressions Over Time")
st.line_chart(df.set_index("date")[["reach", "impressions"]])

st.subheader("Raw Data Summary")
st.dataframe(df, use_container_width=True)
