
// Create an Audio object
let audio = new Audio();
audio.playbackRate = 2.0;
// Connect to the WebSocket server
const ws = new WebSocket('ws://landslide/ws');

// Handle connection open event
ws.onopen = () => {
    console.log('Connected to the WebSocket server');
};

// Handle incoming WebSocket messages
ws.onmessage = (event) => {
    // Parse the JSON message
    const message = JSON.parse(event.data);

    // Check if the message type is the one that should trigger audio playback
    if (message.event_type === 'wav_url') {
        console.log(message.wav_url)
        let audioUrl = message.wav_url;
        audio.src = audioUrl; // Set the source of the audio
        audio.play();         // Play the audio
    }
    else if (message.event_type === 'text') {
        console.log(message.text);
    }
};

// Handle connection close event
ws.onclose = () => {
    console.log('Disconnected from the WebSocket server');
};

// Handle WebSocket errors
ws.onerror = (error) => {
    console.error('WebSocket error:', error);
};
