#!/usr/bin/env python3
"""
Service Gemini pour PGI-IA
Analyse de documents avec Google Gemini
"""

from flask import Flask, request, jsonify
import os

app = Flask(__name__)

# Gemini configuration
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY', '')

@app.route('/health')
def health():
    return jsonify({
        "status": "healthy", 
        "service": "Gemini Service",
        "api_configured": bool(GEMINI_API_KEY)
    })

@app.route('/analyze', methods=['POST'])
def analyze_document():
    """Analyse un document avec Gemini"""
    if not GEMINI_API_KEY:
        return jsonify({"error": "Gemini API key not configured"}), 503
    
    data = request.json
    if not data or 'text' not in data:
        return jsonify({"error": "No text provided"}), 400
    
    # TODO: Implement Gemini analysis when API key is available
    return jsonify({
        "status": "pending",
        "message": "Gemini analysis will be available once API key is configured",
        "text_length": len(data['text'])
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5001))
    app.run(host='0.0.0.0', port=port, debug=True)