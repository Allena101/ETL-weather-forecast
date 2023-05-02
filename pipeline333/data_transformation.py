import pandas as pd
import json
from datetime import datetime
from pathlib import Path
import glob
import log

log = log.get_logger(__name__)


CURR_DIR_PATH = Path(__file__).resolve().parent
current_date = datetime.now().strftime("%Y-%m-%d")
file_pattern = CURR_DIR_PATH / "raw" / f"{current_date}_*_forecast.json"

# test so that current date works as a function parameter and that teh scope is correct
def extract_features():
    log.info("Starting extract_features func")
    df_combined = pd.DataFrame()
    # for file_path in glob.glob(file_pattern):
    for file_path in glob.glob(str(file_pattern)):

        # file_name = os.path.basename(file_path)
        file_name = Path(file_path).name

        # save city name
        city = file_name.split("_")[1]
        # loop through each city json
        with open(file_path, 'r') as f:
            data = json.load(f)

        # Create a DataFrame from the json file
        df = pd.json_normalize(data['timeSeries'])


        # Extract weather features from prognosis
        df['temperature'] = df['parameters'].apply(lambda x: x[10]['values'][0])
        df['wind_speed'] = df['parameters'].apply(lambda x: x[12]['values'][0])
        df['precipitation'] = df['parameters'].apply(lambda x: x[14]['values'][0])
        df['air_pressure'] = df['parameters'].apply(lambda x: x[11]['values'][0])
        
        # dropping the 'parameters' column after feature extraction
        # parameters = df.pop('parameters')
        df = df.drop('parameters', axis=1)
        
        # Change validTime to dateTime so we can convert to mm-dd-hhmm
        df['validTime'] = pd.to_datetime(df['validTime'])
        df['validTime'] = df['validTime'].dt.strftime('%m-%d %H:%M')  
        
        # save individual city data
        df.to_csv(CURR_DIR_PATH / "data" / (current_date + '_' + city + ".csv"), index=False)
        
        # create new a feature from the city name 
        df['city'] = city
        # add each iterative (i.e. i) dataFrame to a combined dataFrame
        df_combined = pd.concat([df_combined, df], axis=0)
    
    # Save the combined dataFrame to a CSV file    
    df_combined.to_csv(Path(CURR_DIR_PATH) / "combined_cities" / (current_date + '_concat.csv'), index=False)


    log.info("Finished extract_features func. dataFrames saved")

# extract_features()