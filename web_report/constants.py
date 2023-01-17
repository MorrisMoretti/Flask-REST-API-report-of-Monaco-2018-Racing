from enum import Enum

FOLDER = 'road_data'


class RequestType(str, Enum):
    json = 'json'
    xml = 'xml'
