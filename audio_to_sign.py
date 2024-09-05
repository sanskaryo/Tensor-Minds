import speech_recognition as sr
import os
import string
from flask import Flask, jsonify

app = Flask(__name__)

# Paths for ISL GIFs and letter images
ISL_GIF_PATH = 'static/ISL_Gifs'
LETTER_IMG_PATH = 'static/letters'

# ISL phrases available as GIFs
isl_gif = [
    'any questions', 'are you angry', 'are you busy', 'are you hungry', 'are you sick', 'be careful',
    'can we meet tomorrow', 'did you book tickets', 'did you finish homework', 'do you go to office', 'do you have money',
    'do you want something to drink', 'do you want tea or coffee', 'do you watch TV', 'dont worry', 'flower is beautiful',
    'good afternoon', 'good evening', 'good morning', 'good night', 'good question', 'had your lunch', 'happy journey',
    'hello what is your name', 'how many people are there in your family', 'i am a clerk', 'i am bore doing nothing',
    'i am fine', 'i am sorry', 'i am thinking', 'i am tired', 'i dont understand anything', 'i go to a theatre', 'i love to shop',
    'i had to say something but i forgot', 'i have headache', 'i like pink colour', 'i live in nagpur', 'lets go for lunch', 'my mother is a homemaker',
    'my name is john', 'nice to meet you', 'no smoking please', 'open the door', 'please call me later',
    'please clean the room', 'please give me your pen', 'please use dustbin dont throw garbage', 'please wait for sometime', 'shall I help you',
    'shall we go together tommorow', 'sign language interpreter', 'sit down', 'stand up', 'take care', 'there was traffic jam', 'wait I am thinking',
    'what are you doing', 'what is the problem', 'what is todays date', 'what is your father do', 'what is your job',
    'what is your mobile number', 'what is your name', 'whats up', 'when is your interview', 'when we will go', 'where do you stay',
    'where is the bathroom', 'where is the police station', 'you are wrong', 'address', 'agra', 'ahemdabad', 'all', 'april', 'assam', 'august', 'australia', 'badoda', 'banana', 'banaras', 'banglore',
    'bihar', 'bridge', 'cat', 'chandigarh', 'chennai', 'christmas', 'church', 'clinic', 'coconut', 'crocodile', 'dasara',
    'deaf', 'december', 'deer', 'delhi', 'dollar', 'duck', 'febuary', 'friday', 'fruits', 'glass', 'grapes', 'gujrat', 'hello',
    'hindu', 'hyderabad', 'india', 'january', 'jesus', 'job', 'july', 'karnataka', 'kerala', 'krishna', 'litre', 'mango',
    'may', 'mile', 'monday', 'mumbai', 'museum', 'muslim', 'nagpur', 'october', 'orange', 'pakistan', 'pass', 'police station',
    'post office', 'pune', 'punjab', 'rajasthan', 'ram', 'restaurant', 'saturday', 'september', 'shop', 'sleep', 'southafrica',
    'story', 'sunday', 'tamil nadu', 'temperature', 'temple', 'thursday', 'toilet', 'tomato', 'town', 'tuesday', 'usa', 'village',
    'voice', 'wednesday', 'weight', 'please wait for sometime', 'what is your mobile number', 'what are you doing', 'are you busy'
]

def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        print("I am Listening")
        audio = recognizer.listen(source)
        try:
            text = recognizer.recognize_google(audio).lower().translate(str.maketrans('', '', string.punctuation))
            print('You Said: ' + text)
            return text
        except sr.UnknownValueError:
            print("Could not understand audio")
        except sr.RequestError as e:
            print(f"Could not request results; {e}")
        return None

def get_gif_path(text):
    if text in isl_gif:
        gif_file = os.path.join(ISL_GIF_PATH, f'{text}.gif')
        if os.path.exists(gif_file):
            return gif_file
    return None

def get_letter_image_paths(text):
    image_paths = []
    for char in text:
        if char in string.ascii_lowercase:
            image_file = os.path.join(LETTER_IMG_PATH, f'{char}.jpg')
            if os.path.exists(image_file):
                image_paths.append(image_file)
    return image_paths

@app.route('/recognize_speech')
def handle_recognition():
    spoken_text = recognize_speech()
    if spoken_text:
        gif_path = get_gif_path(spoken_text)
        letter_image_paths = get_letter_image_paths(spoken_text)
        return jsonify({
            'gif_path': gif_path,
            'letter_image_paths': letter_image_paths
        })
    return jsonify({
        'error': 'No speech recognized or no matching GIF/letters found.'
    })

if __name__ == "__main__":
    app.run(debug=True)
