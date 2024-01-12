import os, base64, json
import google.generativeai as genai
from flask import Flask, render_template, make_response, request, flash
from xhtml2pdf import pisa
from pdfminer.high_level import extract_text
from werkzeug.utils import secure_filename
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.docstore.document import Document
from langchain.prompts import PromptTemplate
from langchain.chains.summarize import load_summarize_chain
from langchain.text_splitter import RecursiveCharacterTextSplitter
import langchain_gemini_utils as lg
from dotenv import load_dotenv
load_dotenv()

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
def paraphrase_route():
    try:
        text = request.get_json().get('text')
        paraphrased_text = lg.paraphrase(text)
        return paraphrased_text
    except Exception as e:
        flash(f'Text not paraphrased due to an error: {str(e)}')
        return request.get_json().get('text')

@app.route('/summarise', methods=['POST'])
def summarise_route():
    try:
        text = request.get_json().get('text')
        summarized_text = lg.summarise(text)
        return summarized_text
    except Exception as e:
        flash(f'Text not summarised due to an error: {str(e)}')
        return request.get_json().get('text')



if __name__ == '__main__':
    app.run(debug=True)