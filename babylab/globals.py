"""Global variables."""

from importlib.resources import files
from json import load

from polars import Boolean, Datetime, Int64, Schema, String

URI: str = "https://apps.sjdhospitalbarcelona.org/redcap/api/"

with files("babylab.data").joinpath("colnames.json").open("r") as f:
    COLNAMES = load(f)

with files("babylab.data").joinpath("fields-to-rename.json").open("r") as f:
    FIELDS_TO_RENAME = load(f)

with files("babylab.data").joinpath("int-fields.json").open("r") as f:
    INT_FIELDS = load(f)

SCHEMA = {
    "participants": Schema(
        [
            ("record_id", String),
            ("date_created", Datetime(time_unit="us", time_zone=None)),
            ("date_updated", Datetime(time_unit="us", time_zone=None)),
            ("source", String),
            ("is_born", Boolean),
            ("name", String),
            ("age_created_months", Int64),
            ("age_created_days", Int64),
            ("sex", String),
            ("twin", String),
            ("isdropout", Boolean),
            ("parent1_name", String),
            ("parent1_surname", String),
            ("email1", String),
            ("phone1", String),
            ("parent2_name", String),
            ("parent2_surname", String),
            ("email2", String),
            ("phone2", String),
            ("address", String),
            ("city", String),
            ("postcode", String),
            ("birth_type", String),
            ("gest_weeks", Int64),
            ("birth_weight", Int64),
            ("head_circumference", Int64),
            ("apgar1", Int64),
            ("apgar2", Int64),
            ("apgar3", Int64),
            ("hearing", String),
            ("diagnoses", String),
            ("comments", String),
            ("age_now_months", Int64),
            ("age_now_days", Int64),
        ]
    ),
    "appointments": Schema(
        [
            ("record_id", String),
            ("redcap_repeat_instance", Int64),
            ("study", String),
            ("date_created", Datetime(time_unit="us", time_zone=None)),
            ("date_updated", Datetime(time_unit="us", time_zone=None)),
            ("date", Datetime(time_unit="us", time_zone=None)),
            ("transport", String),
            ("taxi_address", String),
            ("taxi_isbooked", Boolean),
            ("status", String),
            ("confirmation_comments", String),
            ("comments", String),
            ("id", String),
        ]
    ),
    "questionnaires": Schema(
        [
            ("record_id", String),
            ("redcap_repeat_instance", Int64),
            ("date_created", Datetime(time_unit="us", time_zone=None)),
            ("date_updated", Datetime(time_unit="us", time_zone=None)),
            ("isestimated", Boolean),
            ("lang1", String),
            ("lang1_exp", Int64),
            ("lang2", String),
            ("lang2_exp", Int64),
            ("lang3", String),
            ("lang3_exp", Int64),
            ("lang4", String),
            ("lang4_exp", Int64),
            ("comments", String),
            ("complete", String),
        ]
    ),
}
