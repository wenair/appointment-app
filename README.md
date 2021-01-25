# appointment-app
Small flask app to make and get appointments.

###  Disclaimer
I am a Java Developer and if I go by my strengths I would have either coded this in Java or maybe nodejs. But given the usage of flask and python in the role I am trying for, I took it as a learning opportunity to build my first flask app:). I cheated a bit, it took me about 5 to 6 hours to do this and not the prescribed 3. Hope you do not mind.

### To run application:  
Clone this repository  
cd appointment-app  
python3 -m venv env  
source env/bin/activate  
pip install flask  

### To start application(port is 5000):  
python3 gateway.py

### To run tests
python3 gateway.test.py

### To test application  
There is one API endpoint:  
http://localhost:5000/appointments/userid

where userid is any alphanumeric string(there is no validation on the userid)

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

### Structure  
gateway.py contains the actual flask logic. sql.py deals with all the sqllite related logic. gateway.test.py has the tests.

###  Things I wish I could have done or I could have done better:  
1. There should be a middle layer between gateway and sql. gateway should only accept requests. Other logic should move into a separate layer between gateway and sql.  

1. I did not quite figure out usage of app context in the tests. So I am doing the not so nice bit of opening and closing database connections each time. This was done just to make the tests pass.

1. More unit tests for sql.py  

1. Better error handling on sql execution errors in sql.py.  

1. Delete method on the app. Also an update appointment.

1. Validation of userid

1. Refactoring code to more structured methods

1. Testing post without using get


