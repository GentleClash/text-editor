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
from dotenv import load_dotenv
load_dotenv()

"""
Gemini configurations, IGNORE
"""
API_KEY = os.getenv('API_KEY')
model = 'gemini-pro'
generation_config_b64 = 'eyJ0ZW1wZXJhdHVyZSI6MC43LCJ0b3BfcCI6MC44LCJ0b3BfayI6NDAsIm1heF9vdXRwdXRfdG9rZW5zIjoyMDAwMCwic3RvcF9zZXF1ZW5jZXMiOltdfQ=='
safety_settings_b64 = 'W3siY2F0ZWdvcnkiOiJIQVJNX0NBVEVHT1JZX0hBUkFTU01FTlQiLCJ0aHJlc2hvbGQiOiJCTE9DS19PTkxZX0hJR0gifSx7ImNhdGVnb3J5IjoiSEFSTV9DQVRFR09SWV9IQVRFX1NQRUVDSCIsInRocmVzaG9sZCI6IkJMT0NLX09OTFlfSElHSCJ9LHsiY2F0ZWdvcnkiOiJIQVJNX0NBVEVHT1JZX1NFWFVBTExZX0VYUExJQ0lUIiwidGhyZXNob2xkIjoiQkxPQ0tfT05MWV9ISUdIIn0seyJjYXRlZ29yeSI6IkhBUk1fQ0FURUdPUllfREFOR0VST1VTX0NPTlRFTlQiLCJ0aHJlc2hvbGQiOiJCTE9DS19PTkxZX0hJR0gifV0='
question_prompt_template = """
                  Please provide a summary of the following text.Return your response in parts separated by individual headings that covers the key points of the text. 
                  Do NOT use markdown format. Do not make summary too short.
                  TEXT: {text}
                  SUMMARY:
                  """
refine_prompt_template = """
              "Your job is to produce a final summary\n"
    "We have provided an existing summary up to a certain point: {existing_answer}\n"
    "We have the opportunity to refine the existing summary"
    "(only if needed) with some more context below.\n"
    "------------\n"
    "{text}\n"
    "------------\n"
              Return your response in parts separated by individual headings that covers the key points of the text. Do NOT use markdown format. Do not make the summary too short
              SUMMARY:
              """

generation_config = json.loads(base64.b64decode(generation_config_b64))
safety_settings = json.loads(base64.b64decode(safety_settings_b64))
genai.configure(api_key=API_KEY)
llm = ChatGoogleGenerativeAI(model="gemini-pro", google_api_key=API_KEY, \
                                 safety_settings=safety_settings, generation_config=generation_config)
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
    try:
        text = request.get_json().get('text')
        contents_ = "Your job is to paraphrase the given texts into easier language. Your output should only contain the paraphrased text, no other text, not a thing unrelated, not even inverted commas. Paraphrase : \"{}\" ".format(text)
        gemini = genai.GenerativeModel(model_name=model)
        response = gemini.generate_content(
            contents_,
            generation_config=generation_config,
            safety_settings=safety_settings,
            stream=False)
        return response.candidates[0].content.parts[0].text
    except Exception as e:
        flash('Text not paraphrased due to an error : {}'.format(str(e)))
        return text

@app.route('/summarise', methods=['POST'])
def summarise():
    try:
        text=request.get_json().get('text')
        text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=10000, chunk_overlap=1000
        )
        split_docs = text_splitter.split_text(text)
        split_docs = [Document(page_content=t) for t in split_docs]
        question_prompt = PromptTemplate(
        template=question_prompt_template, input_variables=["text"]
        )
        refine_prompt = PromptTemplate(
        template=refine_prompt_template, input_variables=["text"]
        )
        refine_chain = load_summarize_chain(
        llm,
        chain_type="refine",
        question_prompt=question_prompt,
        refine_prompt=refine_prompt,
        return_intermediate_steps=False
        )
        result = refine_chain({"input_documents": split_docs}, return_only_outputs=True)
        return result["output_text"]
    except Exception as e:
        flash('Text not summarised due to an error : {}'.format(str(e)))
        return text



if __name__ == '__main__':
    app.run(debug=True)