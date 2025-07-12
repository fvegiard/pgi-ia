#!/usr/bin/env python3
"""Test all configured APIs"""

import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from configure_all_apis import APIConfigurator

def test_all_apis():
    configurator = APIConfigurator()
    configurator.load_existing_keys()
    
    print("\n🧪 Testing all APIs...")
    print("=" * 50)
    
    results = {}
    
    for api_name in ["deepseek", "openai", "gemini", "anthropic"]:
        if configurator.apis[api_name]["key"]:
            print(f"\nTesting {api_name}...")
            success = configurator.test_api(api_name)
            results[api_name] = "✅ Working" if success else "❌ Failed"
        else:
            results[api_name] = "⚠️ No key"
    
    print("\n📊 API Status Summary:")
    print("=" * 50)
    for api, status in results.items():
        print(f"{api.capitalize()}: {status}")
    
    # Test specific functionality
    if configurator.apis["deepseek"]["configured"]:
        print("\n🔧 Testing DeepSeek code analysis...")
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
