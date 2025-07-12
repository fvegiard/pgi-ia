#!/usr/bin/env python3
"""
PGI-IA Complete System Test
Tests all components to ensure 100% functionality
"""

import os
import sys
import time
import json
import requests
import subprocess
from pathlib import Path
from datetime import datetime
import sqlite3

PROJECT_ROOT = Path(__file__).parent
sys.path.append(str(PROJECT_ROOT))

class SystemTester:
    def __init__(self):
        self.results = {
            "timestamp": datetime.now().isoformat(),
            "tests": {},
            "overall_status": "UNKNOWN",
            "ready_percentage": 0
        }
        self.backend_url = "http://localhost:5000"
    
    def test_environment(self):
        """Test environment setup"""
        print("\n🔍 Testing Environment...")
        test_name = "environment"
        self.results["tests"][test_name] = {}
        
        checks = {
            "venv": (PROJECT_ROOT / "venv_pgi_ia").exists(),
            "database": (PROJECT_ROOT / "pgi_ia.db").exists(),
            "uploads_dir": (PROJECT_ROOT / "uploads").exists(),
            "frontend": (PROJECT_ROOT / "frontend" / "dashboard.html").exists(),
            "env_file": (PROJECT_ROOT / ".env").exists()
        }
        
        for check, result in checks.items():
            self.results["tests"][test_name][check] = result
            print(f"  {check}: {'✅' if result else '❌'}")
        
        return all(checks.values())
    
    def test_gpu(self):
        """Test GPU availability"""
        print("\n🎮 Testing GPU...")
        test_name = "gpu"
        self.results["tests"][test_name] = {}
        
        try:
            result = subprocess.run(["nvidia-smi", "--query-gpu=name,memory.total", "--format=csv,noheader"],
                                  capture_output=True, text=True)
            if result.returncode == 0:
                gpu_info = result.stdout.strip()
                self.results["tests"][test_name]["available"] = True
                self.results["tests"][test_name]["info"] = gpu_info
                print(f"  GPU: ✅ {gpu_info}")
                return True
        except:
            pass
        
        self.results["tests"][test_name]["available"] = False
        print("  GPU: ⚠️ Not available (CPU mode)")
        return True  # Not critical
    
    def test_backend(self):
        """Test backend API"""
        print("\n🌐 Testing Backend...")
        test_name = "backend"
        self.results["tests"][test_name] = {}
        
        endpoints = [
            ("/health", "GET", None),
            ("/api/documents", "GET", None),
            ("/api/status", "GET", None)
        ]
        
        all_ok = True
        for endpoint, method, data in endpoints:
            try:
                if method == "GET":
                    response = requests.get(f"{self.backend_url}{endpoint}", timeout=5)
                else:
                    response = requests.post(f"{self.backend_url}{endpoint}", json=data, timeout=5)
                
                success = response.status_code in [200, 201]
                self.results["tests"][test_name][endpoint] = success
                print(f"  {endpoint}: {'✅' if success else '❌'} ({response.status_code})")
                
                if not success:
                    all_ok = False
            except Exception as e:
                self.results["tests"][test_name][endpoint] = False
                print(f"  {endpoint}: ❌ ({str(e)})")
                all_ok = False
        
        return all_ok
    
    def test_apis(self):
        """Test all configured APIs"""
        print("\n🔌 Testing APIs...")
        test_name = "apis"
        self.results["tests"][test_name] = {}
        
        # Load API keys
        env_path = PROJECT_ROOT / ".env"
        apis = {}
        
        if env_path.exists():
            with open(env_path) as f:
                for line in f:
                    if "API_KEY=" in line and not line.startswith("#"):
                        parts = line.strip().split("=", 1)
                        if len(parts) == 2:
                            api_name = parts[0].replace("_API_KEY", "").lower()
                            apis[api_name] = parts[1]
        
        # Test each API
        for api_name, api_key in apis.items():
            if api_key and api_key != "YOUR_" + api_name.upper() + "_KEY":
                if api_name == "deepseek":
                    # Test DeepSeek
                    try:
                        headers = {"Authorization": f"Bearer {api_key}"}
                        response = requests.get("https://api.deepseek.com/v1/models", 
                                              headers=headers, timeout=5)
                        success = response.status_code == 200
                        self.results["tests"][test_name][api_name] = success
                        print(f"  {api_name}: {'✅' if success else '❌'}")
                    except:
                        self.results["tests"][test_name][api_name] = False
                        print(f"  {api_name}: ❌")
                else:
                    self.results["tests"][test_name][api_name] = True
                    print(f"  {api_name}: ✅ (key present)")
            else:
                self.results["tests"][test_name][api_name] = False
                print(f"  {api_name}: ⚠️ Not configured")
        
        return len([v for v in self.results["tests"][test_name].values() if v]) > 0
    
    def test_database(self):
        """Test database functionality"""
        print("\n🗄️ Testing Database...")
        test_name = "database"
        self.results["tests"][test_name] = {}
        
        db_path = PROJECT_ROOT / "pgi_ia.db"
        
        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            # Check tables
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = cursor.fetchall()
            
            self.results["tests"][test_name]["connected"] = True
            self.results["tests"][test_name]["tables"] = len(tables)
            
            print(f"  Connection: ✅")
            print(f"  Tables: {len(tables)}")
            
            # Check for data
            if tables:
                cursor.execute("SELECT COUNT(*) FROM documents")
                doc_count = cursor.fetchone()[0]
                self.results["tests"][test_name]["documents"] = doc_count
                print(f"  Documents: {doc_count}")
            
            conn.close()
            return True
            
        except Exception as e:
            self.results["tests"][test_name]["connected"] = False
            self.results["tests"][test_name]["error"] = str(e)
            print(f"  Database: ❌ ({str(e)})")
            return False
    
    def test_services(self):
        """Test additional services"""
        print("\n⚙️ Testing Services...")
        test_name = "services"
        self.results["tests"][test_name] = {}
        
        # Check if email watcher exists
        email_watcher = PROJECT_ROOT / "backend" / "workers" / "email_watcher.py"
        self.results["tests"][test_name]["email_watcher"] = email_watcher.exists()
        print(f"  Email Watcher: {'✅' if email_watcher.exists() else '❌'}")
        
        # Check Docker setup
        dockerfile = PROJECT_ROOT / "Dockerfile"
        docker_compose = PROJECT_ROOT / "docker-compose.yml"
        self.results["tests"][test_name]["docker"] = dockerfile.exists() and docker_compose.exists()
        print(f"  Docker Setup: {'✅' if dockerfile.exists() else '❌'}")
        
        # Check startup script
        startup_script = PROJECT_ROOT / "start_pgi_ia_auto.sh"
        self.results["tests"][test_name]["startup_script"] = startup_script.exists()
        print(f"  Startup Script: {'✅' if startup_script.exists() else '❌'}")
        
        return True
    
    def calculate_readiness(self):
        """Calculate overall system readiness"""
        total_tests = 0
        passed_tests = 0
        
        critical_weights = {
            "environment": 2,
            "backend": 3,
            "database": 2,
            "apis": 1,
            "gpu": 0.5,
            "services": 1
        }
        
        total_weight = sum(critical_weights.values())
        weighted_score = 0
        
        for test_category, results in self.results["tests"].items():
            if isinstance(results, dict):
                category_passed = sum(1 for v in results.values() if v)
                category_total = len(results)
                
                if category_total > 0:
                    category_score = category_passed / category_total
                    weight = critical_weights.get(test_category, 1)
                    weighted_score += category_score * weight
                    
                    total_tests += category_total
                    passed_tests += category_passed
        
        self.results["ready_percentage"] = round((weighted_score / total_weight) * 100, 1)
        self.results["tests_passed"] = f"{passed_tests}/{total_tests}"
        
        if self.results["ready_percentage"] >= 90:
            self.results["overall_status"] = "PRODUCTION_READY"
        elif self.results["ready_percentage"] >= 70:
            self.results["overall_status"] = "FUNCTIONAL"
        elif self.results["ready_percentage"] >= 50:
            self.results["overall_status"] = "PARTIAL"
        else:
            self.results["overall_status"] = "NOT_READY"
    
    def generate_report(self):
        """Generate final report"""
        print("\n" + "=" * 60)
        print("📊 PGI-IA SYSTEM TEST REPORT")
        print("=" * 60)
        
        print(f"\n🎯 Overall Status: {self.results['overall_status']}")
        print(f"📈 System Readiness: {self.results['ready_percentage']}%")
        print(f"✅ Tests Passed: {self.results['tests_passed']}")
        
        print("\n📋 Recommendations:")
        
        if self.results["ready_percentage"] < 100:
            if not self.results["tests"].get("apis", {}).get("gemini"):
                print("  - Configure Gemini API for PDF analysis")
            
            if not self.results["tests"].get("backend", {}).get("/api/documents"):
                print("  - Fix backend document endpoints")
            
            if not self.results["tests"].get("gpu", {}).get("available"):
                print("  - Consider using GPU for faster processing")
            
            if self.results["tests"].get("database", {}).get("documents", 0) == 0:
                print("  - Upload test documents to validate pipeline")
        else:
            print("  ✅ System is fully operational!")
        
        # Save report
        report_path = PROJECT_ROOT / "test_results.json"
        with open(report_path, 'w') as f:
            json.dump(self.results, f, indent=2)
        
        print(f"\n💾 Detailed report saved to: {report_path}")
        
        return self.results
    
    def run_all_tests(self):
        """Run all system tests"""
        print("🚀 Starting PGI-IA Complete System Test...")
        print("=" * 60)
        
        # Check if backend is running
        try:
            response = requests.get(f"{self.backend_url}/health", timeout=2)
            backend_running = response.status_code == 200
        except:
            backend_running = False
        
        if not backend_running:
            print("⚠️ Backend not running. Starting it now...")
            # Start backend in background
            subprocess.Popen([
                sys.executable, 
                str(PROJECT_ROOT / "backend" / "main.py")
            ])
            time.sleep(5)  # Wait for startup
        
        # Run tests
        test_functions = [
            self.test_environment,
            self.test_gpu,
            self.test_backend,
            self.test_apis,
            self.test_database,
            self.test_services
        ]
        
        for test_func in test_functions:
            try:
                test_func()
            except Exception as e:
                print(f"  Error in {test_func.__name__}: {str(e)}")
        
        # Calculate readiness
        self.calculate_readiness()
        
        # Generate report
        return self.generate_report()

def main():
    """Main entry point"""
    tester = SystemTester()
    results = tester.run_all_tests()
    
    # Exit code based on readiness
    if results["ready_percentage"] >= 90:
        sys.exit(0)  # Success
    else:
        sys.exit(1)  # Needs attention

if __name__ == "__main__":
    main()