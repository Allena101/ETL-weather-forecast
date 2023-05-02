import json
import requests
from datetime import datetime
from pathlib import Path
import pandas as pd
import pandera as pa
import log

log = log.get_logger(__name__)
CURR_DIR_PATH = Path(__file__).resolve().parent

# sample of cities coordinates to use with the API
geo_locations = {
    "uppsala": (59.9, 17.6),
    "östersund": (63.2, 14.6),
    "luleå": (65.6, 22.1),
    "göteborg": (57.7, 12),
    "trelleborg": (55.4, 13.2),
    "stockholm": (59.3, 18.1)
}

WEATHER_URL = "https://opendata-download-metfcst.smhi.se/api/category/pmp3g/version/2/geotype/point/lon/{}/lat/{}/data.json"


# Get the current date
current_date = datetime.now().strftime("%Y-%m-%d")

# Define a Pandera schema for data validation
schema = pa.DataFrameSchema({
    "time": pa.Column(pa.String),
    "temperature": pa.Column(pa.Float),
    "precipitation": pa.Column(pa.Float),
    "windSpeed": pa.Column(pa.Float),
    "pressure": pa.Column(pa.Float)
})



def get_weather_forecast():
    log.info("Starting API call -> get_weather_forecast function")    
    for city, coordinates in geo_locations.items():
        
        # Add the city coordinates to the url endpoint    
        url = WEATHER_URL.format(coordinates[1], coordinates[0])

        # Send a request to the API endpoint
        response = requests.get(url)

        # Parse the response JSON
        response_json = response.json()
        log.info("start weather data validation")
        
        for entry in response_json["timeSeries"]:
    # Extract the relevant fields from the JSON entry
            data = {
                "time": entry["validTime"],
                "temperature": float(entry["parameters"][10]["values"][0]),
                "precipitation": float(entry["parameters"][9]["values"][0]),
                "windSpeed": float(entry["parameters"][12]["values"][0]),
                "pressure": float(entry["parameters"][11]["values"][0]),
            }
            data = pd.DataFrame([data])
            

            # Validate the data against the schema
            # log.info("start weather data validation")
            try:
                validated_data = schema.validate(data)
                
                # If validation succeeds, print the validated data
                # log.info("data was successfully validated")
                
            except pa.errors.SchemaErrors as e:
                # If validation fails, print the validation error message
                log.info("data failed validation")
                print(f"Error validating data: {e}")
        
        log.info("data was successfully validated")
        # Trying to use Path instead of os
        file_path = Path(CURR_DIR_PATH) / "raw" / f"{current_date}_{city}_forecast.json"

        # Dump the forecast data into a JSON file
        with open(file_path, "w") as f:
            json.dump(response_json, f)
            
    log.info("json file has been dumped")    
        
            
# get_weather_forecast()