from typing import List, Union

import dicttoxml
from flask import Response, abort, jsonify, request
from flask_restful import Resource
from report_monaco import Racer

from .constants import RequestType
from .get_data import Analyze, RacerToJS


def handle_response(from_request: str, racer: Union[List[RacerToJS], List[Racer]]) -> Response:
    json_racer = jsonify(racer).json
    if from_request == RequestType.json:
        return json_racer
    if from_request == RequestType.xml:
        return Response(dicttoxml.dicttoxml(json_racer), mimetype='text/xml')
    return abort(400, str('Format not found'))


class ReportApi(Resource):

    def get(self) -> Response:
        """
        Report api
        ---
        parameters:
          - name: 'format'
            in: query
            type: string
            enum: ['json', 'xml']
            required: true
        responses:
          200:
            description: Show sorted list with drivers by asc
            schema:
              type: "object"
              properties:
                order:
                  type: "object"
              example: { "position": 1, "driver_info": {"lap_time": "0:01:04.415000","car":
                        "FERRARI","driver": "Sebastian Vettel","abr": "SVF"}}
          400:
            description: Format not found
            schema:
              type: "object"
              properties:
                order:
                  type: "object"
              example: { "message": "Format not found" }
          500:
            description: Internal Server Error
            schema:
              type: "object"
              properties:
                order:
                  type: "object"
              example: { "message": "Internal Server Error" }
        """
        racer_data = Analyze().sort(direction=False)
        return handle_response(from_request=request.args.get('format'), racer=racer_data)


class ReportApiAsc(Resource):

    def get(self) -> Response:
        """
        Report Api ASC/DESK XML/JSON
        ---
        parameters:
          - name: 'order'
            in: query
            type: string
            enum: ['asc', 'desc']
            required: false
          - name: 'format'
            in: query
            type: string
            enum: ['json', 'xml']
            required: true
        responses:
          200:
            description: Show sorted list with drivers by asc or desk
            schema:
              type: "object"
              properties:
                order:
                  type: "object"
              example: { "position": 1, "driver_info": {"lap_time": "0:01:04.415000",
                        "car": "FERRARI","driver": "Sebastian Vettel","abr": "SVF"}}
          400:
            description: Format not found
            schema:
              type: "object"
              properties:
                order:
                  type: "object"
              example: { "message": "Format not found" }
          500:
            description: Internal Server Error
            schema:
              type: "object"
              properties:
                order:
                  type: "object"
              example: { "message": "Internal Server Error" }
        """
        analyzer = Analyze()
        racer_data = analyzer.sort(direction=False)
        if request.args.get('order', type=str) == 'desc':
            racer_data = analyzer.sort(direction=True)
        return handle_response(from_request=request.args.get('format'), racer=racer_data)


class DetailDriverApi(Resource):

    def get(self, code: str) -> Response:
        """
        Detail driver view
        ---
        parameters:
          - name: 'code'
            in: path
            type: string
            required: true
          - name: 'format'
            in: query
            type: string
            enum: ['json', 'xml']
            required: true
        responses:
          200:
            description: Show info about driver
            schema:
              type: "object"
              properties:
                order:
                  type: "object"
              example: { "lap_time": "0:01:04.415000", "car": "FERRARI", "driver": "Sebastian Vettel", "abr": "SVF" }
          400:
            description: Format not found or Driver not found
            schema:
              type: "object"
              properties:
                order:
                  type: "object"
              example: { "message": "Driver not found" }
          500:
            description: Internal Server Error
            schema:
              type: "object"
              properties:
                order:
                  type: "object"
              example: { "message": "Internal Server Error" }
        """
        racer_data = Analyze().find_code(code)
        if not racer_data:
            return abort(400, 'Driver not found')
        return handle_response(from_request=request.args.get('format'), racer=[racer_data])
