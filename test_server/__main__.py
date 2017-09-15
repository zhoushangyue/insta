from flask import Flask, request, session, g, redirect, url_for, abort, \
    render_template, flash, make_response, Response,send_file,jsonify,send_from_directory
import threading
from time import sleep

app = Flask(__name__)
indexs = 'helloworld'

@app.route('/',methods=['GET', 'POST'])
def index():
    return indexs

def test1():
    global indexs
    i = 0
    while True:
        i += 1
        indexs = 'helloworld' + str(i)
        sleep(1)

def main():
    t = threading.Thread(target=test1)
    t.setDaemon(True)
    t.start()
    app.run(host='0.0.0.0', port=20000, debug=True, use_reloader=False, threaded=True)


if __name__ == '__main__':
    main()
