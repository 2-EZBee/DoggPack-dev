# DoggPack Network Infrastructure Security Guide

## Overview

This guide provides a comprehensive plan to transform your current FZNet into a secure, segmented, and remotely accessible network infrastructure optimized for the DoggPack ecosystem.

## Current Network Analysis

Based on your network export, here's what we're working with:

### **Current Setup**
- **Network**: FZNet (192.168.68.0/24)
- **Gateway**: 192.168.68.1
- **DNS**: 1.1.1.1 (Cloudflare)
- **ISP**: Aussie Broadband
- **Key Devices**: NasDogg (Synology), Gaming devices, Smart home devices, Personal devices

### **Identified Security Risks**
1. **Flat Network**: All devices on same subnet (security risk)
2. **No Network Segmentation**: Smart home devices can access everything
3. **Limited Remote Access**: No secure VPN for remote management
4. **Basic DNS**: No local DNS server for custom domains
5. **Unorganized IP Allocation**: Devices scattered across IP range

## Proposed Network Architecture

### **VLAN Segmentation Strategy**

```
┌─────────────────────────────────────────────────────────────┐
│                    Router (192.168.x.1)                    │
│                     Gateway & VPN                          │
└─────────────┬───────────────┬───────────┬──────────────────┘
              │               │           │
    ┌─────────▼─────────┐  ┌──▼────┐  ┌──▼──────┐
    │   Infrastructure  │  │Gaming │  │Personal │
    │   VLAN 10         │  │VLAN 30│  │VLAN 40  │
    │ 192.168.10.0/24   │  │.30.0  │  │.40.0    │
    │                   │  │       │  │         │
    │ • NasDogg (.40)   │  │• Xbox │  │• Phones │
    │ • NucDogg (.50)   │  │• Games│  │• Tablets│
    │ • WorkDogg (.51)  │  │       │  │• Guests │
    │ • ZenDogg (.52)   │  │       │  │         │
    └───────┬───────────┘  └───────┘  └─────────┘
            │
    ┌───────▼───────┐
    │   SmartHome   │
    │   VLAN 20     │
    │ 192.168.20.0  │
    │               │
    │ • Tuya devices│
    │ • Nest Hub    │
    │ • IoT devices │
    └───────────────┘
```

### **Security Zones**

1. **Infrastructure Zone (VLAN 10)** - Highest Security
   - DoggPack core machines
   - Network services (DNS, monitoring)
   - Full access to all zones for management

2. **Smart Home Zone (VLAN 20)** - Isolated
   - IoT devices with internet access only
   - No access to other zones
   - Restricted outbound connections

3. **Gaming Zone (VLAN 30)** - Performance Optimized
   - Gaming consoles and entertainment
   - QoS prioritization
   - Limited cross-zone access

4. **Personal Zone (VLAN 40)** - Standard Access
   - Personal devices and guests
   - Internet access and limited infrastructure access
   - BYOD policy enforcement

## Implementation Plan

### **Phase 1: Network Preparation (15 minutes)**

1. **Backup Current Configuration**
   ```bash
   # Document current network state
   ip route show
   arp -a
   nmap -sn 192.168.68.0/24
   ```

2. **Create Network Diagram**
   - Document all current device locations
   - Plan new IP assignments
   - Identify critical services

### **Phase 2: Router Configuration (30 minutes)**

1. **Create VLANs**
   ```
   VLAN 10: Infrastructure (192.168.10.0/24)
   VLAN 20: SmartHome (192.168.20.0/24)
   VLAN 30: Gaming (192.168.30.0/24)
   VLAN 40: Personal (192.168.40.0/24)
   ```

2. **Configure Inter-VLAN Routing**
   ```
   Infrastructure → All VLANs (management)
   Personal → Infrastructure (limited services)
   Gaming → Internet only
   SmartHome → Internet only
   ```

3. **Set Up Firewall Rules**
   ```
   DENY SmartHome → Infrastructure
   DENY SmartHome → Personal
   DENY Gaming → Infrastructure
   ALLOW Infrastructure → All
   ALLOW Personal → Infrastructure (ports 80, 443, 53)
   ```

### **Phase 3: DNS Server Setup (20 minutes)**

