import data_ingestion
import data_transformation
import data_plotting
import data_psql
import log

logger = log.get_logger('log')

if __name__ == "__main__":
    logger.info("Starting main.py script")
    print('0')
    data_ingestion.get_weather_forecast()
    print('1')
    data_transformation.extract_features()
    print('2')
    data_plotting.plot_weather_data()
    print('3')
    data_psql.write_to_psql()
    print('4')
    logger.info("Finished running main.py script")
    
    
    

