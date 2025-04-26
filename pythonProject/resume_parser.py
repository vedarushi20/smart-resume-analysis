import fitz  # PyMuPDF
import spacy

nlp = spacy.load("en_core_web_sm")

def extract_text(pdf_file):
    doc = fitz.open(stream=pdf_file.read(), filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def extract_skills(text):
    doc = nlp(text.lower())
    keywords = ["python", "ml", "data", "sql", "java", "nlp", "flask"]
    return [token.text for token in doc if token.text in keywords]


# skills_list.txt contains a list of valid skill keywords
def extract_skills(text):
    with open("skills_list.txt", "r") as f:
        keywords = [line.strip().lower() for line in f]

    words = text.lower().split()
    found_skills = [word for word in words if word in keywords]
    return list(set(found_skills))
