from apscheduler.schedulers.blocking import BlockingScheduler
import data_ingestion
import data_transformation
import data_plotting
import data_psql
import log

scheduler = BlockingScheduler()

@scheduler.scheduled_job('cron', day='*', hour=4, minute=30)
def run_script():
    if __name__ == "__main__":
        logger = log.get_logger('log')
        logger.info("Starting main.py script")
        data_ingestion.get_weather_forecast()
        data_transformation.extract_features()
        data_plotting.plot_weather_data()
        data_psql.write_to_psql()
        logger.info("Finished running main.py script")

scheduler.start()