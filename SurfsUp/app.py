# Import the dependencies.
from flask import Flask, jsonify
import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import func, create_engine


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(bind=engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

@app.route("/")
def home():
    print("Server attempted to go to home page...") # prints in output console
    return (f"Welcome! <br>"
            f"Current Routes: <br>"
            f"/api/v1.0/precipitation <br>"
            f"/api/v1.0/stations <br>"
            f"/api/v1.0/tobs <br>"
            f"/api/v1.0/<start> <br>"
            f"/api/v1.0/<start>/<end>")


#################################################
# Flask Routes
#################################################
@app.route("/api/v1.0/precipitation")
def precipitation():
    results=session.query(Measurement.date,
                          Measurement.prcp).filter(Measurement.date>="2016-08-23").all()
    
    result_list=[]
    for date, prcp in results: 
        result_dict = {}
        result_dict[date] = prcp # using date as key and precipitation (prcp) as value
        result_list.append(result_dict)
    
    return jsonify(result_list)

@app.route("/api/v1.0/stations")
def stations():
    station_results=session.query(Station.station).all()

# using all data from the station table as question does not clarify if only some data is needed
    station_list = []
    for station in station_results:
        station_dict = {}
        station_dict["station"] = station["station"]
        station_list.append(station_dict)
    return jsonify(station_list)

@app.route("/api/v1.0/tobs")
def tobs():
    tobs_results=session.query(Measurement.date, 
                              Measurement.tobs).filter(Measurement.station=="USC00519281").all()
    
    tobs_list= []
    for tobs in tobs_results:
        tobs_dict={}
        tobs_dict["date"] = tobs["date"]
        tobs_dict["tobs"] = tobs["tobs"]
        tobs_list.append(tobs_dict)
    
    return jsonify(tobs_list)

@app.route("/api/v1.0/<start>")
def start(start):
    start_results=session.query(func.min(Measurement.tobs),
                               func.avg(Measurement.tobs),
                               func.max(Measurement.tobs)).filter(Measurement.date>=start).all()
    
    start_list=[]
    for min, avg, max in start_results:
        if min is None:
            return jsonify({"error": f" {start} data not found"})
        start_dict={}
        start_dict["TMIN"] = min
        start_dict["TAVG"] = avg
        start_dict["TMAX"] = max
        start_list.append(start_dict)

    return jsonify(start_list)

@app.route("/api/v1.0/<start>/<end>")
def start_end(start,end):
    start_end_results=session.query(func.min(Measurement.tobs),
                                    func.avg(Measurement.tobs),
                                    func.max(Measurement.tobs)).filter(Measurement.date>=start).filter(Measurement.date<=end).all()
    
    start_end_list=[]
    for min, avg, max in start_end_results:
        if min is None:
            return jsonify({"error": f" {start} to {end} data not found"})
        start_end_dict={}
        start_end_dict["TMIN"] = min
        start_end_dict["TAVG"] = avg
        start_end_dict["TMAX"] = max
        start_end_list.append(start_end_dict)

    return jsonify(start_end_list)
    
if __name__== "__main__":
    app.run(debug=True)