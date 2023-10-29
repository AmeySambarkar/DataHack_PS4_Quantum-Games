import os
from flask import Flask, request, send_file, jsonify
from flask_cors import CORS
#import MarianMT

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:5500"}})

# Define the folder where PDFs will be stored
pdf_folder = "uploads/"

# Ensure the PDF folder exists
if not os.path.exists(pdf_folder):
    os.makedirs(pdf_folder)

# API to upload a PDF
@app.route('/upload', methods=['POST'])
def upload_pdf():
    if 'pdf' not in request.files:
        return jsonify({"error": "No file part"})

    pdf_file = request.files['pdf']
    if pdf_file.filename == '':
        return jsonify({"error": "No selected file"})

    if pdf_file:
        pdf_file.save(os.path.join(pdf_folder, pdf_file.filename))
        return jsonify({"message": "File uploaded successfully"})

# API to list available PDFs
@app.route('/listpdf', methods=['GET'])
def list_pdfs():
    pdfs = os.listdir(pdf_folder)
    return jsonify({"pdfs": pdfs})

# API to download a specific PDF
@app.route('/download/<pdf_name>', methods=['GET'])
def download_pdf(pdf_name):
    pdf_path = os.path.join(pdf_folder, pdf_name)
    if os.path.exists(pdf_path):
        return send_file(pdf_path, as_attachment=True)
    else:
        return jsonify({"error": "File not found"})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
