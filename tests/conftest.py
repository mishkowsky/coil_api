from datetime import datetime
import pytest
from pytest_postgresql.janitor import DatabaseJanitor
from sqlalchemy import create_engine
from sqlalchemy.orm.session import sessionmaker
import src
from src.database.model import Coil, Base


@pytest.fixture(scope="session")
def db_session(test_db):
    pg_host = test_db.host
    pg_port = test_db.port
    pg_user = test_db.user
    pg_password = test_db.password
    pg_db = test_db.dbname

    with DatabaseJanitor(pg_user, pg_host, pg_port, pg_db, test_db.version, pg_password):
        connection_str = f"postgresql+psycopg2://{pg_user}:@{pg_host}:{pg_port}/{pg_db}"
        engine = create_engine(connection_str)
        with engine.connect() as con:
            Base.metadata.create_all(con)
            con.commit()
            src.database.session.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
            yield sessionmaker(bind=engine, autocommit=False, autoflush=False)


@pytest.fixture(scope="module")
def create_test_data(db_session):

    date_format = '%Y-%m-%d %H:%M:%S.%f'
    test_objs = [
        Coil(length=1, weight=5,
             created_at=datetime.strptime('2023-10-07 01:16:00.850625', date_format),
             deleted_at=None),
        Coil(length=4, weight=4,
             created_at=datetime.strptime('2023-10-07 01:16:00.850625', date_format),
             deleted_at=datetime.strptime('2023-10-07 23:15:03.758473', date_format)),
        Coil(length=25, weight=12,
             created_at=datetime.strptime('2023-10-08 02:26:01.095368', date_format),
             deleted_at=datetime.strptime('2023-10-08 02:41:18.723611', date_format)),
        Coil(length=12, weight=12,
             created_at=datetime.strptime('2023-10-07 01:16:00.850625', date_format),
             deleted_at=datetime.strptime('2023-10-08 02:42:33.787865', date_format)),
        Coil(length=23, weight=12,
             created_at=datetime.strptime('2023-10-08 11:11:28.658098', date_format),
             deleted_at=datetime.strptime('2023-10-08 11:11:34.68338', date_format)),
    ]

    session = db_session()
    for obj in test_objs:
        session.add(obj)
    session.commit()

    return test_objs
