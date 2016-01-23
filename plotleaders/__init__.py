from gevent import monkey

monkey.patch_all()

from flask import Flask
from flask.ext.socketio import SocketIO
from collections import OrderedDict
from .utils import write_templates, write_controls
import os
import pandas as pd

#Initializing the App and Socket
app = Flask(__name__)
socketio = SocketIO(app)

#Loading the data to be plotted later
data = pd.read_csv(os.path.join(os.path.dirname(__file__), 'static', 'dataleaders.csv'))

#Creating the variables
var_leaders = data.columns[1:11]
opts = OrderedDict()
for x in sorted(var_leaders):
    opts[x] = x

#Adding a "No Variable" option for the Z axis.
opts_null = opts.copy()
opts_null["*NoVariable*"] = '*No Variable*'

#Storing the categories of leaders
cats = data["DetailedType"].unique()

#Writing the template
write_templates(
        {
            'controls': [
                write_controls(cats, opts, opts_null)
            ]
        }, __name__
)

from plotleaders import views