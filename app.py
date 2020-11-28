##########################################################################################################
# Import Dependencies
##########################################################################################################

from flask import Flask, jsonify

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect

import datetime as dt

##########################################################################################################
# Connect to Database
##########################################################################################################

engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)
session = Session(engine)

Measurement = Base.classes.measurement
Station = Base.classes.station

##########################################################################################################
# Flask Routes
##########################################################################################################

# start flask
app = Flask(__name__)

##########################################################################################################
# root route
##########################################################################################################
@app.route("/")
def home():
    return (
        f"Returns date and prcp for all records in the dataset:<br/>"
        f"http://127.0.0.1:5000//api/v1.0/precipitation<br/>"
        f"<br/>"
        f"Returns station and name for all records in the dataset:<br/>"
        f"http://127.0.0.1:5000//api/v1.0/stations<br/>"
        f"<br/>"
        f"Returns date and tobs for the most active station in the dataset over the last 12 months of the dates in the dataset:<br/>"
        f"http://127.0.0.1:5000//api/v1.0/tobs<br/>"
        f"<br/>"
        f'Enter the start date (YYYY-MM-DD) to retrieve the TMIN, TMAX, and TAVG for all dates after the start date. Example:<br/>'
        f"http://127.0.0.1:5000//api/v1.0/2016-01-01<br/>"
        f"<br/>"
        f'Enter the start date and end dates (YYYY-MM-DD). Example:<br/>'
        f"http://127.0.0.1:5000//api/v1.0/2016-01-01/2016-01-31"
    )

##########################################################################################################
# precipitation route
## Convert the query results to a dictionary using `date` as the key and `prcp` as the value.
##########################################################################################################
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

##########################################################################################################    
# station route 
## Return a JSON list of stations from the datase
##########################################################################################################
@app.route("/api/v1.0/stations")
def stations():

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

##########################################################################################################
# tobs route
## Query the dates and temperature observations of the most active station for the last year of data.
##########################################################################################################
@app.route("/api/v1.0/tobs")
def tobs():    

    session = Session(engine)

    # get the date from 12 months ago
    max_date_str = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    max_date = dt.datetime.strptime(max_date_str[0], '%Y-%m-%d')
    prior_year_date = dt.date(max_date.year -1, max_date.month, max_date.day)

    active_stations = session.query(Measurement.station,func.count(Measurement.id)).\
                        filter(Measurement.date >= prior_year_date).\
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

##########################################################################################################
# Start Date Route
## When given the start only, calculate `TMIN`, `TAVG`, and `TMAX` for all dates >= to the start date.
##########################################################################################################
@app.route("/api/v1.0/<start>")
def t_start(start):
    
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

##########################################################################################################
# Start Date/End Date Route
## When given start and end dates, calculate `TMIN`, `TAVG`, and `TMAX` for dates between start & end date
##########################################################################################################
@app.route("/api/v1.0/<start>/<end>")
def t_start_end(start,end):

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