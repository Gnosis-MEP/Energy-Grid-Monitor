import datetime
import os
import csv

from flask import Flask, request, jsonify, make_response, abort, url_for, render_template
from sqlalchemy_utils import database_exists, create_database

from models import EnergyModel, db


DATABASE_URL = 'sqlite:///energy.db'

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

ENERGENIE_FILE = os.path.join(ROOT_DIR, 'src', 'energenie.csv')

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)


@app.route('/api/get-energy')
def get_energy_consumption():
    start_time = request.args.get('starttimestamp', None)
    end_time = request.args.get('endtimestamp', None)
    device = request.args.get('device', None)
    query = db.session.query(EnergyModel)
    if start_time:
        start_time = datetime.datetime.fromtimestamp(float(start_time))
        query = query.filter(EnergyModel.timestamp >= start_time)
    if end_time:
        end_time = datetime.datetime.fromtimestamp(float(end_time))
        query = query.filter(EnergyModel.timestamp <= end_time)

    if device:
        device = int(device)
        query = query.filter(EnergyModel.device_id == device)

    readings = query.all()

    data = {
        'readings': [r.as_json_friendly_dict() for r in readings]
    }
    return make_response(jsonify(data), 200)


@app.route('/api/set-energy', methods=['post'])
def set_energy_consumption():
    if not request.json:
        abort(400)

    try:
        readings = request.json
        readings['timestamp'] = datetime.datetime.fromtimestamp(readings['timestamp'])
        new_reading = EnergyModel(**readings)
        db.session.add(new_reading)
        db.session.commit()
    except:
        abort(400)

    return make_response(jsonify({'status': 'ok'}), 200)


def database_is_empty():
    if not database_exists(db.engine.url):
        create_database(db.engine.url)
    table_names = db.inspect(db.engine).get_table_names()
    is_empty = table_names == []
    print('Db is empty: {}'.format(is_empty))
    return is_empty


if __name__ == '__main__':
    app.app_context().push()
    if database_is_empty():
        db.drop_all()
        db.create_all()

    app.run(host='0.0.0.0', port=5000, debug=False)
