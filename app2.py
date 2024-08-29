import os
import ssl
import eventlet
from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO
from googletrans import Translator
from live_translation import live_translation_bp

app = Flask(__name__)
app.register_blueprint(live_translation_bp, url_prefix='/live-translation')
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

# Route definitions
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/sign-to-audio')
def sign_to_audio():
    return render_template('sign_to_audio.html')

@app.route('/audio-to-sign')
def audio_to_sign():
    return render_template('audio_to_sign.html')

@app.route('/translation')
def translation():
    return render_template('translation.html')

@app.route('/live-isl-audio')
def live_isl_audio():
    return render_template('live_isl_audio.html')

@app.route('/video-call')
def video_call():
    return render_template('video_call.html')

@app.route('/translate', methods=['POST'])
def translate():
    data = request.json
    source_text = data.get('text')
    source_lang = data.get('source_lang')
    target_lang = data.get('target_lang')
    translated_text = translate_text(source_text, source_lang, target_lang)
    return jsonify({'translated_text': translated_text})

def translate_text(text, source_lang, target_lang):
    translator = Translator()
    result = translator.translate(text, src=source_lang, dest=target_lang)
    return result.text

if __name__ == '__main__':
    if not os.path.exists('uploads'):
        os.makedirs('uploads')
    
    # SSL context setup
    ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    ssl_context.load_cert_chain(certfile='server.crt', keyfile='server.key')

    # Use eventlet's wrap_ssl to wrap the server socket
    eventlet_socket = eventlet.listen(('0.0.0.0', 5001))  # Changed port to 5001
    wrapped_socket = eventlet.wrap_ssl(eventlet_socket, certfile='server.crt', keyfile='server.key', server_side=True)

    # Run the server with the wrapped socket
    socketio.run(app, debug=True, host='0.0.0.0', port=5001, use_reloader=False, socket=wrapped_socket)