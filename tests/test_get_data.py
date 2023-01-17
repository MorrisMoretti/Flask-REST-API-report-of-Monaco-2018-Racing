from unittest.mock import patch

from tests.conftest import DATA
from web_report.get_data import Analyze, RacerToJS


def test_analyze(validate_path, mocker_folder):
    assert 'web_report.get_data.Analyze object' in str(Analyze())


@patch('web_report.get_data.RacingDataAnalyzer.sort_by_time', return_value=[DATA])
@patch('web_report.get_data.RacingDataAnalyzer.enumerate_drivers', return_value=[(1, DATA)])
def test_sort(mock_sort_by_time, enumerate_drivers, validate_path, mocker_folder):
    assert Analyze().sort(direction=True) == [RacerToJS(position=1, driver_info=DATA)]
    mock_sort_by_time.assert_called_once()
    enumerate_drivers.assert_called_once()


@patch('web_report.get_data.RacingDataAnalyzer.find_driver_by_code', return_value=DATA)
def test_find_code(mock_find_driver_by_code, validate_path, mocker_folder):
    assert Analyze().find_code(code='SVF') == DATA
    mock_find_driver_by_code.assert_called_once()
