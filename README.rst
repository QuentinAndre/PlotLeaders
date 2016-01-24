.. highlight:: sh
=============
 Introduction
=============

:Date: January 24, 2016
:Version: 1.0.0
:Authors: Quentin ANDRE, quentin.andre@insead.edu
:Web site: https://github.com/QuentinAndre/Plotleaders
:Copyright: This document has been placed in the public domain.
:License: Plotleaders is released under the MIT license.

Purpose
=======

Plot-Leaders is a minimalist web app built with Flask, Socketio, Plotly and Bootstrap. It aims at vizualizing the
results of a current research project lead by Quentin ANDRE and David Dubois, on people's perceptions of leaders.

Content
=======

The organization of the folders is typical of a Flask web app:
 * The root folders contains the licensing information and the deployement files.
 * The plotleaders folder contains:
  * The python files used to initialize the app and render the views.
  * Templates/Layout: The Flask templates used to generate the views
  * Static: The JS and CSS files, as well as the data used to generate the plots.

Installation
============

Dependencies
------------
This code has been tested in Python 3.4.1, and the dependencies are listed in the requirements.txt file.

Download
--------

* Using git:
 * git clone https://github.com/QuentinAndre/Plotleaders.git

* Download the master branch as a zip:
 * https://github.com/QuentinAndre/Plotleaders/archive/master.zip

