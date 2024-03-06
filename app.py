import sqlite3
import traceback
from chat import chat_model
from flask_cors import CORS
from flask import Flask, request, jsonify

app = Flask(__name__)
CORS(app)

@app.route('/health', methods = ['GET'])
def health():
    return 'I am running!!!'

@app.route('/newSlot', methods = ['POST'])
def new_slots():
    try:
        request_data = request.get_json()
        for slot in request_data:
            if ('date' and 'time') in slot:
                slot_date = slot['date']
                for slot_time in slot['time']:
                    connection = sqlite3.connect("appointments.db")
                    cursor = connection.cursor()
                    cursor.execute('SELECT * FROM slots where slot_date = ? AND slot_time = ?',(slot_date, slot_time))
                    rows = cursor.fetchall()
                    if len(rows) == 0:
                        cursor.execute('INSERT INTO slots VALUES (?, ?, "AVAILABLE", "", "", "")',(slot_date, slot_time))
                    else:
                        cursor.execute('UPDATE slots SET status = "AVAILABLE", patient_name = "", patient_mobile_number = "" WHERE slot_date = ? AND slot_time = ? AND purpose = ""', (slot_date, slot_time))
                    connection.commit()
                    connection.close()
        reponse = {
            'Success': True,
            'Message':'SLOTS_INSERTED_SUCCESSFULLY'
        }
        return jsonify(reponse)
    except:
        traceback.print_exc()
        reponse = {
            'Success': False,
            'Message': 'INTERNAL_SERVER_ERROR'
        }
        return jsonify(reponse)
    
@app.route('/cancelSlot', methods = ['POST'])
def cancel_slot():
    try:
        request_data = request.get_json()
        for slot in request_data:
            if ('date' and 'time') in slot:
                slot_date = slot['date']
                for slot_time in slot['time']:
                    connection = sqlite3.connect("appointments.db")
                    cursor = connection.cursor()
                    cursor.execute('SELECT * FROM slots where slot_date = ? AND slot_time = ?',(slot_date, slot_time))
                    rows = cursor.fetchall()
                    if len(rows) != 0:
                        cursor.execute('UPDATE slots SET status = "CANCELLED", patient_name = "", patient_mobile_number = "", purpose = "" WHERE slot_date = ? AND slot_time = ?', (slot_date, slot_time))
                        connection.commit()
                        connection.close()
        reponse = {
            'Success': True,
            'Message':'SLOTS_REMOVED_SUCCESSFULLY'
        }
        return jsonify(reponse)
    except:
        traceback.print_exc()
        reponse = {
            'Success': False,
            'Message': 'INTERNAL_SERVER_ERROR'
        }
        return jsonify(reponse)

@app.route('/chat', methods = ['POST'])
def user_chat():
    try: 
        request_data = request.get_json()
        model_response = chat_model(request_data['chat'])
        response = {
            'botReply': model_response
        }
        print(response)
        return jsonify(response)
    except:
        traceback.print_exc()
        return jsonify({'botReply': 'BOT - ERROR in execution'})



if __name__ == '__main__':
    app.run(port=5000)