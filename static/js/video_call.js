const localVideo = document.getElementById('localVideo');
const remoteVideo = document.getElementById('remoteVideo');
const socket = io();

let localStream;
let peerConnection;
const config = {
    iceServers: [
        { urls: 'stun:stun.l.google.com:19302' }
    ]
};

navigator.mediaDevices.getUserMedia({ video: true, audio: true })
    .then(stream => {
        localVideo.srcObject = stream;
        localStream = stream;
        socket.emit('join', 'room1');
    })
    .catch(error => console.error('Error accessing media devices.', error));

socket.on('offer', (data) => {
    const { id, description } = data;
    peerConnection = new RTCPeerConnection(config);
    peerConnection
        .setRemoteDescription(description)
        .then(() => peerConnection.createAnswer())
        .then(sdp => peerConnection.setLocalDescription(sdp))
        .then(() => {
            socket.emit('answer', { id, description: peerConnection.localDescription, room: 'room1' });
        });
    peerConnection.ontrack = event => {
        remoteVideo.srcObject = event.streams[0];
    };
    localStream.getTracks().forEach(track => peerConnection.addTrack(track, localStream));
});

socket.on('answer', (data) => {
    const { description } = data;
    peerConnection.setRemoteDescription(description);
});

socket.on('candidate', (data) => {
    const { candidate } = data;
    peerConnection.addIceCandidate(new RTCIceCandidate(candidate));
});

socket.on('ready', () => {
    peerConnection = new RTCPeerConnection(config);
    peerConnection.onicecandidate = event => {
        if (event.candidate) {
            socket.emit('candidate', { candidate: event.candidate, room: 'room1' });
        }
    };
    peerConnection.ontrack = event => {
        remoteVideo.srcObject = event.streams[0];
    };
    localStream.getTracks().forEach(track => peerConnection.addTrack(track, localStream));
    peerConnection.createOffer()
        .then(sdp => peerConnection.setLocalDescription(sdp))
        .then(() => {
            socket.emit('offer', { id: socket.id, description: peerConnection.localDescription, room: 'room1' });
        });
});