1. **Configure NasDogg as DNS Server**
   ```bash
   # On Synology NasDogg
   # Enable DNS Server package
   # Configure forwarders: 1.1.1.1, 1.0.0.1
   # Create local zone: doggpack.local
   ```

2. **Create Local DNS Records**
   ```
   nasdogg.doggpack.local  → 192.168.10.40
   nucdogg.doggpack.local  → 192.168.10.50
   workdogg.doggpack.local → 192.168.10.51
   zendogg.doggpack.local  → 192.168.10.52
   mcp.doggpack.local      → 192.168.10.50
   docker.doggpack.local   → 192.168.10.50
   ```

### **Phase 4: VPN Configuration (25 minutes)**

1. **Enable OpenVPN Server**
   ```bash
   # Router configuration
   Port: 1194 (UDP)
   Encryption: AES-256
   Authentication: Certificate + Password
   ```

2. **Create VPN Certificates**
   ```bash
   # Generate CA and server certificates
   # Create client certificates for each user
   # Configure client profiles with appropriate network access
   ```

3. **Configure VPN Access Levels**
   ```
   Admin Profile: Full network access
   User Profile: Infrastructure zone only
   ReadOnly Profile: Monitoring access only
   ```

### **Phase 5: Dynamic DNS Setup (15 minutes)**

1. **Configure DDNS Service**
   ```bash
   # Router DDNS settings
   Service: Cloudflare or No-IP
   Domain: doggpack.net
   Update interval: 5 minutes
   ```

2. **Verify External Access**
   ```bash
   nslookup vpn.doggpack.net
   ping vpn.doggpack.net
   ```

### **Phase 6: Cloudflare Integration (20 minutes)**

1. **Create DNS Records**
   ```
   A     vpn.doggpack.net      → Dynamic IP (Not Proxied)
   A     home.doggpack.net     → Dynamic IP (Proxied)
   CNAME mcp.doggpack.net      → home.doggpack.net (Proxied)
   CNAME remote.doggpack.net   → home.doggpack.net (Proxied)
   ```

2. **Configure Security Settings**
   ```
   SSL Mode: Full (Strict)
   Min TLS Version: 1.2
   Security Level: Medium
   Always Use HTTPS: Enabled
   ```

### **Phase 7: RDP Configuration (25 minutes)**

1. **Configure Custom RDP Ports**
   ```
   NucDogg:  External 3390 → Internal 3389
   WorkDogg: External 3391 → Internal 3389
   ZenDogg:  External 3392 → Internal 3389
   ```

2. **Enable Network Level Authentication**
   ```bash
   # On each Windows machine
   # System Properties → Remote → Enable NLA
   # Windows Firewall → Allow RDP through firewall
   # Configure custom port if needed
   ```

3. **Create Firewall Rules**
   ```
   Allow VPN → RDP ports
   Deny Internet → RDP ports
   Log all RDP connection attempts
   ```

### **Phase 8: SSH Configuration (15 minutes)**

1. **Configure SSH on Linux Machines**
   ```bash
   # NucDogg
   sudo ufw allow 2222/tcp
   sudo systemctl enable ssh
   
   # WorkDogg
   sudo ufw allow 2223/tcp
   sudo systemctl enable ssh
   ```

2. **Set Up Key-Based Authentication**
   ```bash
   # Generate SSH keys
   ssh-keygen -t ed25519 -C "doggpack-admin"
   
   # Copy to machines
   ssh-copy-id -p 2222 user@nucdogg.doggpack.local
   ssh-copy-id -p 2223 user@workdogg.doggpack.local
   ```

## Security Best Practices

### **Immediate Actions**
1. **Change Default Passwords**
   - Router admin password
   - All device passwords
   - WiFi passwords (use WPA3)

2. **Disable Unnecessary Services**
   - WPS on WiFi
   - Telnet on devices
   - Default SNMP communities

3. **Enable Logging**
   - Router firewall logs
   - VPN connection logs
   - Failed authentication attempts

### **Ongoing Security**
1. **Regular Updates**
   - Router firmware monthly
   - Device security patches
   - VPN certificate renewal

2. **Monitoring**
   - Network traffic analysis
   - Unusual connection patterns
   - Failed login attempts

