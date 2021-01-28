########################################################################
############ Import libraries
# Flask
from flask import Flask,jsonify
#SQL toolkit and Object Relational Mapper
import sqlalchemy
from sqlalchemy import engine
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session 
from sqlalchemy import create_engine,func
# datetime imports
import datetime as dt

########################################################################
############# Database setup
engine=create_engine('sqlite:///../Resources/hawaii.sqlite')
Base=automap_base()
Base.prepare(engine, reflect=True)
# Save references to each table
Measurement,Station=Base.classes.measurement, Base.classes.station

########################################################################
############# Flask setup
app=Flask(__name__)

########################################################################
############# Utility function -  find out latest date for data
def latest_date():
     """Finds the most recent date in the data set"""
     session=Session(engine)
     # Find the most recent date in the data set.
     myquery=session.query(Measurement.date).\
          order_by(Measurement.date.desc()).first()
     date=myquery[0]
     # close session
     session.close()
     return date

############# Utility function - find out start date for data +365 days
def start_date():
     """Finds out start date for data +365 days to last date"""
     # Find the most recent date in the data set.
     # Starting from the most recent data point in the database.
     last_date=latest_date()
     last_date=dt.date.fromisoformat(last_date)
     # Calculate the date one year from the last date in data set.
     date=last_date-dt.timedelta(days=365)
     date=date.isoformat()
     return date

############# Utility function -  most active station
def most_active():
     """Finds the most active station based on count of temp records"""
     session=Session(engine)
     # same as above but with station ID , aslo trying subquery method
     active_station_id=session.query(\
        Station.id,Station.station,\
        func.count(Station.station).label('activity_count')).\
        join(Measurement, Measurement.station==Station.station).\
        group_by(Station.station).order_by(func.count(Station.station).desc()).\
        subquery()
     # getting most active station id
     myquery=session.query(active_station_id.c.id).first()
     station=myquery[0]
     # close session
     session.close()
     return station

########################################################################
############# routes

############# setup home page with list of available routes
@app.route('/')
def home_page():
     """create home page for weather data api"""
     print("homepage vizited")
     prcp="/api/v1.0/precipitation"
     stations="/api/v1.0/station"
     tobs="/api/v1.0/tobs"
     date_search="/api/v1.0/"
     dateformat="yyyy-mm-dd"
     page_list =f'<h1>Welcome to Climate API page</h1>\
         <p><b>List of available routes:</b></p>\
         <p><b>precipitation for most recent available dates - 365 days all stations </b> -  {prcp} <br/></p>\
         <p><b>stations sorted by activity </b> - {stations} <br/></p>\
         <p><b>most active station temperature for most recent available dates - 365 days   </b> -  {tobs} <br/></p>\
         <p><b> min max avg temperature for date range </b> -  {date_search}<i>"enter your date"</i> \
         <br/> {date_search}<i>{dateformat} </i>  - from date or\
         <br/> {date_search}<i>{dateformat}/{dateformat} </i> - from/to date</p>'
     return page_list

############# setup precipitation API route
@app.route('/api/v1.0/precipitation')
def precipitation():
     """returns JSON with precipitation data"""
     print('visited precipitation ')
     session=Session(engine)
     start_d=start_date() # getting start date for query - based on 1 year of data
     # Perform a query to retrieve the data and precipitation scores
     myquery=session.query(Measurement.date,Measurement.prcp,Measurement.station).\
          filter(Measurement.prcp!=None,Measurement.date>=start_d).order_by(Measurement.date).all()
     # create dictionary
     prcp_dict=[{date:(prcp,station)} for date, prcp,station in myquery]
     
     # close session
     session.close()
     return jsonify(prcp_dict)

############# setup weather stations API route
@app.route('/api/v1.0/station')
def station():
     """returns JSON with station data"""
     print('visited stations ')
     session=Session(engine)
     #perform query on active stations
     active_station_id=session.query(\
        Station.id,Station.station,\
        func.count(Station.station).label('activity_count')).\
        join(Measurement, Measurement.station==Station.station).\
        group_by(Station.station).order_by(func.count(Station.station).desc()).\
        subquery()
     myquery=session.query(active_station_id).all()
     # create dictionary
     sttn_dict=[{station_id:(station,records)} for station_id, station, records in myquery]
     # close session
     session.close()
     return jsonify(sttn_dict)

############# setup temperature data API route
@app.route('/api/v1.0/tobs')
def tobs():
     """returns JSON with temperature data:
     dates and temperature observations of the most active station for the last year of data"""
     print('visited temperature ')
     
     # getting most active station ID
     most_active_id=most_active()
    
     # getting start Date
     start_d=start_date()

     # create subquery temperature data- join Station and Measurement tables 
     session=Session(engine)
     temp_join=session.query(Station.id,Station.station,\
          Measurement.date,Measurement.tobs).\
          join(Station,Station.station==Measurement.station).\
          subquery()
     # filter based on most active station and start date
     myquery=session.query(temp_join.c.date,\
          temp_join.c.tobs).\
          filter(temp_join.c.id==most_active_id,\
          temp_join.c.tobs!=None,\
          temp_join.c.date>=start_d)\
            .all()
     tobs_dict=[{date:temp} for date, temp in myquery]
     # close session
     session.close()
     return jsonify(tobs_dict)

