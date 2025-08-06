# DoggPack Single-Network Security Implementation Guide

## 🎯 Overview

This guide provides a comprehensive implementation plan for securing the DoggPack network within the constraints of the TP-Link Deco X20 DSL consumer mesh system. **VLAN segmentation is NOT available**, so we implement a multi-layered security approach using available Deco features.

## 🚨 Critical Discovery: Hardware Limitations

### **TP-Link Deco X20 DSL Reality Check**
- ❌ **No VLAN support** for internal LAN segmentation
- ❌ **No enterprise firewall** with advanced rule creation
- ❌ **No port-based VLANs** or switch management
- ✅ **Consumer features available**: Guest Network, Access Control, Basic Firewall, VPN Server

### **Previous VLAN-Based Plan: ABANDONED**
- All documentation referencing VLANs 10, 20, 30, 40 is **obsolete**
- Network segmentation must be achieved through alternative methods
- Security strategy completely redesigned for single flat network

---

## 🏗️ **Current Network Architecture**

### **Single Network Configuration**
```
Network:      192.168.68.0/24 (Flat network - cannot be changed)
Gateway:      192.168.68.1 (TP-Link Deco X20 DSL)
DHCP Range:   192.168.68.100-250
DNS Server:   192.168.68.40 (NasDogg - Phase 1 Complete ✅)
Internet:     144.6.156.14/22 (VDSL2: 82.9/22.6 Mbps)
```

### **Device Categories**
```
DoggPack Infrastructure (192.168.68.50-52):
  - Highest security requirements
  - Full network management access
  - Critical service hosting

Smart Home/IoT (192.168.68.100-150):
  - Must be isolated from infrastructure
  - Internet access only
  - No lateral movement allowed

Gaming/Media (192.168.68.151-200):
  - Standard access with QoS priority
  - Internet + local media sharing
  - Limited infrastructure access

Personal/Mobile (192.168.68.201-250):
  - Standard access for trusted devices
  - Limited infrastructure service access
  - Guest access capabilities
```

---

## 🛡️ **Multi-Layered Security Strategy**

### **Security Layer Overview**
```
┌─────────────────────────────────────────────┐
│         Layer 5: Monitoring & Response      │
│  ┌───────────────────────────────────────┐  │
│  │      Layer 4: Application Security    │  │
│  │  ┌─────────────────────────────────┐  │  │
│  │  │   Layer 3: Software-Defined     │  │  │
│  │  │         Perimeter (VPN)         │  │  │
│  │  │  ┌───────────────────────────┐  │  │  │
│  │  │  │ Layer 2: Firewall Rules   │  │  │  │
│  │  │  │    & Access Control       │  │  │  │
│  │  │  │  ┌─────────────────────┐  │  │  │  │
│  │  │  │  │ Layer 1: WiFi-Based │  │  │  │  │
│  │  │  │  │   Segmentation      │  │  │  │  │
│  │  │  │  └─────────────────────┘  │  │  │  │
│  │  │  └───────────────────────────┘  │  │  │
│  │  └─────────────────────────────────┘  │  │
│  └───────────────────────────────────────┘  │
└─────────────────────────────────────────────┘
```

---

## 📋 **Implementation Plan**

## **Phase 1: DNS Server ✅ ALREADY COMPLETE**

**Status**: 100% Operational
- DNS server running on NasDogg (192.168.68.40)
- Local domains (.doggpack.local) resolving correctly
- External DNS forwarding through Cloudflare (1.1.1.1)
- No action required - foundation is solid

---

## **Phase 2: Single-Network Security Implementation**

### **Step 1: WiFi-Based Segmentation (15 minutes)**

#### **Enable Guest Network for IoT Isolation**
```bash
# Access Deco app or web interface (192.168.68.1)
# Navigate: Network Settings → Guest Network

Configuration:
  Network Name: DoggPackIoT
  Password: [Generate strong 16-character password]
  Access: Isolated from main network ✅
  Internet Access: Enabled ✅
  Bandwidth Limit: 50% of total (optional)
  Time Restrictions: None (24/7 access)
```

#### **Main Network Configuration**
```bash
Main Network: DoggPackNet (existing)
Purpose: Infrastructure + trusted devices
Access: Full network access
DNS: 192.168.68.40 (NasDogg)
```

