from flask import Flask, request, send_file
import fitz  # PyMuPDF
import io
from datetime import datetime

app = Flask(__name__)

ENGINEER_NAME = "Ahmed Jalil"
COMPANY_NAME = "1 Sparky Ltd"
POSITION = "Skilled person"
PHONE = "07970377375"

FIELD_COORDS = {
    "client_contact": (100, 155),
    "client_address": (100, 180),
    "client_postcode": (100, 210),
    "installation_contact": (350, 155),
    "installation_address": (350, 180),
    "installation_postcode": (350, 210),
    "auto_system_fitted": (100, 285),
    "site_responsible_person": (100, 320),
    "test_date": (500, 410),
    "addition_modification": (100, 485),
    "address_inspection": (100, 810),
    "areas_covered": (350, 810),
}

@app.route("/generate", methods=["POST"])
def generate_pdf():
    data = request.form.to_dict()
    template_path = "template.pdf"

    doc = fitz.open(template_path)
    page1, page3 = doc[0], doc[2]

    page1.insert_text(FIELD_COORDS["client_contact"], data["client_contact"], fontsize=10)
    page1.insert_text(FIELD_COORDS["client_address"], data["client_address"], fontsize=10)
    page1.insert_text(FIELD_COORDS["client_postcode"], data["client_postcode"], fontsize=10)
    page1.insert_text(FIELD_COORDS["installation_contact"], data["installation_contact"], fontsize=10)
    page1.insert_text(FIELD_COORDS["installation_address"], data["installation_address"], fontsize=10)
    page1.insert_text(FIELD_COORDS["installation_postcode"], data["installation_postcode"], fontsize=10)
    page1.insert_text(FIELD_COORDS["auto_system_fitted"], data["auto_system_fitted"], fontsize=10)
    page1.insert_text(FIELD_COORDS["site_responsible_person"], data["site_responsible_person"], fontsize=10)
    page1.insert_text(FIELD_COORDS["test_date"], data.get("test_date", datetime.now().strftime("%d/%m/%Y")), fontsize=10)
    page1.insert_text(FIELD_COORDS["addition_modification"], data["addition_modification"], fontsize=10)

    page3.insert_text(FIELD_COORDS["address_inspection"], data["address_inspection"], fontsize=10)
    page3.insert_text(FIELD_COORDS["areas_covered"], data["areas_covered"], fontsize=10)

    output = io.BytesIO()
    doc.save(output)
    output.seek(0)

    filename = f"FireCert-{data['client_contact'].replace(' ', '_')}-{datetime.now().strftime('%Y%m%d')}.pdf"
    return send_file(output, as_attachment=True, download_name=filename, mimetype='application/pdf')

if __name__ == "__main__":
    app.run(debug=True, port=5000)
