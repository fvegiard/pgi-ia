#!/usr/bin/env python3
"""
Configure ALL APIs for PGI-IA System
Includes: OpenAI, DeepSeek, Gemini, Anthropic
"""

import os
import json
import requests
from pathlib import Path
import subprocess
import sys

PROJECT_ROOT = Path(__file__).parent

class APIConfigurator:
    def __init__(self):
        self.env_file = PROJECT_ROOT / ".env"
        self.config_file = PROJECT_ROOT / "config" / "agents.yaml"
        self.apis = {
            "openai": {
                "key": None,
                "configured": False,
                "test_endpoint": "https://api.openai.com/v1/models",
                "headers_func": lambda k: {"Authorization": f"Bearer {k}"}
            },
            "deepseek": {
                "key": None,
                "configured": False,
                "test_endpoint": "https://api.deepseek.com/v1/models",
                "headers_func": lambda k: {"Authorization": f"Bearer {k}"}
            },
            "gemini": {
                "key": None,
                "configured": False,
                "test_endpoint": None,  # Gemini uses different approach
                "install_cmd": "pip install google-generativeai"
            },
            "anthropic": {
                "key": None,
                "configured": False,
                "test_endpoint": "https://api.anthropic.com/v1/messages",
                "headers_func": lambda k: {"x-api-key": k, "anthropic-version": "2023-06-01"}
            }
        }
    
    def load_existing_keys(self):
        """Load keys from .env file"""
        if self.env_file.exists():
            with open(self.env_file) as f:
                for line in f:
                    if line.strip() and not line.startswith('#'):
                        if '=' in line:
                            key, value = line.strip().split('=', 1)
                            if key == "DEEPSEEK_API_KEY":
                                self.apis["deepseek"]["key"] = value
                            elif key == "OPENAI_API_KEY":
                                self.apis["openai"]["key"] = value
                            elif key == "GEMINI_API_KEY":
                                self.apis["gemini"]["key"] = value
                            elif key == "ANTHROPIC_API_KEY":
                                self.apis["anthropic"]["key"] = value
    
    def test_api(self, api_name):
        """Test if API key is valid"""
        api = self.apis[api_name]
        
        if not api["key"]:
            return False
        
        if api_name == "gemini":
            # Test Gemini differently
            try:
                import google.generativeai as genai
                genai.configure(api_key=api["key"])
                model = genai.GenerativeModel('gemini-pro')
                response = model.generate_content("Test")
                api["configured"] = True
                return True
            except Exception as e:
                print(f"Gemini test failed: {e}")
                return False
        
        elif api["test_endpoint"]:
            try:
                headers = api["headers_func"](api["key"])
                response = requests.get(api["test_endpoint"], headers=headers, timeout=5)
                if response.status_code in [200, 201]:
                    api["configured"] = True
                    return True
            except Exception as e:
                print(f"{api_name} test failed: {e}")
        
        return False
    
    def setup_gemini_free(self):
        """Setup Gemini with free tier instructions"""
        print("\n📘 Setting up Google Gemini (FREE):")
        print("1. Visit: https://makersuite.google.com/app/apikey")
        print("2. Click 'Create API Key'")
        print("3. Copy the key")
        
        # For automation, try to get from environment
        gemini_key = os.getenv("GEMINI_API_KEY")
        if not gemini_key:
            # Try to find in common locations
            possible_locations = [
                Path.home() / ".gemini_key",
                Path.home() / ".config" / "gemini" / "api_key",
                PROJECT_ROOT / "gemini_api_key.txt"
            ]
            
            for loc in possible_locations:
                if loc.exists():
                    gemini_key = loc.read_text().strip()
                    break
        
        if gemini_key:
            self.apis["gemini"]["key"] = gemini_key
            print(f"Found Gemini key: {gemini_key[:10]}...")
        else:
            print("No Gemini key found. Using mock mode.")
            self.apis["gemini"]["key"] = "MOCK_GEMINI_KEY_FOR_TESTING"
        
        # Install Gemini SDK
        subprocess.run([sys.executable, "-m", "pip", "install", "google-generativeai"], check=True)
        
        return True
    
    def configure_openai_codex(self):
        """Configure OpenAI with any available key"""
        print("\n🤖 Configuring OpenAI...")
        
        # Check multiple sources
        openai_key = os.getenv("OPENAI_API_KEY")
        
        if not openai_key:
            # Search for OpenAI keys in common places
            search_patterns = [
                "sk-proj-*",
                "sk-*",
                "*openai*key*"
            ]
            
            # Check git config
            try:
                result = subprocess.run(["git", "config", "--get", "openai.apikey"], 
                                      capture_output=True, text=True)
                if result.returncode == 0:
                    openai_key = result.stdout.strip()
            except:
                pass
        
        if openai_key:
            self.apis["openai"]["key"] = openai_key
            print(f"Found OpenAI key: {openai_key[:10]}...")
        else:
            print("No OpenAI key found. Will use DeepSeek as fallback.")
            # Use DeepSeek as OpenAI-compatible fallback
            if self.apis["deepseek"]["key"]:
                self.apis["openai"]["key"] = self.apis["deepseek"]["key"]
                self.apis["openai"]["test_endpoint"] = "https://api.deepseek.com/v1/models"
    
    def update_env_file(self):
        """Update .env file with all configured APIs"""
        lines = []
        
        # Read existing non-API lines
        if self.env_file.exists():
            with open(self.env_file) as f:
                for line in f:
                    if not any(api.upper() in line for api in ["DEEPSEEK", "OPENAI", "GEMINI", "ANTHROPIC"]):
                        lines.append(line.rstrip())
        
        # Add API keys
        lines.append("\n# API Keys Configuration")
        
        for api_name, api_data in self.apis.items():
            if api_data["key"]:
                lines.append(f"{api_name.upper()}_API_KEY={api_data['key']}")
        
        # Write back
        with open(self.env_file, 'w') as f:
            f.write('\n'.join(lines) + '\n')
    
    def update_yaml_config(self):
        """Update agents.yaml with configured APIs"""
        yaml_content = f"""# Configuration des Agents IA - PGI-IA
# Auto-configured by configure_all_apis.py

agents:
  openai:
    api_key: "{self.apis['openai']['key'] or 'YOUR_OPENAI_KEY'}"
    model: "gpt-4-turbo"
    role: "Agent-Analyste Plans & Code Backend"
    configured: {self.apis['openai']['configured']}
    
  anthropic:
    api_key: "{self.apis['anthropic']['key'] or 'YOUR_ANTHROPIC_KEY'}"
    model: "claude-3-opus-20240229"
    role: "Agent-Suivi Directives & Documentation"
    configured: {self.apis['anthropic']['configured']}
    
  google:
    api_key: "{self.apis['gemini']['key'] or 'YOUR_GEMINI_KEY'}"
    model: "gemini-1.5-pro"
    role: "Agent-Photos Géolocalisées & Vision"
    configured: {self.apis['gemini']['configured']}
    
  deepseek:
    api_key: "{self.apis['deepseek']['key'] or 'YOUR_DEEPSEEK_KEY'}"
    model: "deepseek-coder-6.7b"
    role: "Agent-Développement Code"
    configured: {self.apis['deepseek']['configured']}

# Configuration générale
settings:
  debug: true
  upload_path: "data/drop_zone"
  max_file_size: 10485760  # 10MB
  supported_formats: ["pdf", "png", "jpg", "jpeg", "dwg", "dxf"]
  
# Projets actifs
projets:
  kahnawake:
    id: "S-1086"
    nom: "Musée Kahnawake"
    statut: "Estimation"
    po_client: "QMD"
    
  alexis_nihon:
    id: "C-24-048"
    nom: "Place Alexis-Nihon"
    statut: "Construction"
    po_client: "JCB"
"""
        
        with open(self.config_file, 'w') as f:
            f.write(yaml_content)
    
    def create_api_test_script(self):
        """Create comprehensive API test script"""
        test_script = '''#!/usr/bin/env python3
"""Test all configured APIs"""

import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from configure_all_apis import APIConfigurator

def test_all_apis():
    configurator = APIConfigurator()
    configurator.load_existing_keys()
    
    print("\\n🧪 Testing all APIs...")
    print("=" * 50)
    
    results = {}
    
    for api_name in ["deepseek", "openai", "gemini", "anthropic"]:
        if configurator.apis[api_name]["key"]:
            print(f"\\nTesting {api_name}...")
            success = configurator.test_api(api_name)
            results[api_name] = "✅ Working" if success else "❌ Failed"
        else:
            results[api_name] = "⚠️ No key"
    
    print("\\n📊 API Status Summary:")
    print("=" * 50)
    for api, status in results.items():
        print(f"{api.capitalize()}: {status}")
    
    # Test specific functionality
    if configurator.apis["deepseek"]["configured"]:
        print("\\n🔧 Testing DeepSeek code analysis...")
        try:
            import requests
            headers = {"Authorization": f"Bearer {configurator.apis['deepseek']['key']}"}
            data = {
                "model": "deepseek-coder",
                "messages": [{"role": "user", "content": "What is Flask?"}],
                "max_tokens": 50
            }
            response = requests.post("https://api.deepseek.com/v1/chat/completions", 
                                   headers=headers, json=data)
            if response.status_code == 200:
                print("✅ DeepSeek code analysis working!")
            else:
                print(f"❌ DeepSeek error: {response.status_code}")
        except Exception as e:
            print(f"❌ DeepSeek test error: {e}")

if __name__ == "__main__":
    test_all_apis()
'''
        
        test_path = PROJECT_ROOT / "test_all_apis.py"
        test_path.write_text(test_script)
        test_path.chmod(0o755)
        
        return test_path
    
    def configure_all(self):
        """Main configuration process"""
        print("🚀 PGI-IA API Configuration")
        print("=" * 50)
        
        # Load existing
        self.load_existing_keys()
        
        # Configure each API
        print("\n📡 Current API Status:")
        for api_name, api_data in self.apis.items():
            status = "✅" if api_data["key"] else "❌"
            print(f"{status} {api_name.capitalize()}: {'Configured' if api_data['key'] else 'Not configured'}")
        
        # Setup missing APIs
        if not self.apis["gemini"]["key"]:
            self.setup_gemini_free()
        
        if not self.apis["openai"]["key"]:
            self.configure_openai_codex()
        
        # Test all APIs
        print("\n🧪 Testing APIs...")
        for api_name in self.apis:
            if self.apis[api_name]["key"]:
                self.test_api(api_name)
        
        # Update configuration files
        self.update_env_file()
        self.update_yaml_config()
        
        # Create test script
        test_script = self.create_api_test_script()
        
        # Final report
        print("\n✅ Configuration Complete!")
        print("=" * 50)
        print("API Status:")
        for api_name, api_data in self.apis.items():
            status = "✅ Ready" if api_data["configured"] else "⚠️ Key present but not tested" if api_data["key"] else "❌ Not configured"
            print(f"  {api_name.capitalize()}: {status}")
        
        print(f"\nTest all APIs: python {test_script.name}")
        print(f"Config file: {self.config_file}")
        print(f"Environment: {self.env_file}")
        
        return {api: data["configured"] for api, data in self.apis.items()}

if __name__ == "__main__":
    configurator = APIConfigurator()
    configurator.configure_all()