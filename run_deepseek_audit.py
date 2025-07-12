import os
from openai import OpenAI

client = OpenAI(
    api_key="sk-ccc37a109afb461989af8cf994a8bc60",
    base_url="https://api.deepseek.com/v1"
)

# Test simple de l'API
try:
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": "Tu es un auditeur de système PGI-IA."},
            {"role": "user", "content": "État du système: Backend Flask opérationnel, Docker configuré, Base de données avec projets réels. Évalue la préparation pour présentation actionnaires."}
        ],
        max_tokens=500
    )
    
    print("🎯 Réponse DeepSeek:")
    print(response.choices[0].message.content)
    
    with open("deepseek_audit_result.txt", "w") as f:
        f.write(response.choices[0].message.content)
        
except Exception as e:
    print(f"❌ Erreur DeepSeek: {e}")
