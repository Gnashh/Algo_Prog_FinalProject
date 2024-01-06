import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st

class PlayerComparator:
    def __init__(self, file_path):
        # Initialize the class with the provided file path
        self.df = self.read_data(file_path)

    def read_data(self, file_path):
        # Read data from the specified CSV file and return a DataFrame
        return pd.read_csv(file_path)

    def extract_player_names(self):
        # Extract and return the 'short_name' column from the DataFrame
        return self.df['long_name']

    def separate_players(self, player_choice):
        # Determine if goalkeepers or outfielders are selected
        goalkeepers_selected = any(self.df.loc[self.df['long_name'] == player, 'club_position'].values[0] == 'GK' for player in player_choice)
        outfielders_selected = any(self.df.loc[self.df['long_name'] == player, 'club_position'].values[0] != 'GK' for player in player_choice)

        if goalkeepers_selected and not outfielders_selected:
            # Define columns for goalkeepers if selected
            selected_columns = ['long_name', 'goalkeeping_diving', 'goalkeeping_handling', 'goalkeeping_kicking', 'goalkeeping_positioning', 'goalkeeping_reflexes', 'goalkeeping_speed']
        elif not goalkeepers_selected and outfielders_selected:
            # Define columns for outfielders if selected
            selected_columns = ['long_name', 'pace', 'shooting', 'passing', 'dribbling', 'defending', 'physic']
        else:
            # Display a warning for mixed selection and return None
            st.warning("Please choose either goalkeepers or outfielders, not both.")
            return None, None, None, None

        # Create a list of player DataFrames based on the selected positions
        player_data_list = [self.df[self.df['long_name'] == player][selected_columns] for player in player_choice]

        return player_data_list, goalkeepers_selected, outfielders_selected, selected_columns

    def display_player_data(self, player_data, goalkeepers_selected, outfielders_selected):
        # Display selected player data with appropriate label
        if goalkeepers_selected:
            st.write("Selected Goalkeepers Data:")
        elif outfielders_selected:
            st.write("Selected Outfielders Data:")

        # Start the index from 1
        player_data.index += 1
        st.write(player_data)

    def plot_radar_chart(self, player_data_list, selected_columns, player_names):
    # Prepare data for radar chart plotting
        num_vars = len(selected_columns) - 1
        angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()

        # Create a radar chart
        fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True))
        
        ax.set_yticklabels(["20", "40", "60", "80", "100"])

        # Plot radar chart for each player and add legend
        for player_data, player_name in zip(player_data_list, player_names):
            # Start the index from 1
            player_data.index += 1

            # Extract numerical values from player_data
            players_stat = player_data[selected_columns[1:]].values.flatten().tolist()
            players_stat += [players_stat[0]]

            player_angles = angles + [angles[0]]

            # Plot radar chart
            ax.plot(player_angles, players_stat, linewidth=2, marker='o', label=player_name)
            ax.fill(player_angles, players_stat, alpha=0.25)

        # Customize the radar chart appearance
        ax.set_xticks(angles)
        ax.set_xticklabels(selected_columns[1:])
        ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1))

        return fig


