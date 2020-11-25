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
        f"Returns date and prcp for all records in the dataset:<br/>"
        f"http://127.0.0.1:5000//api/v1.0/precipitation<br/>"
        f"<br/>"
        f"Returns station and name for all records in the dataset:<br/>"
        f"http://127.0.0.1:5000//api/v1.0/stations<br/>"
        f"<br/>"
        f"Returns date and tobs for the most active station in the dataset:<br/>"
        f"http://127.0.0.1:5000//api/v1.0/tobs<br/>"
        f"<br/>"
        f'Enter the start date to retrieve the TMIN, TMAX, and TAVG for all dates after the start date:<br/>'
        f"http://127.0.0.1:5000//api/v1.0/YYYY-MM-DD<br/>"
        f"<br/>"
        f'Enter the start date and the end date:<br/>'
        f"http://127.0.0.1:5000//api/v1.0/YYYY-MM-DD/YYYY-MM-DD"
    )

# # precipitation

@app.route("/api/v1.0/precipitation")
def precipitation():
    """Convert the query results to a dictionary using `date` as the key and `prcp` as the value."""
    session = Session(engine)

    prcp_query =   session.query(Measurement.date, Measurement.prcp).\
                        order_by(Measurement.date).all()

    session.close()

    prcp_dict_list = []
    
    for date, prcp in prcp_query:
         prcp_dict = {}
         prcp_dict[date] = prcp
         prcp_dict_list.append(prcp_dict)

    return jsonify(prcp_dict_list)
    

@app.route("/api/v1.0/stations")
def stations():
    """Return a JSON list of stations from the dataset."""
    session = Session(engine)

    station_query =   session.query(Station.station, Station.name).\
                        order_by(Station.station).all()

    session.close()

    station_dict_list = []

    for station, name in station_query:
         station_dict = {}
         station_dict["station"] = station
         station_dict["name"] = name
         station_dict_list.append(station_dict)

    return jsonify(station_dict_list)


@app.route("/api/v1.0/tobs")
def tobs():
#     """Query the dates and temperature observations of the most active station for the last year of data."""

    session = Session(engine)

    active_stations = session.query(Measurement.station,\
                        func.count(Measurement.id)).\
                        group_by(Measurement.station).\
                        order_by(func.count(Measurement.date).desc()).all()
    
    station_id = active_stations[0][0]

    tobs_sel = [Measurement.date, Measurement.tobs]

    tobs_query = session.query(*tobs_sel).\
    filter(Measurement.station == station_id).all()

    session.close()

    tobs_dict_list = []

    for date, tobs in tobs_query:
         tobs_dict = {}
         tobs_dict["date"] = date
         tobs_dict["tobs"] = tobs
         tobs_dict_list.append(tobs_dict)

    return jsonify(tobs_dict_list)

    


@app.route("/api/v1.0/<start>")
def t_start(start):
# When given the start only, calculate `TMIN`, `TAVG`, and `TMAX` for all dates >= to the start date.
    
    session = Session(engine)

    t_start_sel = [func.min(Measurement.tobs),func.avg(Measurement.tobs),func.max(Measurement.tobs)]

    t_start_query = session.query(*t_start_sel).\
                        filter(Measurement.date >= start).all()
        
    session.close()

    t_start_dict_list = []

    for min, avg, max in t_start_query:
            t_start_dict = {}
            t_start_dict["Min"] = min
            t_start_dict["Average"] = avg
            t_start_dict["Max"] = max
            t_start_dict_list.append(t_start_dict)

    return jsonify(t_start_dict_list)


@app.route("/api/v1.0/<start>/<end>")
def t_start_end(start,end):
#  When given the start and the end date, calculate the `TMIN`, `TAVG`, and `TMAX` for dates between the start and end date inclusive."""

    session = Session(engine)

    t_start_end_sel = [func.min(Measurement.tobs),func.avg(Measurement.tobs),func.max(Measurement.tobs)]

    t_start_end_query = session.query(*t_start_end_sel).\
                    filter(Measurement.date >= start).\
                    filter(Measurement.date <= end).all()
        
    session.close()

    t_start_end_dict_list = []

    for min, avg, max in t_start_end_query:
            t_start_end_dict = {}
            t_start_end_dict["Min"] = min
            t_start_end_dict["Average"] = avg
            t_start_end_dict["Max"] = max
            t_start_end_dict_list.append(t_start_end_dict)

    return jsonify(t_start_end_dict_list)

if __name__ == "__main__":
    app.run(debug=True)