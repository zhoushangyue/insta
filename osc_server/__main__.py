from flask import Flask, request, session, g, redirect, url_for, abort, \
    render_template, flash, make_response, Response,send_file,jsonify,send_from_directory
from osc_config import *
from util.ins_util import *
from osc.osc_statu import *
from camera_server.camera_command import *
import threading
import time

app = Flask(__name__)


#@app.route('/', methods=['GET', 'POST'])
#def index():
    #return '<h1>Hello World!</h1>'


@app.route('/osc/<path>', methods=['GET', 'POST'])
def osc_path(path):
    exe = execute()
    try:
        h = request.headers
        content_type = h.get('Content-Type')
        # fp = None
        data = OrderedDict()
        if content_type is not None and 'application/json' in content_type:
            data = OrderedDict(request.get_json())
        res = exe.osc_api_execute(path, data)

    except Exception as err:
        res = set_error(str(err))
    return res


@app.route('/osc/commands/execute', methods=['GET', 'POST'])
def osc_cmd():
    exe = execute()
    h = request.headers
    try:
        content_type = h.get('Content-Type')
        data = OrderedDict()
        if content_type is not None and 'application/json' in content_type:
            data = request.get_json()
        res = exe.osc_cmd_execute(data)
    except Exception as err:
        res = set_error(str(err))
        print(str(err))
    return res

@app.route('/osc/commands/status' ,methods=['GET', 'POST'])
def cmd_statu():
    try:
        h = request.headers
        content_type = h.get('Content-Type')
        data = OrderedDict()
        if content_type is not None and 'application/json' in content_type:
            data = request.get_json()
        if 'id' not in data.keys():
            res = set_error("status", "missingParameter")
        elif len(data) != 1:
            res = set_error("status", "invalidParameterName")
        else:
            res = service_osc_statu.osc_statu(data['id'])
    except Exception as err:
        res = set_error(str(err))
    return res


def test1():
    while True:
        print("test1")
        time.sleep(1)


def main():
    t = threading.Thread(target=http_state)
    t.setDaemon(True)
    t.start()
    app.run(host='0.0.0.0', port=80, debug=True, use_reloader=False, threaded=True)


if __name__ == '__main__':
    main()
    #c.diconnect_to_cameraserver()
