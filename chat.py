import os
import json
import logging
from dotenv import load_dotenv
import google.generativeai as genai
import google.ai.generativelanguage as glm
from patient_actions.functions_call import appointment_functions
from patient_actions.book_appointment import book_appointment
from patient_actions.cancel_appointment import cancel_appointment
from patient_actions.list_available_appointments import list_available_appointments

load_dotenv()

genai.configure(api_key=os.environ.get('API_KEY'))

model = genai.GenerativeModel('gemini-pro', tools=[appointment_functions])

chat = model.start_chat()

def identify_response_type(response_data):
    api_response =  response_data.candidates[0].content.parts[0]
    if 'text' in api_response:
        return 'TEXT', api_response.text
    elif 'function_call' in api_response:
        return 'FUNCTION_CALL', api_response.function_call

def chat_model(prompt):
    response = chat.send_message(prompt)
    response_type, response = identify_response_type(response)
    print(response_type)
    if response_type == 'FUNCTION_CALL':
        function_name = response.name
        if function_name == 'book_appointment':
            response = book_appointment(response.args)
        elif function_name == 'cancel_appointment':
            response = cancel_appointment(response.args)
        elif function_name == 'list_available_appointments':
            response = list_available_appointments(response.args)
        final_response = chat.send_message(
            glm.Content(
                parts=[
                    glm.Part(
                        function_response = glm.FunctionResponse(
                        name=function_name,
                        response={'result': response}
                        )
                    )
                ]
            )
        )
        response_type, response = identify_response_type(final_response)
        if response_type == 'FUNCTION_CALL':
            if function_name == 'list_available_appointments':
                response = list_available_appointments(response.args)
            final_response = chat.send_message(
                glm.Content(
                    parts=[
                        glm.Part(
                            function_response = glm.FunctionResponse(
                            name=function_name,
                            response={'result': response}
                            )
                        )
                    ]
                )
            )
        print(final_response)
        final_response = final_response.text
    elif response_type == 'TEXT':
        final_response = response
    print(final_response)
    return final_response