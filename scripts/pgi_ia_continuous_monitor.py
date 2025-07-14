#!/usr/bin/env python3
"""
PGI-IA Continuous Monitoring System
Pipeline Francis - Point 7: Validation continue immédiate
"""

import time
import requests
import psutil
import json
import threading
from datetime import datetime
import subprocess
import os

class ContinuousMonitor:
    def __init__(self):
        self.metrics = {
            'api_health': [],
            'response_times': [],
            'cpu_usage': [],
            'memory_usage': [],
            'container_status': [],
            'error_count': 0,
            'last_check': None
        }
        self.thresholds = {
            'response_time_ms': 100,  # Alert if > 100ms
            'cpu_percent': 80,        # Alert if > 80%
            'memory_percent': 90,     # Alert if > 90%
            'error_rate': 0.1         # Alert if > 10% errors
        }
        self.alerts = []
        self.running = True
        
    def check_api_health(self):
        """Check Flask API health endpoint"""
        try:
            start_time = time.time()
            response = requests.get('http://localhost:5000/health', timeout=5)
            response_time = (time.time() - start_time) * 1000  # ms
            
            if response.status_code == 200:
                data = response.json()
                self.metrics['api_health'].append({
                    'timestamp': datetime.now().isoformat(),
                    'status': 'healthy',
                    'response_time_ms': response_time,
                    'data': data
                })
                self.metrics['response_times'].append(response_time)
                
                # Check response time threshold
                if response_time > self.thresholds['response_time_ms']:
                    self.add_alert('PERFORMANCE', f'API response time {response_time:.1f}ms exceeds threshold')
                    
                return True
            else:
                self.metrics['error_count'] += 1
                return False
                
        except Exception as e:
            self.metrics['error_count'] += 1
            self.add_alert('ERROR', f'API health check failed: {str(e)}')
            return False
            
    def check_system_resources(self):
        """Monitor system CPU and memory"""
        cpu_percent = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        
        self.metrics['cpu_usage'].append({
            'timestamp': datetime.now().isoformat(),
            'percent': cpu_percent
        })
        
        self.metrics['memory_usage'].append({
            'timestamp': datetime.now().isoformat(),
            'percent': memory.percent,
            'used_gb': memory.used / (1024**3),
            'available_gb': memory.available / (1024**3)
        })
        
        # Check thresholds
        if cpu_percent > self.thresholds['cpu_percent']:
            self.add_alert('RESOURCE', f'CPU usage {cpu_percent}% exceeds threshold')
            
        if memory.percent > self.thresholds['memory_percent']:
            self.add_alert('RESOURCE', f'Memory usage {memory.percent}% exceeds threshold')
            
    def check_docker_containers(self):
        """Monitor Docker container status"""
        try:
            cmd = "docker ps --format '{{json .}}'"
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            
            if result.returncode == 0:
                containers = []
                for line in result.stdout.strip().split('\n'):
                    if line:
                        container = json.loads(line)
                        containers.append({
                            'name': container['Names'],
                            'status': container['Status'],
                            'state': container['State']
                        })
                        
                        # Alert on unhealthy containers
                        if 'unhealthy' in container['Status'].lower():
                            self.add_alert('CONTAINER', f"{container['Names']} is unhealthy")
                        elif container['State'] != 'running':
                            self.add_alert('CONTAINER', f"{container['Names']} is not running")
                            
                self.metrics['container_status'] = containers
                
        except Exception as e:
            self.add_alert('ERROR', f'Docker check failed: {str(e)}')
            
    def add_alert(self, alert_type, message):
        """Add alert to the list"""
        alert = {
            'timestamp': datetime.now().isoformat(),
            'type': alert_type,
            'message': message
        }
        self.alerts.append(alert)
        print(f"🚨 ALERT [{alert_type}]: {message}")
        
    def generate_report(self):
        """Generate monitoring report"""
        # Calculate averages
        avg_response_time = sum(self.metrics['response_times']) / len(self.metrics['response_times']) if self.metrics['response_times'] else 0
        avg_cpu = sum([m['percent'] for m in self.metrics['cpu_usage']]) / len(self.metrics['cpu_usage']) if self.metrics['cpu_usage'] else 0
        avg_memory = sum([m['percent'] for m in self.metrics['memory_usage']]) / len(self.metrics['memory_usage']) if self.metrics['memory_usage'] else 0
        
        # Calculate error rate
        total_checks = len(self.metrics['api_health']) + self.metrics['error_count']
        error_rate = self.metrics['error_count'] / total_checks if total_checks > 0 else 0
        
        report = {
            'monitoring_period': {
                'start': self.metrics['api_health'][0]['timestamp'] if self.metrics['api_health'] else None,
                'end': datetime.now().isoformat(),
                'duration_minutes': len(self.metrics['api_health']) * 0.5  # 30s intervals
            },
            'performance': {
                'avg_response_time_ms': round(avg_response_time, 2),
                'max_response_time_ms': max(self.metrics['response_times']) if self.metrics['response_times'] else 0,
                'min_response_time_ms': min(self.metrics['response_times']) if self.metrics['response_times'] else 0
            },
            'resources': {
                'avg_cpu_percent': round(avg_cpu, 2),
                'avg_memory_percent': round(avg_memory, 2),
                'max_cpu_percent': max([m['percent'] for m in self.metrics['cpu_usage']]) if self.metrics['cpu_usage'] else 0,
                'max_memory_percent': max([m['percent'] for m in self.metrics['memory_usage']]) if self.metrics['memory_usage'] else 0
            },
            'reliability': {
                'total_checks': total_checks,
                'successful_checks': len(self.metrics['api_health']),
                'failed_checks': self.metrics['error_count'],
                'error_rate': round(error_rate, 3),
                'uptime_percent': round((1 - error_rate) * 100, 2)
            },
            'alerts': {
                'total': len(self.alerts),
                'by_type': {}
            },
            'current_status': {
                'api': 'healthy' if self.check_api_health() else 'unhealthy',
                'containers': self.metrics['container_status']
            }
        }
        
        # Count alerts by type
        for alert in self.alerts:
            alert_type = alert['type']
            report['alerts']['by_type'][alert_type] = report['alerts']['by_type'].get(alert_type, 0) + 1
            
        return report
        
    def monitor_loop(self):
        """Main monitoring loop"""
        print("🚀 Starting PGI-IA Continuous Monitoring")
        print("=" * 50)
        
        check_count = 0
        while self.running:
            check_count += 1
            print(f"\n⏰ Check #{check_count} at {datetime.now().strftime('%H:%M:%S')}")
            
            # Run all checks
            self.check_api_health()
            self.check_system_resources()
            self.check_docker_containers()
            
            # Show quick status
            if self.metrics['response_times']:
                last_response = self.metrics['response_times'][-1]
                print(f"  API Response: {last_response:.1f}ms")
                
            if self.metrics['cpu_usage']:
                last_cpu = self.metrics['cpu_usage'][-1]['percent']
                print(f"  CPU Usage: {last_cpu}%")
                
            if self.metrics['memory_usage']:
                last_mem = self.metrics['memory_usage'][-1]['percent']
                print(f"  Memory Usage: {last_mem}%")
                
            # Sleep for 30 seconds
            time.sleep(30)
            
            # Generate report every 10 checks (5 minutes)
            if check_count % 10 == 0:
                report = self.generate_report()
                report_file = f"/mnt/c/Users/fvegi/pgi_ia_monitor_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
                with open(report_file, 'w') as f:
                    json.dump(report, f, indent=2)
                print(f"\n📊 Report saved to: {report_file}")
                
    def stop(self):
        """Stop monitoring"""
        self.running = False
        
