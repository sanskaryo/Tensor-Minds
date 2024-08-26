from flask import Flask, render_template, request, jsonify
from googletrans import Translator

app = Flask(__name__)

def translate_text(text, source_lang, target_lang):
    translator = Translator()
    result = translator.translate(text, src=source_lang, dest=target_lang)
    return result.text

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/translate', methods=['POST'])
def translate():
    data = request.json
    source_text = data.get('text')
    source_lang = data.get('source_lang')
    target_lang = data.get('target_lang')
    translated_text = translate_text(source_text, source_lang, target_lang)
    return jsonify({'translated_text': translated_text})

if __name__ == '__main__':
    app.run(debug=True)










# # Python script for Real-Time Translation
# from flask import Flask, request, jsonify
# from google.cloud import speech_v1p1beta1 as speech
# from google.cloud import translate_v2 as translate
# import io

# app = Flask(__name__)

# @app.route('/translate', methods=['POST'])
# def translate_audio():
#     audio_file = request.files['audio']
#     input_lang = request.form['input_lang']
#     output_lang = request.form['output_lang']

#     # Convert audio to text
#     client = speech.SpeechClient()
#     audio = speech.RecognitionAudio(content=audio_file.read())
#     config = speech.RecognitionConfig(
#         encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
#         sample_rate_hertz=16000,
#         language_code=input_lang
#     )

#     response = client.recognize(config=config, audio=audio)
#     text = response.results[0].alternatives[0].transcript

#     # Translate text
#     translate_client = translate.Client()
#     translation = translate_client.translate(text, target_language=output_lang)

#     return jsonify({'translation': translation['translatedText']})

# if __name__ == '__main__':
#     app.run(debug=True)