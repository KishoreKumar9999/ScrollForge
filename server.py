import os
from flask import Flask, render_template, send_from_directory

app = Flask(__name__)

PDF_DIR = "pdfs"

@app.route('/')
def home():
    pdf_files = [f for f in os.listdir(PDF_DIR) if f.endswith(".pdf")]
    return render_template("index.html", pdf_files = pdf_files)

@app.route('/pdf/<filename>')
def serve_pdf(filename):
    return send_from_directory(PDF_DIR, filename)
    

if __name__ == "__main__":
    app.run(debug=True)