#### **Device Assignment Strategy**
```bash
Move to Guest Network (DoggPackIoT):
  - All Tuya smart devices
  - Nest Hub and Google devices  
  - Unknown/untrusted IoT devices
  - Any device that doesn't need infrastructure access

Keep on Main Network:
  - DoggPack infrastructure (NasDogg, NucDogg, WorkDogg, ZenDogg)
  - Gaming consoles (Xbox, PlayStation)
  - Personal computers and phones
  - Trusted media devices
```

### **Step 2: Access Control Rules (20 minutes)**

#### **Deco Access Control Configuration**
```bash
# Deco App → More → Security → Access Control

Create Rule: "Block IoT to Infrastructure"
  Source: Guest Network devices (or specific MAC addresses)
  Destination: 192.168.68.40-52 (Infrastructure range)
  Action: Block
  Schedule: Always
  Logging: Enabled

Create Rule: "Block IoT to Admin Ports"
  Source: Guest Network devices
  Destination: Any, Ports 22,23,80,443,3389,5000-5050
  Action: Block
  Schedule: Always
  Logging: Enabled

Create Rule: "Infrastructure Management Access"
  Source: 192.168.68.50-52 (Infrastructure devices)
  Destination: Any
  Action: Allow
  Schedule: Always
  Logging: Enabled (for audit)
```

#### **Device-Based Access Control**
```bash
# For devices that can't be moved to guest network:

High Priority (No Restrictions):
  - DoggPack infrastructure (MAC addresses)
  - Primary workstations
  - Network admin devices

Medium Priority (Limited Access):
  - Gaming consoles → Block ports 22,23,3389,5432
  - Media devices → Block management ports
  - Personal phones → Allow most access

Low Priority (Heavily Restricted):
  - IoT devices remaining on main network
  - Unknown devices → Block all non-web traffic
  - Guest devices → Time-based restrictions
```

### **Step 3: VPN Server Configuration (25 minutes)**

#### **Enable OpenVPN Server**
```bash
# Deco App → More → Advanced → VPN Server

OpenVPN Configuration:
  Protocol: UDP
  Port: 1194
  Encryption: AES-256-CBC
  Authentication: SHA256
  Compression: Enabled
  External Access: Auto (DDNS)
```

#### **Certificate Generation**
```bash
# Deco will generate certificates automatically
# Download client configurations:

admin.ovpn:
  - Full network access
  - No restrictions
  - For system administrators

user.ovpn:
  - Limited to infrastructure services
  - Block access to other client devices
  - For regular users

readonly.ovpn:
  - Monitoring access only
  - Read-only access to status pages
  - For monitoring systems
```

#### **External Access Configuration**
```bash
# Dynamic DNS setup (if not already configured):
Service: Deco built-in DDNS or No-IP
Domain: doggpack.net (register if needed)
Update: Automatic

# Firewall rule will be auto-created for port 1194 UDP
# Test from external network: OpenVPN client to doggpack.net:1194
```

### **Step 4: Firewall Rules & Port Forwarding (20 minutes)**

#### **Essential Port Forwarding (Emergency Access)**
```bash
# Deco App → More → Advanced → Port Forwarding

Emergency RDP Access:
  Service Name: "NucDogg Emergency RDP"
  External Port: 3390
  Internal IP: 192.168.68.50
  Internal Port: 3389
  Protocol: TCP

  Service Name: "WorkDogg Emergency RDP"  
  External Port: 3391
  Internal IP: 192.168.68.51
  Internal Port: 3389
  Protocol: TCP

  Service Name: "ZenDogg Emergency RDP"
  External Port: 3392
  Internal IP: 192.168.68.52
  Internal Port: 3389
  Protocol: TCP

Emergency SSH Access:
  Service Name: "NucDogg Emergency SSH"
  External Port: 2222
  Internal IP: 192.168.68.50
  Internal Port: 22
  Protocol: TCP

  Service Name: "WorkDogg Emergency SSH"
  External Port: 2223  
  Internal IP: 192.168.68.51
  Internal Port: 22
  Protocol: TCP
```

#### **Firewall Security Rules**
```bash
# Deco App → More → Security → Firewall

Default Policy: 
  Inbound: Deny (except allowed services)
  Outbound: Allow (internet access)

Allowed Inbound:
  1194/UDP → VPN Server
  3390-3392/TCP → Emergency RDP
  2222-2223/TCP → Emergency SSH

Blocked Always:
  All other inbound connections
  Port scanning attempts (automatic)
  Known malicious IP ranges (automatic)
```

### **Step 5: DNS Security & Filtering (15 minutes)**

