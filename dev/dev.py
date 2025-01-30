"""
Fixtures for testing
"""

from babylab.src import api
from babylab.app import create_app
from babylab.app import config as conf
from tests import utils as tutils


TOKEN = conf.get_api_key()
RECORDS = api.Records(token=TOKEN)
DATA_DICT = api.get_data_dict(token=TOKEN)
PPT_REC = tutils.create_record_ppt()
APT_REC = tutils.create_record_apt()
QUE_REC = tutils.create_record_que()
PPT_FINPUT = tutils.create_finput_ppt()
APT_FINPUT = tutils.create_finput_apt()
QUE_FINPUT = tutils.create_finput_que()
APP = create_app(env="test")
CLIENT = APP.test_client()
APP.config["API_KEY"] = TOKEN
APP.config["EMAIL"] = "gonzalo.garcia@sjd.es"
