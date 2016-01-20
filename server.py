from gevent import monkey
monkey.patch_all()

from flask import Flask, render_template
from flask.ext.socketio import SocketIO, emit
import os
import json
import pandas as pd
from plotleaders.utils import plot_to_div, write_templates
from plotleaders.components import write_controls
from plotleaders.components import graph
from collections import OrderedDict
from settings import APP_STATIC

app = Flask(__name__)
app.debug = True
app.config['key'] = 'secret'
socketio = SocketIO(app)
data = pd.read_csv(os.path.join(APP_STATIC, 'dataleaders.csv'))

var_leaders = data.columns[1:]
opts = OrderedDict()
for x in sorted(var_leaders):
    opts[x] = x
opts_null = opts.copy()
opts_null["*NoVariable*"] = '*No Variable*'
# Write the HTML "includes" blocks to /templates/runtime/Plotleaders
# Alternatively, include the HTML yourself in that folder
write_templates(
        {
            'controls': [write_controls(opts, opts_null)],

            'main_pane': [
                graph()
            ]
        }, __name__
)


def get_area(x_array, y_array):
    dist_x = max(x_array) - min(x_array)
    dist_y = max(y_array) - min(y_array)
    return dist_x * dist_y


@app.route('/')
def index():
    return render_template('layouts/layout.html',
                           app_name=__name__)


@socketio.on('replot')
def replot(app_state, data=data):
    x_var = data[app_state['x-axis']]
    y_var = data[app_state['y-axis']]
    print(app_state['z-axis'])
    if app_state['z-axis'] == '*NoVariable*':
        z_var = 'red'
    else:
        z_var = data[app_state['z-axis']]
    x_lims = [min(x_var) - 0.5, max(x_var) + 0.5]
    y_lims = [min(y_var) - 0.5, max(y_var) + 0.5]
    text = data["Leader Name"]
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
    layout = {'title': 'Perception of Leaders',
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
    print(div_content, js_content)
    message = json.dumps({'div_content': div_content, 'js_content': js_content})
    emit('postMessage', message)


if __name__ == "__main__":
    # Fetch the environment variable (so it works on Heroku):
    socketio.run(app, host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
    #socketio.run(app)