from pypdf import PdfReader
import os

pdf_directory = "./papers/"

def extract_text_from_pdf(pdf_file_path):
    reader = PdfReader(pdf_file_path)
    text = ''
    for page in reader.pages:
        text += page.extract_text()
    return text

def get_all_text():
    text_list = {}
    for filename in os.listdir(pdf_directory):
        if filename.endswith(".pdf"):
            filepath = os.path.join(pdf_directory, filename)
            text = extract_text_from_pdf(filepath)
            text_list[filename] = text
    return text_list