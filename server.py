from flask import Flask
from flask_socketio import SocketIO

app = Flask(__name__, static_folder='static')
socketio = SocketIO(app)


@app.route('/')
def hello():
    return app.send_static_file('index.html')

@app.route('/map')
def map():
    return app.send_static_file('map.html')

@socketio.on('connect')
def handle_connect():
    print('Client connected')

if __name__ == '__main__':
    app.run(debug=True)

