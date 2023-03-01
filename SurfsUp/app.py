import numpy as np

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
Measurement = Base.classes.measurement
Station = Base.classes.station


# create an app
app = Flask(__name__)


# start homepage
@app.route("/")
def home():
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>")

@app.route("/api/v1.0/precipitation")
def precipitation():
    #start session
    session = Session(engine)

    # query precipitation results from the last 12 months
    precipitation = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date.between('2016-08-23', '2017-08-23')).all()

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
    # start session
    session = Session(engine)

    # query the dates and temperature observations of the most-active station for the previous year of data
    temperature = session.query(Measurement.date, Measurement.tobs).filter(Measurement.station == 'USC00519281').\
        filter(Measurement.date.between('2016-08-23', '2017-08-23')).all()

    session.close()

    all_temps = []
    for date, tobs in temperature:
        temp_dict = {}
        temp_dict[date] = tobs
        all_temps.append(temp_dict)

    return jsonify(all_temps)



if __name__ == '__main__':
    app.run(debug=True)






