let recordButton = document.getElementById("recordButton");
let stopButton = document.getElementById("stopButton");
let audioPlayback = document.getElementById("audioPlayback");

let recorder;
let audioStream;

recordButton.addEventListener("click", async () => {
    // Request access to the microphone
    audioStream = await navigator.mediaDevices.getUserMedia({ audio: true });
    recorder = new RecordRTC(audioStream, {
        type: 'audio',
        mimeType: 'audio/wav'
    });
    recorder.startRecording();
    recordButton.disabled = true;
    stopButton.disabled = false;
});

stopButton.addEventListener("click", async () => {
    stopButton.disabled = true;
    recorder.stopRecording(function() {
        let audioBlob = recorder.getBlob();

        // Check if blob is not null
        if (audioBlob) {
            audioPlayback.src = URL.createObjectURL(audioBlob);
            uploadAudio(audioBlob);
        } else {
            console.error('Recording failed or no data available.');
        }
    });
    recordButton.disabled = false;
    audioStream.getTracks().forEach(track => track.stop()); // Stop all tracks to release the microphone
});

function uploadAudio(blob) {
    let formData = new FormData();
    formData.append("audio", blob);

    fetch("/upload", {
        method: "POST",
        body: formData,
    })
    .then(response => response.json())
    .then(data => {
        console.log("Success:", data);
        if (data.transcript) {
            document.getElementById('transcript').innerText = 'Transcript: ' + data.transcript;
        } else {
            document.getElementById('transcript').innerText = 'No transcript available.';
        }
    })
    .catch((error) => {
        console.error("Error:", error);
        document.getElementById('transcript').innerText = 'Failed to retrieve transcript.';
    });
}
