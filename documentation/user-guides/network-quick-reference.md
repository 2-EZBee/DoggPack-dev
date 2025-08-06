# DoggPack Network Quick Reference

## 🚀 Single-Network Security Configuration

### **Current Network Status**
```
Network:        192.168.68.0/24 (Single flat network)
Gateway:        192.168.68.1 (TP-Link Deco X20 DSL)
DNS Server:     192.168.68.40 (NasDogg) ✅ OPERATIONAL
DHCP Range:     192.168.68.100-250
Internet:       144.6.156.14/22 (VDSL2: 82.9/22.6 Mbps)
Active Devices: 35 IP assignments
```

**⚠️ Hardware Reality: VLAN segmentation NOT supported by Deco X20 DSL**

---

## 🏠 **DoggPack Infrastructure Addresses**

### **Core Infrastructure (Static Assignments)**
```
192.168.68.40  →  NasDogg       ✅ DNS Server, Storage (OPERATIONAL)
192.168.68.50  →  NucDogg       🎯 Infrastructure Hub, Docker Manager
192.168.68.51  →  WorkDogg      🎯 Development Machine, Docker Worker
192.168.68.52  →  ZenDogg       🎯 Primary Workstation, Control Interface
```

### **Device Categories (Dynamic Assignment)**
```
192.168.68.100-150  →  Smart Home/IoT    (Guest Network isolation)
192.168.68.151-200  →  Gaming/Media      (Main network, QoS priority)
192.168.68.201-250  →  Personal/Mobile   (Main network, standard access)
```

---

## 🌐 **DNS Configuration (Phase 1 Complete ✅)**

### **Local DNS Server**: 192.168.68.40 (NasDogg)
```
Status:         ✅ OPERATIONAL
Primary DNS:    192.168.68.40 (NasDogg)
Secondary DNS:  1.1.1.1 (Cloudflare Forwarder)
Search Domain:  doggpack.local
```

### **Local Domain Records (Active ✅)**
```
nasdogg.doggpack.local   →  192.168.68.40  ✅
nucdogg.doggpack.local   →  192.168.68.50  🎯
workdogg.doggpack.local  →  192.168.68.51  🎯
zendogg.doggpack.local   →  192.168.68.52  🎯
mcp.doggpack.local       →  192.168.68.50  🎯
docker.doggpack.local    →  192.168.68.50  🎯
```

### **External Domain (Planned)**
```
doggpack.net             →  Dynamic IP     🎯
vpn.doggpack.net         →  Dynamic IP     🎯  
home.doggpack.net        →  Dynamic IP     🎯
```

---

## 🛡️ **Multi-Layered Security Strategy**

### **Layer 1: WiFi-Based Segmentation**
```
Main Network:    DoggPackNet     (Infrastructure + Trusted devices)
Guest Network:   DoggPackIoT     (Smart home devices - ISOLATED)
Admin Network:   DoggPackAdmin   (Management access - if available)
```

### **Layer 2: Access Control Rules (Deco Feature)**
```
BLOCK: Guest Network → Main Network devices
BLOCK: IoT devices → DoggPack infrastructure (50-52)
BLOCK: Unknown devices → Critical services
ALLOW: Infrastructure → All (management access)
```

### **Layer 3: Firewall Rules (Port-Based)**
```
BLOCK: External → All except VPN/RDP/SSH ports
BLOCK: IoT → TCP/UDP ports 2200-2299 (MCP servers)
BLOCK: IoT → TCP/UDP ports 8100-8199 (Web interfaces)
ALLOW: Infrastructure → All ports (management)
```

### **Layer 4: Service-Level Security**
```
MCP Servers:     Certificate authentication
Docker API:      TLS with client certificates  
SSH:             Key-based authentication only
RDP:             Network Level Authentication
```

---

## 🔐 **Remote Access Configuration**

### **VPN Server (TP-Link Deco Built-in)**
```
Protocol:        OpenVPN
Port:            1194 UDP
Encryption:      AES-256
Authentication:  Certificate + Password
External Access: vpn.doggpack.net:1194
```

### **VPN Client Profiles**
```
admin:           Full network access + infrastructure management
user:            Limited access to infrastructure services only  
readonly:        Monitoring and status checking only
emergency:       Critical system access during outages
```

### **RDP Access (Through VPN Preferred)**
```
Internal Access (VPN connected):
  NucDogg:   mstsc /v:nucdogg.doggpack.local:3389
  WorkDogg:  mstsc /v:workdogg.doggpack.local:3389
  ZenDogg:   mstsc /v:zendogg.doggpack.local:3389

External Access (Emergency Only):
  NucDogg:   mstsc /v:home.doggpack.net:3390
  WorkDogg:  mstsc /v:home.doggpack.net:3391
  ZenDogg:   mstsc /v:home.doggpack.net:3392
```

