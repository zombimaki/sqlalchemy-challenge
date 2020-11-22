#####################################################
# Climate App
#####################################################

# import dependencies
from flask import Flask, jsonify

app = Flask(__name__)

#####################################################
# Dictionaries
#####################################################


#####################################################
# Flask Routes
#####################################################

@app.route("/")
def home():
    return "This is Home"

# precipitation

@app.route("/api/v1.0/precipitation")
def precipitation():
    """Convert the query results to a dictionary using `date` as the key and `prcp` as the value."""

    return jsonify(precipitation_dict)


@app.route("/api/v1.0/stations")
def stations():
    """Return a JSON list of stations from the dataset."""

    return jsonify(stations_dict)


@app.route("/api/v1.0/tobs")
def tobs():
    """Query the dates and temperature observations of the most active station for the last year of data."""

    return jsonify(tobs_dict)


@app.route("/api/v1.0/<start>")
def start_date():
    """When given the start only, calculate `TMIN`, `TAVG`, and `TMAX` for all dates greater than and equal to the start date.
   

@app.route("/api/v1.0/<start>/<end>")
def end_date():
    """When given the start and the end date, calculate the `TMIN`, `TAVG`, and `TMAX` for dates between the start and end date inclusive."""

