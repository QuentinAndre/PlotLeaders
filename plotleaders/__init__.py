from gevent import monkey

monkey.patch_all()

from flask import Flask, render_template
from flask.ext.socketio import SocketIO, emit
from collections import OrderedDict
from .utils import write_templates
from .components import write_controls
import os
import pandas as pd


app = Flask(__name__)
#DEBUG = False
#SECRET_KEY = "devkey"
#USERNAME = "admin"
#PASSWORD = "default"
socketio = SocketIO(app)
data = pd.read_csv(os.path.join(os.path.dirname(__file__), 'static', 'dataleaders.csv'))

var_leaders = data.columns[1:11]
opts = OrderedDict()
for x in sorted(var_leaders):
    opts[x] = x

opts_null = opts.copy()
opts_null["*NoVariable*"] = '*No Variable*'

cats = data["DetailedType"].unique()

write_templates(
        {
            'controls': [
                write_controls(cats, opts, opts_null)
            ]
        }, __name__
)

from plotleaders import views