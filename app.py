from flask import Flask, request, render_template,jsonify

app = Flask(__name__)
op_forms_db = []
ip_forms_db = []


@app.route('/main', methods=['GET'])
def main_form():
    return render_template('main.html')


@app.route('/op-form', methods=['GET'])
def op_form():
    return render_template('op.html')


@app.route('/ip-form', methods=['GET'])
def ip_form():
    return render_template('ip.html')


@app.route('/submit-op', methods=['POST'])
def submit_op():
    data = request.form
    doctor_name = data.get('doctor_name')
    diagnostics = data.get('diagnostics')
    medications = data.get('medications')
    radiology_interpretation = data.get('radiology_interpretation')
    next_followup_date = data.get('next_followup_date')

    prescription = request.files.getlist('prescription')
    if len(prescription) == 0:
        return "Error: At least one prescription image is required!", 400

    patient_name = data.get('patient_name')
    patient_phone = data.get('patient_phone')
    patient_id = data.get('patient_id')
    gender = data.get('gender')

    op_forms_db.append({
        "doctor_name": doctor_name,
        "diagnostics": diagnostics,
        "medications": medications,
        "radiology_interpretation": radiology_interpretation,
        "next_followup_date": next_followup_date,
        "prescription": [file.filename for file in prescription],
        "patient_name": patient_name,
        "patient_phone": patient_phone,
        "patient_id": patient_id,
        "gender": gender
    })
    return "OP Form submitted successfully!"


@app.route('/submit-ip', methods=['POST'])
def submit_ip():
    data = request.form
    doctor_name = data.get('doctor_name')
    surgery_name = data.get('surgery_name')

    prescription = request.files.getlist('prescription')
    if len(prescription) == 0:
        return "Error: At least one prescription image is required!", 400

    patient_name = data.get('patient_name')
    patient_phone = data.get('patient_phone')
    patient_id = data.get('patient_id')
    gender = data.get('gender')
    ip_forms_db.append({
        "doctor_name": doctor_name,
        "surgery_name": surgery_name,
        "prescription": [file.filename for file in prescription],
        "patient_name": patient_name,
        "patient_phone": patient_phone,
        "patient_id": patient_id,
        "gender": gender
    })
    return "IP Form submitted successfully!"

@app.route('/patient/<int:patient_id>', methods=['GET'])
def get_patient(patient_id):
    result = []
    for form in op_forms_db:
        if form['patient_id'] == str(patient_id):
            result.append({"source": "OP Form", "details": form})
    for form in ip_forms_db:
        if form['patient_id'] == str(patient_id):
            result.append({"source": "IP Form", "details": form})

    if not result:
        return jsonify({"message": "No records found for this patient ID"}), 404

    return jsonify(result)

            
if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=port, debug=True)
