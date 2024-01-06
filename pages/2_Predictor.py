import streamlit as st
import pandas as pd
import locale
from PlayerPredictor import DataProcessor, PredictMarketValue

# Set page configuration and title
st.set_page_config(page_title="Predictor Page")

# Display a success message in the sidebar
st.sidebar.success("Select a page above")

# Main title of the app
st.title("Predicting Market Value")

# Load and preprocess the dataset
df = pd.read_csv('fifa_data.csv', usecols=['short_name', 'overall', 'potential', 'value_eur', 'age', 'league_level', 'international_reputation', 'work_rate'])
df = df.head(2000)  # Limiting to the first 2000 rows for quicker processing
processing_data = DataProcessor(df)
processing_data.process_data()
df_processed = processing_data.df

# Create an instance of PredictMarketValue with the processed data
predictor_processed = PredictMarketValue(df_processed)

# Train the model for processed data and display accuracy
score_processed = predictor_processed.train_model()
score_processed_in_percentage = round(score_processed * 100, 2)
st.subheader(f"Processed Data Model Accuracy: {score_processed_in_percentage}%")

# User input section
st.subheader("Predict your own player:")
overall = st.number_input("Please input your player overall (1-100 higher means better value)", min_value=1, max_value=100, step=1)
potential = st.number_input("Please input your player potential (1-100 higher means better value)", min_value=1, max_value=100, step=1)
age = st.number_input("Please input your player age (above 18)", min_value=18, step=1)
league_level = st.number_input("Please input your league level (1-5) *lower is better", min_value=1, max_value=5, step=1)
st.markdown("League level example:  \nLevel 1 = FA Premier League  \nLevel 2 = EFL Championship  \nLevel 3 = EFL League One  \nLevel 4 = EFL League Two  \nLevel 5 = National League")
international_reputation = st.number_input("Please input your player reputation (1-5) *higher is better", min_value=1, max_value=5, step=1)
wr_option = ['Low/Low', 'Low/Medium', 'Low/High', 'Medium/Low', 'Medium/Medium', 'Medium/High', 'High/Low', 'High/Medium', 'High/High']
work_rate = st.selectbox("Please select your player work rate", wr_option)

# Button to trigger value calculation
calculate_button = st.button("Calculate Value")

# Calculation and prediction section
if calculate_button:
    # Mapping work rate to numeric value
    wr_mapping = {'Low/Low': 1, 'Low/Medium': 2, 'Low/High': 3,
                  'Medium/Low': 4, 'Medium/Medium': 5, 'Medium/High': 6,
                  'High/Low': 7, 'High/Medium': 8, 'High/High': 9}
    wr_num = wr_mapping.get(work_rate)

    # Input features for prediction
    input_features = [overall, potential, age, league_level, international_reputation, wr_num]

    # Get the rounded prediction
    rounded_prediction_processed = predictor_processed.predict_value(input_features)

    # Format and display the predicted value in Euros
    locale.setlocale(locale.LC_ALL, 'de_DE')
    value_euro = locale.currency(rounded_prediction_processed, grouping=True)
    st.subheader(f"Predicted Value (EUR) = {value_euro}")

else:
    pass  # Do nothing if the button is not clicked