#### **NasDogg DNS Configuration Enhancement**
```bash
# Access Synology NasDogg: http://192.168.68.40:5000
# Control Panel → DNS Server

Security Settings:
  Enable DNS filtering: Yes
  Block malicious domains: Yes
  Block advertising domains: Optional
  
Custom Block Lists:
  Add Pi-hole block lists (optional):
  - https://raw.githubusercontent.com/StevenBlack/hosts/master/hosts
  - Malware and phishing protection

Local Domain Validation:
  Test: nslookup nucdogg.doggpack.local
  Should return: 192.168.68.50 (when NucDogg is assigned)
```

#### **DHCP DNS Assignment**
```bash
# Deco App → More → Advanced → DHCP Server
Primary DNS: 192.168.68.40 (NasDogg)
Secondary DNS: 1.1.1.1 (Cloudflare backup)

# Verify all devices get correct DNS:
nslookup nasdogg.doggpack.local  # Should work from any device
```

### **Step 6: Quality of Service (QoS) (10 minutes)**

#### **Traffic Prioritization**
```bash
# Deco App → More → Advanced → QoS

Enable QoS: Yes
Total Bandwidth: Auto-detect or manual (82.9 Mbps down, 22.6 up)

Priority Assignment:
  Highest Priority:
    - DoggPack Infrastructure (192.168.68.40-52)
    - VPN traffic (port 1194)
    - DNS queries (port 53)

  High Priority:  
    - Video conferencing (Zoom, Teams, etc.)
    - VoIP applications
    - Gaming traffic (Xbox, PlayStation)

  Medium Priority:
    - Web browsing (ports 80, 443)
    - General applications
    - Media streaming

  Low Priority:
    - File downloads and backups
    - OS updates
    - IoT device updates
```

### **Step 7: Advanced Security Features (15 minutes)**

#### **Enable All Available Security**
```bash
# Deco App → More → Security

Intrusion Detection: Enabled
  - Monitors for port scanning
  - Detects suspicious connection patterns
  - Blocks known attack signatures

Infected Device Detection: Enabled
  - Monitors outbound connections
  - Detects malware communication
  - Quarantines infected devices

Malicious Website Blocking: Enabled
  - Blocks known phishing sites
  - Prevents malware downloads
  - Updates threat database automatically
```

#### **Parental Controls as Security Tool**
```bash
# Deco App → More → Parental Controls

Create Profile: "IoT Devices"
  Devices: All Guest Network devices
  Time Restrictions: None (24/7 access)
  Content Filtering: 
    - Block Adult Content: No (causes issues with IoT)
    - Block Social Media: No
    - Custom Block: Add any problematic IoT domains

Create Profile: "Infrastructure"
  Devices: DoggPack infrastructure devices
  Time Restrictions: None
  Content Filtering: Disabled
  Priority: Highest
```

---

## 🔐 **Advanced Security Configuration**

### **MCP Server Protection (Post-Foundation)**
```bash
# After Docker containers are deployed:

Container Network Security:
  - Use custom Docker networks for service isolation
  - Bind MCP servers to localhost only (127.0.0.1)
  - Use nginx reverse proxy for external access
  - Enable TLS for all MCP communications

Example Docker Compose security:
  networks:
    mcp-internal:
      driver: bridge
      internal: true  # No external access
    mcp-external:
      driver: bridge
  
  services:
    mcp-coordinator:
      networks:
        - mcp-internal
      ports:
        - "127.0.0.1:8100:8100"  # Localhost only
```

### **Certificate Management**
```bash
# For services requiring certificates:

Generate self-signed certificates for internal services:
openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365 -nodes

Or use Let's Encrypt with domain validation:
certbot certonly --standalone -d mcp.doggpack.net

Store certificates in: /opt/doggpack/certs/
```

### **Monitoring and Alerting**
```bash
# Set up basic monitoring (post-foundation):

Network Monitoring:
  - Monitor VPN connections
  - Track failed login attempts  
  - Alert on new device connections
  - Monitor bandwidth usage by device

Security Monitoring:
  - Failed SSH attempts
  - Unusual outbound connections from IoT devices
  - Access attempts to blocked ports
  - DNS queries to suspicious domains
```

---

## 🧪 **Testing and Validation**

### **Security Test Suite**

#### **Test 1: IoT Isolation Validation**
```bash
# From a device on Guest Network (DoggPackIoT):
ping 192.168.68.50          # Should TIMEOUT (blocked)
telnet 192.168.68.40 22     # Should FAIL (blocked)  
curl http://192.168.68.40:5000  # Should FAIL (blocked)
ping 8.8.8.8                # Should WORK (internet access)

Expected Result: Only internet access, no infrastructure access
```

