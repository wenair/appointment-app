from flask import Flask,request,make_response
import sql
import datetime

app = Flask(__name__)

@app.route('/')
def home():
    return "Hello World!"

@app.route('/appointments/<userid>', methods=['GET', 'POST'])
def get_appointments(userid):
    if request.method == 'GET':
        print("Gateway: GET")
        records = sql.get_records_for_id(userid)
        if records is None or len(records) == 0:
            print("Gateway: Records is none for some reason")
            response = make_response('Found no appointments for %s ' % userid, 200)
            return response

        appointment_times = process_records(userid, records)
        response = make_response(appointment_times, 200)
        response.headers["content-type"] = "text/plain"
        return response
    elif request.method == 'POST':
        print("Gateway: Post")
        data = request.get_json()
        if data is None:
            print("Gateway: no data found")
            response = make_response('ERROR: No data or incorrectly formatted data passed in ', 400)
            return response
        date_time_str =  data.get('datetime', None)
        print("Gateway datetime string", date_time_str)
        if date_time_str is None:
            print("Gateway: No datetime passed in")
            response = make_response('ERROR: No datetime passed in ', 400)
            return response
        try:
            dt = datetime.datetime.strptime(date_time_str, '%Y-%m-%d %H:%M')
        except ValueError as error:
            print("Gateway: error converting to datetime", error)
            print("Gateway: String passed in", date_time_str)
            response = make_response('ERROR: Datetime has to be of format Y-M-D H:M .H is 24 hr clock. ', 400)
            return response

        print("Date:", dt.date())

        foundMatch =  sql.get_matches(userid, dt)

        if foundMatch is True:
            response = make_response('ERROR: Appointment already exists for date. Please delete that appointment before continuing. ', 400)
            return response

        sql.insert_record(userid, dt)
        response = make_response('Appointment updated', 200)
        return response
        
        

def process_records(userid, records):
    numberOfAppointments = str(len(records))
    appointment_times="Found "+numberOfAppointments +" appointment(s) for " + userid + ":\n"
    for row in records:
        userid= row[0]
        appointment = row[1]
        appointment_times += row[1].strftime("%Y-%m-%d, %H:%M") + "\n"
        print("Gateway: ",userid, " has appointment on ", appointment)
        print("Gateway: appointment type is", type(appointment))
    return appointment_times

if __name__ == '__main__':
    app.run(debug=True)
