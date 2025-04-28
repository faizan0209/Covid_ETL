import streamlit as st
import pandas as pd
import sqlalchemy
import os
from dotenv import load_dotenv
import plotly.express as px

# Step 1: Load environment variables
load_dotenv()

user = os.getenv('DB_USER')
password = os.getenv('DB_PASSWORD')
host = os.getenv('DB_HOST')
db = os.getenv('DB_NAME')

# Step 2: Connect to Database
engine = sqlalchemy.create_engine(f'mysql+pymysql://{user}:{password}@{host}/{db}')

# Step 3: Read Data
df = pd.read_sql('SELECT * FROM covid_stats', engine)

# Step 4: Streamlit App
st.title('🌍 COVID-19 Global Dashboard')

# Show DataFrame
if st.checkbox('Show Raw Data'):
    st.write(df)

# Line Chart
st.subheader('Confirmed Cases Over Time')
fig1 = px.line(df, x='date', y='confirmed', color='country')
st.plotly_chart(fig1)

# Bar Chart
st.subheader('Top Countries by Deaths')
top10_deaths = df.groupby('country')['deaths'].max().sort_values(ascending=False).head(10).reset_index()
fig2 = px.bar(top10_deaths, x='country', y='deaths')
st.plotly_chart(fig2)

# Pie Chart
st.subheader('Recovered vs Active vs Deaths')
total = df[['recovered', 'active', 'deaths']].sum()
fig3 = px.pie(values=total.values, names=total.index)
st.plotly_chart(fig3)
