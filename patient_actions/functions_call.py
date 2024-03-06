import google.ai.generativelanguage as glm

appointment_functions = glm.Tool(
    function_declarations = [
        glm.FunctionDeclaration(
            name = "book_appointment",
            description = "Book a doctor's appointment when the patient's name, mobile number, appointment date and time is given by the patient. Convert the date and time received from user in required format. The time is converted in 12 hour format for e.g. 3pm should be strictly 03:00 pm",
            parameters = glm.Schema(
                type= glm.Type.OBJECT,
                properties = {
                    "name": glm.Schema(
                        type = glm.Type.STRING,
                        description = "Name of the patient"
                    ),
                    "mobile_number": glm.Schema(
                        type = glm.Type.STRING,
                        description = "Mobile Number of the patient"
                    ),
                    "appointment_date": glm.Schema(
                        type = glm.Type.STRING,
                        description = "Appointment Date in the format YYYY-MM-DD"
                    ),
                    "appointment_time": glm.Schema(
                        type = glm.Type.STRING,
                        description = "Appointment Time in the format HH:MM am/pm"
                    ),
                    "purpose": glm.Schema(
                        type = glm.Type.STRING,
                        description = "Purpose of visiting the doctor"
                    ),
                },
                required = [
                    "name",
                    "mobile_number",
                    "appointment_date",
                    "appointment_time",
                ]
            )
        ),
        glm.FunctionDeclaration(
            name = "cancel_appointment",
            description = "Cancel a doctor's appointment when the patient's name, mobile number, appointment date and time is given by the patient. Convert the date and time received from user in required format. The time is converted in 12 hour format",
            parameters = glm.Schema(
                type= glm.Type.OBJECT,
                properties = {
                    "name": glm.Schema(
                        type = glm.Type.STRING,
                        description = "Name of the patient"
                    ),
                    "mobile_number": glm.Schema(
                        type = glm.Type.STRING,
                        description = "Mobile Number of the patient"
                    ),
                    "appointment_date": glm.Schema(
                        type = glm.Type.STRING,
                        description = "Appointment Date in the format YYYY-MM-DD"
                    ),
                    "appointment_time": glm.Schema(
                        type = glm.Type.STRING,
                        description = "Appointment Time in the format HH:MM am/pm"
                    ),
                },
                required = [
                    "name",
                    "mobile_number",
                    "appointment_date",
                    "appointment_time",
                ]
            )
        ),
        glm.FunctionDeclaration(
            name = "list_available_appointments",
            description = "List all the appointments available for a given date by the user. Convert the date and time received from user in required format. ",
            parameters = glm.Schema(
                type= glm.Type.OBJECT,
                properties = {
                    "appointment_date": glm.Schema(
                        type = glm.Type.STRING,
                        description = "Appointment Date in the format YYYY-MM-DD"
                    ),
                },
                required = [
                    "appointment_date",
                ]
            )
        ),
    ]
)
