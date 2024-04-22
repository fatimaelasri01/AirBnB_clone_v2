"""start Flask web app and fetches db from storage engine"""
from flask import Flask, render_template
from models import *
from models import storage
app = Flask(__name__)


@app.route('/hbnb', strict_slashes=False)
def hbnb():
    """display a HTML page like 8-index.html on /hbnb"""
    states = storage.all("State").values()
    amenities = storage.all("Amenity").values()
    places = storage.all(Place).values()
    return render_template('100-hbnb.html', states=states,
                           amenities=amenities)

@app.teardown_appcontext
def teardown_db(exception):
    """closes session"""
    storage.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000')