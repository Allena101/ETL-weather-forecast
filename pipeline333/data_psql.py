import pandas as pd
import configparser
from sqlalchemy import create_engine, Table, Column, Integer, String, Float, MetaData
from pathlib import Path
import log

log = log.get_logger(__name__)

CURR_DIR_PATH = Path(__file__).resolve().parent


def write_to_psql():
    log.info("Starting write_to_psql func")
    config = configparser.ConfigParser()

    # read config file
    # you have to add your password to the config.ini file!!! 
    config.read(CURR_DIR_PATH / "config.ini")
    db_pw = config.get("DEV", "psycopg2_pw")
    
    # database must exist
    db_name = 'weather222'

    # define the database URL
    db_url = f'postgresql+psycopg2://postgres:{db_pw}@localhost/{db_name}'

    # create the database engine
    engine = create_engine(db_url)

    # create a metadata object
    metadata = MetaData()

    # creates pqsql table with the same columns as the combined cities dataFrame
    table_name = 'weather_data'
    weather_data = Table(table_name, metadata,
                        Column('id', Integer, primary_key=True),
                        Column('validTime', String),
                        Column('temperature', Float),
                        Column('wind_speed', Float),
                        Column('precipitation', Float),
                        Column('air_pressure', Float),
                        Column('city', String)
                        )

    # create the table in the database
    metadata.create_all(engine)

    # read the csv file into a pandas DataFrame
    df = pd.read_csv(r"C:\Users\Magnus\Desktop\ETL\pipeline\combined_cities\2023-04-30_concat.csv")

    # insert the data into the table
    with engine.connect() as conn:
        for _, row in df.iterrows():
            insert_statement = weather_data.insert().values(
                validTime=row['validTime'],
                temperature=row['temperature'],
                wind_speed=row['wind_speed'],
                precipitation=row['precipitation'],
                air_pressure=row['air_pressure'],
                city=row['city']
            )
            conn.execute(insert_statement)
    
    log.info("Finished write_to_psql func")

# write_to_psql()