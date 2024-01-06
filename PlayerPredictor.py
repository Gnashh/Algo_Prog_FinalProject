import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

class DataProcessor:
    """
    DataProcessor class for processing FIFA player data.

    Parameters:
    - data (pd.DataFrame): Input DataFrame containing FIFA player data.

    Methods:
    - process_data(): Process the data by mapping 'work_rate' values, dropping NaN rows,
      resetting the index, and normalizing 'value_eur' column.
    """

    def __init__(self, data):
        self.df = data
        self.work_rate_mapping = {
            'Low/Low': 1, 'Low/Medium': 2, 'Low/High': 3,
            'Medium/Low': 4, 'Medium/Medium': 5, 'Medium/High': 6,
            'High/Low': 7, 'High/Medium': 8, 'High/High': 9
        }

    def process_data(self):
        self.__map_work_rate()
        self.__drop_na_rows()
        self.__reset_index()
        self.__normalize_value_eur()

    def __map_work_rate(self):
        self.df['work_rate'] = self.df['work_rate'].map(self.work_rate_mapping)

    def __drop_na_rows(self):
        self.df = self.df.dropna()

    def __reset_index(self):
        self.df.index += 1

    def __normalize_value_eur(self):
        self.df['value_eur'] = self.df['value_eur'] / 100000000


class CorrelationVisualizer:
    """
    Plot a correlation heatmap for selected columns in the given DataFrame.

    Parameters:
    - data (pd.DataFrame): The input DataFrame.
    - selected_columns (list): List of column names for which correlation is to be calculated and visualized.
    """
    
    def __init__(self, data, selected_columns):
        self.df = data[selected_columns]
        self.selected_columns = selected_columns

    def generate_heatmap(self):
        correlation_matrix = self.df.corr()

        plt.figure(figsize=(12, 10))
        sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt=".2f", annot_kws={"size": 10})
        plt.title("Correlation Matrix Heatmap")
        
        return plt.gcf()
    
class PredictMarketValue:
    def __init__(self, df):
        self.df = df
        self.features = ['overall', 'potential', 'age', 'league_level', 'international_reputation', 'work_rate']
        self.target = 'value_eur'
        self.model = LinearRegression()
        
    def train_model(self):
        X = self.df[self.features]
        y = self.df[self.target]
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        self.model.fit(X_train, y_train)
        score = self.model.score(X_test, y_test)
        return score
    
    def predict_value(self, input_features):
        input_data = [input_features]
        prediction = self.model.predict(input_data)
        prediction_value = round(prediction[0] * 100000000)

        return prediction_value