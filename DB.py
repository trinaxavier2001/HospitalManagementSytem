from flask import Flask, get_flashed_messages, render_template, request, redirect, jsonify, url_for, json, flash
import csv
from pymongo import MongoClient
from datetime import datetime
from routes.Doctor import doc_record
from routes.Department import dep_record
from routes.General_Staff import gs_record
from routes.Hospital_Admin import ha_record
from routes.Appointment import appo_record, appo_record1
from routes.Patient import pat_record
from routes.Medical_Records import med_record
from routes.Resource_Management import resm_record
from routes.Nurse import nur_record
from routes.Employee import emp_record
from models.appointment import updateappointment, get_appointment_records, deleteappointment, process_imported_appointment_data, get_export_data_for_appointment


# Initialize Flask app
app = Flask(__name__)
app.secret_key = 'supreethbmohan'
# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['HospitalManagementSystem']

# Route to render the HTML page
@app.route('/')
def index():
    # Get the list of collection names (tables) from the database
    tables = db.list_collection_names()
    return render_template('index.html', tables=tables)

@app.route('/emp', methods=['GET', 'POST'])
def emp():
        if request.method == 'GET':
            return emp_record(db)
        elif request.method == 'POST':
            return emp_record(db)

@app.route('/nur', methods=['GET', 'POST'])
def nur():
        if request.method == 'GET':
            return nur_record(db)
        elif request.method == 'POST':
            return nur_record(db)

@app.route('/resm', methods=['GET', 'POST'])
def resm():
        if request.method == 'GET':
            return resm_record(db)
        elif request.method == 'POST':
            return resm_record(db)

@app.route('/med', methods=['GET', 'POST'])
def med():
        if request.method == 'GET':
            return med_record(db)
        elif request.method == 'POST':
            return med_record(db)

@app.route('/pat', methods=['GET', 'POST'])
def pat():
        if request.method == 'GET':
            return pat_record(db)
        elif request.method == 'POST':
            return pat_record(db)

@app.route('/doc', methods=['GET', 'POST'])
def doc():
        if request.method == 'GET':
            return doc_record(db)
        elif request.method == 'POST':
            return doc_record(db)

@app.route('/dep', methods=['GET', 'POST'])
def dep():
        if request.method == 'GET':
            return dep_record(db)
        elif request.method == 'POST':
            return dep_record(db)

@app.route('/gs', methods=['GET', 'POST'])
def gs():
        if request.method == 'GET':
            return gs_record(db)
        elif request.method == 'POST':
            return gs_record(db)

@app.route('/ha', methods=['GET', 'POST'])
def ha():
        if request.method == 'GET':
            return ha_record(db)
        elif request.method == 'POST':
            return ha_record(db)

@app.route('/appo', methods=['GET', 'POST'])
def appo():
        if request.method == 'GET':
            return appo_record(db)
        elif request.method == 'POST':
            return appo_record(db)

@app.route('/appo1', methods=['GET', 'POST','PUT'])
def appo1():
        
        messages = request.args.get('messages','').split('_')
        # print('message',messages)
        if request.method == ('GET'):
            return appo_record1(db,messages)
        elif request.method == 'POST':
            return appo_record1(db,messages)
        # elif request.method == 'PUT':
        #     return appo_record1(db,messages)
        
def get_appointment_record(appointment_id):
    # Connect to MongoDB
    client = MongoClient('mongodb://localhost:27017/')
    # Access the database
    db = client['HospitalManagementSystem']
    # Access the collection containing appointments' records
    appointment_collection = db['Appointment']

    appointment = appointment_collection.find_one({'AppointmentID': appointment_id})
    # # Query to retrieve all appointments' records
    # appointments = list(appointment_collection.find())

    # Close the database connection
    client.close()

    return appointment


@app.route('/api/appointments/<int:appointment_id>', methods=['GET', 'PUT'])
def get_appointment(appointment_id):
    # Connect to MongoDB
    client = MongoClient('mongodb://localhost:27017/')
    # Access the database
    db = client['HospitalManagementSystem']
    if request.method == 'GET':
        # Fetch all appointments' records
        appointment_id = int(appointment_id)
        appointment = get_appointment_record(appointment_id)
        
        # # Search for the appointment with the specified ID
        # appointment = next((a for a in appointments if a["AppointmentID"] == appointment_id), None)
        
        
        if appointment:
            appointment['_id'] = str(appointment['_id'])
  
            return jsonify(appointment), 200
        else:
            return jsonify({"error": "Appointment not found"}), 404
        
    elif request.method == 'PUT':
        updated_data = request.json
        action = updated_data.get('action')
        print(action)
        if(action == 'update'):
            # Update the appointment record with the specified ID
            appointment_id = int(appointment_id)
            # updated_data = request.json
            updated_patient_id = int(updated_data.get('PatientID'))
            updated_doctor_id = int(updated_data.get('DoctorID'))
            updated_datetime = updated_data.get('DateTime')
            updated_purpose = updated_data.get('Purpose')
            updated_status = updated_data.get('Status')
            success = updateappointment(db,appointment_id,updated_patient_id,updated_doctor_id,updated_datetime,updated_purpose,updated_status )
            appointments = get_appointment_records()
            message = get_flashed_messages(with_categories=True)
            print(message)
            # Render the template with the list of appointments
            return render_template('/Appointment/Appo1.html', appointments=appointments, messages=message)
            # if success:
            #     return redirect(url_for('appo1'))
            # else:
            #return jsonify({"error": "Failed to update appointment"}), 500
            
            # return redirect(url_for('appo1',method='GET'))
        elif(action == 'delete'):
            appointment_id = int(appointment_id)
            success = deleteappointment(db,appointment_id)
            appointments = get_appointment_records()
            # Render the template with the list of appointments
            return render_template('/Appointment/Appo1.html', appointments=appointments, messages ='_'.join(get_flashed_messages()))

