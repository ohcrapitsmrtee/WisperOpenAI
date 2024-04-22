import os
print(os.environ['PATH'])  # Check current PATH
os.environ['PATH'] += ";C:\\Users\\j\\ffmpeg-master-latest-win64-gpl\\bin"  # Append FFmpeg bin directory
