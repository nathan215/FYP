import numpy as np
import pandas as pd
import statsmodels.api as sm
import matplotlib.pyplot as plt
from sqlalchemy import create_engine

def fetch_data_from_database():
    username = 'postgres'
    password = '0000'
    host = 'localhost'
    port = '5433'
    database_name = 'FYP'
    engine = create_engine(f'postgresql+psycopg2://{username}:{password}@{host}:{port}/{database_name}')
    
    query = "SELECT * FROM test_records"
    df = pd.read_sql(query, engine)
    return df

def plot_intervals(df, x, y, xlabel, ylabel, filename):
    plt.figure(figsize=(10, 6))
    
    # Fit regression model
    x_const = sm.add_constant(x)
    model = sm.OLS(y, x_const).fit()
    
    # Predict values and intervals
    predictions = model.get_prediction(x_const)
    frame = predictions.summary_frame(alpha=0.05)
    
    # Plot the regression line and prediction interval
    plt.plot(x, frame['mean'], color='red', label='Regression line')
    plt.fill_between(x, frame['obs_ci_lower'], frame['obs_ci_upper'], color='green', alpha=0.3, label='95% Prediction interval')
    
    # Randomly sample 50 data points and plot them
    random_samples = df.sample(50)
    plt.scatter(random_samples[x.name], random_samples[y.name], color='black', s=20)
    
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(f"{ylabel} vs {xlabel} with Regression Line and Prediction Intervals")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(filename)
    plt.show(block=False)


def main():
    df = fetch_data_from_database()
    
    df['distance'] = np.log10(np.sqrt(df['x']**2 + df['y']**2 + df['z']**2))
    df['horizen_distance'] = np.log10(np.sqrt(df['x']**2 + df['y']**2))
    
    plot_rssi_variance(df)
    plot_intervals(df, df['distance'], df['rssi'], 'Log(Distance)', 'RSSI', 'distance_rssi_plot.png')
    plot_intervals(df, df['horizen_distance'], df['rssi'], 'Log(Horizen Distance)', 'RSSI', 'horizen_distance_rssi_plot.png')
    plot_intervals(df, df['z'], df['rssi'], 'Z', 'RSSI', 'z_rssi_plot.png')

import pandas as pd
import matplotlib.pyplot as plt


def plot_rssi_variance(df):
    """
    Plot the variance of RSSI across distances, considering 100 data points in each group.

    Parameters:
    - df: DataFrame containing the data with columns 'distance' and 'rssi'.
    """

    # Sort dataframe by distance
    df = df.sort_values(by="distance").reset_index(drop=True)

    # Create a new column to indicate the group for each row
    df['group'] = (df.index // 100) + 1

    # Compute the variance of RSSI for each group and mean distance for each group
    rssi_variance = df.groupby('group')['rssi'].var()
    distance_mean = df.groupby('group')['distance'].mean()

    # Plot
    plt.figure(figsize=(10, 6))
    plt.plot(distance_mean, rssi_variance)
    plt.title('Variance of RSSI vs. Distance')
    plt.xlabel('Mean Distance of Group')
    plt.ylabel('Variance of RSSI')
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    main()
