"""start Flask web app and fetches db from storage engine"""
from flask import Flask, render_template
from models import *
from models import storage
app = Flask(__name__)


@app.route('/states', strict_slashes=False)
@app.route('/states/<state_id>', strict_slashes=False)
def states(id=None):
    """display the states and cities sorted by name"""
    states = storage.all("State")
    if id is not None:
        id = 'State.' + id
    return render_template('9-states.html', states=states, id=id)


@app.teardown_appcontext
def teardown_db(exception):
    """closes session"""
    storage.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000')