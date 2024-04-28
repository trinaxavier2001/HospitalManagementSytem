from pymongo import MongoClient


def insertpatient(db,patient_id,doctor_id, first_name, last_name, dob, gender, address, phone, email, emergency_contact_name, emergency_contact_phone, insurance_company, insurance_policy_number, medical_history_summary, current_medications):
    # Access Patient collection
    patient_collection = db['Patient']

    # Find the last used PatientID, if any
    last_patient = patient_collection.find_one(sort=[("PatientID", -1)])

    # Determine the starting value for PatientID
    start_patient_id = 1 if last_patient is None else last_patient['PatientID'] + 1

    # Construct patient data
    patient_data = {
        "PatientID": start_patient_id,
        "DoctorID": doctor_id,
        "FirstName": first_name,
        "LastName": last_name,
        "DOB": dob,
        "Gender": gender,
        "Address": address,
        "Phone": phone,
        "Email": email,
        "EmergencyContactName": emergency_contact_name,
        "EmergencyContactPhone": emergency_contact_phone,
        "InsuranceCompany": insurance_company,
        "InsurancePolicyNumber": insurance_policy_number,
        "MedicalHistorySummary": medical_history_summary,
        "CurrentMedications": current_medications
    }

    # Check if the patient already exists in the collection
    existing_patient = patient_collection.find_one({"PatientID": patient_id})
    
    if existing_patient:
        # Patient exists, update their record
        new_doctor_id = patient_data["DoctorID"]
        
        # Update DoctorID
        patient_collection.update_one(
            {"PatientID": patient_id},
            {"$set": {"DoctorID": new_doctor_id}}
        )
        
        # Add previous doctor and prescription to medical history summary
        previous_doctor = existing_patient.get("DoctorID")
        prescription = existing_patient.get("CurrentMedications")
        medical_history = existing_patient.get("MedicalHistorySummary")
        
        if medical_history:
            medical_history += f",\nPrevious Doctor: {previous_doctor}, Prescription: {prescription}"
        else:
            medical_history = f"Current Doctor: {previous_doctor}, Prescription: {prescription}"
        
        # Update MedicalHistorySummary
        patient_collection.update_one(
            {"PatientID": patient_id},
            {"$set": {"MedicalHistorySummary": medical_history}}
        )
        
        print(f"Updated record for PatientID {patient_id}")
        return (f"Updated record for PatientID {patient_id}")
    else:
        # Patient doesn't exist, insert a new record
        result = patient_collection.insert_one(patient_data)
        return (f"Inserted ID: {result.inserted_id}")

    
def updatepatient(db,patient_id,doctor_id, first_name, last_name, dob, gender, address, phone, email, emergency_contact_name, emergency_contact_phone, insurance_company, insurance_policy_number, medical_history_summary, current_medications):
    # Access Patient collection
    patient_collection = db['Patient']

    # Check if the patient already exists in the collection
    existing_patient = patient_collection.find_one({"PatientID": patient_id})
    
    patient_data = {
        "DoctorID": doctor_id,
        "FirstName": first_name,
        "LastName": last_name,
        "DOB": dob,
        "Gender": gender,
        "Address": address,
        "Phone": phone,
        "Email": email,
        "EmergencyContactName": emergency_contact_name,
        "EmergencyContactPhone": emergency_contact_phone,
        "InsuranceCompany": insurance_company,
        "InsurancePolicyNumber": insurance_policy_number,
        "MedicalHistorySummary": medical_history_summary,
        "CurrentMedications": current_medications
    }
    
    if existing_patient:

        patient_collection.update_one(
            {"PatientID": patient_id},
            {
                "$set": {
                    "DoctorID": doctor_id,
                    "FirstName": first_name if first_name else existing_patient.get("FirstName"),
                    "LastName": last_name if last_name else existing_patient.get("LastName"),
                    "DOB": dob if dob else existing_patient.get("DOB"),
                    "Gender": gender if gender else existing_patient.get("Gender"),
                    "Address": address if address else existing_patient.get("Address"),
                    "Phone": phone if phone else existing_patient.get("Phone"),
                    "Email": email if email else existing_patient.get("Email"),
                    "EmergencyContactName": emergency_contact_name if emergency_contact_name else existing_patient.get("EmergencyContactName"),
                    "EmergencyContactPhone": emergency_contact_phone if emergency_contact_phone else existing_patient.get("EmergencyContactPhone"),
                    "InsuranceCompany": insurance_company if insurance_company else existing_patient.get("InsuranceCompany"),
                    "InsurancePolicyNumber": insurance_policy_number if insurance_policy_number else existing_patient.get("InsurancePolicyNumber"),
                    "MedicalHistorySummary": medical_history_summary if medical_history_summary else existing_patient.get("MedicalHistorySummary"),
                    "CurrentMedications": current_medications if current_medications else existing_patient.get("CurrentMedications")
                }
            }
        )


    
        # Add previous doctor and prescription to medical history summary
        previous_doctor = existing_patient.get("DoctorID")
        prescription = existing_patient.get("CurrentMedications")
        medical_history = existing_patient.get("MedicalHistorySummary")
        
        if medical_history:
            medical_history += f",\nPrevious Doctor: {previous_doctor}, Prescription: {prescription}"
        else:
            medical_history = f"Current Doctor: {previous_doctor}, Prescription: {prescription}"
        
        # Update MedicalHistorySummary
        patient_collection.update_one(
            {"PatientID": patient_id},
            {"$set": {"MedicalHistorySummary": medical_history}}
        )
        
        print(f"Updated record for PatientID {patient_id}")
        
        return (f"Updated record for PatientID {patient_id}")
    else:
        # Patient doesn't exist, insert a new record
        result = patient_collection.insert_one(patient_data)
        print("Inserted ID:", result.inserted_id)

        return (f"Inserted ID:{result.inserted_id}")
    
    
def deletepatient(db, patient_id):
    # Access HospitalAdmin collection
    patient_collection = db['HospitalAdmin']

    # Check if the admin exists
    existing_patient = patient_collection.find_one({"PatientID": patient_id})
    if not existing_patient:
        print(f"Patient with ID {patient_id} not found.")
        return (f"Patient with ID {patient_id} not found. False")

    # Delete the admin record
    patient_collection.delete_one({"PatientID": patient_id})
    print(f"Deleted record for PatientID {patient_id}")
    return (f"Deleted record for PatientID {patient_id} True")

def get_patient_records():
    # Connect to MongoDB
    client = MongoClient('mongodb://localhost:27017/')
    # Access the database
    db = client['HospitalManagementSystem']
    # Access the collection containing doctors' records
    patient_collection = db['Patient']

    # Query to retrieve all doctors' records
    patient = list(patient_collection.find())

    # Close the database connection
    client.close()

    return patient