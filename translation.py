import os
from flask import Blueprint, request, jsonify, send_file
from googletrans import Translator
from gtts import gTTS
from io import BytesIO
import uuid

translation_bp = Blueprint('translation', __name__)

@translation_bp.route('/translate', methods=['POST'])
def translate():
    data = request.json
    source_text = data.get('text')
    source_lang = data.get('source_lang')
    target_lang = data.get('target_lang')
    
    translator = Translator()
    translated = translator.translate(source_text, src=source_lang, dest=target_lang)
    translated_text = translated.text
    
    # Convert translated text to audio
    tts = gTTS(translated_text, lang=target_lang)
    audio_file = BytesIO()
    tts.write_to_fp(audio_file)
    audio_file.seek(0)
    
    # Ensure the temp_audio directory exists
    if not os.path.exists('temp_audio'):
        os.makedirs('temp_audio')
    
    # Save the audio file to a temporary location
    audio_filename = f"{uuid.uuid4()}.mp3"
    audio_path = os.path.join('temp_audio', audio_filename)
    with open(audio_path, 'wb') as f:
        f.write(audio_file.read())
    
    return jsonify({
        'translated_text': translated_text,
        'audio_url': f'/translation/audio/{audio_filename}'
    })

@translation_bp.route('/audio/<filename>')
def audio(filename):
    audio_path = os.path.join('temp_audio', filename)
    return send_file(audio_path, mimetype='audio/mp3')