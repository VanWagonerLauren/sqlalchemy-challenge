import numpy as np
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

#Database and Engine
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)
Measurement = Base.classes.measurement
Station = Base.classes.station

#Flask
app = Flask(__name__)
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Welcome to the SQL-Alchemy APP API!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/[start_date format:yyyy-mm-dd]<br/>"
        f"/api/v1.0/[start_date format:yyyy-mm-dd]/[end_date format:yyyy-mm-dd]<br/>"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
 #Session
 session = Session(engine)


"""Return a list of all Precipitation Data"""
 #Query
results = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= "2016-08-24").\
        all()

session.close()

#Dictionary
  all_prcp = []
    for date,prcp  in results:
        prcp_dict = {}
        prcp_dict["date"] = date
        prcp_dict["prcp"] = prcp
               
        all_prcp.append(prcp_dict)

    return jsonify(all_prcp)
@app.route("/api/v1.0/stations")
def stations():

#Create Session py
 session = Session(engine)
 """Return a list of all Stations"""
 #Query Stations
 results = session.query(Station.station).\
                 order_by(Station.station).all()

    session.close()
 
 all_stations = list(np.ravel(results))

    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)

"""Return a list of all TOBs"""    
results = session.query(Measurement.date,  Measurement.tobs,Measurement.prcp).\
                filter(Measurement.date >= '2016-08-23').\
                filter(Measurement.station=='USC00519281').\
                order_by(Measurement.date).all()

    session.close()




