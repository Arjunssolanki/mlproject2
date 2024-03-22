import os
import sys # we are using it because we want to use custom exception
from src.mlproject.exception import CustomException
from logger import logging
import pandas as pd
from src.mlproject.utils import read_sql_data
from sklearn.model_selection import train_test_split


from dataclasses import dataclass


@dataclass
class DataIngestionConfig:
    train_data_path:str=os.path.join('artifacts','train.csv')
    test_data_path:str=os.path.join('artifacts','test.csv')
    raw_data_path:str=os.path.join('artifacts','raw.csv')
    
class DataIngestion:
    def __init__(self):
        self.ingestion_config=DataIngestionConfig()
        
    def initiate_data_ingestion(self):
        try:
            # reading the data from mysql
            #df=read_sql_data()
            
            # reading the data from notebook/data/raw.csv
            df=pd.read_csv(os.path.join('notebook/data','raw.csv'))
            
            logging.info("Reading from mysql database")
            os.makedirs(os.path.dirname(self.ingestion_config.train_data_path),exist_ok=True)
            # since in __init__(self), data is present in self.ingestion_config
            
            # getting data from sql and saving raw data
            df.to_csv(self.ingestion_config.raw_data_path,index=False,header=True)
            # data will be savedin artifact folder as raw data
            train_set,test_set=train_test_split(df,test_size=0.2, random_state=42)
            #saving test and train data in artifacts folder
            df.to_csv(self.ingestion_config.train_data_path,index=False,header=True)
            df.to_csv(self.ingestion_config.test_data_path,index=False,header=True)
            logging.info("Data Ingestion is completed")
            
            return(
                self.ingestion_config.train_data_path,
                self.ingestion_config.test_data_path
                
            )

            

        except Exception as e:
            raise CustomException(e,sys)