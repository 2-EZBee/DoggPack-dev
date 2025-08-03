# Network Implementation Quick Reference

## 🚀 DoggPack Network Configuration Cheat Sheet

### **Current → Target Migration**
```
FROM: 192.168.68.0/24 (Flat Network)
TO:   Segmented VLANs with Security
```

---

## 📊 VLAN Configuration

| VLAN | Purpose | Subnet | Gateway | DHCP Range |
|------|---------|--------|---------|------------|
| 10 | Infrastructure | 192.168.10.0/24 | .10.1 | .10.100-.10.199 |
| 20 | SmartHome | 192.168.20.0/24 | .20.1 | .20.100-.20.199 |
| 30 | Gaming | 192.168.30.0/24 | .30.1 | .30.100-.30.199 |
| 40 | Personal | 192.168.40.0/24 | .40.1 | .40.100-.40.199 |

---

## 🏠 Static IP Assignments

### **DoggPack Core Infrastructure (VLAN 10)**
```
192.168.10.40  →  NasDogg       (DNS Server, Storage)
192.168.10.50  →  NucDogg       (Infrastructure Hub, Docker Manager)
192.168.10.51  →  WorkDogg      (Development Machine, Docker Worker)
192.168.10.52  →  ZenDogg       (Primary Workstation, Control Interface)
```

### **Current Device Migration**
```
OLD IP              NEW IP           DEVICE
192.168.68.40   →   192.168.10.40   NasDogg (Synology)
192.168.68.XXX  →   192.168.10.50   NucDogg
192.168.68.XXX  →   192.168.10.51   WorkDogg  
192.168.68.XXX  →   192.168.10.52   ZenDogg

Gaming devices  →   192.168.30.XXX  (Xbox, consoles)
Smart devices   →   192.168.20.XXX  (Tuya, Nest Hub)
Personal devices→   192.168.40.XXX  (Phones, tablets)
```

---

## 🌐 DNS Configuration

### **Local DNS Server**: 192.168.10.40 (NasDogg)
```
Primary DNS:    192.168.10.40
Secondary DNS:  1.1.1.1
Search Domain:  doggpack.local
```

### **Local Domain Records**
```
nasdogg.doggpack.local   →  192.168.10.40
nucdogg.doggpack.local   →  192.168.10.50
workdogg.doggpack.local  →  192.168.10.51
zendogg.doggpack.local   →  192.168.10.52
mcp.doggpack.local       →  192.168.10.50
docker.doggpack.local    →  192.168.10.50
```

---

## 🔐 VPN Configuration

### **OpenVPN Server Settings**
```
Port:        1194 UDP
Encryption:  AES-256
Protocol:    OpenVPN
Auth:        Certificate + Password
External:    vpn.doggpack.net:1194
```

### **VPN Client Profiles**
```
admin:     Full network access (all VLANs)
user:      Infrastructure only (VLAN 10)
readonly:  Monitoring only (NasDogg)
```

---

## 🖥️ Remote Access Ports

### **RDP Access (Through VPN)**
```
NucDogg:   nucdogg.doggpack.local:3389
WorkDogg:  workdogg.doggpack.local:3389  
ZenDogg:   zendogg.doggpack.local:3389
```

### **External RDP (Emergency Only)**
```
NucDogg:   home.doggpack.net:3390
WorkDogg:  home.doggpack.net:3391
ZenDogg:   home.doggpack.net:3392
```

### **SSH Access**
```
NucDogg:   ssh -p 2222 user@nucdogg.doggpack.local
WorkDogg:  ssh -p 2223 user@workdogg.doggpack.local
External:  ssh -p 2222 user@home.doggpack.net
```

---

## 🔥 Firewall Rules Summary

### **Inter-VLAN Access**
```
✅ Infrastructure → All VLANs    (Management)
✅ Personal → Infrastructure      (Limited services)
❌ SmartHome → Infrastructure     (Blocked)
❌ SmartHome → Personal          (Blocked)
❌ Gaming → Infrastructure        (Blocked)
```

