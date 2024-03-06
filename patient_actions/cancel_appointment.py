import sqlite3
import traceback

def cancel_appointment(args):
    try:
        name = args['name']
        mobile_number = args['mobile_number']
        appointment_date = args['appointment_date']
        appointment_time = args['appointment_time'].lower()
        print(appointment_time)
        connection = sqlite3.connect("appointments.db")
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM slots where slot_date = ? AND slot_time = ? AND patient_name = ? AND patient_mobile_number = ?',(appointment_date, appointment_time, name, mobile_number))
        rows = cursor.fetchall()
        if len(rows) != 0:
            cursor.execute('UPDATE slots SET status = "AVAILABLE", patient_name = "", patient_mobile_number = "", purpose = "" WHERE slot_date = ? AND slot_time = ?', (appointment_date, appointment_time))
            connection.commit()
            connection.close()
            return 'Appointment Cancelled'
        else:
            return 'Appointment Not found'
    except:
        traceback.print_exc()
        return 'Error in cancelling'