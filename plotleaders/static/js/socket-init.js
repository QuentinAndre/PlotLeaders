/**
 * Created by Quentin ANDRE on 17/01/2016.
 */

var socket = io.connect(window.location.protocol + '//' + document.domain + ':' + location.port);

$(document).ready(function () {

    // Sockets
    //

    namespace = ''; // change to an empty string to use the global namespace

    // the socket.io documentation recommends sending an explicit package upon connection
    // this is specially important when using the global namespace

    socket.on('connect', function () {
        socket.emit('my event', {data: 'I\'m connected!'});
    });

    socket.on('postMessage', function (msg_string) {
        var msgs = JSON.parse(msg_string);
        document.getElementById("plot_content").innerHTML = msgs.div_content;
        window.eval(msgs.js_content);
    });
});