if __name__ == "__main__":
    import sys
    
    # Check for quick test mode
    quick_test = '--quick' in sys.argv
    
    monitor = ContinuousMonitor()
    
    if quick_test:
        print("🧪 Running quick test (2 checks only)")
        for i in range(2):
            print(f"\n⏰ Check #{i+1} at {datetime.now().strftime('%H:%M:%S')}")
            monitor.check_api_health()
            monitor.check_system_resources()
            monitor.check_docker_containers()
            
            if monitor.metrics['response_times']:
                print(f"  API Response: {monitor.metrics['response_times'][-1]:.1f}ms")
            if monitor.metrics['cpu_usage']:
                print(f"  CPU Usage: {monitor.metrics['cpu_usage'][-1]['percent']}%")
            if monitor.metrics['memory_usage']:
                print(f"  Memory Usage: {monitor.metrics['memory_usage'][-1]['percent']}%")
                
            if i < 1:
                time.sleep(5)
                
        # Generate quick report
        report = monitor.generate_report()
        report_file = f"/mnt/c/Users/fvegi/pgi_ia_monitor_quick_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)
        print(f"\n📊 Quick test report saved to: {report_file}")
    else:
        try:
            # Run monitoring in main thread
            monitor.monitor_loop()
        except KeyboardInterrupt:
            print("\n⏹️  Stopping monitoring...")
            monitor.stop()
            
            # Generate final report
            final_report = monitor.generate_report()
            report_file = f"/mnt/c/Users/fvegi/pgi_ia_monitor_final_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(report_file, 'w') as f:
                json.dump(final_report, f, indent=2)
                
            print(f"\n📊 Final report saved to: {report_file}")
            print("\n🏁 Monitoring stopped")