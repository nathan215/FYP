from flask import Flask, jsonify
from flask_socketio import SocketIO
import subprocess
from threading import Thread

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

@app.route('/')
def index():
    return 'Server is running'

@app.route('/status', methods=['GET'])
def status():
    return jsonify({'status': 'Server is running and processing data'})

@socketio.on('connect')
def handle_connect():
    print('A client connected')

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

def start_python():
    print('Attempting to start SeperateJob.py')
    subprocess.Popen(['python', './python-scripts/SeperateJob.py'])

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=3000)
    start_python()
    