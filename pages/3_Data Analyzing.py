from PlayerPredictor import DataProcessor
from PlayerPredictor import CorrelationVisualizer
import pandas as pd
import streamlit as st

# Set page configuration and title
st.set_page_config(page_title="Data Analyzing Page")

# Display a success message in the sidebar
st.sidebar.success("Select a page above")

# Main title of the app
st.title("Market Value Predictor")
st.subheader("How it works :")

st.write("Raw data")
# Read the CSV file into a DataFrame and choosing the columns that gonna be use
df = pd.read_csv('fifa_data.csv', usecols=['short_name','overall', 'potential','value_eur','age','league_level','international_reputation','work_rate',])
st.table(df.head())

# Processing the data and isplay the processed DataFrame
processing_data = DataProcessor(df)
processing_data.process_data()
dfc = processing_data.df
st.subheader('Cleaned the data and changed "work_rate" value into number')
st.table(dfc.head())

#Describing data content
st.subheader('Describe data content')
st.table(dfc.describe())

#Generate heatmap
st.subheader('Generate Heatmap')
selected_columns = ['overall', 'potential', 'age', 'league_level', 'international_reputation', 'work_rate', 'value_eur']
visualizer = CorrelationVisualizer(df, selected_columns)
heatmap = visualizer.generate_heatmap()
st.pyplot(heatmap)

