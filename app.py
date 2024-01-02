import os
from flask import Flask, render_template, make_response, request
from xhtml2pdf import pisa
from pdfminer.high_level import extract_text
from werkzeug.utils import secure_filename

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.htm')

@app.route('/generate-pdf', methods=['POST'])
def generate_pdf():
    html_content = request.get_json().get('html_content')
    pdf_file = open('generated.pdf', 'w+b')
    pisa.CreatePDF(html_content, dest=pdf_file)
    pdf_file.close()
    response = None
    with open('generated.pdf', 'rb') as pdf:
        response = make_response(pdf.read())
        response.headers['Content-Disposition'] = 'inline; filename=output.pdf'
        response.headers['Content-Type'] = 'application/pdf'
    os.remove('generated.pdf')
    return response

@app.route('/upload-pdf', methods=['POST'])
def upload_pdf():
   pdf_file = request.files['pdf']
   filename = secure_filename(pdf_file.filename)
   pdf_path = os.path.join('temp', filename)
   pdf_file.save(pdf_path)
   text = extract_text(pdf_path)
   os.remove(pdf_path)
   return text

if __name__ == '__main__':
    app.run(debug=True)