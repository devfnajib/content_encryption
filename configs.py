import os
from dotenv import load_dotenv
from loguru import logger


logger.info('Loading configurations from environment variables.')
load_dotenv()
DB_HOST = os.getenv('DB_HOST')
DB_PORT = int(os.getenv('DB_PORT'))
DB_USERNAME = os.getenv('DB_USERNAME')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_NAME = os.getenv('DB_NAME')

logger.info('Environment variables loaded, preparing db connection string.')
DB_CONNECTION_STRING = 'postgresql+psycopg2://{}:{}@{}:{}/{}'.format(DB_USERNAME, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME)
