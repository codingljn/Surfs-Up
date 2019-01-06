# Import same dependencies as in the notebook
import numpy as np
import pandas as pd
import datetime as dt

# Python SQL toolkit and Object Relational Mapper
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

# As used on previous flask examples
from flask import Flask, jsonify

#Lines copied from the notebook where the analysis was performed
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#Setting up flask
app = Flask(__name__)

# hello_dict = {"Hello": "World!"}


@app.route("/")
def home():
    return (
        f"Welcome to the Hawaii Climate Analysis API!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start/end"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
# Returns the precipitation data 
    lastyr = dt.date(2017, 8, 23) - dt.timedelta(days=365)

# Perform a query to retrieve the data and precipitation scores
    precip = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= lastyr).all()

# Return data in JSON format
    return jsonify({date: prcp for date, prcp in precip})


@app.route("/api/v1.0/stations")
def station():
# Returns the station data
    stationum = session.query(Station.station).all()

# List the stations in JSON format
    return jsonify(list(np.ravel(stationum)))


@app.route("/api/v1.0/tobs")
def temphist():

    lastyr = dt.date(2017, 8, 23) - dt.timedelta(days=365)
# Query station USC00519281 for the last 12 months of data from the selected date
    temphist = session.query(Measurement.tobs).filter(Measurement.station == 'USC00519281').filter(Measurement.date >= lastyr).all()

 # List the stations in JSON format
    return jsonify(list(np.ravel(temphist)))


@app.route("/api/v1.0/<start>")
def calc_temp(start_date="2017-08-01"):
    temps = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]
# Calculate TMIN, TAVG, TMAX for dates greater than start
    toutput = session.query(*temps).filter(Measurement.date >= start_date).all()
# List the response in JSON format
    return jsonify(list(np.ravel(toutput)))
@app.route("/api/v1.0/<start>/<end>")
def calc_temps(start_date="2017-08-01", end_date="2017-08-16"):
    temps1 = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]
# Calculate TMIN, TAVG, TMAX for dates greater than start
    tout = session.query(*temps1).\
        filter(Measurement.date >= start_date).all()
# List the response in JSON format
    return jsonify(list(np.ravel(tout)))

# Calculate TMIN, TAVG, TMAX when a start and end date are provided
    tout = session.query(*temps1).filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()
# List the response in JSON format
    return jsonify(list(np.ravel(tout)))

if __name__ == "__main__":
    app.run(debug=True)