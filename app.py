#####################################################
# Import Dependencies
#####################################################

from flask import Flask, jsonify

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect

#####################################################
# Connect to Database
#####################################################

engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)
session = Session(engine)

Measurement = Base.classes.measurement
Station = Base.classes.station

#####################################################
# Flask Routes
#####################################################

# start flask
app = Flask(__name__)

@app.route("/")
def home():
    return (
        f"All Available Routes:<br/>"
        f"-----------------------------------------------------<br/>"
        f"http://127.0.0.1:5000//api/v1.0/precipitation<br/>"
        f"http://127.0.0.1:5000//api/v1.0/stations<br/>"
        f"http://127.0.0.1:5000//api/v1.0/tobs<br/>"
        f"http://127.0.0.1:5000//api/v1.0/[start]<br/>"
        f"http://127.0.0.1:5000//api/v1.0/[start]/[end]"
    )

# # precipitation

@app.route("/api/v1.0/precipitation")
def precipitation():
    """Convert the query results to a dictionary using `date` as the key and `prcp` as the value."""
    session = Session(engine)

    prcp_query =   session.query(Measurement.date, Measurement.prcp).order_by(Measurement.date).all()

    prcp_dict_list = []
    
    for date, prcp in prcp_query:
         prcp_dict = {}
         prcp_dict[date] = prcp
         prcp_dict_list.append(prcp_dict)

    return jsonify(prcp_dict_list)

    session.close()
    

@app.route("/api/v1.0/stations")
def stations():
    """Return a JSON list of stations from the dataset."""
    session = Session(engine)

    station_query =   session.query(Station.station, Station.name).order_by(Station.station).all()

    station_dict_list = []

    for station, name in station_query:
         station_dict = {}
         station_dict["Station"] = station
         station_dict["Name"] = name
         station_dict_list.append(station_dict)

    return jsonify(station_dict_list)

    session.close()


# @app.route("/api/v1.0/tobs")
# def tobs():
#     """Query the dates and temperature observations of the most active station for the last year of data."""

#     return jsonify(tobs_dict)


# @app.route("/api/v1.0/<start>")
# def start_date():
#     """When given the start only, calculate `TMIN`, `TAVG`, and `TMAX` for all dates greater than and equal to the start date."""
   

# @app.route("/api/v1.0/<start>/<end>")
# def end_date():
#     """When given the start and the end date, calculate the `TMIN`, `TAVG`, and `TMAX` for dates between the start and end date inclusive."""

if __name__ == "__main__":
    app.run(debug=True)