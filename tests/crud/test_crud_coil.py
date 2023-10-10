from datetime import datetime
from src.crud.crud_coil import coil
from src.database.model import Coil
from src.schemas.coil import GetCoilRequestBody, CoilCreate, CoilUpdate
from tests.utils import count_stats_for_test_data


def test_get_by_ranges(create_test_data, db_session):
    session = db_session()
    request = GetCoilRequestBody(id_range={'start': 1, 'end': 3}, weight_range={'start': 5, 'end': 12})
    result = coil.get_coils_by_ranges(session, request)
    assert len(result) == 2


def test_create(db_session):
    session = db_session()
    create_coil = CoilCreate(length=10, weight=15)
    coil.create(session, obj_in=create_coil)
    query_result = session.query(Coil).all()
    assert len(query_result) == 1

    coil_from_db = query_result[0]
    assert coil_from_db.length == create_coil.length
    assert coil_from_db.weight == create_coil.weight


def test_remove(create_test_data, db_session):
    session = db_session()
    coil_from_db = session.query(Coil).filter(Coil.id == 3).one()
    assert coil_from_db is not None

    coil.remove(session, id_to_remove=3)
    coil_from_db = session.query(Coil).filter(Coil.id == 3).one_or_none()
    assert coil_from_db is None


def test_update(create_test_data, db_session):
    session = db_session()
    coil_from_db = session.query(Coil).filter(Coil.id == 1).one()
    assert coil_from_db.deleted_at is None

    delete_time_1 = datetime.now()
    update_obj = CoilUpdate(deleted_at=delete_time_1)
    coil.update(session, db_obj=coil_from_db, obj_in=update_obj)
    assert coil_from_db.deleted_at == delete_time_1

    updated_coil_from_db = session.query(Coil).filter(Coil.id == 1).one()
    assert updated_coil_from_db.deleted_at == delete_time_1

    delete_time_2 = datetime.now()
    update_obj = {'deleted_at': delete_time_2}
    coil.update(session, db_obj=coil_from_db, obj_in=update_obj)
    assert coil_from_db.deleted_at == delete_time_2

    updated_coil_from_db = session.query(Coil).filter(Coil.id == 1).one()
    assert updated_coil_from_db.deleted_at == delete_time_2


def test_get(create_test_data, db_session):
    session = db_session()
    coil_from_crud = coil.get(session, object_id=1)
    assert coil_from_crud.id == 1
    assert coil_from_crud.weight == create_test_data[0].weight
    assert coil_from_crud.length == create_test_data[0].length


def test_get_stat(create_test_data, db_session):
    session = db_session()
    date_format = '%Y-%m-%d %H:%M:%S.%f'
    start_date = datetime.strptime('2023-10-06 01:16:00.850625', date_format)
    end_date = datetime.strptime('2023-10-08 01:16:00.850625', date_format)

    result = coil.get_stats(session, start_date=start_date, end_date=end_date)

    stats = count_stats_for_test_data(create_test_data, start_date=start_date, end_date=end_date)

    assert stats == result
