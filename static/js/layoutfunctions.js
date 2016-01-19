$(document).ready(function () {

    // Record and send the state when inputs change
    $('input, select').each(function (i, obj) {
        if (obj.type === "checkbox" || obj.type === "radio") {
            $(obj).change(function () {
                console.log(getState());
                sendState({}, {});
            });
        } else {
            obj.oninput = function () {
                if ($(obj).hasClass("show-output")) {
                    $('output[for=' + obj.name + ']')[0].value = obj.value;
                }
                console.log(getState());
                sendState({}, {});
            };
        }
    });
});

function getState(payload) {
    var payload = payload || {};
    $('input').each(function (i, el) {
        if (el.type === "radio") {
            var value = $('input[name=' + el.name + ']:checked').val();
            if (typeof value === "undefined") {
                value = null;
            }
            payload[el.name] = value;
        } else if (el.type === "checkbox") {
            payload[el.name] = $(el).is(':checked');
        } else if (el.type === "text") {
            payload[el.name] = el.value;
        } else {
            payload[el.name] = el.value;
        }
    });
    $('select').each(function (i, el) {
        payload[el.name] = el.value;
    });
    return payload;
};

function sendState(that, payload) {
    var payload = payload || {};
    payload = getState(payload);
    socket.emit('replot', payload);
};

function adjustSize(area) {
    $('#PlotLeaders').bind('plotly_relayout', function (event, eventdata) {
        var x0 = eventdata['xaxis.range[0]'];
        var x1 = eventdata['xaxis.range[1]'];
        var y0 = eventdata['yaxis.range[0]'];
        var y1 = eventdata['yaxis.range[1]'];
        var scaling = area / ((x1 - x0) * (y1 - y0));
        var factorscale = 8 + Math.log(scaling) * 1.2;
        var newpars = {
            'marker.size': factorscale,
            'textfont.size': factorscale
        };
        Plotly.restyle(this, newpars);
    });
};

