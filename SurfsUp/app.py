import numpy as np
import datetime as dt

# import Flask
from flask import Flask, jsonify

#import SQLalchemy dependencies
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

# databease setup
engine = create_engine("sqlite:///../Resources/hawaii.sqlite")

# reflect existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)

#assign each class to a variable
measurement = Base.classes.measurement
Station = Base.classes.station


# create an app
app = Flask(__name__)


# start homepage
@app.route("/")
def home():
    return (
        f"Available Routes:<br/>"
        f"<strong>/api/v1.0/precipitation</strong><br/>"
        f"<strong>/api/v1.0/stations</strong><br/>"
        f"<strong>/api/v1.0/tobs</strong><br/>"
        f"<strong>/api/v1.0/start</strong>  (REPLACE START WITH ACTUAL DATE - MUST FORMAT: yyyy-mm-dd) <br/>"
        f"<strong>/api/v1.0/start/end</strong>  (REPLACE START WITH ACTUAL DATE - MUST FORMAT: yyyy-mm-dd/yyyy-mm-dd)")

@app.route("/api/v1.0/precipitation")
def precipitation():
    """Return precipitation data for the last 12 months as json"""
    #start session
    session = Session(engine)

    # query precipitation results from the last 12 months
    precipitation = session.query(measurement.date, measurement.prcp).\
        filter(measurement.date.between('2016-08-23', '2017-08-23')).all()

    session.close()

    # convert query results into a dictionary
    # 'date' = key , 'prcp' = value
    prcp_data = []
    for date, prcp in precipitation:
        prcp_dict = {}
        prcp_dict[date] = prcp
        prcp_data.append(prcp_dict)

    return jsonify(prcp_data)


@app.route("/api/v1.0/stations")
def stations():
    """Return a JSON list of stations from the dataset"""
    #start session
    session = Session(engine)

    # query to get list of station info
    station_data = session.query(Station.station, Station.name, Station.latitude, Station.longitude, Station.elevation).all()

    session.close()

    all_stations = []
    for station, name, latitude, longitude, elevation in station_data:
        station_dict = {}
        station_dict["station"] = station
        station_dict["name"] = name
        station_dict["latitude"] = latitude
        station_dict["longitude"] = longitude
        station_dict["elevation"] = elevation
        all_stations.append(station_dict)

    return jsonify(all_stations)


@app.route("/api/v1.0/tobs")
def tobs():
    """Return a JSON list of temperatures observations for the previous year using the most-active station"""
    # start session
    session = Session(engine)

    # query the dates and temperature observations of the most-active station for the previous year of data
    temperature = session.query(measurement.date, measurement.tobs).filter(measurement.station == 'USC00519281').\
        filter(measurement.date.between('2016-08-23', '2017-08-23')).all()

    session.close()

    all_temps = []
    for date, tobs in temperature:
        temp_dict = {}
        temp_dict[date] = tobs
        all_temps.append(temp_dict)

    return jsonify(all_temps)

@app.route("/api/v1.0/<start>")
@app.route("/api/v1.0/<start>/<end>")
def date(start, end=None):

    session = Session(engine)
    # if start and end date is given

    start = dt.datetime.strptime(start, '%Y-%m-%d')
    end = dt.datetime.strptime(end, '%Y-%m-%d')

    
    if not end: 
        start_date = session.query(func.min(measurement.tobs),func.max(measurement.tobs),func.avg(measurement.tobs)).\
        filter(measurement.date.between(start, end)).all()
        

    #if no end date is given
    else:

        start_date = session.query(func.min(measurement.tobs),func.max(measurement.tobs),func.avg(measurement.tobs)).\
        filter(measurement.date >= start).all()
        
        
        #filter(measurement.date.between(start, end)).all()

    
    session.close()
    

    date_list = []
    for min, max, avg in start_date:
        date_dict = {}
        date_dict['min_temp'] = min
        date_dict['max_temp'] = max
        date_dict['avg_temp'] = avg

        date_list.append(date_dict)

        return jsonify(date_list)
    


        
if __name__ == '__main__':
    app.run(debug=True)






