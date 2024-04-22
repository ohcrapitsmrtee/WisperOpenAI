import datetime 
import whisper
import os

# Append FFmpeg bin directory to PATH
#os.environ['PATH'] += ";C:\\Users\\j\\ffmpeg-master-latest-win64-gpl\\bin"

try:
    model = whisper.load_model('base.en')
    print("Model loaded successfully.")
except Exception as e:
    print(f"Failed to load model: {e}")
    exit(1)


model = whisper.load_model('base.en')
whisper.DecodingOptions(language='en', fp16=False)
audio_file_path = r"C:\Users\j\Downloads\Create A Google Cloud Speech-To-Text Desktop App With Python.mp4"
result = model.transcribe(audio_file_path)
transcription_text = result["text"]
if not os.path.exists(audio_file_path):
    print(f"File not found: {audio_file_path}")
    exit(1)

save_target = "Google StoT Jie.vtt"
with open(save_target, 'w', encoding='utf-8') as file:
    file.write("WEBVTT\n\n")  # VTT files start with WEBVTT identifier
    for index, segment in enumerate(result['segments']):
        start = str(datetime.timedelta(seconds=segment['start'])).replace('.', ',')
        end = str(datetime.timedelta(seconds=segment['end'])).replace('.', ',')
        file.write(f"{index+1}\n")
        file.write(f"{start} --> {end}\n")  # Corrected syntax
        file.write(segment['text'].strip() + '\n')
        file.write('\n')


