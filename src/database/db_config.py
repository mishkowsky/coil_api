import os
from dataclasses import dataclass
from dotenv import load_dotenv
load_dotenv()


@dataclass(frozen=True)
class DBConfig:
    DBMS: str
    DRIVER: str
    HOSTNAME: str
    DATABASE: str
    USERNAME: str
    PASSWORD: str
    config_name: str


class DBConfigInstance:

    def __init__(self, in_db_config: DBConfig):
        self.DB_URI = '{}+{}://{}:{}@{}/{}'.format(
            in_db_config.DBMS, in_db_config.DRIVER, in_db_config.USERNAME,
            in_db_config.PASSWORD, in_db_config.HOSTNAME, in_db_config.DATABASE
        )


# DEBUG_CONFIG = DBConfigInstance(
#     DBConfig(
#         DBMS='postgresql',
#         DRIVER='psycopg2',
#         HOSTNAME='localhost',
#         DATABASE='postgres',
#         USERNAME='postgre',
#         PASSWORD='postgres',
#         config_name='debugging_config'
#     ))

DEBUG_CONFIG = DBConfigInstance(
    DBConfig(
        DBMS=os.getenv("DBMS"),
        DRIVER=os.getenv("DB_DRIVER"),
        HOSTNAME=os.getenv("DB_HOSTNAME"),
        DATABASE=os.getenv("DB_DATABASE"),
        USERNAME=os.getenv("DB_USERNAME"),
        PASSWORD=os.getenv("DB_PASSWORD"),
        config_name='debugging_config'
    ))


DB_CONFIG = DEBUG_CONFIG
