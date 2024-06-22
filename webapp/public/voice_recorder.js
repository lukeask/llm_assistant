let constraintObj = { 
    audio: true, 
    video: false
}; 

if (navigator.mediaDevices === undefined) {
    navigator.mediaDevices = {};
    navigator.mediaDevices.getUserMedia = function(constraintObj) {
        let getUserMedia = navigator.webkitGetUserMedia || navigator.mozGetUserMedia;
        if (!getUserMedia) {
            return Promise.reject(new Error('getUserMedia is not implemented in this browser'));
        }
        return new Promise(function(resolve, reject) {
            getUserMedia.call(navigator, constraintObj, resolve, reject);
        });
    }
} else {
    navigator.mediaDevices.enumerateDevices()
    .then(devices => {
        devices.forEach(device => {
            console.log(device.kind.toUpperCase(), device.label);
        })
    })
    .catch(err => {
        console.log(err.name, err.message);
    });
}

navigator.mediaDevices.getUserMedia(constraintObj)
.then(function(mediaStreamObj) {
    let start = document.getElementById('btnStart');
    let stop = document.getElementById('btnStop');
    let vidSave = document.getElementById('vid2');
    
    // CHANGED: Set MIME type for MediaRecorder to 'video/webm;codecs=opus'
    let mediaRecorder = new MediaRecorder(mediaStreamObj, { mimeType: 'video/webm; codecs=opus' });
    let chunks = [];
    let recording = false;
    let intervalId;
    
    start.addEventListener('click', (ev) => {
        mediaRecorder.start();
        recording = true;
        console.log(mediaRecorder.state);

        intervalId = setInterval(() => {
            if (!recording) {
                clearInterval(intervalId);
                return;
            }

            mediaRecorder.stop();
            mediaRecorder.start();
            
            console.log('2 seconds passed');
        }, 2000); 
    });

    stop.addEventListener('click', (ev) => {
        mediaRecorder.stop();
        recording = false;
        clearInterval(intervalId);
        console.log(mediaRecorder.state);
    });

    mediaRecorder.ondataavailable = function(ev) {
        chunks.push(ev.data);
        console.log(chunks.length)
    };

    mediaRecorder.onstop = (ev) => {
        // CHANGED: Update the blob type to 'video/webm; codecs=opus'
        let blob = new Blob(chunks, { 'type': 'video/webm; codecs=opus' });
        chunks = [];

        let audioURL = window.URL.createObjectURL(blob);
        vidSave.src = audioURL;

        let formData = new FormData();
        // CHANGED: Update the file extension to 'audio.webm'
        formData.append('file', blob, 'audio.webm');

        fetch('http://landslide:8008/uploads', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => console.log(data))
        .catch(error => console.error(error));
    };
}).catch(function(err) { 
    console.log(err.name, err.message); 
});