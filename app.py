from flask import Flask, request, jsonify, render_template
from ai_detector import ai_likelihood
from similarity import compute_similarity
from docx import Document
from PyPDF2 import PdfReader
from internet_similarity import internet_plagiarism

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 5 * 1024 * 1024

@app.route("/")
def home():
    return render_template("index.html")

def read_txt(file):
    return file.read().decode("utf-8", errors="ignore")

def read_pdf(file):
    reader = PdfReader(file)
    return "".join(page.extract_text() or "" for page in reader.pages)

def read_docx(file):
    doc = Document(file)
    return "\n".join(p.text for p in doc.paragraphs)

@app.route("/detect", methods=["POST"])
def detect_ai():
    text = request.form.get("text", "")

    if "file" in request.files:
        file = request.files["file"]
        name = file.filename.lower()

        if name.endswith(".txt"):
            text = read_txt(file)
        elif name.endswith(".pdf"):
            text = read_pdf(file)
        elif name.endswith(".docx"):
            text = read_docx(file)
        else:
            return jsonify({"error": "Unsupported file type"}), 400

    if not text.strip():
        return jsonify({"error": "No text provided"}), 400

    return jsonify(ai_likelihood(text))
@app.route("/similarity", methods=["POST"])
def detect_similarity():
    try:
        text1 = request.form.get("text1", "")
        text2 = request.form.get("text2", "")

        if not text1.strip() or not text2.strip():
            return jsonify({"error": "Two texts required"}), 400

        result = compute_similarity(text1, text2)
        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/internet_check", methods=["POST"])
def internet_check():
    text = request.form.get("text", "")
    if not text.strip():
        return jsonify({"error": "No text provided"}), 400
    return jsonify(internet_plagiarism(text))

if __name__ == "__main__":
    app.run(debug=True)
