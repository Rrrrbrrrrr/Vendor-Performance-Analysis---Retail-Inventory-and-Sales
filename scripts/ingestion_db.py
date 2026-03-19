# IMPORTING LIBRARIES

import pandas as pd
import os
from sqlalchemy import create_engine
import logging
import time

logging.basicConfig(
    filename ="logs/ingestion_db.log",
    level = logging.DEBUG,
    format = "%(asctime)s - %(levelname)s - %(message)s",
    filemode = "a"
)

# CREATING INVENTORY DATABASE

# engine = create_engine('sqlite:///inventory.db')
engine = create_engine('sqlite:///inventory.db', connect_args={'timeout': 30})

# INSERTING DATA(TABLES) IN INVENTORY DATABASE
def ingest_db(df, table_name, engine):
    '''This function will ingest the dataframe into database table'''

    df.to_sql(
        table_name,
        con=engine,
        if_exists='replace',
        index=False
    )

def load_raw_data():
    ''''This function will load CSVs into dataframe and ingest into DB'''
    start_time = time.time()
    
    for file in os.listdir('Data'):
        if file.endswith('.csv'):
            table_name = file[:-4]
            file_path = 'Data/' + file
            # logging.info(f"Ingesting {file in db}")
            logging.info(f"Ingesting {file} into DB")
            print("Inserting:", table_name)
            # ingest_db(file_path, table_name, engine)
            df = pd.read_csv(file_path)
            ingest_db(df, table_name, engine)
    
    end_time = time.time()
    total_time = (end_time - start_time)/60
    logging.info('----------Ingestion Complete----------')
    logging.info(f'\nTotal time Taken: {total_time} minutes')

if __name__ == '__main__':
    load_raw_data()