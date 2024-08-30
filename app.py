import os
from flask import Flask, render_template, request, jsonify, send_file
from googletrans import Translator
import pyttsx3
engine = pyttsx3.init()
from io import BytesIO
from translation import translation_bp


app = Flask(__name__)

app.config['SECRET_KEY'] = 'secret!'

app.register_blueprint(translation_bp, url_prefix='/translation')

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
    return render_template('videoapp.html')
    
@app.route('/translate', methods=['POST'])
def translate():
    data = request.json
    source_text = data.get('text')
    source_lang = data.get('source_lang')
    target_lang = data.get('target_lang')
    translated_text = translate_text(source_text, source_lang, target_lang)
    return jsonify({'translated_text': translated_text, 'audio_url': '/translation/audio'})

def translate_text(text, source_lang, target_lang):
    translator = Translator()
    result = translator.translate(text, src=source_lang, dest=target_lang)
    return result.text

@app.route('/text-to-speech', methods=['POST'])
def text_to_speech():
    text = request.form.get('text')
    if text:
        engine = pyttsx3.init()
        audio_file = BytesIO()
        engine.save_to_file(text, audio_file)
        engine.runAndWait()
        audio_file.seek(0)
        return send_file(audio_file, mimetype='audio/mp3', as_attachment=True, download_name='speech.mp3')
    return jsonify({'status': 'error', 'message': 'No text provided.'})

if __name__ == '__main__':
    if not os.path.exists('uploads'):
        os.makedirs('uploads')
    
    app.run(debug=True, host='0.0.0.0')