#### **Test 2: VPN Functionality**
```bash
# From external network (mobile hotspot):
openvpn --config admin.ovpn  # Should connect successfully

# Once connected via VPN:
ping nasdogg.doggpack.local     # Should WORK
ssh user@nucdogg.doggpack.local # Should WORK
curl http://mcp.doggpack.local:8100  # Should WORK (post-foundation)

Expected Result: Full internal access via VPN
```

#### **Test 3: Emergency Access**
```bash
# From external network (VPN disconnected):
mstsc /v:doggpack.net:3390      # Should connect to NucDogg
ssh -p 2222 user@doggpack.net   # Should connect to NucDogg
telnet doggpack.net 80          # Should FAIL (not forwarded)

Expected Result: Only emergency ports accessible
```

#### **Test 4: DNS Resolution**
```bash
# From any internal device:
nslookup nasdogg.doggpack.local     # Should return 192.168.68.40
nslookup nucdogg.doggpack.local     # Should return 192.168.68.50
nslookup google.com                 # Should resolve via Cloudflare
nslookup malicious-test-domain.com  # Should be blocked (if filtering enabled)

Expected Result: Local domains work, external DNS works, filtering active
```

#### **Test 5: Service Protection**
```bash
# From guest network device:
nmap -sS 192.168.68.50          # Should show filtered ports
curl http://192.168.68.50:8100  # Should FAIL (MCP server blocked)
curl http://192.168.68.40:5000  # Should FAIL (NAS admin blocked)

Expected Result: Critical services protected from IoT devices
```

### **Performance Validation**
```bash
# Speed test from infrastructure device:
speedtest-cli                   # Should achieve near full speed

# Speed test through VPN:
speedtest-cli                   # Should achieve 85-90% of full speed

# Local network performance:
iperf3 -s (on NasDogg)
iperf3 -c nasdogg.doggpack.local (from other device)
# Should achieve near gigabit on local network
```

---

## 🚨 **Troubleshooting Guide**

### **Common Issues and Solutions**

#### **Problem: IoT device blocked but needs infrastructure access**
```bash
Solution:
1. Identify the specific service needed
2. Create custom access control rule
3. Allow only specific port/protocol
4. Monitor for abuse

Example: Smart TV needs NAS media access:
- Allow specific device MAC → 192.168.68.40 port 5000-5001
- Monitor connection logs
- Review access quarterly
```

#### **Problem: VPN connection fails**
```bash
Troubleshooting steps:
1. Check VPN server status in Deco app
2. Verify port 1194 UDP is open (external port test)
3. Regenerate client certificates
4. Test from different external network
5. Check router logs for connection attempts

Common fixes:
- Regenerate certificates: Delete and recreate client profile
- Check ISP blocking: Try different VPN ports if available
- Verify external IP: Ensure DDNS is updating correctly
```

#### **Problem: DNS resolution not working**
```bash
Troubleshooting steps:
1. Check NasDogg DNS server: http://192.168.68.40:5000
2. Verify DHCP DNS assignment: ipconfig /all
3. Clear DNS cache: ipconfig /flushdns
4. Test direct DNS query: nslookup google.com 192.168.68.40
5. Check DNS server logs on NasDogg

Common fixes:
- Restart DNS service on NasDogg
- Verify zone files are correct
- Check forwarder configuration (should be 1.1.1.1)
```

#### **Problem: Remote access not working**
```bash
Troubleshooting steps:
1. Test from internal network first
2. Verify port forwarding rules
3. Check Windows firewall on target machine
4. Test different external network
5. Verify target machine is online

Common fixes:
- Enable RDP in Windows system settings
- Add firewall exception for RDP
- Verify static IP assignment
- Test with emergency ports (3390-3392)
```

### **Emergency Procedures**

#### **Complete Security Reset (if locked out)**
```bash
1. Physical access to Deco X20:
   - Hold reset button for 10 seconds
   - Router will reset to factory defaults

2. Basic connectivity restore:
   - Connect via Ethernet cable
   - Access 192.168.68.1 (default IP)
   - Run initial setup wizard
   - Restore internet connectivity

3. Minimal security restore:
   - Change admin password
   - Enable basic firewall
   - Set DNS to 192.168.68.40 (if NasDogg works)
   - Test basic internet access

4. Gradual security re-implementation:
   - Re-enable guest network
   - Recreate access control rules
   - Reconfigure VPN server
   - Test each layer before adding next
```

