import datetime
import json
import time
from urllib import request
from urllib.parse import urlencode


def build_url(base, endpoint):
    return base + endpoint


SERVER_URL = 'http://localhost:5000'
SET_ENERGY_ENDPOINT = '/api/set-energy'
GET_ENERGY_ENDPOINT = '/api/get-energy'

SET_ENERGY_URL = build_url(SERVER_URL, SET_ENERGY_ENDPOINT)
GET_ENERGY_URL = build_url(SERVER_URL, GET_ENERGY_ENDPOINT)


def make_request_post(url, data):

    params = json.dumps(data).encode('utf8')
    req = request.Request(url,
                          data=params, headers={'content-type': 'application/json'})
    response = request.urlopen(req)
    return response


def make_request_get(url, params):
    encodeddata = urlencode(params)
    url_with_params = f'{url}?{encodeddata}'
    req = request.Request(url_with_params)
    response = request.urlopen(req)
    return response


def add_readings():
    timestamps = []
    for i in range(10):
        timestamp = time.time()
        timestamps.append(timestamp)
        sensorid = 1
        voltage = f'{i*10.1}'
        frequency = f'{i*10.01}'
        real_energy = f'{i*10.001}'
        data = {
            'device_id': sensorid,
            'timestamp': timestamp,
            'voltage': voltage,
            'frequency': frequency,
            'real_energy': real_energy,
        }
        resp = make_request_post(SET_ENERGY_URL, data)
        print(resp.status)
        time.sleep(1)
    return timestamps


def get_first_last_timestamp(timestamps):
    return timestamps[0], timestamps[-1]


def get_readings(timestamps, ret_indexes):
    # first_half = timestamps[:int(len(timestamps) / 2)]
    # second_half = timestamps[int(len(timestamps) / 2):]
    asked_timestamps = [timestamps[i] for i in ret_indexes]

    starttimestamp, endtimestamp = get_first_last_timestamp(asked_timestamps)
    params = {
        'starttimestamp': starttimestamp,
        'endtimestamp': endtimestamp,
        'device': 1,
    }
    resp = make_request_get(GET_ENERGY_URL, params)
    content = resp.read().decode('utf8')
    data = json.loads(content)
    return data


def check_readings(timestamps, readings, ret_indexes):
    for i in ret_indexes:
        correct_stamp = timestamps[i]
        correct_date = datetime.datetime.fromtimestamp(float(correct_stamp))
        correct_reading = None
        for reading_index, reading in enumerate(readings['readings']):
            reading_date = datetime.datetime.fromtimestamp(float(reading['timestamp']))
            if reading_date.strftime("%m/%d/%Y, %H:%M:%S") == correct_date.strftime("%m/%d/%Y, %H:%M:%S"):
                correct_reading = reading_index
                break
        if correct_reading is not None:
            print(f'Found: "{correct_stamp}" / "{correct_date}"')
            readings['readings'].pop(reading_index)
        else:
            print(f'Didint find: {i} "{correct_stamp}" / "{correct_date}" in {readings}')


if __name__ == '__main__':
    timestamps = add_readings()
    ret_indexes = [3, 4, 5, 6]
    readings = get_readings(timestamps, ret_indexes)
    check_readings(timestamps, readings, ret_indexes)
