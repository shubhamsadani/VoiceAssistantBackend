import sqlite3
import traceback

def list_available_appointments(args):
    try:
        appointment_date = str(args['appointment_date'])
        print(appointment_date)
        connection = sqlite3.connect("appointments.db")
        cursor = connection.cursor()
        cursor.execute('SELECT slot_time FROM slots where slot_date = ? AND status = "AVAILABLE"',(appointment_date,))
        rows = cursor.fetchall()
        if len(rows) != 0:
            connection.close()
            return rows
        else:
            return 'No slot available'
    except:
        traceback.print_exc()
        return 'Error in finding availble slots'