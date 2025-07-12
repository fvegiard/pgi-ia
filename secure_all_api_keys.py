#!/usr/bin/env python3
"""
Secure all API keys in the project
Replace hardcoded keys with environment variables
"""

import os
import re
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent

# Files to update
files_to_update = {
    "backend/main.py": {
        'DEEPSEEK_API_KEY = "sk-ccc37a109afb461989af8cf994a8bc60"': 
        'DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY", "")'
    },
    "backend/services/deepseek_service.py": {
        "DEEPSEEK_API_KEY = os.environ.get('DEEPSEEK_API_KEY', 'sk-ccc37a109afb461989af8cf994a8bc60')":
        'DEEPSEEK_API_KEY = os.environ.get("DEEPSEEK_API_KEY", "")'
    },
    "add_ai_analysis.py": {
        'DEEPSEEK_API_KEY = "sk-ccc37a109afb461989af8cf994a8bc60"':
        'DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY", "")'
    },
    "backend_with_ai.py": {
        'DEEPSEEK_API_KEY = "sk-ccc37a109afb461989af8cf994a8bc60"':
        'DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY", "")'
    },
    "force_analyze.py": {
        'DEEPSEEK_API_KEY = "sk-ccc37a109afb461989af8cf994a8bc60"':
        'DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY", "")'
    }
}

# Process each file
for file_path, replacements in files_to_update.items():
    full_path = PROJECT_ROOT / file_path
    if full_path.exists():
        print(f"Securing {file_path}...")
        
        with open(full_path, 'r') as f:
            content = f.read()
        
        # Make replacements
        for old_text, new_text in replacements.items():
            if old_text in content:
                content = content.replace(old_text, new_text)
                print(f"  ✅ Replaced hardcoded key")
        
        # Add import os if needed
        if "import os" not in content and "os.getenv" in content:
            # Add after other imports
            import_pos = content.find("import")
            if import_pos >= 0:
                # Find end of import section
                lines = content.split('\n')
                for i, line in enumerate(lines):
                    if line.startswith("import") or line.startswith("from"):
                        continue
                    else:
                        if i > 0:
                            lines.insert(i, "import os")
                            content = '\n'.join(lines)
                            break
        
        # Write back
        with open(full_path, 'w') as f:
            f.write(content)

# Update YAML files
yaml_files = {
    "config/agents.yaml": {
        'api_key: "sk-ccc37a109afb461989af8cf994a8bc60"':
        'api_key: "${DEEPSEEK_API_KEY}"',
        'api_key: "sk-xxxxxxxx"':
        'api_key: "${OPENAI_API_KEY}"'
    }
}

for file_path, replacements in yaml_files.items():
    full_path = PROJECT_ROOT / file_path
    if full_path.exists():
        print(f"Securing {file_path}...")
        
        with open(full_path, 'r') as f:
            content = f.read()
        
        for old_text, new_text in replacements.items():
            if old_text in content:
                content = content.replace(old_text, new_text)
                print(f"  ✅ Replaced hardcoded key")
        
        with open(full_path, 'w') as f:
            f.write(content)

# Update documentation files to remove exposed keys
doc_files = {
    "DOCKER_GUIDE.md": {
        "sk-ccc37a109afb461989af8cf994a8bc60": "${DEEPSEEK_API_KEY}",
        "sk-proj-...": "${OPENAI_API_KEY}",
        "sk-ant-...": "${ANTHROPIC_API_KEY}"
    },
    "NEXT_CHAT_INSTRUCTIONS.md": {
        "sk-ccc37a109afb461989af8cf994a8bc60": "${DEEPSEEK_API_KEY}"
    },
    "SYSTEM_100_PERCENT_REPORT.md": {
        "sk-ccc37a109afb461989af8cf994a8bc60": "${DEEPSEEK_API_KEY}",
        "sk-proj-a9ep26vz6IqS...": "${OPENAI_API_KEY}"
    }
}

for file_path, replacements in doc_files.items():
    full_path = PROJECT_ROOT / file_path
    if full_path.exists():
        print(f"Securing {file_path}...")
        
        with open(full_path, 'r') as f:
            content = f.read()
        
        for old_text, new_text in replacements.items():
            if old_text in content:
                content = content.replace(old_text, new_text)
                print(f"  ✅ Replaced exposed key")
        
        with open(full_path, 'w') as f:
            f.write(content)

# Create a secure environment template
env_template = """# Configuration des clés API pour PGI-IA
# COPIER ce fichier vers .env et remplacer les valeurs

# OpenAI API (obtenir sur https://platform.openai.com/api-keys)
OPENAI_API_KEY=your_openai_key_here

# DeepSeek API (obtenir sur https://platform.deepseek.com)
DEEPSEEK_API_KEY=your_deepseek_key_here

# Google Gemini (obtenir sur https://makersuite.google.com/app/apikey)
GEMINI_API_KEY=your_gemini_key_here

# Anthropic Claude (obtenir sur https://console.anthropic.com)
ANTHROPIC_API_KEY=your_anthropic_key_here
"""

env_template_path = PROJECT_ROOT / ".env.template"
with open(env_template_path, 'w') as f:
    f.write(env_template)

print(f"\n✅ Created {env_template_path}")

# Update .gitignore to ensure .env is ignored
gitignore_path = PROJECT_ROOT / ".gitignore"
gitignore_content = ""

if gitignore_path.exists():
    with open(gitignore_path, 'r') as f:
        gitignore_content = f.read()

if ".env" not in gitignore_content:
    with open(gitignore_path, 'a') as f:
        f.write("\n# Environment variables\n.env\n.env.local\n.env.*.local\n")
    print("✅ Updated .gitignore")

print("\n🔒 Security update complete!")
print("\nNOTE: Les clés API sont maintenant sécurisées:")
print("1. Utilisez les variables d'environnement du fichier .env")
print("2. Ne committez JAMAIS le fichier .env")
print("3. Utilisez .env.template comme modèle")
print("\nPour configurer vos clés:")
print("  cp .env.template .env")
print("  # Éditez .env avec vos vraies clés")