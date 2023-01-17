from flasgger import Swagger
from flask import Flask, abort, render_template, request
from flask_restful import Api

from .api_views import DetailDriverApi, ReportApi, ReportApiAsc
from .get_data import Analyze

app = Flask(__name__)
api = Api(app)
Swagger(app)
app.config['JSON_SORT_KEYS'] = False


@app.route('/report')
def report() -> str:
    return render_template('common_statistic.html', info_race=Analyze().sort(direction=False))


@app.route('/drivers/driver_id=<code>')
def detail_driver(code: str) -> str:
    analyzer = Analyze()
    if analyzer.find_code(code):
        return render_template('driver.html', info_race=analyzer.find_code(code))
    return abort(400, "ID not found")


@app.route('/drivers/')
def report_drivers() -> str:
    analyzer = Analyze()
    order = request.args.get('order', type=str)
    if order is None:
        return render_template('report_code_name.html', info_race=analyzer.sort(direction=True))
    elif order == 'desc':
        return render_template('common_statistic.html', info_race=analyzer.sort(direction=True))
    elif order == 'asc':
        return render_template('common_statistic.html', info_race=analyzer.sort(direction=False))
    return abort(404)


api.add_resource(ReportApi, '/api/v1/report/')
api.add_resource(ReportApiAsc, '/api/v1/drivers/')
api.add_resource(DetailDriverApi, '/api/v1/drivers/driver_id=<code>')
