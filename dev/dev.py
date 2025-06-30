"""
Fixtures for testing
"""

from babylab.src import api
from babylab.app import create_app
from babylab.app import config as conf
from tests import utils as tutils


token = conf.get_api_key()
records = api.Records(token=token)
data_dict = api.get_data_dict(token=token)
ppt = tutils.create_record_ppt()
apt = tutils.create_record_apt()
que = tutils.create_record_que()
ppt_finput = tutils.create_finput_ppt()
apt_finput = tutils.create_finput_apt()
que_finput = tutils.create_finput_que()
app = create_app(env_="test")
client = app.test_client()
app.config["API_KEY"] = token
