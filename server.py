from datetime import time
import random
from flask import Flask
from flask_socketio import SocketIO
import gps

app = Flask(__name__, static_folder='static')
socketio = SocketIO(app, cors_allowed_origins="*")

@app.route('/')
def hello():
    return app.send_static_file('index.html')

@app.route('/map')
def map():
    return app.send_static_file('map.html')

@socketio.on('connect')
def connect():
    print('Client connected!')

@socketio.on('gps_data')
def gps_data(data):
    print("here comes the data!")
    gps.emit_data(socketio)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=3000, debug=True)

