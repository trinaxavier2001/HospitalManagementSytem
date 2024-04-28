from flask import flash
from pymongo import MongoClient

def insertappointment(patient_id, doctor_id, date_time, purpose, status):
    client = MongoClient('mongodb://localhost:27017/') 
    db = client['HospitalManagementSystem']  
    # Access Appointment collection
    appointment_collection = db['Appointment']
    # Find the last used PatientID, if any
    last_appointment = appointment_collection.find_one(sort=[("AppointmentID", -1)])

    # Determine the starting value for PatientID
    start_appointment_id = 1 if last_appointment is None else last_appointment['AppointmentID'] + 1
    print(patient_id)
    # Construct appointment data
    appointment_data = {
        "AppointmentID": start_appointment_id,
        "PatientID": patient_id,
        "DoctorID": doctor_id,
        "DateTime": date_time,
        "Purpose": purpose,
        "Status": 'Scheduled'
    }
    
    # Verify if PatientID exists
    patient_exists = db['Patient'].find_one({"PatientID": patient_id})
    if not patient_exists:
        return (f"Error: PatientID {patient_id} does not exist. Skipping insertion. False")
    
    # Verify if DepartmentNumber exists
    doctor_exists = db['Doctor'].find_one({"DoctorID": doctor_id})
    if not doctor_exists:
        return (f"Error: DoctorID {doctor_id} does not exist. Skipping insertion for AppointmentID {start_appointment_id}. False")
        
    
    # Check if the record already exists
    existing_appointment = appointment_collection.find_one({"PatientID": patient_id})
    
    if existing_appointment:
        # Update existing record
        existing_department = appointment_collection.find_one({"DoctorID": doctor_id})
        if(existing_department):
            return (f"Appointment already scheduled for Patient with doctor {doctor_id} False")
        else:
            appointment_collection.update_one(
                {"AppointmentID": appointment_collection["AppointmentID"]},
                {"$set": {"PatientID": patient_id, "DoctorID": doctor_id, "DateTime": date_time, "Purpose": purpose, "Status": status}}
            )

            return (f"Updated record for AppointmentID {start_appointment_id} True")
    else:
        # Insert a new record
        result = appointment_collection.insert_one(appointment_data)
        return (f"Inserted ID:{result.inserted_id} True")



def updateappointment(db, appointment_id, patient_id, doctor_id, appointment_date, purpose, status):
    # Access Appointment collection
    appointment_collection = db['Appointment']
    
    # Check if the appointment ID exists
    existing_appointment = appointment_collection.find_one({"AppointmentID": appointment_id})
    print(existing_appointment)
    if not existing_appointment:
        print(f"Appointment with ID {appointment_id} not found. Update failed.")
        return (f"Appointment with ID {appointment_id} not found. Update failed. False")

    # Check if the patient ID exists
    existing_patient = db['Patient'].find_one({"PatientID": patient_id})
    if not existing_patient:
        print(existing_patient)
        print(f"Patient with ID {patient_id} not found. Update failed.")
        return (f"Patient with ID {patient_id} not found. Update failed. False")
    
    # Check if the department number exists
    existing_doctor = db['Doctor'].find_one({"DoctorID": doctor_id})
    if not existing_doctor:
        flash(f"Doctor with ID {doctor_id} not found. Update failed.",'error')
        return (f"Doctor with ID {doctor_id} not found. Update failed. False")

    # Construct update query
    update_query = {
        "PatientID": patient_id,
        "DoctorID": doctor_id,
        "DateTime": appointment_date,
        "Purpose": purpose,
        "Status": status
    }

    # Perform the update
    result = appointment_collection.update_one({"AppointmentID": appointment_id}, {"$set": update_query})
    if result.modified_count > 0:
        print(f"Updated record for AppointmentID {appointment_id}")
        return (f"Updated record for AppointmentID {appointment_id} True")
    else:
        print(f"Failed to update appointment. AppointmentID {appointment_id} not found.")
        return (f"Failed to update appointment. AppointmentID {appointment_id} not found. False")


def deleteappointment(db, appointment_id):
    # Access HospitalAdmin collection
    appointment_collection = db['Appointment']

    # Check if the admin exists
    existing_appointment = appointment_collection.find_one({"AppointmentID": appointment_id})
    if not existing_appointment:
        print(f"Appointment with ID {appointment_id} not found.")
        return (f"Appointmentwith ID {appointment_id} not found. False")

    # Delete the admin record
    appointment_collection.delete_one({"AppointmentID": appointment_id})
    print(f"Deleted record for AppointmentID {appointment_id}")
    return (f"Deleted record for AppointmentID {appointment_id} True")


def process_imported_appointment_data(imported_data):
    
   
    success_count = 0
    error_messages = []
    print(imported_data)
    # Loop through imported data and insert each appointment
    for appointment in imported_data:
        # Extract appointment details
        patient_id = appointment.get('PatientID')
        doctor_id = appointment.get('DoctorID')
        date_time = appointment.get('DateTime')
        purpose = appointment.get('Purpose')
        status = appointment.get('Status', 'Scheduled')  # Default status to 'Scheduled'
        print('oid',patient_id)
        # Insert appointment
        result = insertappointment(patient_id, doctor_id, date_time, purpose, status)
        
    # Check result
    if result.startswith('Inserted'):
        success_count += 1
        return success_count, error_messages, True
    else:
        error_messages.append(result)
        return success_count, error_messages, False
        

    # return success_count, error_messages, True


# Function to refresh the database connection
def refresh_db_connection():
   
    client.close()  # Close existing connection
    

def get_export_data_for_appointment():
    client = MongoClient('mongodb://localhost:27017/') 
    db = client['HospitalManagementSystem']  
    # Access the Appointment collection
    appointment_collection = db['Appointment']
    
    # Query the Appointment collection to retrieve the data
    appointment_data = appointment_collection.find({}, {'_id': 0})
    
    # Format the data into a list of dictionaries
    export_data = []
    for appointment in appointment_data:
        export_data.append({
            'AppointmentID': appointment.get('AppointmentID', ''),
            'PatientID': appointment.get('PatientID', ''),
            'DoctorID': appointment.get('DoctorID', ''),
            'DateTime': appointment.get('DateTime', ''),
            'Purpose': appointment.get('Purpose', ''),
            'Status': appointment.get('Status', '')
        })
    
    return export_data

def get_appointment_records():
    # Connect to MongoDB
    client = MongoClient('mongodb://localhost:27017/')
    # Access the database
    db = client['HospitalManagementSystem']
    # Access the collection containing doctors' records
    appointment_collection = db['Appointment']

    # Query to retrieve all doctors' records
    appointment = list(appointment_collection.find())

    # Close the database connection
    client.close()

    return appointment