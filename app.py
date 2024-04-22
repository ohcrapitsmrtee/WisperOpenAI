from flask import Flask, request, jsonify,render_template
import os
from pathlib import Path
import whisper

app = Flask(__name__)
@app.route('/')
def index():
    return render_template('index.html')


UPLOAD_FOLDER = './uploads'
Path(UPLOAD_FOLDER).mkdir(exist_ok=True)

model = whisper.load_model("base")  # Loads the base Whisper model, consider using "small" for faster performance but less accuracy

@app.route('/upload', methods=['POST'])
def upload_audio():
    if 'audio' not in request.files:
        return jsonify({'message': 'No file part'}), 400
    file = request.files['audio']
    if file.filename == '':
        return jsonify({'message': 'No selected file'}), 400
    if file:
        filepath = os.path.join(UPLOAD_FOLDER, 'audio.wav')
        file.save(filepath)
        transcript = transcribe_audio(filepath)
        return jsonify({'transcript': transcript}), 200

def transcribe_audio(audio_path):
    audio = whisper.load_audio(audio_path)
    audio = whisper.pad_or_trim(audio)
    mel = whisper.log_mel_spectrogram(audio).to(model.device)
    options = whisper.DecodingOptions()
    result = whisper.decode(model, mel, options)
    return result.text

if __name__ == '__main__':
    app.run(debug=True)
