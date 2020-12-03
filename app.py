import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify
#Added
import datetime as dt

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

# var. to hold date 12 months prior
last_year = '2016-08-23'
busiest = "USC00519281"

# Home page & 
# list all available routes
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/station<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/&lt;start&gt;<br/>"
        f"/api/v1.0/&lt;start&gt;/&lt;end&gt;"
    )

# Convert the query results to a dictionary using date as the key and prcp as the value.
# Return the JSON representation of your dictionary:
@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    results = session.query(Measurement.date, Measurement.prcp).all()
    session.close()
    return jsonify(results)

# Return a JSON list of stations from the dataset:
@app.route("/api/v1.0/station")
def station():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    results = session.query(Station.station).all()
    session.close()
    return jsonify(results)

# Query the dates and temperature observations of the most active station for the last year of data.
# Return a JSON list of temperature observations (TOBS) for the previous year:
@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    tobs_results = session.query(Measurement.date, Measurement.station, Measurement.tobs).\
        filter(Measurement.station == busiest, Measurement.date >= last_year).all()
    session.close()
    return jsonify(tobs_results)

# When given the start date, calculate TMIN, TAVG, and TMAX for all dates greater than and equal to the start date.
@app.route("/api/v1.0/<start>")
def trip1(start):
 
    session = Session(engine)
    start_date= dt.datetime.strptime(start, '%Y-%m-%d')
    last_year = dt.timedelta(days=365)
    start = start_date-last_year
    end =  dt.date(2017, 8, 23)
    trip_data = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    trip1_results = list(np.ravel(trip_data))
    return jsonify(trip1_results)


# When given the start and the end date, calculate the TMIN, TAVG, and TMAX for dates between 
# the start and end date inclusive.
@app.route("/api/v1.0/<start_date>/<end_date>")
def trip2(start_date,end_date):
    session = Session(engine)
  # go back one year from start/end date and get Min/Avg/Max temp     
    start_datetime= dt.datetime.strptime(start_date, '%Y-%m-%d')
    end_datetime= dt.datetime.strptime(end_date,'%Y-%m-%d')
    last_year = dt.timedelta(days=365)
    start_date = start_datetime-last_year
    end_date = end_datetime-last_year
    trip_data = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()
    trip2_results = list(np.ravel(trip_data))
    return jsonify(trip2_results)

if __name__ == '__main__':
    app.run(debug=True)
