import os, base64, json
import google.generativeai as genai
from flask import Flask, render_template, make_response, request
from xhtml2pdf import pisa
from pdfminer.high_level import extract_text
from werkzeug.utils import secure_filename
from dotenv import load_dotenv
load_dotenv()

"""
Gemini configurations, IGNORE
"""
API_KEY = os.getenv('API_KEY')
model = 'gemini-pro'
generation_config_b64 = 'eyJ0ZW1wZXJhdHVyZSI6MC43LCJ0b3BfcCI6MC44LCJ0b3BfayI6NDAsIm1heF9vdXRwdXRfdG9rZW5zIjoyMDAwMCwic3RvcF9zZXF1ZW5jZXMiOltdfQ=='
safety_settings_b64 = 'W3siY2F0ZWdvcnkiOiJIQVJNX0NBVEVHT1JZX0hBUkFTU01FTlQiLCJ0aHJlc2hvbGQiOiJCTE9DS19PTkxZX0hJR0gifSx7ImNhdGVnb3J5IjoiSEFSTV9DQVRFR09SWV9IQVRFX1NQRUVDSCIsInRocmVzaG9sZCI6IkJMT0NLX09OTFlfSElHSCJ9LHsiY2F0ZWdvcnkiOiJIQVJNX0NBVEVHT1JZX1NFWFVBTExZX0VYUExJQ0lUIiwidGhyZXNob2xkIjoiQkxPQ0tfT05MWV9ISUdIIn0seyJjYXRlZ29yeSI6IkhBUk1fQ0FURUdPUllfREFOR0VST1VTX0NPTlRFTlQiLCJ0aHJlc2hvbGQiOiJCTE9DS19PTkxZX0hJR0gifV0='
generation_config = json.loads(base64.b64decode(generation_config_b64))
safety_settings = json.loads(base64.b64decode(safety_settings_b64))

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

@app.route('/paraphrase', methods=['POST'])
def paraphrase():
    genai.configure(api_key=API_KEY)
    try:
        text = request.get_json().get('text')
        contents_ = "Your job is to paraphrase the given texts into easier language. Your output should only contain the paraphrased text, no other text, not a thing unrelated. Paraphrase : \"{}\" ".format(text)
        gemini = genai.GenerativeModel(model_name=model)
        response = gemini.generate_content(
            contents_,
            generation_config=generation_config,
            safety_settings=safety_settings,
            stream=False)
        return response.candidates[0].content.parts[0].text
    except:
        return text


if __name__ == '__main__':
    app.run(debug=True)