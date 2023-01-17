from dataclasses import dataclass
from typing import List, Union

from report_monaco import Racer, RacingDataAnalyzer, read_files, validate_path

from web_report.constants import FOLDER


@dataclass
class RacerToJS:
    position: int
    driver_info: Racer


class Analyze:

    @property
    def run_analyzer(self) -> RacingDataAnalyzer:
        folder_path = validate_path(FOLDER)
        raw_data = read_files(folder_path)
        analyzer = RacingDataAnalyzer(raw_data)
        analyzer.build_report()
        return analyzer

    def sort(self, direction: bool) -> List[RacerToJS]:
        analyzer = self.run_analyzer
        analyzer.sort_by_time(direction=direction)
        return [RacerToJS(driver_info=info, position=number) for number, info in analyzer.enumerate_drivers()]

    def find_code(self, code: str) -> Union[Racer, None]:
        try:
            return self.run_analyzer.find_driver_by_code(driver_code=code)
        except StopIteration:
            return None
