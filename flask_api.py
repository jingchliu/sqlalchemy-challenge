import datetime as dt
import numpy as np
import pandas as pd
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)
Measurement = Base.classes.measurement
Station = Base.classes.station


app = Flask(__name__)

@app.route("/")
def welcome():
    return (
        f"Available APIs:<br/>"
        f"Precipitation:/api/v1.0/precipitation<br/>"
        f"Stations: /api/v1.0/stations<br/>"
        f"Temperature: /api/v1.0/tobs<br/>"
        f"Start Date Only: /api/v1.0/start(YYYY-MM-DD)<br/>"
        f"With End Date: /api/v1.0/start(YYYY-MM-DD)/end(YYYY-MM-DD)"
    )
@app.route("/api/v1.0/precipitation")
def prcp():
    session = Session(engine)
    last_date=session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    last_date_1_year_ago=dt.date(2017,8,23)-dt.timedelta(days=365)
    precipitation=session.query(Measurement.date,Measurement.prcp).filter(Measurement.date>last_date_1_year_ago).all()
    session.close()
    list_p=[]
    for date,prcp in precipitation:
        prcp_dict={}
        prcp_dict['Date']=date
        prcp_dict['Precipitation']=prcp
        list_p.append(prcp_dict)
    return jsonify(list_p)
@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    sta_list=session.query(Station.station).all()
    session.close()
    sta_names=list(np.ravel(sta_list))
    return jsonify(sta_names)
@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)
    last_date=session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    last_date_1_year_ago=dt.date(2017,8,23)-dt.timedelta(days=365)
    temperature=session.query(Measurement.tobs).filter(Measurement.date>last_date_1_year_ago).all()
    session.close()
    list_t=list(np.ravel(temperature))
    return jsonify(list_t)
@app.route("/api/v1.0/<start>")
def start(start):
    session = Session(engine)
    start_only=session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).all()
    session.close()
    list_s=list(np.ravel(start_only))
    return jsonify(list_s)
@app.route("/api/v1.0/<start>/<end>")
def start_end(start,end):
    session = Session(engine)
    start_end=session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    session.close()
    list_s_e=list(np.ravel(start_end))
    return jsonify(list_s_e)
if __name__ == "__main__":
    app.run(debug=True)