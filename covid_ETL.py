import pandas as pd
import sqlalchemy
from dotenv import load_dotenv
import os

data = pd.read_csv('files/covid_19_clean_complete.csv')

def transform(data):
    data = data.dropna()
    data['Date']=pd.to_datetime(data['Date'])
    selected_columns = ['Province/State','Country/Region','Date','Confirmed','Deaths','Recovered','Active']
    data=data[selected_columns]
    data['Active'] = data['Confirmed'] - (data['Deaths'] + data['Recovered'])
    # Rename columns to match the desired names
    data = data.rename(columns={
    'Province/State': 'province_state',
    'Country/Region': 'country',
    'Date': 'date',
    'Confirmed': 'confirmed',
    'Deaths': 'deaths',
    'Recovered': 'recovered',
    'Active': 'active'
})
    # print(len(data))
    data.to_csv('Output-covidData.csv', index = True)
    print('''Successfully Transform Your Data
             Output file generated!
          ''')
# transform(data)

def load():
    data = pd.read_csv('files/Output-covidData.csv')
    load_dotenv()

    # Step 2: Get database credentials securely
    user = os.getenv('DB_USER')
    password = os.getenv('DB_PASSWORD')
    host = os.getenv('DB_HOST')
    db = os.getenv('DB_NAME')

    # Step 3: Create engine
    engine = sqlalchemy.create_engine(f'mysql+pymysql://{user}:{password}@{host}/{db}')

    data.to_sql('covid_stats', engine, if_exists='replace', index=False)
    print('Data Loaded Sucessfully!')

load()