### **SSH Access**
```
Internal (VPN):
  ssh -p 2222 user@nucdogg.doggpack.local
  ssh -p 2223 user@workdogg.doggpack.local

External (Emergency):
  ssh -p 2222 user@home.doggpack.net
  ssh -p 2223 user@home.doggpack.net
```

---

## 🔥 **Security Rules Summary**

### **Access Control Matrix**
```
Device Category    → Infrastructure  → Internet  → Other Devices
Infrastructure     →     ALLOW       →  ALLOW    →    ALLOW
Gaming/Media       →     BLOCK       →  ALLOW    →    ALLOW
Personal/Mobile    →   LIMITED       →  ALLOW    →    ALLOW
Smart Home/IoT     →     BLOCK       →  ALLOW    →    BLOCK
Guest Devices      →     BLOCK       →  ALLOW    →    BLOCK
```

### **Critical Port Protection**
```
ALWAYS BLOCKED FROM INTERNET:
  22, 23      → SSH, Telnet
  3389        → Default RDP
  445, 139    → SMB/CIFS
  5432, 3306  → Database ports

BLOCKED FROM IOT DEVICES:
  2200-2299   → MCP coordination ports
  8100-8199   → Service web interfaces
  8300-8399   → API endpoints

ALLOWED EXTERNAL (Emergency):
  1194/UDP    → VPN Server
  3390-3392   → Emergency RDP
  2222-2223   → Emergency SSH
```

---

## ☁️ **Cloudflare Integration** 

### **DNS Records (Planned)**
```
Type  Name                 Target          Proxy  Purpose
A     vpn.doggpack.net     Dynamic IP      No     VPN access
A     home.doggpack.net    Dynamic IP      Yes    Web services  
CNAME mcp.doggpack.net     home            Yes    MCP interfaces
CNAME remote.doggpack.net  home            Yes    Remote access
```

### **Security Settings**
```
SSL Mode:           Full (Strict)
Min TLS Version:    1.2
Always HTTPS:       Enabled
Security Level:     Medium
DDoS Protection:    Enabled
```

---

## ⚡ **Implementation Steps**

### **Phase 2: Single-Network Security (Next)**

#### **1. Enable Guest Network (10 min)**
```
Deco App → WiFi → Guest Network → Enable
Name: DoggPackIoT
Password: [Strong password]
Access: Isolated from main network
```

#### **2. Configure Access Control (15 min)**
```
Deco App → Advanced → Access Control → Add Rules
Block: Guest Network devices → Infrastructure IPs
Block: Specific MAC addresses → Critical ports
Log: All blocked attempts for monitoring
```

#### **3. Set Up VPN Server (20 min)**
```
Deco App → Advanced → VPN Server → OpenVPN
Enable server on port 1194
Generate certificates for admin/user profiles  
Configure client access levels
Test connection from external network
```

#### **4. Configure Port Forwarding (15 min)**
```
Emergency RDP:
  3390 → 192.168.68.50:3389 (NucDogg)
  3391 → 192.168.68.51:3389 (WorkDogg)
  3392 → 192.168.68.52:3389 (ZenDogg)

Emergency SSH:
  2222 → 192.168.68.50:22 (NucDogg)
  2223 → 192.168.68.51:22 (WorkDogg)
```

#### **5. Configure QoS (10 min)**
```
Deco App → Advanced → QoS → Enable
High Priority: DoggPack Infrastructure (50-52)
Medium Priority: Gaming/Media devices
Low Priority: IoT/Guest devices
```

#### **6. Set DNS Server (5 min)**
```
Deco App → Internet → DNS Settings
Primary DNS: 192.168.68.40
Secondary DNS: 1.1.1.1
Validate: nslookup nucdogg.doggpack.local
```

---

## 🧪 **Testing & Validation**

### **DNS Resolution Test**
```bash
# From any device on network
nslookup nasdogg.doggpack.local     # Should return 192.168.68.40
nslookup google.com                 # Should resolve via forwarder
ping nucdogg.doggpack.local         # Should work when NucDogg online
```

### **Security Validation**
```bash
# From IoT device (should FAIL):
telnet 192.168.68.50 22             # SSH to NucDogg
curl http://192.168.68.50:8100      # MCP server
ping 192.168.68.52                  # ZenDogg workstation

# From infrastructure (should WORK):
ssh nucdogg.doggpack.local          # SSH access
curl http://docker.doggpack.local:2376  # Docker API
```

### **VPN Connection Test**
```bash
# Connect VPN client, then test:
ping nasdogg.doggpack.local         # Should work through VPN
mstsc /v:nucdogg.doggpack.local     # RDP should connect
ssh user@workdogg.doggpack.local    # SSH should work
```

