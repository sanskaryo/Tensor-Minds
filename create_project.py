import os

# Define the project structure
project_structure = {
    "project_root": {
        "app.py": "# Flask app entry point\n",
        "static": {
            "css": {
                "styles.css": "/* Stylesheet for the website */\n"
            },
            "js": {
                "scripts.js": "// JavaScript for the website\n"
            }
        },
        "templates": {
            "base.html": "<!-- Base template for all pages -->\n",
            "index.html": "<!-- Homepage template -->\n",
            "sign_to_audio.html": "<!-- Sign Language Keyboard to Audio page -->\n",
            "audio_to_sign.html": "<!-- Audio/Text to ISL page -->\n",
            "translation.html": "<!-- Real-Time Vernacular Translation page -->\n",
            "live_isl_audio.html": "<!-- Live ISL to Audio Translation page -->\n",
            "video_call.html": "<!-- Video Call & Chat Rooms page -->\n"
        },
        "sign_to_audio.py": "# Python script for ISL Keyboard to Audio\n",
        "audio_to_sign.py": "# Python script for Audio to Sign\n",
        "translation.py": "# Python script for Real-Time Translation\n",
        "live_isl_audio.py": "# Python script for Live ISL to Audio\n",
        "video_call.py": "# Python script for Video Call & Chat\n"
    }
}

def create_project_structure(base_path, structure):
    for name, content in structure.items():
        path = os.path.join(base_path, name)
        if isinstance(content, dict):
            os.makedirs(path, exist_ok=True)
            create_project_structure(path, content)
        else:
            with open(path, 'w') as file:
                file.write(content)

if __name__ == "__main__":
    base_path = "project_root"
    create_project_structure(base_path, project_structure)
    print(f"Project structure created at {os.path.abspath(base_path)}")
