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

(function (i, s, o, g, r, a, m) {
    i['GoogleAnalyticsObject'] = r;
    i[r] = i[r] || function () {
            (i[r].q = i[r].q || []).push(arguments)
        }, i[r].l = 1 * new Date();
    a = s.createElement(o),
        m = s.getElementsByTagName(o)[0];
    a.async = 1;
    a.src = g;
    m.parentNode.insertBefore(a, m)
})(window, document, 'script', '//www.google-analytics.com/analytics.js', 'ga');

ga('create', 'UA-72773152-1', 'auto');
ga('send', 'pageview');