def export_data_to_csv(data, filename):
    # Write data to a CSV file
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)

@app.route('/importexportjson', methods=['GET', 'POST'])
def importexportjson():
    if request.method == 'POST':
        action = request.form.get('action')
        selected_collection = request.form.get('collection_name')

        if action == 'import':
            import_json_file = request.files.get('import_json')
            if import_json_file:
                import_data = import_json_file.read()
                try:
                    imported_data = json.loads(import_data)
                except json.JSONDecodeError as e:
                    error_message = f"Error decoding JSON file: {str(e)}"
                    flash('Insert Unsuccessful!\n' + error_message, 'error')
                    return redirect(url_for('importexportjson',messages = error_message ))
                    # return error_messages
                
                if selected_collection == 'Appointment':
                    # Process imported data for Appointment collection
                    success, error, yn = process_imported_appointment_data(imported_data)
                    result = yn
                    if yn:
                        flash('Insert successful!', 'success')
                        print (f"Appointment data imported successfully:{result} {error}.",)
                        return redirect(url_for('importexportjson',messages = success ))

                    else:
                        flash(f'Insert Unsuccessful!\n + {success}', 'error')
                        print (f"Failed to import Appointment data.")
                        return redirect(url_for('importexportjson',messages ='_'.join(get_flashed_messages())))

                elif selected_collection == 'Department':
                    # Process imported data for Department collection
                    # success = process_imported_department_data(imported_data)
                    if success:
                        return (f"Department data imported successfully.")
                    else:
                        return (f"Failed to import Department data.")
                else:
                    return (f"Invalid collection selected.")
            else:
                return (f"No import JSON file provided.")
        
        elif action == 'export':
            if selected_collection == 'Appointment':
                # Get export data for Appointment collection
                export_data = get_export_data_for_appointment()
            elif selected_collection == 'Department':
                # Get export data for Department collection
                # export_data = get_export_data_for_department()
                True
            # Add more conditions for other collections as needed
            else:
                return (f"Invalid collection selected.")
            
            if export_data:
                # Define the filename for the CSV file
                filename = f"{selected_collection}_export.csv"
                export_json_file = request.files.get('export_json')
                print(export_json_file)
                # Export data to CSV file
                export_data_to_csv(export_data, filename)
                
                # Return the export data as JSON response
                # return jsonify(export_data)
                flash('Imported the File Successfully','success')
                return redirect(url_for('importexportjson', message='success'))
            else:
                flash('Error While Importing the File','error')
                return (f"No export data available.")
            # import os

            # if export_data:
            #     # Check if export_json file is provided
            #     export_json_file = request.files.get('export_json')
            #     if export_json_file:
            #         # Get the selected directory path from the file input
            #         export_directory = os.path.dirname(export_json_file.filename)
            #         # Define the filename for the CSV file
            #         filename = f"{selected_collection}_export.csv"
            #         # Construct the full path to save the CSV file
            #         csv_file_path = os.path.join(export_directory, filename)
            #         # Export data to CSV file
            #         export_data_to_csv(export_data, csv_file_path)
            #         # Return success message with the path where CSV is saved
            #         return f"CSV file exported successfully to {csv_file_path}."
            #     else:
            #         return "No export location provided."
            # else:
            #     return "No export data available."

        
            # else:
            #     return (f"Invalid action specified.")

        # # If the method is GET or the action is not recognized, render the same page
        # return render_template('importexportjson.html', collection=selected_collection)
        return redirect(url_for('importexportjson'))
    else:
        collection_names = db.list_collection_names()
        return render_template('/importexportjson.html',collection_names=collection_names)
          

@app.route('/trigger_alert')
def trigger_alert():
    # Logic to determine alert message
    alert_message = "Alert: Something important happened!"

    # Return the alert message as JSON
    return jsonify(message=alert_message)



# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True, port=8000)