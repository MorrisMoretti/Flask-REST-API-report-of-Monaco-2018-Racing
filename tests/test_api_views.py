from http import HTTPStatus
from unittest.mock import patch

import pytest

from tests.conftest import DATA
from web_report import RacerToJS, handle_response

DR_URL = '/api/v1/drivers/'
REP_URL = '/api/v1/report/'


@pytest.mark.parametrize('param, expected_result', [
    (f'{REP_URL}''?format=json', HTTPStatus.OK),
    (f'{REP_URL}''?format=xml', HTTPStatus.OK),
    (f'{REP_URL}''?format=fake_format', HTTPStatus.BAD_REQUEST),
    (f'{DR_URL}''?format=json&order=desc', HTTPStatus.OK),
    (f'{DR_URL}''?format=xml&order=desc', HTTPStatus.OK),
    (f'{DR_URL}''?format=xml&order=asc', HTTPStatus.OK),
    (f'{DR_URL}''?format=json&order=asc', HTTPStatus.OK),
    (f'{DR_URL}''?format=json', HTTPStatus.OK),
    (f'{DR_URL}''?format=xml', HTTPStatus.OK),
    (f'{DR_URL}''?format=fake_format', HTTPStatus.BAD_REQUEST),
    (f'{DR_URL}''driver_id=SVF?format=xml', HTTPStatus.OK),
    (f'{DR_URL}''driver_id=SVF?format=json', HTTPStatus.OK),
    (f'{DR_URL}''driver_id=SVF?format=fake_format', HTTPStatus.BAD_REQUEST),
    (f'{DR_URL}''driver_id=fake_abr?format=json', HTTPStatus.BAD_REQUEST),
])
def test_links_to_resp_status(validate_path, mocker_folder, param, expected_result, app, client):
    with app.app_context():
        response = client.get(param)
        assert expected_result == response.status_code


@pytest.mark.parametrize('param, expected_result', [('json', HTTPStatus.OK), ('xml', HTTPStatus.OK), ])
def test_handle_response(param, expected_result, app):
    with app.app_context():
        resp = app.make_response(handle_response(from_request=param, racer=[RacerToJS(position=1, driver_info=DATA)]))
    assert expected_result == resp.status_code


@pytest.mark.parametrize('param, expected_result',
                         [('?format=json', b'[{"position": 1, "driver_info": {"lap_time": "0:01:04.41'),
                          ('?format=xml', b'e="int">1</position><driver_info type="dict"><lap_time ty'),
                          ('/undefined_page/', b'404 Not Found'), ])
def test_report_api(client, param, expected_result):
    with patch('web_report.api_views.Analyze.sort', return_value=[RacerToJS(position=1, driver_info=DATA)]):
        response = client.get(f'{REP_URL}{param}')
        assert expected_result in response.data


@pytest.mark.parametrize('param, expected_result',
                         [('?format=json&order=desc', b'[{"position": 1, "driver_info": {"lap_time":'),
                          ('?format=xml&order=desc', b'e="int">1</position><driver_info type="dict"'),
                          ('?format=xml&order=asc', b'<car type="str">FERRARI</car><driver type="st'),
                          ('/undefined_page/', b'404 Not Found'), ])
def test_report_api_asc(client, param, expected_result):
    with patch('web_report.api_views.Analyze.sort', return_value=[RacerToJS(position=1, driver_info=DATA)]):
        response = client.get(f'{DR_URL}{param}')
        assert expected_result in response.data


@pytest.mark.parametrize('param, expected_result',
                         [('driver_id=SVF?format=json', b'[{"position": 1, "driver_info": {"lap_time"'),
                          ('driver_id=SVF?format=xml', b'<abr type="str">SVF</abr>'),
                          ('/undefined_page/', b'404 Not Found'), ])
def test_detail_driver_api(client, param, expected_result):
    with patch('web_report.api_views.Analyze.find_code', return_value=[RacerToJS(position=1, driver_info=DATA)]):
        response = client.get(f'{DR_URL}{param}')
        assert expected_result in response.data