### **External Access Test**
```bash
# From outside network (VPN disconnected):
nmap home.doggpack.net              # Should only show: 1194, 3390-3392, 2222-2223
telnet home.doggpack.net 3390       # Emergency RDP should work
```

---

## 🔧 **Port Allocation Strategy**

### **MCP Services (Single Network)**
```
8100-8199: MCP Server APIs          
  8100 → Planning Coordinator MCP
  8101 → Docker Management MCP  
  8102 → Monitoring MCP
  8103 → Knowledge Base MCP
  8104 → Reserved for expansion
```

### **Web Interfaces**
```
8200-8299: Service Web UIs
  8200 → N8N Workflow Interface
  8201 → Monitoring Dashboard (Grafana)
  8202 → Container Registry UI
  8203 → System Status Dashboard
  8204 → Knowledge Management UI
```

### **Development Access**
```
2200-2299: Development Environments
  2200 → CCN Development SSH
  2201 → CCW Development SSH  
  2202 → Shared Development Environment
  2203 → Testing Environment
```

### **External Access Ports**
```
3000-3099: Public Service Access
  3000 → Primary MCP Gateway
  3001 → Public API Endpoint  
  3002 → Status/Health Check API
  3003 → Reserved for expansion
```

---

## ⚠️ **Emergency Procedures**

### **Total Network Reset**
```
1. Physical reset: Hold Deco reset button 10 seconds
2. Reconfigure basic internet: WAN settings
3. Restore DNS: Set to 192.168.68.40 (if NasDogg working)
4. Test basic connectivity: ping 8.8.8.8
5. Restore security rules: Guest network + access control
```

### **DNS Server Failure**
```
1. Temporary DNS: Change to 1.1.1.1 in Deco settings
2. Access NasDogg: http://192.168.68.40:5000
3. Restart DNS Server: Package Center → DNS Server → Restart
4. Validate resolution: nslookup nasdogg.doggpack.local
5. Switch back to 192.168.68.40 as primary DNS
```

### **VPN Connection Issues**
```
1. Check VPN server: Deco App → Advanced → VPN Server
2. Regenerate certificates: Create new client profile
3. Test internal access: Try emergency RDP ports
4. Verify port forwarding: 1194 UDP should be open
5. Check external IP: whatismyipaddress.com
```

---

## 📊 **Network Performance**

### **Expected Performance**
```
Local DNS Resolution:    < 10ms
Internet Speed:          82.9 Mbps down, 22.6 Mbps up
VPN Overhead:            ~10-15% speed reduction
RDP Latency:             < 50ms on LAN, < 200ms via VPN
Container Access:        Near-native performance
```

### **QoS Prioritization**
```
Highest:    DoggPack Infrastructure (192.168.68.50-52)
High:       Video conferencing, VoIP
Medium:     Gaming, streaming  
Low:        File downloads, backups
Lowest:     IoT device updates
```

---

## 🎯 **Success Criteria**

### **✅ Single-Network Security Working If:**
- IoT devices cannot access DoggPack infrastructure
- VPN connects from external networks
- Local domains resolve correctly (.doggpack.local)
- Emergency RDP/SSH works from outside
- Critical services only accessible via VPN
- Guest network properly isolates devices

### **📈 Expected Benefits:**
- Enterprise-level security within consumer hardware
- Centralized DNS with custom domains ✅
- Secure remote access for development work
- IoT device isolation without VLAN complexity
- Professional infrastructure on home network
- Zero-config local service discovery

---

## 🚀 **Integration with DoggPack**

### **MCP Server Access (Post-Foundation)**
```bash
# Via VPN or from infrastructure:
curl http://mcp.doggpack.local:8100/health      # Planning coordinator
curl http://docker.doggpack.local:2376/version  # Docker API
curl http://nucdogg.doggpack.local:8200         # N8N interface
```

### **Claude Development Environment**
```bash  
# SSH into development containers:
ssh -p 2200 claude@nucdogg.doggpack.local       # CCN environment
ssh -p 2201 claude@workdogg.doggpack.local      # CCW environment
```

### **Service Discovery**
```bash
# All services accessible via local DNS:
http://mcp.doggpack.local:8100                  # MCP coordination
http://docker.doggpack.local:2376               # Docker management
http://monitor.doggpack.local:8201              # System monitoring
http://knowledge.doggpack.local:8204            # Knowledge base
```

---

**⏱️ Total Implementation Time: 1.5-2 hours**  
**🛡️ Security Level: Enterprise-grade within consumer constraints**  
**🚀 DoggPack Ready: After Phase 2 completion**  
**✅ DNS Foundation: Already operational**

*This reference reflects the hardware realities and provides achievable security within TP-Link Deco X20 DSL constraints!*