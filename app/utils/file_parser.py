from PyPDF2 import PdfReader

def extract_text_from_pdf(file):
    reader = PdfReader(file)
    return "\n".join([page.extract_text() for page in reader.pages if page.extract_text()])

def extract_text_from_txt(file):
    return file.read().decode("utf-8")