### **External Access Ports**
```
1194/UDP  →  VPN Server
3390/TCP  →  NucDogg RDP
3391/TCP  →  WorkDogg RDP  
3392/TCP  →  ZenDogg RDP
2222/TCP  →  NucDogg SSH
2223/TCP  →  WorkDogg SSH
```

---

## ☁️ Cloudflare DNS Records

### **Required DNS Records**
```
A     vpn.doggpack.net      →  Dynamic IP  (🔒 Not Proxied)
A     home.doggpack.net     →  Dynamic IP  (🛡️ Proxied)
CNAME mcp.doggpack.net      →  home.doggpack.net
CNAME remote.doggpack.net   →  home.doggpack.net
```

### **Security Settings**
```
SSL Mode:           Full (Strict)
Min TLS Version:    1.2
Always HTTPS:       Enabled
Security Level:     Medium
```

---

## ⚡ Quick Implementation Steps

### **1. Router Backup (2 min)**
```bash
# Access router admin panel
# System → Backup → Save current config
```

### **2. Create VLANs (15 min)**
```
Network → VLANs → Add:
- VLAN 10: Infrastructure
- VLAN 20: SmartHome  
- VLAN 30: Gaming
- VLAN 40: Personal
```

### **3. Configure DHCP (10 min)**
```
Set DHCP ranges for each VLAN
Set DNS server to 192.168.10.40
Enable DHCP reservations for static IPs
```

### **4. Setup Firewall (10 min)**
```
Create firewall rules between VLANs
Block SmartHome → Infrastructure
Allow Infrastructure → All
```

### **5. Enable VPN (15 min)**
```
VPN → OpenVPN Server → Enable
Port: 1194, Encryption: AES-256
Generate certificates
Create client profiles
```

### **6. Configure NasDogg DNS (15 min)**
```
Synology → DNS Server → Enable
Create zone: doggpack.local
Add A records for all machines
Set forwarders: 1.1.1.1, 1.0.0.1
```

---

## 🧪 Testing Commands

### **Network Connectivity**
```bash
# Test from each VLAN
ping 8.8.8.8                    # Internet
ping nasdogg.doggpack.local     # Local DNS
nslookup google.com             # External DNS
```

### **VPN Testing**
```bash
# Connect VPN then test
curl http://nasdogg.doggpack.local
ssh nucdogg.doggpack.local
```

### **Security Validation**
```bash
# External port scan
nmap -sS home.doggpack.net
# Should only show: 1194, 3390-3392, 2222-2223
```

---

## ⚠️ Emergency Rollback

### **If Something Goes Wrong**
```
1. Access router admin panel
2. System → Restore → Load backup
3. Reboot router
4. Disable VLANs if needed
5. Test basic internet connectivity
```

### **Backup Communication**
```
Mobile hotspot for emergency internet
Physical access to router reset button
Phone support: Aussie Broadband
```

---

## 📱 Quick Connection Guide

### **Connect via VPN**
```
1. Install OpenVPN client
2. Import .ovpn profile
3. Connect to vpn.doggpack.net:1194
4. Access: mstsc /v:nucdogg.doggpack.local
```

### **Emergency Direct Access**
```
# If VPN fails:
mstsc /v:home.doggpack.net:3390  # NucDogg
ssh -p 2222 user@home.doggpack.net
```

---

## 🎯 Success Validation

### **✅ Network Working If:**
- All devices get IP from correct VLAN
- Can ping between allowed VLANs
- Cannot ping between blocked VLANs
- VPN connects from external network
- Local domains resolve correctly
- RDP works through VPN

### **📊 Expected Results:**
- Internet speed unchanged
- Local access faster (local DNS)
- Secure remote access working
- Smart devices isolated
- Gaming performance unchanged

---

**⏱️ Total Implementation Time: 2-3 hours**  
**🛡️ Security Level: Enterprise-grade**  
**🚀 DoggPack Ready: Yes**

*Print this reference and keep handy during implementation!*
