#!/usr/bin/env python3
"""
Service OCR pour PGI-IA
Extraction de texte depuis images et PDFs
"""

from flask import Flask, request, jsonify
import easyocr
import PyPDF2
from PIL import Image
import io
import os

app = Flask(__name__)

# Initialize OCR reader (English and French)
reader = easyocr.Reader(['en', 'fr'], gpu=True if os.environ.get('CUDA_VISIBLE_DEVICES') else False)

@app.route('/health')
def health():
    return jsonify({"status": "healthy", "service": "OCR Service", "gpu": bool(os.environ.get('CUDA_VISIBLE_DEVICES'))})

@app.route('/extract', methods=['POST'])
def extract_text():
    """Extrait le texte d'une image ou PDF"""
    try:
        if 'file' not in request.files:
            return jsonify({"error": "No file provided"}), 400
        
        file = request.files['file']
        filename = file.filename.lower()
        
        if filename.endswith(('.png', '.jpg', '.jpeg')):
            # Process image
            image = Image.open(file.stream)
            results = reader.readtext(image)
            text = ' '.join([result[1] for result in results])
            
        elif filename.endswith('.pdf'):
            # Process PDF
            pdf_reader = PyPDF2.PdfReader(file.stream)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
        else:
            return jsonify({"error": "Unsupported file type"}), 400
        
        return jsonify({
            "filename": filename,
            "text": text,
            "length": len(text)
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5003))
    app.run(host='0.0.0.0', port=port, debug=True)