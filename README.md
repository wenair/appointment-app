# appointment-app
Small flask app to make and get appointments

To run application:  
Clone this repository  
cd appointment-app  
python3 -m venv env  
source env/bin/activate  
pip install flask  

To start application(port is 5000):  
python3 gateway.py

To test application  
There is one API endpoint:  
http://localhost:5000/appointments/<userid>  

Appointment time is supported in only YYYY-MM-DD HH:MM  

There are two methods it supports- GET and POST  

To try it out, try the following sequence on commandline  
> curl http://localhost:5000/appointments/Tom  
Found no appointments for Tom  
>curl -X POST -H 'Content-Type: application/json' -d '{"datetime":"2020-01-01 14:00"}' http://localhost:5000/appointments/Tom  
Appointment updated  
>curl http://localhost:5000/appointments/Tom  
Found 1 appointment(s) for Tom:  
2020-01-01, 14:00  

Now repeat the appointment
> curl -X POST -H 'Content-Type: application/json' -d '{"datetime":"2020-01-01 14:00"}' http://localhost:5000/appointments/Tom  
ERROR: Appointment already exists for date. Please delete that appointment before continuing.  

