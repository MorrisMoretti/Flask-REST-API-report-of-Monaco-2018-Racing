from unittest import mock
from unittest.mock import MagicMock, mock_open, patch

import pytest
from report_monaco import Racer

from web_report.app import app as flask_app

TAGS = [b'<th scope="row">1.</th>', b'<td>Sebastian Vettel</td>', b'<td>FERRARI</td>', b'<td>0:01:04.415000</td>']
DATA = Racer(lap_time='0:01:04.415000', car='FERRARI', driver='Sebastian Vettel', abr='SVF')
FILES = {'path/to/open/start.log': 'SVF2018-05-24_12:02:58.917',
         'path/to/open/end.log': 'SVF2018-05-24_12:04:03.332',
         'path/to/open/abbreviations.txt': 'SVF_Sebastian Vettel_FERRARI'}


@pytest.fixture
def app():
    yield flask_app


@pytest.fixture
def client(app):
    return app.test_client()


def open_mock(filename):
    for expected_filename, content in FILES.items():
        if filename == expected_filename:
            return mock_open(read_data=content).return_value
    return MagicMock(side_effect=open_mock)


@pytest.fixture
def mocker_folder():
    file_mock = MagicMock()
    with mock.patch("builtins.open", open_mock(FILES)):
        yield file_mock


@pytest.fixture
def validate_path():
    with patch('web_report.get_data.validate_path', return_value="path/to/open") as folder:
        yield folder
