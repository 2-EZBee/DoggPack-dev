#!/usr/bin/env python3
"""
DoggPack Connectivity Validation Tool

Validates port allocations, network connectivity, and service configurations
to prevent conflicts and ensure optimal deployment.
"""

import yaml
import socket
import subprocess
import ipaddress
import sys
import argparse
from collections import defaultdict, Counter
from pathlib import Path
from typing import Dict, List, Tuple, Set

class ConnectivityValidator:
    def __init__(self, config_file: str = None):
        """Initialize the validator with configuration"""
        self.config_file = config_file or "planning/specifications/connectivity-port-mapping.yml"
        self.config = {}
        self.errors = []
        self.warnings = []
        self.port_allocations = defaultdict(list)
        self.ip_allocations = {}
        
    def load_config(self) -> bool:
        """Load the connectivity configuration file"""
        try:
            config_path = Path(self.config_file)
            if not config_path.exists():
                self.errors.append(f"Configuration file not found: {self.config_file}")
                return False
                
            with open(config_path, 'r') as f:
                self.config = yaml.safe_load(f)
            print(f"✅ Loaded configuration from {self.config_file}")
            return True
        except Exception as e:
            self.errors.append(f"Failed to load configuration: {e}")
            return False
    
    def validate_port_conflicts(self) -> bool:
        """Check for port conflicts across all services"""
        print("\n🔍 Validating port allocations...")
        
        # Collect all port allocations
        services = {}
        
        # Foundation services
        if 'foundation_services' in self.config:
            services.update(self.config['foundation_services'])
            
        # Application services
        if 'application_services' in self.config:
            services.update(self.config['application_services'])
            
        # Monitoring stack
        if 'monitoring_stack' in self.config:
            services.update(self.config['monitoring_stack'])
            
        # Development environments
        if 'development_environments' in self.config:
            services.update(self.config['development_environments'])
            
        # Check for port conflicts
        port_conflicts = defaultdict(list)
        
        for service_name, service_config in services.items():
            if isinstance(service_config, dict):
                host_ip = service_config.get('host_ip', 'unknown')
                host_port = service_config.get('host_port')
                ssh_port = service_config.get('ssh_port')
                vnc_port = service_config.get('vnc_port')
                
                # Check host ports
                if host_port:
                    key = f"{host_ip}:{host_port}"
                    port_conflicts[key].append(f"{service_name} (host_port)")
                    self.port_allocations[host_ip].append(host_port)
                
                # Check SSH ports
                if ssh_port:
                    key = f"{host_ip}:{ssh_port}"
                    port_conflicts[key].append(f"{service_name} (ssh_port)")
                    self.port_allocations[host_ip].append(ssh_port)
                
                # Check VNC ports
                if vnc_port:
                    key = f"{host_ip}:{vnc_port}"
                    port_conflicts[key].append(f"{service_name} (vnc_port)")
                    self.port_allocations[host_ip].append(vnc_port)
        
        # Report conflicts
        conflicts_found = False
        for port_key, service_list in port_conflicts.items():
            if len(service_list) > 1:
                self.errors.append(f"Port conflict on {port_key}: {', '.join(service_list)}")
                conflicts_found = True
        
        if not conflicts_found:
            print("   ✅ No port conflicts detected")
        
        return not conflicts_found
    
    def validate_ip_assignments(self) -> bool:
        """Validate IP address assignments and subnets"""
        print("\n🌐 Validating IP address assignments...")
        
        # Check physical infrastructure IPs
        if 'network_architecture' in self.config:
            phys_infra = self.config['network_architecture'].get('physical_infrastructure', {})
            
            for machine_name, machine_config in phys_infra.items():
                ip = machine_config.get('ip')
                if ip:
                    try:
                        ip_obj = ipaddress.IPv4Address(ip)
                        # Check if IP is in the infrastructure VLAN
                        infra_network = ipaddress.IPv4Network('192.168.10.0/24')
                        if ip_obj not in infra_network:
                            self.warnings.append(f"Machine {machine_name} IP {ip} not in infrastructure VLAN")
                        
                        self.ip_allocations[ip] = machine_name
                    except Exception as e:
                        self.errors.append(f"Invalid IP address for {machine_name}: {ip}")
        
        # Check Docker network subnets
        if 'docker_networking' in self.config:
            docker_nets = self.config['docker_networking'].get('swarm_networks', {})
            
            for net_name, net_config in docker_nets.items():
                subnet = net_config.get('subnet')
                if subnet:
                    try:
                        net_obj = ipaddress.IPv4Network(subnet)
                        print(f"   ✅ Docker network {net_name}: {subnet}")
                    except Exception as e:
                        self.errors.append(f"Invalid subnet for Docker network {net_name}: {subnet}")
        
        return len([e for e in self.errors if 'IP' in e or 'subnet' in e]) == 0
    
    def validate_port_ranges(self) -> bool:
        """Validate that services are using appropriate port ranges"""
        print("\n📊 Validating port range compliance...")
        
        if 'port_allocation' not in self.config:
            self.warnings.append("No port allocation ranges defined")
            return True
            
        port_ranges = self.config['port_allocation'].get('port_ranges', {})
        range_violations = []
        
        # Parse port ranges
        ranges = {}
        for range_name, range_str in port_ranges.items():
            if '-' in range_str:
                start, end = map(int, range_str.split('-'))
                ranges[range_name] = (start, end)
        
        # Check services against ranges
        services = {}
        if 'foundation_services' in self.config:
            services.update(self.config['foundation_services'])
        if 'application_services' in self.config:
            services.update(self.config['application_services'])
        if 'monitoring_stack' in self.config:
            services.update(self.config['monitoring_stack'])
            
        for service_name, service_config in services.items():
            if isinstance(service_config, dict):
                host_port = service_config.get('host_port')
                if host_port:
                    # Determine expected range based on service type
                    expected_range = None
                    if 'mcp' in service_name.lower() or 'coordinator' in service_name.lower():
                        expected_range = 'mcp_servers'
                    elif 'monitoring' in service_name.lower() or 'prometheus' in service_name.lower():
                        expected_range = 'monitoring'
                    elif 'api' in service_name.lower() or 'gateway' in service_name.lower():
                        expected_range = 'web_interfaces'
                    
                    if expected_range and expected_range in ranges:
                        start, end = ranges[expected_range]
                        if not (start <= host_port <= end):
                            range_violations.append(
                                f"{service_name} port {host_port} outside expected range {expected_range} ({start}-{end})"
                            )
        
        if range_violations:
            for violation in range_violations:
                self.warnings.append(violation)
        else:
            print("   ✅ All services using appropriate port ranges")
            
        return True
    
    def validate_domain_mappings(self) -> bool:
        """Validate domain name mappings and DNS configuration"""
        print("\n🌍 Validating domain mappings...")
        
        if 'domain_mapping' not in self.config:
            self.warnings.append("No domain mapping configuration found")
            return True
            
        domain_config = self.config['domain_mapping']
        
        # Check internal domains
        internal_domains = domain_config.get('internal_domains', {})
        if 'records' in internal_domains:
            for record in internal_domains['records']:
                name = record.get('name')
                record_type = record.get('type')
                value = record.get('value')
                
                if record_type == 'A':
                    try:
                        ipaddress.IPv4Address(value)
                        print(f"   ✅ Internal A record: {name}.doggpack.local → {value}")
                    except Exception:
                        self.errors.append(f"Invalid IP in A record: {name} → {value}")
                elif record_type == 'CNAME':
                    print(f"   ✅ Internal CNAME record: {name}.doggpack.local → {value}")
        
        # Check external domains
        external_domains = domain_config.get('external_domains', {})
        if 'records' in external_domains:
            for record in external_domains['records']:
                name = record.get('name')
                record_type = record.get('type')
                value = record.get('value')
                proxied = record.get('proxied', False)
                
                print(f"   ✅ External {record_type} record: {name}.doggpack.net → {value} (Proxied: {proxied})")
        
        return len([e for e in self.errors if 'domain' in e.lower()]) == 0
    
    def check_system_ports(self) -> bool:
        """Check if any allocated ports conflict with system/reserved ports"""
        print("\n⚠️  Checking for system port conflicts...")
        
        if 'port_allocation' not in self.config:
            return True
            
        reserved_ports = self.config['port_allocation'].get('reserved_system_ports', [])
        
        conflicts = []
        for host_ip, ports in self.port_allocations.items():
            for port in ports:
                if port in reserved_ports:
                    conflicts.append(f"Service port {port} on {host_ip} conflicts with reserved system port")
        
        if conflicts:
            for conflict in conflicts:
                self.errors.append(conflict)
        else:
            print("   ✅ No conflicts with reserved system ports")
            
        return len(conflicts) == 0
    
    def validate_docker_networking(self) -> bool:
        """Validate Docker networking configuration"""
        print("\n🐳 Validating Docker networking...")
        
        if 'docker_networking' not in self.config:
            self.warnings.append("No Docker networking configuration found")
            return True
            
        docker_config = self.config['docker_networking']
        
        # Check overlay networks don't overlap
        overlay_networks = docker_config.get('swarm_networks', {})
        networks = []
        
        for net_name, net_config in overlay_networks.items():
            subnet = net_config.get('subnet')
            if subnet:
                try:
                    net_obj = ipaddress.IPv4Network(subnet)
                    networks.append((net_name, net_obj))
                except Exception as e:
                    self.errors.append(f"Invalid Docker network subnet {net_name}: {subnet}")
        
        # Check for overlapping networks
        for i, (name1, net1) in enumerate(networks):
            for name2, net2 in networks[i+1:]:
                if net1.overlaps(net2):
                    self.errors.append(f"Docker networks overlap: {name1} ({net1}) and {name2} ({net2})")
        
        if not any('Docker networks overlap' in e for e in self.errors):
            print(f"   ✅ {len(networks)} Docker overlay networks configured without overlap")
            
        return len([e for e in self.errors if 'Docker' in e]) == 0
    
    def check_port_availability(self, host_ips: List[str] = None) -> bool:
        """Check if ports are actually available on target hosts"""
        print("\n🔌 Checking port availability on target hosts...")
        
        if not host_ips:
            # Use IPs from configuration
            host_ips = []
            if 'network_architecture' in self.config:
                phys_infra = self.config['network_architecture'].get('physical_infrastructure', {})
                host_ips = [config.get('ip') for config in phys_infra.values() if config.get('ip')]
        
        availability_issues = []
        
        for host_ip in host_ips:
            if host_ip in self.port_allocations:
                ports_to_check = self.port_allocations[host_ip]
                
                for port in ports_to_check:
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.settimeout(1)
                    
                    try:
                        result = sock.connect_ex((host_ip, port))
                        if result == 0:
                            # Port is open - might be in use
                            availability_issues.append(f"Port {port} appears to be in use on {host_ip}")
                        else:
                            # Port is available
                            pass
                    except Exception as e:
                        self.warnings.append(f"Could not check port {port} on {host_ip}: {e}")
                    finally:
                        sock.close()
        
        if availability_issues:
            for issue in availability_issues:
                self.warnings.append(issue)
        else:
            print(f"   ✅ All allocated ports appear available on target hosts")
            
        return True
    
    def generate_port_summary(self) -> None:
        """Generate a summary of port allocations"""
        print("\n📋 Port Allocation Summary:")
        print("=" * 50)
        
        for host_ip, ports in self.port_allocations.items():
            hostname = self.ip_allocations.get(host_ip, host_ip)
            ports_sorted = sorted(set(ports))
            print(f"\n{hostname} ({host_ip}):")
            
            # Group consecutive ports
            if ports_sorted:
                ranges = []
                start = end = ports_sorted[0]
                
                for port in ports_sorted[1:]:
                    if port == end + 1:
                        end = port
                    else:
                        if start == end:
                            ranges.append(str(start))
                        else:
                            ranges.append(f"{start}-{end}")
                        start = end = port
                
                # Add the last range
                if start == end:
                    ranges.append(str(start))
                else:
                    ranges.append(f"{start}-{end}")
                
                print(f"   Ports: {', '.join(ranges)}")
                print(f"   Total: {len(ports_sorted)} ports")
    
    def run_validation(self, check_availability: bool = False) -> bool:
        """Run all validation checks"""
        print("🔍 DoggPack Connectivity Validation")
        print("=" * 40)
        
        if not self.load_config():
            return False
        
        validation_passed = True
        
        # Run all validation checks
        validation_passed &= self.validate_port_conflicts()
        validation_passed &= self.validate_ip_assignments()
        validation_passed &= self.validate_port_ranges()
        validation_passed &= self.validate_domain_mappings()
        validation_passed &= self.check_system_ports()
        validation_passed &= self.validate_docker_networking()
        
        if check_availability:
            validation_passed &= self.check_port_availability()
        
        # Generate summary
        self.generate_port_summary()
        
        # Report results
        print(f"\n📊 Validation Results:")
        print(f"   Errors: {len(self.errors)}")
        print(f"   Warnings: {len(self.warnings)}")
        
        if self.errors:
            print(f"\n❌ Errors found:")
            for error in self.errors:
                print(f"   • {error}")
        
        if self.warnings:
            print(f"\n⚠️  Warnings:")
            for warning in self.warnings:
                print(f"   • {warning}")
        
        if validation_passed and not self.errors:
            print(f"\n✅ Connectivity validation passed!")
            print(f"   Ready for deployment with {len(self.port_allocations)} hosts configured")
            return True
        else:
            print(f"\n❌ Validation failed - please fix errors before deployment")
            return False

def main():
    parser = argparse.ArgumentParser(description='Validate DoggPack connectivity configuration')
    parser.add_argument('--config', '-c', 
                       help='Path to connectivity configuration file',
                       default='planning/specifications/connectivity-port-mapping.yml')
    parser.add_argument('--check-availability', '-a', 
                       action='store_true',
                       help='Check if ports are actually available on target hosts')
    parser.add_argument('--summary-only', '-s',
                       action='store_true', 
                       help='Only show port allocation summary')
    
    args = parser.parse_args()
    
    validator = ConnectivityValidator(args.config)
    
    if args.summary_only:
        if validator.load_config():
            # Just collect port allocations and show summary
            validator.validate_port_conflicts()  # This populates the port allocations
            validator.generate_port_summary()
        return
    
    success = validator.run_validation(check_availability=args.check_availability)
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