3. **Access Reviews**
   - Quarterly user access review
   - VPN certificate audit
   - Device inventory updates

## Remote Access Guide

### **VPN Connection**
1. **Install OpenVPN Client**
2. **Import Client Certificate**
3. **Connect to vpn.doggpack.net:1194**
4. **Access internal services via local domains**

### **RDP Access Through VPN**
```bash
# Connect to VPN first, then:
mstsc /v:nucdogg.doggpack.local:3389   # NucDogg
mstsc /v:workdogg.doggpack.local:3389  # WorkDogg
mstsc /v:zendogg.doggpack.local:3389   # ZenDogg
```

### **SSH Access Through VPN**
```bash
# Connect to VPN first, then:
ssh -p 2222 user@nucdogg.doggpack.local
ssh -p 2223 user@workdogg.doggpack.local
```

### **Direct External Access (Emergency)**
```bash
# If VPN fails, use external ports:
mstsc /v:home.doggpack.net:3390  # NucDogg RDP
mstsc /v:home.doggpack.net:3391  # WorkDogg RDP
mstsc /v:home.doggpack.net:3392  # ZenDogg RDP

ssh -p 2222 user@home.doggpack.net  # NucDogg SSH
ssh -p 2223 user@home.doggpack.net  # WorkDogg SSH
```

## Testing Procedures

### **Network Connectivity Tests**
```bash
# From each VLAN, test:
ping 8.8.8.8                    # Internet connectivity
ping nasdogg.doggpack.local     # Local DNS resolution
nslookup google.com             # External DNS resolution
```

### **Security Validation**
```bash
# Port scanning from external network
nmap -sS home.doggpack.net

# Expected open ports:
# 1194 (VPN)
# 3390-3392 (RDP)
# 2222-2223 (SSH)
```

### **VPN Testing**
```bash
# Connect VPN and test access
curl http://nasdogg.doggpack.local  # Should work
curl http://192.168.10.50:8080      # MCP services
```

## Troubleshooting Guide

### **Common Issues**

1. **Cannot Access Local Domains**
   - Check DNS server configuration
   - Verify DHCP is assigning correct DNS server
   - Clear DNS cache: `ipconfig /flushdns`

2. **VPN Connection Fails**
   - Check router VPN server status
   - Verify port 1194 UDP is open
   - Check certificate validity

3. **RDP Connection Refused**
   - Verify RDP is enabled on target machine
   - Check firewall rules
   - Test from same VLAN first

4. **Inter-VLAN Communication Issues**
   - Verify VLAN configuration
   - Check firewall rules
   - Test with ping first

### **Emergency Rollback**
If anything goes wrong:
1. **Restore router backup**
2. **Disable VLANs (return to flat network)**
3. **Reset DNS to 1.1.1.1**
4. **Test basic internet connectivity**

## Maintenance Schedule

### **Weekly**
- Review VPN connection logs
- Check for firmware updates
- Monitor network traffic patterns

### **Monthly**
- Update router firmware
- Review firewall logs
- Test backup connectivity methods

### **Quarterly**
- Full security audit
- VPN certificate review
- Access permission review
- Network performance analysis

## Integration with DoggPack

### **MCP Server Access**
```bash
# Once VPN connected:
curl http://mcp.doggpack.local:8100/health      # Planning coordinator
curl http://docker.doggpack.local:2376/version  # Docker API
```

### **Docker Swarm Management**
```bash
# Remote Docker Swarm management
export DOCKER_HOST=tcp://docker.doggpack.local:2376
docker node ls
docker service ls
```

### **Development Environment**
```bash
# SSH into development containers
ssh -p 2200 claude@nucdogg.doggpack.local  # CCN dev environment
ssh -p 2201 claude@workdogg.doggpack.local # CCW dev environment
```

This network infrastructure provides a secure, scalable foundation for the DoggPack ecosystem while maintaining easy remote access and proper security segmentation. The combination of VPN access, network segmentation, and local DNS creates a professional-grade home network infrastructure.

**Next Steps:**
1. Review the deployment plan thoroughly
2. Schedule a maintenance window for implementation
3. Prepare backup connectivity method
4. Execute the plan step by step with validation at each stage
