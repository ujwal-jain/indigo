import dotenv
import os
import pandas as pd

from alpha_vantage.timeseries import TimeSeries

# Load the environment variables
dotenv.load_dotenv(dotenv.find_dotenv())

# The default ticker to use for data retrieval
TICKER="SPY"

# The default data directory to save the data
DATA_DIR="data"

# Retrieves the historical time series data for a given ticker using the Alpha
# Vantage API as a PD DataFrame
def alpha_vantage_time_series_historical(ticker) -> tuple:
    ts = TimeSeries(output_format='pandas')
    return ts.get_daily(symbol=ticker, outputsize='full')

# Saves the historical time series data to a CSV file
def save_time_series_historical(data, metadata):
    # Write the pandas dataframe 'data' to a CSV file with name 'ticker_${current_date}.csv' in the 'data/' directory
    dest = os.path.join(DATA_DIR, f'ticker_{TICKER}_{metadata["3. Last Refreshed"]}.csv')
    data.to_csv(dest, index=True)

# Loads the most recent historical time series data from a CSV file for a given
# ticker
def load_time_series_historical(ticker) -> pd.DataFrame:
    # find all files in the 'data/' directory that start with 'ticker_${ticker}' and end with '.csv'
    # From these files, load the most recent one
    candidates = [f for f in os.listdir(DATA_DIR) if f.startswith(f'ticker_{ticker}') and f.endswith('.csv')]
    datafile_ctime = lambda f: os.path.getctime(os.path.join(DATA_DIR, f)) 
    src = os.path.join(DATA_DIR, max(candidates, key=datafile_ctime))

    try:
        # Load the CSV file into a pandas DataFrame
        loaded_data = pd.read_csv(src)
        return loaded_data
    except FileNotFoundError:
        print(f"Error: File not found at {src}. Make sure the file exists in the specified directory.")
    except Exception as e:
        print(f"An error occurred while loading the data: {e}")
    raise Exception("Failed to load data for ticker: {}".format(ticker))

if __name__ == '__main__':
    # save_time_series_historical(*alpha_vantage_time_series_historical(TICKER))
    data = load_time_series_historical(TICKER)
    print(data.describe())
    


