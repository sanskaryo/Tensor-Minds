from flask import Blueprint, render_template, request, jsonify
from googletrans import Translator
import speech_recognition as sr
import os

live_translation_bp = Blueprint('live_translation', __name__)

@live_translation_bp.route('/live-translation')
def live_translation():
    return render_template('live_translation.html')

@live_translation_bp.route('/speech-to-text', methods=['POST'])
def speech_to_text():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'})
    
    # Save the file
    file_path = os.path.join('uploads', file.filename)
    file.save(file_path)
    
    # Convert audio to text
    recognizer = sr.Recognizer()
    with sr.AudioFile(file_path) as source:
        audio_data = recognizer.record(source)
        text = recognizer.recognize_google(audio_data)
    
    # Translate text
    target_lang = request.form.get('target_lang', 'en')
    translated_text = translate_text(text, 'auto', target_lang)
    
    return jsonify({'text': text, 'translated_text': translated_text})

def translate_text(text, source_lang, target_lang):
    translator = Translator()
    result = translator.translate(text, src=source_lang, dest=target_lang)
    return result.text