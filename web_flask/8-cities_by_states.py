#!/usr/bin/python3
"""start Flask web app and fetches db from storage engine"""

from flask import Flask, render_template
from models import *
from models import storage
app = Flask(__name__)


@app.route('/cities_by_states', strict_slashes=False)
def cities_by_states():
    """lists states from storage engine sorted by name"""
    states = storage.all("State").values()
    return render_template('8-cities_by_states.html', states=states)


@app.teardown_appcontext
def teardown_db(exception):
    """closes session"""
    storage.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000')