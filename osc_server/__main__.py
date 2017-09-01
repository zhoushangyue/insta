from flask import Flask, request, session, g, redirect, url_for, abort, \
    render_template, flash, make_response, Response,send_file,jsonify,send_from_directory
from osc_config import *
from util.ins_util import *

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    res = service_osc_info.get_osc_info()
    return res


@app.route('/osc/<path>', methods=['GET', 'POST'])
def osc_path_execute(path):
    exe = execute()
    try:
        if request.headers.get('Content-Type'):
            content_type = request.headers.get('Content-Type')
            if 'application/json' in content_type:
                data = jsonstr_to_dic(request.get_json())
                res = exe.osc_api_execute(path, data)
        else:
            res = exe.osc_api_execute(path)

    except Exception as err:
        print("osc_path_execute:"+str(err))
    return res


def main():
    app.run(host='0.0.0.0', port=20000, debug=True)

if __name__ == '__main__':
    main()