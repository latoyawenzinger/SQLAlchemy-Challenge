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
measurement = Base.classes.measurement
station = Base.classes.station


# create an app
app = Flask(__name__)


# date one year before the most recent recored date
year = '2016-08-23'

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
    precipitation = session.query(measurement.date, measurement.prcp).filter(measurement.date >= year).all()

    session.close()

    # convert query results into a dictionary
    # 'date' = key , 'prcp' = value
    prcp_data = []
    for date in precipitation:
        prcp_dict = {}
        prcp_dict["date"] = 'prcp'
        prcp_data.append(prcp_dict)

    return jsonify(precipitation)


@app.route("/api/v1.0/stations")
def stations():
    #start session
    session = Session(engine)

    # query to get list of stations
    stations = session.query(measurement.station).all()

    session.close()

    return jsonify(stations)


@app.route("/api/v1.0/tobs")
def tobs():
    # start session
    session = Session(engine)

    # query the dates and temperature observations of the most-active station for the previous year of data
    tobs = session.query(measurement.tobs).filter(measurement.station == 'USC00519281').filter(measurement.date >= year).all()

    session.close()

    temps = list(np.ravel(tobs))

    return jsonify(temps)



if __name__ == '__main__':
    app.run(debug=True)






