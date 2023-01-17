from http import HTTPStatus
from unittest.mock import patch

import pytest

from tests.conftest import DATA


def test_report(client):
    with patch('web_report.app.Analyze.sort', return_value=[(1, DATA)]):
        response = client.get('/report')
        assert b'<td>FERRARI</td>' in response.data


def test_report_drivers(client):
    with patch('web_report.app.Analyze.sort', return_value=[(1, DATA)]):
        response = client.get('/drivers/')
        link = b'<td><a href=" /drivers/driver_id=SVF"> SVF </a> </td>\n'
        assert link in response.data


@pytest.mark.parametrize('param',
                         ['/drivers/?order=asc',
                          '/drivers/?order=desc', ])
def test_report_drivers_desc(param, client):
    with patch('web_report.app.Analyze.sort', return_value=[(1, DATA)]):
        tags = [b'<th scope="row">1.</th>', b'<td>Sebastian Vettel</td>',
                b'<td>FERRARI</td>', b'<td>0:01:04.415000</td>']
        response = client.get(param)
        for tag in tags:
            assert tag in response.data


@pytest.mark.parametrize('param, expected_result',
                         [('/drivers/?order=asc1', HTTPStatus.NOT_FOUND),
                          ('/undefined_page/', HTTPStatus.NOT_FOUND), ])
def test_fail_page(param, expected_result, client):
    response = client.get(param)
    assert expected_result == response.status_code


def test_detail_driver(client):
    with patch('web_report.app.Analyze.find_code', return_value=DATA):
        response = client.get('/drivers/driver_id=SVF')
        assert b'<td>Sebastian Vettel</td>' in response.data
