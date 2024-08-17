from flask import Flask, render_template, Response
from flask_socketio import SocketIO

import cv2 


app = Flask(__name__)
camera = cv2.VideoCapture(0)
socketio = SocketIO(app)

def generate_frame():
    while True:
        # Ye camera frame ko read karta hai
        success, frame = camera.read()
        if not success:
            break
        else:
            # Frame ko JPEG format mein encode karta hai
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            
            # Frame ko stream ke liye yield karta hai varna vo sirf ek frame bhej dega
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/')
def index ():
    return render_template('index.html')

@app.route('/video')
def video():
    return Response(generate_frame(),mimetype='multipart/x-mixed-replace; boundary=frame')



if __name__ == '__main__':
    socketio.run(app, debug = True)