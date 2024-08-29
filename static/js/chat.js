$(document).ready(function() {
    var socket = io();

    $('#send').click(function() {
        var message = $('#message').val();
        socket.send(message);
        $('#message').val('');
    });

    socket.on('message', function(msg) {
        $('#chat-box').append('<div>' + msg + '</div>');
    });
});