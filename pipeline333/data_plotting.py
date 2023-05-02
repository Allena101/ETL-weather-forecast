import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
from datetime import datetime
from datetime import datetime, timedelta
from pathlib import Path
import log

log = log.get_logger(__name__)


# CURR_DIR_PATH = Path(__file__).resolve().parent
current_date = datetime.now().strftime("%Y-%m-%d")

# the measurment units for each feature. Used for labeling the y-axis
measurement_units = {
    "temperature": "°C",
    "wind_speed": "m/s",
    "precipitation": "mm/h",
    "air_pressure": "hPa"
}

# most of the plots are not that good since there is so much missing data for most days. -9 for missing values shows up in the plot, but if you know about it then you can interpret it
# Would probably have been a better idea of just plotting the first day or 24 ours after the current hour
def plot_weather_data():
    
    log.info("Starting plot_weather_data func")
    
    CURR_DIR_PATH = Path(__file__).resolve().parent

    # Get current date and format it
    current_date = datetime.now()
    future_date = current_date + timedelta(days=5)
    current_date = current_date.strftime("%Y-%m-%d")
    future_date = future_date.strftime("%Y-%m-%d")

    # Read in the data
    df = pd.read_csv(CURR_DIR_PATH / "combined_cities" / (current_date + "_concat.csv"))

    # since i saved validTime as 'mm-dd hh:mm' i have to do some extra formatting
    # i should have just save the full dateTime object instead 
    df.set_index('validTime', inplace=True)
    df.index = pd.to_datetime(df.index, format='%m-%d %H:%M')
    df = df.sort_index()
    df = df.loc[f'1900-{current_date[5:]}':f'1900-{future_date[5:]}']

# i do several loops since i the plots got messed up when i nested...
# Loop over the unique cities in the DataFrame
    log.info("plotting single features")
    for city_name in df['city'].unique():
        # Filter the DataFrame to just the city you want to plot
        df_city = df[df['city'] == city_name]

        # Group the data by day and calculate the mean temperature for each day
        daily_mean = df_city.groupby(df_city.index.date)['temperature'].mean()

        # Set the figure size
        plt.figure(figsize=(12,6))

        # Set the xticks labels
        unique_dates = pd.unique(df_city.index.date)
        date_str = [d.strftime('%m-%d') for d in unique_dates]

        # Create the line plot
        sns.lineplot(data=df_city, x='validTime', y='temperature', color='lightcoral', linewidth=2.5)

        # Create the bar chart for the average value per day
        plt.bar(daily_mean.index, daily_mean.values, alpha=0.5)

        # Set the xticks positions and labels
        plt.xticks(unique_dates, date_str, rotation=45)

        # Set the labels and title
        plt.xlabel('Date')
        plt.ylabel('Temperature (°C)')
        plt.title(f'Temperature in {city_name}')

        # save plots
        plt.savefig(CURR_DIR_PATH / "plots" / "single_features" / f"{current_date}_{city_name}_temperature" )

    for city_name in df['city'].unique():
        df_city = df[df['city'] == city_name]

        daily_mean = df_city.groupby(df_city.index.date)['wind_speed'].mean()

        plt.figure(figsize=(12,6))

        unique_dates = pd.unique(df_city.index.date)
        date_str = [d.strftime('%m-%d') for d in unique_dates]

        sns.lineplot(data=df_city, x='validTime', y='wind_speed', color='green', linewidth=2.5)

        plt.bar(daily_mean.index, daily_mean.values, alpha=0.5)

        plt.xticks(unique_dates, date_str, rotation=45)

        plt.xlabel('Date')
        plt.ylabel(f'wind_speed {measurement_units["wind_speed"]}')
        plt.title(f'wind_speed in {city_name}')

        plt.savefig(CURR_DIR_PATH / "plots" / "single_features" / f"{current_date}_{city_name}_wind_speed" )

    for city_name in df['city'].unique():
        
        df_city = df[df['city'] == city_name]

        daily_mean = df_city.groupby(df_city.index.date)['precipitation'].mean()

        plt.figure(figsize=(12,6))

        unique_dates = pd.unique(df_city.index.date)
        date_str = [d.strftime('%m-%d') for d in unique_dates]

        sns.lineplot(data=df_city, x='validTime', y='precipitation', color='blue', linewidth=2.5)

        plt.bar(daily_mean.index, daily_mean.values, alpha=0.5)

        plt.xticks(unique_dates, date_str, rotation=45)

        plt.xlabel('Date')
        plt.ylabel(f'precipitation ({measurement_units["precipitation"]})')
        plt.title(f'precipitation in {city_name}')

        plt.savefig(CURR_DIR_PATH / "plots" / "single_features" / f"{current_date}_{city_name}_precipitation")
    log.info("Finished plotting single features")
    
    
    # I am skipping air pressure since it only has data for one day
    features = ['temperature', 'wind_speed', 'precipitation']
    log.info("plotting feature comparisons")
    for feature in features:
        # Group by city so we can compare
        grouped = df.groupby('city')

        # Create a figure and axis
        fig, ax = plt.subplots()

        # Loop over each city and plot its features
        for city, data in grouped:
            data.plot(y=feature, ax=ax, label=city)
            
        # Set the title and axis labels
        ax.set_title(f'{feature} by city')
        ax.set_xlabel('Time')
        ax.set_ylabel(f"{feature} {measurement_units[feature]}")
        
        # to remove the 1900 on the xticks due to bad formatting 
        date_format = '%m-%d'
        ax.xaxis.set_major_formatter(mdates.DateFormatter(date_format))

        # Add a legend
        ax.legend()
        
        plt.savefig(CURR_DIR_PATH / "plots" / "feature_comparisons" / f"{current_date}_{feature}")
        plt.close(fig)
    log.info("Finished plotting feature comparisons")       
        
# plot_weather_data()

