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
        f"<strong>Available Routes:</strong><br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/&lt;start&gt;    <strong>(REPLACE &lt;START&gt; WITH ACTUAL DATE - MUST FORMAT: yyyy-mm-dd)</strong><br/>"
        f"/api/v1.0/&lt;start&gt;/&lt;end&gt;   <strong>(REPLACE &lt;START&gt; AND &lt;END&gt; WITH ACTUAL DATE - MUST FORMAT: yyyy-mm-dd/yyyy-mm-dd)</strong>")

@app.route("/api/v1.0/precipitation")
def precipitation():
    """Return precipitation data for the last 12 months as json"""
    #start session
    session = Session(engine)

    # query precipitation results from the last 12 months
    precipitation = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date.between('2016-08-23', '2017-08-23')).all()
    
    #close session
    session.close()

    # convert query results into a jsonified dictionary
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
    
    session = Session(engine)

    # query to get list of station info
    station_data = session.query(Station.station, Station.name, Station.latitude, Station.longitude, Station.elevation).all()

    session.close()

    #convert results into a jsonified dictionary
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
   
    session = Session(engine)

    # query the dates and temperature observations of the most-active station for the previous year of data
    temperature = session.query(Measurement.date, Measurement.tobs).filter(Measurement.station == 'USC00519281').\
        filter(Measurement.date.between('2016-08-23', '2017-08-23')).all()

    session.close()

    # #convert results into a jsonified dictionary
    all_temps = []
    for date, tobs in temperature:
        temp_dict = {}
        temp_dict[date] = tobs
        all_temps.append(temp_dict)

    return jsonify(all_temps)
    


@app.route("/api/v1.0/<start>")
def start_date(start):
    """Returns JSON the min, max, and average temperatures calculated from the given start date to the end of the dataset"""

      
    session = Session(engine)

    # query min, max, and average of all temperatures with specified start range
    start_date = session.query(func.min(Measurement.tobs),func.max(Measurement.tobs),func.avg(Measurement.tobs)).\
        filter(Measurement.date >= start).all()
    
   
    session.close()
    
    # convert results into a jsonified dictionary; 'key '= min, max, and avg : 'value' = espective value for given date 
    start_date_list = []
    for min, max, avg in start_date:
        start_date_dict = {}
        start_date_dict['min_temp'] = min
        start_date_dict['max_temp'] = max
        start_date_dict['avg_temp'] = avg

        start_date_list.append(start_date_dict)

    return jsonify(start_date_list)



@app.route("/api/v1.0/<start>/<end>")
def start_end_date(start, end):
    """Returns the min, max, and average temperatures calculated from the given start date to the given end date"""

    session = Session(engine)
 
    # query min, max, and average of all temperatures with specified start to end range
    start_end_date = session.query(func.min(Measurement.tobs),func.max(Measurement.tobs),func.avg(Measurement.tobs)).\
    filter(Measurement.date.between(start, end)).all()
     
    session.close()
    
    #convert results into a jsonified dictionary
    end_date_list = []
    for min, max, avg in start_end_date:
        date_dict = {}
        date_dict['min_temp'] = min
        date_dict['max_temp'] = max
        date_dict['avg_temp'] = avg

        end_date_list.append(date_dict)

    return jsonify(end_date_list)
    

        
if __name__ == '__main__':
    app.run(debug=True)