#### **NasDogg DNS Failure Recovery**
```bash
1. Temporary DNS bypass:
   - Deco settings → Internet → DNS Settings
   - Set to 1.1.1.1, 1.0.0.1 temporarily
   - Test internet access

2. NasDogg recovery:
   - Physical access to NasDogg
   - Restart device or access via IP
   - Check DNS Server package status
   - Restore DNS service

3. Validate and switch back:
   - Test: nslookup nasdogg.doggpack.local
   - If working, switch Deco DNS back to 192.168.68.40
   - Verify all devices get updated DNS settings
```

---

## 📊 **Security Monitoring and Maintenance**

### **Weekly Monitoring Tasks**
```bash
1. Review Deco security logs:
   - Check for blocked access attempts
   - Identify new devices on network
   - Review VPN connection logs

2. Validate DNS operation:
   - Test .doggpack.local domain resolution
   - Check DNS server logs on NasDogg
   - Verify external DNS forwarding working

3. Test emergency access:
   - VPN connection from external network
   - Emergency RDP/SSH ports
   - Validate access control rules working
```

### **Monthly Security Audit**
```bash
1. Update Deco firmware:
   - Check for latest firmware
   - Apply updates during maintenance window
   - Test all functionality after update

2. Certificate maintenance:
   - Check VPN certificate expiration
   - Regenerate certificates approaching expiry
   - Audit user access levels

3. Access review:
   - Review all devices on network
   - Remove access for unused devices
   - Update access control rules as needed

4. Performance monitoring:
   - Speed test (internal and via VPN)
   - Monitor QoS effectiveness
   - Check for network congestion
```

### **Quarterly Deep Security Review**
```bash
1. Full security assessment:
   - External vulnerability scan
   - Internal penetration testing (if possible)
   - Review all firewall and access rules

2. Documentation updates:
   - Update network diagrams
   - Review and update security procedures
   - Validate emergency recovery procedures

3. User access audit:
   - Review all VPN users and access levels
   - Remove unnecessary accounts
   - Update access based on role changes

4. Infrastructure planning:
   - Assess for any new security needs
   - Plan for upcoming DoggPack expansion
   - Budget for security improvements
```

---

## 🚀 **Integration with DoggPack Foundation**

### **Preparing for Phase 3: Foundation Infrastructure**

Once the single-network security is implemented and validated, the foundation infrastructure can be deployed with confidence:

#### **Docker Network Security**
```bash
# Custom networks for service isolation:
docker network create --driver bridge --internal mcp-internal
docker network create --driver bridge --subnet=172.20.0.0/16 doggpack-services

# Deploy MCP servers with security:
docker-compose.yml security considerations:
  - Bind services to localhost (127.0.0.1)
  - Use custom networks for isolation
  - Implement service authentication
  - Enable container logging
```

#### **MCP Service Protection**
```bash
# Example secure MCP deployment:
version: '3.8'
services:
  mcp-coordinator:
    image: doggpack/mcp-coordinator
    networks:
      - mcp-internal
    ports:
      - "127.0.0.1:8100:8100"  # Localhost binding
    environment:
      - AUTH_REQUIRED=true
      - TLS_ENABLED=true
    volumes:
      - /opt/doggpack/certs:/certs:ro

  nginx-proxy:
    image: nginx:alpine
    networks:
      - mcp-internal
    ports:
      - "8100:8100"  # External access through proxy
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
    depends_on:
      - mcp-coordinator
```

#### **Monitoring Integration**
```bash
# Security monitoring for MCP services:
- Monitor container resource usage
- Track API access patterns
- Alert on unusual MCP communication
- Log all infrastructure service access
```

---

**🎯 Single-Network Security provides enterprise-grade protection within consumer hardware constraints**

**✅ This approach delivers:**
- IoT device isolation without VLAN complexity
- Secure remote access through VPN
- Professional DNS infrastructure ✅ (already operational)
- Multi-layered defense strategy
- Emergency access capabilities
- Foundation ready for MCP deployment

**⏱️ Implementation Time: 1.5-2 hours**  
**🛡️ Security Level: Enterprise-grade within hardware constraints**  
**🚀 DoggPack Foundation Ready: After successful Phase 2 completion**

*This security implementation is designed specifically for the TP-Link Deco X20 DSL hardware and provides maximum protection within its feature limitations.*