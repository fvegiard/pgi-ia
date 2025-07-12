#!/usr/bin/env python3
"""
Service DeepSeek pour PGI-IA
Analyse IA spécialisée en électricité industrielle
"""

from flask import Flask, request, jsonify
from openai import OpenAI
import os

app = Flask(__name__)

# DeepSeek configuration
DEEPSEEK_API_KEY = os.environ.get('DEEPSEEK_API_KEY', 'sk-ccc37a109afb461989af8cf994a8bc60')
client = OpenAI(
    api_key=DEEPSEEK_API_KEY,
    base_url="https://api.deepseek.com/v1"
)

@app.route('/health')
def health():
    return jsonify({
        "status": "healthy",
        "service": "DeepSeek Service",
        "api_configured": True
    })

@app.route('/analyze', methods=['POST'])
def analyze_electrical():
    """Analyse un document électrique avec DeepSeek"""
    try:
        data = request.json
        if not data or 'text' not in data:
            return jsonify({"error": "No text provided"}), 400
        
        prompt = f"""
        Analyse ce document électrique et identifie:
        1. Type de document (plan, directive, devis)
        2. Éléments techniques clés
        3. Risques ou problèmes potentiels
        4. Recommandations
        
        Document:
        {data['text'][:2000]}  # Limite pour l'API
        """
        
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": "Tu es un expert en électricité industrielle."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=500
        )
        
        return jsonify({
            "analysis": response.choices[0].message.content,
            "model": "deepseek-chat",
            "tokens_used": response.usage.total_tokens if hasattr(response, 'usage') else 0
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5002))
    app.run(host='0.0.0.0', port=port, debug=True)