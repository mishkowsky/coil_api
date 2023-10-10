
from src.schemas.coil import Range, GetCoilRequestBody, StatResponseBody
import pytest


class TestRange:
    def test_init(self):

        with pytest.raises(ValueError):
            Range(start=10, end=5)

        with pytest.raises(ValueError):
            assert 'a' < 'b'
            Range(start='a', end='b')

        range_obj = Range(start=1, end=1)
        assert range_obj.start == 1
        assert range_obj.end == 1


class TestGetCoilRequestBody:
    def test_init(self):

        with pytest.raises(ValueError):
            GetCoilRequestBody()

        with pytest.raises(ValueError):
            GetCoilRequestBody(id_range={'start': -1, 'end': 1})

        with pytest.raises(ValueError):
            GetCoilRequestBody(id_range={'start': -1, 'end': 1})

        request_body = GetCoilRequestBody(id_range={'start': 1, 'end': 1})
        assert request_body.id_range is not None


class TestStatResponseBody:
    def test_init(self):
        response_body = StatResponseBody(min_length=1)
        assert response_body.added_coils_count == 0
        assert response_body.deleted_coils_count == 0
        assert response_body.avg_length == 0.0
        assert response_body.avg_weight == 0.0
        assert response_body.max_length is None
        assert response_body.min_length is 1
        assert response_body.max_weight is None
        assert response_body.min_weight is None
        assert response_body.total_weight == 0
        assert response_body.min_period is None
        assert response_body.max_period is None
