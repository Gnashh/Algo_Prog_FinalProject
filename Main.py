from PlayerComparator import PlayerComparator
import streamlit as st
import sys
import pandas as pd


# Set page configuration and title
st.set_page_config(page_title="Comparator Page")

# Display a success message in the sidebar
st.sidebar.success("Select a page above")

# Main title of the app
st.title("Fifa Player Stats Comparator Visualizer")
st.subheader("Choose your player :")

# Create an instance of the PlayerComparator class with the specified file path
compare = PlayerComparator("fifa_data.csv")

# Extract player names from the DataFrame
df_player = compare.extract_player_names()


# Allow the user to select players
player_choice = st.multiselect("", df_player)

# Making the initial state of radar_chart variable
radar_chart = None  

# Check if the number of selected players exceeds the maximum allowed
if len(player_choice) > 3:
    st.warning("Sorry, the maximum number of players to compare is 3 at once.")
    sys.exit()
else:
    # Separate players based on selected positions
    selected_player_data_list, goalkeepers_selected, outfielders_selected, selected_columns = compare.separate_players(player_choice)

    # Check if the selection is valid
    if selected_player_data_list != None:
        # Get the names of selected players
        player_names = [compare.df[compare.df['long_name'] == player]['long_name'].values[0] for player in player_choice]

        # Concatenate player DataFrames into a single DataFrame
        combined_player_data = pd.concat(selected_player_data_list, ignore_index=True).reset_index(drop=True)

        # Display player data
        compare.display_player_data(combined_player_data, goalkeepers_selected, outfielders_selected)

        # Plot radar chart with legend
        radar_chart = compare.plot_radar_chart(selected_player_data_list, selected_columns, player_names)

# Display the radar chart in Streamlit app if it has been generated
if radar_chart != None:
    st.header('Stats Compare :')
    st.pyplot(radar_chart)
