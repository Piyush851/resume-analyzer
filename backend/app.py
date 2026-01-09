import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename
from utils import extract_text_from_pdf, clean_text, extract_skills

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {'pdf'}

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload-resume', methods=['POST'])
def upload_resume():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)

        # Save file temporarily
        file.save(filepath)

        raw_text = extract_text_from_pdf(filepath)
        cleaned_text = clean_text(raw_text)

        skills_data = extract_skills(cleaned_text)

        os.remove(filepath)

        return jsonify({
            "message": "File processed successfully",
            "extracted_text": cleaned_text,
            "skills_found": skills_data
        }), 200

    return jsonify({"error": "Invalid file type. Only PDFs allowed"}), 400

if __name__ == "__main__":
    app.run(debug=True, port=5000)