# Logger.py  14/05/2016  D.J.Whale
#
# A simple logger  request- logs to a server.
import threading
import json
import time
from urllib import request

from energenie import OpenThings


def build_url(base, endpoint):
    return base + endpoint


SERVER_URL = 'http://localhost:5000'
SET_ENERGY_ENDPOINT = '/api/set-energy'

SET_ENERGY_URL = build_url(SERVER_URL, SET_ENERGY_ENDPOINT)


def make_request_post(url, data):

    params = json.dumps(data).encode('utf8')
    req = request.Request(url,
                          data=params, headers={'content-type': 'application/json'})
    response = request.urlopen(req)
    print(f'Log request status: {resp.status}')
    return response


def trace(msg):
    print(str(msg))


def logMessage(msg):
    # get the header
    header = msg['header']
    timestamp = time.time()
    sensorid = header['sensorid']

    # set defaults for any data that doesn't appear in this message
    # but build flags so we know which ones this contains
    flags = [0 for i in range(8)]
    switch = None
    voltage = None
    freq = None
    reactive = None
    real = None
    apparent = None
    current = None
    temperature = None

    # capture any data that we want
    # trace(msg)
    for rec in msg['recs']:
        paramid = rec['paramid']
        try:
            value = rec['value']
        except:
            value = None

        if paramid == OpenThings.PARAM_SWITCH_STATE:
            switch = value
            flags[0] = 1
        elif paramid == OpenThings.PARAM_VOLTAGE:
            flags[1] = 1
            voltage = value
        elif paramid == OpenThings.PARAM_FREQUENCY:
            flags[2] = 1
            freq = value
        elif paramid == OpenThings.PARAM_REACTIVE_POWER:
            flags[3] = 1
            reactive = value
        elif paramid == OpenThings.PARAM_REAL_POWER:
            flags[4] = 1
            real = value
        elif paramid == OpenThings.PARAM_APPARENT_POWER:
            flags[5] = 1
            apparent = value
        elif paramid == OpenThings.PARAM_CURRENT:
            flags[6] = 1
            current = value
        elif paramid == OpenThings.PARAM_TEMPERATURE:
            flags[7] = 1
            temperature = value

    data = {
        'device_id': sensorid,
        'timestamp': timestamp,
        'voltage': voltage,
        'frequency': freq,
        'real_energy': real,
    }
    thread = threading.Thread(target=make_request_post, args=(SET_ENERGY_URL, data))
    thread.start()
