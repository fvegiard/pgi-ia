#!/usr/bin/env python3
"""
PGI-IA Audit Trail System
Pipeline Francis - Point 8: Traçabilité intégrale
"""

import json
import sqlite3
import hashlib
import time
from datetime import datetime
import os
import shutil
import subprocess

class AuditTrailSystem:
    def __init__(self):
        self.db_path = "/mnt/c/Users/fvegi/pgi_ia_audit.db"
        self.archive_dir = "/mnt/c/Users/fvegi/pgi_ia_archives"
        self.init_database()
        self.init_archive()
        
    def init_database(self):
        """Initialize audit trail database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create audit trail table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS audit_trail (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                action_type TEXT NOT NULL,
                action_name TEXT NOT NULL,
                user TEXT DEFAULT 'system',
                details TEXT,
                status TEXT NOT NULL,
                hash TEXT NOT NULL,
                parent_hash TEXT,
                duration_ms REAL
            )
        ''')
        
        # Create system states table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS system_states (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                state_type TEXT NOT NULL,
                state_data TEXT NOT NULL,
                hash TEXT NOT NULL
            )
        ''')
        
        conn.commit()
        conn.close()
        
    def init_archive(self):
        """Initialize archive directory"""
        os.makedirs(self.archive_dir, exist_ok=True)
        
    def calculate_hash(self, data):
        """Calculate SHA256 hash of data"""
        return hashlib.sha256(json.dumps(data, sort_keys=True).encode()).hexdigest()
        
    def log_action(self, action_type, action_name, details=None, status='success', duration_ms=None):
        """Log an action to the audit trail"""
        timestamp = datetime.now().isoformat()
        
        # Get last hash for chain
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT hash FROM audit_trail ORDER BY id DESC LIMIT 1")
        result = cursor.fetchone()
        parent_hash = result[0] if result else "0" * 64
        
        # Create audit entry
        entry = {
            'timestamp': timestamp,
            'action_type': action_type,
            'action_name': action_name,
            'details': details,
            'status': status,
            'parent_hash': parent_hash
        }
        
        entry_hash = self.calculate_hash(entry)
        
        # Insert into database
        cursor.execute('''
            INSERT INTO audit_trail 
            (timestamp, action_type, action_name, details, status, hash, parent_hash, duration_ms)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (timestamp, action_type, action_name, json.dumps(details) if details else None,
              status, entry_hash, parent_hash, duration_ms))
        
        conn.commit()
        conn.close()
        
        print(f"📝 Logged: {action_type} - {action_name} [{status}]")
        return entry_hash
        
    def capture_system_state(self, state_type='full'):
        """Capture current system state"""
        timestamp = datetime.now().isoformat()
        state_data = {}
        
        # Capture running processes
        try:
            result = subprocess.run(['ps', 'aux'], capture_output=True, text=True)
            state_data['processes'] = result.stdout.split('\n')[:50]  # First 50 lines
        except:
            state_data['processes'] = []
            
        # Capture Docker containers
        try:
            result = subprocess.run(['docker', 'ps', '--format', 'json'], capture_output=True, text=True)
            containers = []
            for line in result.stdout.strip().split('\n'):
                if line:
                    containers.append(json.loads(line))
            state_data['docker_containers'] = containers
        except:
            state_data['docker_containers'] = []
            
        # Capture API health
        try:
            import requests
            response = requests.get('http://localhost:5000/health', timeout=5)
            state_data['api_health'] = response.json() if response.status_code == 200 else None
        except:
            state_data['api_health'] = None
            
        # Capture disk usage
        try:
            result = subprocess.run(['df', '-h'], capture_output=True, text=True)
            state_data['disk_usage'] = result.stdout
        except:
            state_data['disk_usage'] = None
            
        # Calculate hash
        state_hash = self.calculate_hash(state_data)
        
        # Store in database
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO system_states (timestamp, state_type, state_data, hash)
            VALUES (?, ?, ?, ?)
        ''', (timestamp, state_type, json.dumps(state_data), state_hash))
        conn.commit()
        conn.close()
        
        # Archive to file
        archive_file = os.path.join(self.archive_dir, f"state_{timestamp.replace(':', '-')}.json")
        with open(archive_file, 'w') as f:
            json.dump({
                'timestamp': timestamp,
                'type': state_type,
                'hash': state_hash,
                'data': state_data
            }, f, indent=2)
            
        print(f"📸 System state captured: {state_hash[:8]}...")
        return state_hash
        
    def verify_integrity(self):
        """Verify audit trail integrity"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM audit_trail ORDER BY id")
        
        issues = []
        prev_hash = "0" * 64
        
        for row in cursor.fetchall():
            # Verify parent hash
            if row[8] != prev_hash:  # parent_hash column
                issues.append(f"Chain broken at ID {row[0]}")
                
            # Verify entry hash
            try:
                details = json.loads(row[4]) if row[4] else None
            except json.JSONDecodeError:
                details = row[4]  # Keep as string if not valid JSON
                
            entry = {
                'timestamp': row[1],
                'action_type': row[2],
                'action_name': row[3],
                'details': details,
                'status': row[5],
                'parent_hash': row[8]
            }
            
            calculated_hash = self.calculate_hash(entry)
            if calculated_hash != row[6]:  # hash column
                issues.append(f"Hash mismatch at ID {row[0]}")
                
            prev_hash = row[6]
            
        conn.close()
        
        return len(issues) == 0, issues
        
    def generate_audit_report(self, start_date=None, end_date=None):
        """Generate audit report"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Build query
        query = "SELECT * FROM audit_trail"
        params = []
        
        if start_date and end_date:
            query += " WHERE timestamp BETWEEN ? AND ?"
            params = [start_date, end_date]
        elif start_date:
            query += " WHERE timestamp >= ?"
            params = [start_date]
        elif end_date:
            query += " WHERE timestamp <= ?"
            params = [end_date]
            
        query += " ORDER BY timestamp DESC"
        
        cursor.execute(query, params)
        
        # Process results
        actions_by_type = {}
        actions_by_status = {'success': 0, 'failure': 0, 'warning': 0}
        total_duration = 0
        action_count = 0
        
        entries = []
        for row in cursor.fetchall():
            entry = {
                'id': row[0],
                'timestamp': row[1],
                'action_type': row[2],
                'action_name': row[3],
                'status': row[5],
                'duration_ms': row[9] if row[9] else 0
            }
            entries.append(entry)
            
            # Statistics
            action_count += 1
            actions_by_type[row[2]] = actions_by_type.get(row[2], 0) + 1
            actions_by_status[row[5]] = actions_by_status.get(row[5], 0) + 1
            if row[9]:
                total_duration += row[9]
                
        conn.close()
        
        # Verify integrity
        integrity_ok, issues = self.verify_integrity()
        
        report = {
            'generated_at': datetime.now().isoformat(),
            'period': {
                'start': start_date or 'beginning',
                'end': end_date or 'now'
            },
            'integrity': {
                'valid': integrity_ok,
                'issues': issues
            },
            'statistics': {
                'total_actions': action_count,
                'by_type': actions_by_type,
                'by_status': actions_by_status,
                'avg_duration_ms': total_duration / action_count if action_count > 0 else 0
            },
            'recent_actions': entries[:10]
        }
        
        # Save report
        report_file = f"/mnt/c/Users/fvegi/pgi_ia_audit_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)
            
        print(f"📊 Audit report generated: {report_file}")
        return report

# Demo usage
if __name__ == "__main__":
    audit = AuditTrailSystem()
    
    print("🔍 PGI-IA AUDIT TRAIL SYSTEM")
    print("=" * 40)
    
    # Log some actions
    print("\n1️⃣ Logging sample actions...")
    
    start_time = time.time()
    audit.log_action('SYSTEM', 'API_START', {'port': 5000}, 'success', 15.2)
    audit.log_action('USER', 'LOGIN', {'user': 'francis'}, 'success', 120.5)
    audit.log_action('API', 'DOCUMENT_UPLOAD', {'file': 'plan.pdf', 'size': '5.3MB'}, 'success', 450.3)
    audit.log_action('AI', 'DEEPSEEK_ANALYSIS', {'model': 'deepseek-reasoner'}, 'success', 2340.1)
    audit.log_action('ERROR', 'DATABASE_CONNECTION', {'error': 'timeout'}, 'failure', 5000.0)
    
    print("\n2️⃣ Capturing system state...")
    audit.capture_system_state()
    
    print("\n3️⃣ Verifying integrity...")
    integrity_ok, issues = audit.verify_integrity()
    print(f"Integrity: {'✅ VALID' if integrity_ok else '❌ INVALID'}")
    if issues:
        for issue in issues:
            print(f"  - {issue}")
            
    print("\n4️⃣ Generating audit report...")
    report = audit.generate_audit_report()
    
    print(f"\nTotal actions logged: {report['statistics']['total_actions']}")
    print(f"Success rate: {report['statistics']['by_status']['success'] / report['statistics']['total_actions'] * 100:.1f}%")
    print(f"Average duration: {report['statistics']['avg_duration_ms']:.1f}ms")