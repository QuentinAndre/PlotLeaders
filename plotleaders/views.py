from plotleaders import app, socketio, data
from flask import render_template, url_for
from flask.ext.socketio import emit
import json
from .utils import get_area, plot_to_div


@app.route('/')
def index():
    return render_template('layouts/app.html',
                           app_name=__name__)


@app.route('/faq/')
def faq():
    return render_template('layouts/faq.html')


@app.route('/survey/')
def survey():
    return render_template('layouts/survey.html')


@socketio.on('replot')
def replot(app_state, data=data):
    scope = app_state['leadtype']
    if scope == "both":
        d = data
    elif scope == "real":
        d = data[data["Type"] == "Real"]
    else:
        d = data[data["Type"] == "Fictitious"]
    x_var = d[app_state['x-axis']]
    y_var = d[app_state['y-axis']]
    if app_state['z-axis'] == '*NoVariable*':
        z_var = 'red'
        title = ""
    else:
        z_var = d[app_state['z-axis']]
        title = "Blue: Least {}, Red: Most {}".format(app_state['z-axis'], app_state['z-axis'])
    x_lims = [min(x_var) - 0.5, max(x_var) + 0.5]
    y_lims = [min(y_var) - 0.5, max(y_var) + 0.5]
    text = d["Leader Name"]
    trace = [{
        'x': x_var,
        'y': y_var,
        'fillcolor': z_var,
        'text': text,
        'mode': 'markers+text',
        'marker': {'color': z_var,
                   'size': 8,
                   'colorscale': 'Bluered'},
        'hoverinfo': 'text',
        'textfont': {'size': 8},
        'textposition': 'top'
    }]
    layout = {'title': title,
              'xaxis': {
                  'title': app_state['x-axis'],
                  'titlefont': {
                      'size': 18,
                      'color': '#7f7f7f'
                  },
                  'range': x_lims,
                  'showgrid': False,
                  'showline': False
              },
              'yaxis': {
                  'title': app_state['y-axis'],
                  'titlefont': {
                      'size': 18,
                      'color': '#7f7f7f'
                  },
                  'range': y_lims,
                  'showgrid': False,
                  'showline': False
              }
              }
    area = get_area(x_var, y_var)
    resize_js = "adjustSize({:.2f})".format(area)
    div_content, js_content = plot_to_div({'data': trace, 'layout': layout}, plotdivid='PlotLeaders',
                                          added_js=resize_js)
    message = json.dumps({'div_content': div_content, 'js_content': js_content})
    emit('postMessage', message)
