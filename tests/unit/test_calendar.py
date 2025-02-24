"""Test calendar"""

from datetime import datetime
import pytest
from babylab.src import api

timestamp = datetime(2024, 12, 17)


def test_get_age():
    """Test ``get_age``"""
    bd = datetime(2024, 5, 1)

    # when only birth date is provided
    assert isinstance(api.get_age(bd), tuple)
    assert all(isinstance(d, int) for d in api.get_age(bd))
    assert len(api.get_age(bd)) == 2

    # when birth date AND timestamp are provided
    assert isinstance(api.get_age(bd, timestamp), tuple)
    assert all(isinstance(d, int) for d in api.get_age(bd, timestamp))
    assert len(api.get_age(bd, timestamp)) == 2

    # when birth date is provided as datetime
    assert isinstance(api.get_age(bd), tuple)
    assert all(isinstance(d, int) for d in api.get_age(bd))
    assert len(api.get_age(bd)) == 2

    assert all(d > 0 for d in api.get_age(bd, timestamp))
    with pytest.raises(ValueError):
        api.get_age("a2025-05-01")
        api.get_age("01-05-2024")
        api.get_age("a2025-05-01", timestamp)
        api.get_age("01-05-2024", timestamp)
        api.get_age("2024/05/01", timestamp)


def test_get_birth_date():
    """Test ``get_birth_date``."""
    bd = api.get_birth_date((0, 1), timestamp)
    assert isinstance(api.get_birth_date((2, 1)), datetime)
    assert bd == datetime(2024, 12, 16, 0, 0)

    bd = api.get_birth_date((1, 0), timestamp)
    assert bd == datetime(2024, 11, 17, 0, 0)

    bd = datetime(2024, 11, 17, 0, 0)
    assert bd == datetime(2024, 11, 17, 0, 0)

    assert api.get_birth_date(("1", 0))
    assert api.get_birth_date((1, "0"))

    with pytest.raises(ValueError):
        api.get_birth_date((1, "a"))

    with pytest.raises(api.BadAgeFormat):
        api.get_birth_date("1:0")
