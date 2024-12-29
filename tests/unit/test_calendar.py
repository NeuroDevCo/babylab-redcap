"""Test calendar"""

from datetime import datetime
import pytest
from babylab.src import api


def test_get_age():
    """Test ``get_age``"""
    # when only birth date is provided
    assert isinstance(api.get_age("2024-05-01"), list)
    assert all(isinstance(d, int) for d in api.get_age("2024-05-01"))
    assert len(api.get_age("2024-05-01")) == 2

    # when birth date AND timestamp are provided
    assert isinstance(api.get_age("2024-05-01", "2024-12-17"), list)
    assert all(isinstance(d, int) for d in api.get_age("2024-05-01", "2024-12-17"))
    assert len(api.get_age("2024-05-01", "2024-12-17")) == 2

    # when birth date is provided as datetime
    assert isinstance(api.get_age(datetime(2024, 5, 1)), list)
    assert all(isinstance(d, int) for d in api.get_age(datetime(2024, 5, 1)))
    assert len(api.get_age(datetime(2024, 5, 1))) == 2

    # when birth date and timestamp are provided as datetimes
    assert isinstance(api.get_age(datetime(2024, 5, 1), datetime(2024, 12, 17)), list)
    assert all(
        isinstance(d, int)
        for d in api.get_age(datetime(2024, 5, 1), datetime(2024, 12, 17))
    )
    assert len(api.get_age(datetime(2024, 5, 1), datetime(2024, 12, 17))) == 2

    assert all(d < 0 for d in api.get_age("2025-05-01", "2024-12-17"))
    with pytest.raises(ValueError):
        api.get_age("a2025-05-01")
        api.get_age("01-05-2024")
        api.get_age("a2025-05-01", "2024-12-17")
        api.get_age("01-05-2024", "2024-12-17")
        api.get_age("2024/05/01", "2024-12-17")


def test_get_birth_date():
    """Test ``get_birth_date``."""

    assert isinstance(
        api.get_birth_date("2:1"), datetime
    )  # pylint: disable=undefined-variable
    assert api.get_birth_date("0:1", "2024-12-17") == datetime(2024, 12, 16, 0, 0)
    assert api.get_birth_date("1:0", "2024-12-17") == datetime(2024, 11, 17, 0, 0)
