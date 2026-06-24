import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

# Page config
st.set_page_config(page_title="Teen Mental Health Dashboard", layout="wide", initial_sidebar_state="expanded")

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv('Teen_Mental_Health_Dataset.csv')
    # Drop empty columns
    df = df.dropna(axis=1, how='all')
    return df

df = load_data()

# Title
st.title("🧠 Teen Mental Health Dashboard")
st.markdown("Analysis of social media impact on teen mental health")

# Sidebar filters
st.sidebar.header("Filters")
age_range = st.sidebar.slider("Age Range", int(df['age'].min()), int(df['age'].max()), 
                               (int(df['age'].min()), int(df['age'].max())))
gender_filter = st.sidebar.multiselect("Gender", df['gender'].unique(), default=df['gender'].unique())
platform_filter = st.sidebar.multiselect("Platform", df['platform_usage'].unique(), default=df['platform_usage'].unique())

# Filter data
filtered_df = df[
    (df['age'] >= age_range[0]) & 
    (df['age'] <= age_range[1]) &
    (df['gender'].isin(gender_filter)) &
    (df['platform_usage'].isin(platform_filter))
]

# Key metrics
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Total Users", len(filtered_df))
with col2:
    st.metric("Avg Stress Level", f"{filtered_df['stress_level'].mean():.1f}/10")
with col3:
    st.metric("Avg Anxiety Level", f"{filtered_df['anxiety_level'].mean():.1f}/10")
with col4:
    st.metric("Avg Sleep Hours", f"{filtered_df['sleep_hours'].mean():.1f}h")

st.divider()

# Row 1: Demographics and Mental Health Overview
col1, col2 = st.columns(2)

with col1:
    st.subheader("Age Distribution")
    fig_age = px.histogram(filtered_df, x='age', nbins=10, title="Age Distribution", 
                           color_discrete_sequence=['#1f77b4'])
    st.plotly_chart(fig_age, use_container_width=True)

with col2:
    st.subheader("Gender Distribution")
    fig_gender = px.pie(filtered_df, names='gender', title="Gender Split",
                        color_discrete_sequence=px.colors.qualitative.Set2)
    st.plotly_chart(fig_gender, use_container_width=True)

st.divider()

# Row 2: Mental Health Metrics
col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("Stress Level Distribution")
    fig_stress = px.box(filtered_df, y='stress_level', color_discrete_sequence=['#ff7f0e'])
    st.plotly_chart(fig_stress, use_container_width=True)

with col2:
    st.subheader("Anxiety Level Distribution")
    fig_anxiety = px.box(filtered_df, y='anxiety_level', color_discrete_sequence=['#d62728'])
    st.plotly_chart(fig_anxiety, use_container_width=True)

with col3:
    st.subheader("Addiction Level Distribution")
    fig_addiction = px.box(filtered_df, y='addiction_level', color_discrete_sequence=['#9467bd'])
    st.plotly_chart(fig_addiction, use_container_width=True)

st.divider()

# Row 3: Social Media & Sleep Analysis
col1, col2 = st.columns(2)

with col1:
    st.subheader("Social Media Hours vs Stress Level")
    fig_media_stress = px.scatter(filtered_df, x='daily_social_media_hours', y='stress_level',
                                  color='anxiety_level', size='addiction_level',
                                  title="Correlation Analysis",
                                  color_continuous_scale='Viridis')
    st.plotly_chart(fig_media_stress, use_container_width=True)

with col2:
    st.subheader("Sleep Hours vs Screen Time Before Sleep")
    fig_sleep = px.scatter(filtered_df, x='screen_time_before_sleep', y='sleep_hours',
                          color='stress_level', size='academic_performance',
                          title="Sleep Impact Analysis",
                          color_continuous_scale='Reds')
    st.plotly_chart(fig_sleep, use_container_width=True)

st.divider()

# Row 4: Platform Analysis
col1, col2 = st.columns(2)

with col1:
    st.subheader("Mental Health by Platform")
    platform_stats = filtered_df.groupby('platform_usage')[['stress_level', 'anxiety_level', 'addiction_level']].mean()
    fig_platform = px.bar(platform_stats, barmode='group', title="Average Mental Health Metrics by Platform",
                         color_discrete_sequence=['#ff7f0e', '#d62728', '#9467bd'])
    st.plotly_chart(fig_platform, use_container_width=True)

with col2:
    st.subheader("Social Interaction vs Mental Health")
    fig_social = px.box(filtered_df, x='social_interaction_level', y='stress_level',
                       color='social_interaction_level', title="Stress Level by Social Interaction",
                       color_discrete_sequence=px.colors.qualitative.Set2)
    st.plotly_chart(fig_social, use_container_width=True)

st.divider()

# Data Explorer
with st.expander("📊 Data Explorer - View Raw Data"):
    st.dataframe(filtered_df, use_container_width=True)
    csv = filtered_df.to_csv(index=False)
    st.download_button("Download Filtered Data", csv, "filtered_data.csv", "text/csv")

# Footer
st.markdown("---")
st.markdown("Dashboard created with Streamlit | Data: Teen Mental Health Dataset")
