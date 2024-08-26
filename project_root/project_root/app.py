from flask import Flask, render_template, request, jsonify
from googletrans import Translator
from live_translation import live_translation_bp
import os

app = Flask(__name__)
app.register_blueprint(live_translation_bp, url_prefix='/live-translation')

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
    app.run(debug=True)