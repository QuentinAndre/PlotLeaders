from gevent import monkey

monkey.patch_all()

from flask import Flask, render_template
from flask.ext.socketio import SocketIO, emit
from collections import OrderedDict
from .utils import write_templates
from .components import write_controls
import os
import pandas as pd


app = Flask(__name__, instance_relative_config=True)
app.config.from_pyfile('config.py')
socketio = SocketIO(app)
data = pd.read_csv(os.path.join(os.path.dirname(__file__), 'static', 'dataleaders.csv'))

var_leaders = data.columns[1:]
opts = OrderedDict()
for x in sorted(var_leaders):
    opts[x] = x

opts_null = opts.copy()
opts_null["*NoVariable*"] = '*No Variable*'

write_templates(
        {
            'controls': [
                write_controls(opts, opts_null)
            ]
        }, __name__
)

from plotleaders import views