import sqlite3
import traceback

def book_appointment(args):
    try:
        appointment_date = args['appointment_date']
        appointment_time = args['appointment_time'].lower()
        print(appointment_time)
        name = args['name']
        mobile_number = args['mobile_number']
        purpose = args.get('purpose', '')
        connection = sqlite3.connect("appointments.db")
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM slots where slot_date = ? AND slot_time = ? AND status = "AVAILABLE"',(appointment_date, appointment_time))
        rows = cursor.fetchall()
        if len(rows) != 0:
            cursor.execute('UPDATE slots SET status = "BOOKED", patient_name = ?, patient_mobile_number = ?, purpose = ? WHERE slot_date = ? AND slot_time = ?', (name, mobile_number, purpose, appointment_date, appointment_time))
            connection.commit()
            connection.close()
            return 'Appointment Booked'
        else:
            return 'Slot not available'
    except:
        traceback.print_exc()
        return 'Error in booking'