############# setup temperature data range "from start date " API route for most active station
@app.route('/api/v1.0/<start>')
def date(start):
     """returns JSON with temperature data for most active station:
     calculate `TMIN`, `TAVG`, and `TMAX` for all dates greater than and equal to the start date.
     """
     print( 'visited start date page')
     
     try:
          # checking date format is in ISO format
          start_d=dt.date.fromisoformat(start)
          start_d=start_d.isoformat()
          print(start_d)
          
          # getting most active station id
          most_active_id=most_active()
          session=Session(engine)
          
          # create subquery temperature data- join Station and Measurement tables 
          temp_join=session.query(Station.id,Station.station,\
          Measurement.date,Measurement.tobs).\
          join(Station,Station.station==Measurement.station).\
          subquery()
          # filtering data for date and station Id and getting min-max-avg
          min_temp=session.query(func.min(temp_join.c.tobs)).\
          filter(temp_join.c.id==most_active_id,temp_join.c.date>=start_d).scalar()
          max_temp=session.query(func.max(temp_join.c.tobs)).\
          filter(temp_join.c.id==most_active_id,temp_join.c.date>=start_d).scalar()
          avg_temp=session.query(func.round(func.avg(temp_join.c.tobs),1)).\
          filter(temp_join.c.id==most_active_id,temp_join.c.date>=start_d).scalar()
          mydict={'TMIN':min_temp, 'TAVG':avg_temp, 'TMAX':max_temp}
          page_output=jsonify(mydict)
          # close session
          session.close() 
     
     except Exception as e:
          # handling error
          error=f"_exception_: {type(e).__name__},</br> _arguments_: {e.args}"
          print(error)
          #  page_output=error
          page_output=f'WARNING - date is most likely is in wrong format  </br>start = {start} </br>\
          please enter as per format -  yyyy-mm-dd </br> {error}'    
   
     return page_output
     

############# setup temperature data range "from start  to end date" API route
@app.route('/api/v1.0/<start>/<end>')
def double_date(start,end):
     """returns JSON with temperature data:
     calculate the `TMIN`, `TAVG`, and `TMAX` for dates between the start and end date inclusive."""
     
     print('visited double date page ')
     try:
          # checking date format is in ISO format
          start_d=dt.date.fromisoformat(start)
          start_d=start_d.isoformat()
          end_d=dt.date.fromisoformat(end)
          end_d=end_d.isoformat()
          print(start_d,end_d)          
          # start date greater than end date error
          if start_d >end_d:
               page_output=f'WARNING - start date cannot be greater than end date   </br>start = {start}</br>end = {end} </br>\
          please enter as per format -  yyyy-mm-dd /yyyy-mm-dd </br>'
          else:           
               # getting most active station id
               most_active_id=most_active()
               session=Session(engine)
               
               # create subquery temperature data- join Station and Measurement tables 
               temp_join=session.query(Station.id,Station.station,\
               Measurement.date,Measurement.tobs).\
               join(Station,Station.station==Measurement.station).\
               subquery()
               # filtering data for date and station Id and getting min-max-avg
               min_temp=session.query(func.min(temp_join.c.tobs)).\
                    filter(temp_join.c.id==most_active_id,\
                         temp_join.c.date>=start_d,\
                         temp_join.c.date<=end_d).\
                    scalar()
               max_temp=session.query(func.max(temp_join.c.tobs)).\
                    filter(temp_join.c.id==most_active_id,\
                         temp_join.c.date>=start_d,\
                         temp_join.c.date<=end_d).\
                    scalar()
               avg_temp=session.query(func.round(func.avg(temp_join.c.tobs),1)).\
                    filter(temp_join.c.id==most_active_id,\
                         temp_join.c.date>=start_d,\
                         temp_join.c.date<=end_d).\
                    scalar()
               mydict={'TMIN':min_temp, 'TAVG':avg_temp, 'TMAX':max_temp}
               page_output=jsonify(mydict)
               # close session
               session.close() 
     
     except (ValueError, TypeError) as e:
          # handling error
          error=f"_exception_: {type(e).__name__},</br> _arguments_: {e.args}"
          print(error)
          #  page_output=error
          page_output=f'WARNING - date is most likely is in wrong format  </br>start = {start}</br>end = {end} </br>\
          please enter as per format -  yyyy-mm-dd /yyyy-mm-dd </br> {error}'    

     
     
     return page_output

if __name__ == '__main__':
    app.run(debug=True)
