import streamlit as st
import pandas as pd
import plotly.express as px

@st.cache_data
def load_data(path="Teen_Mental_Health_Dataset.csv"):
    df = pd.read_csv(path, low_memory=False)
    # drop unnamed or fully empty columns
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
    df = df.dropna(axis=1, how='all')
    # clean column names
    df.columns = [c.strip() for c in df.columns]
    # drop duplicate columns (keep first)
    df = df.loc[:, ~df.columns.duplicated(keep='first')]
    # coerce numeric columns
    num_cols = ['age','daily_social_media_hours','sleep_hours','screen_time_before_sleep',
                'academic_performance','physical_activity','stress_level','anxiety_level','addiction_level']
    for c in num_cols:
        if c in df.columns:
            df[c] = pd.to_numeric(df[c], errors='coerce')
    if 'depression_label' in df.columns:
        try:
            df['depression_label'] = df['depression_label'].astype('category')
        except Exception:
            pass
    return df

# Load
df = load_data()

st.set_page_config(layout='wide')
st.title('Teen Mental Health Dashboard')
st.markdown('Interactive dashboard for Teen_Mental_Health_Dataset.csv')

# Sidebar filters
st.sidebar.header('Filters')
if 'age' in df.columns:
    min_age = int(df['age'].min())
    max_age = int(df['age'].max())
    age_range = st.sidebar.slider('Age range', min_age, max_age, (min_age, max_age))
else:
    age_range = None

if 'gender' in df.columns:
    gender_opts = df['gender'].dropna().unique().tolist()
    genders = st.sidebar.multiselect('Gender', options=gender_opts, default=gender_opts)
else:
    genders = None

if 'platform_usage' in df.columns:
    platform_opts = df['platform_usage'].dropna().unique().tolist()
    platforms = st.sidebar.multiselect('Platform', options=platform_opts, default=platform_opts)
else:
    platforms = None

# apply filters
filtered = df.copy()
if age_range is not None:
    filtered = filtered[(filtered['age'] >= age_range[0]) & (filtered['age'] <= age_range[1])]
if genders is not None and len(genders) > 0:
    filtered = filtered[filtered['gender'].isin(genders)]
if platforms is not None and len(platforms) > 0:
    filtered = filtered[filtered['platform_usage'].isin(platforms)]

# Key metrics
col1, col2, col3 = st.columns(3)
col1.metric('Records', len(filtered))
col2.metric('Avg Stress', f"{filtered['stress_level'].mean():.2f}" if 'stress_level' in filtered.columns and not filtered['stress_level'].isna().all() else 'N/A')
col3.metric('Avg Anxiety', f"{filtered['anxiety_level'].mean():.2f}" if 'anxiety_level' in filtered.columns and not filtered['anxiety_level'].isna().all() else 'N/A')

# Visualizations
st.subheader('Daily Social Media Hours')
if 'daily_social_media_hours' in filtered.columns:
    fig1 = px.histogram(filtered, x='daily_social_media_hours', nbins=30, title='Distribution of Daily Social Media Hours')
    st.plotly_chart(fig1, use_container_width=True)
else:
    st.info('Column `daily_social_media_hours` not found')

st.subheader('Stress vs Social Media Hours')
if 'daily_social_media_hours' in filtered.columns and 'stress_level' in filtered.columns:
    fig2 = px.scatter(filtered, x='daily_social_media_hours', y='stress_level', color='depression_label' if 'depression_label' in filtered.columns else None, trendline='ols', title='Social Media vs Stress')
    st.plotly_chart(fig2, use_container_width=True)

st.subheader('Sleep Hours by Depression Label')
if 'sleep_hours' in filtered.columns and 'depression_label' in filtered.columns:
    fig3 = px.box(filtered, x='depression_label', y='sleep_hours', title='Sleep Hours by Depression Label')
    st.plotly_chart(fig3, use_container_width=True)

st.subheader('Correlation Heatmap (numeric cols)')
numeric = filtered.select_dtypes(include='number')
if not numeric.empty:
    corr = numeric.corr()
    fig4 = px.imshow(corr, text_auto=True, title='Numeric Correlations')
    st.plotly_chart(fig4, use_container_width=True)
else:
    st.info('No numeric columns available for correlation')

st.subheader('Data (sample)')
st.dataframe(filtered.head(200))

st.markdown('---')
st.caption('Built with Streamlit and Plotly')
