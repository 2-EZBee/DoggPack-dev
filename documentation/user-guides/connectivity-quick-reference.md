# DoggPack Connectivity Quick Reference Guide

## 🌐 Network Architecture at a Glance

```
                    ┌─────────────────────────────────────┐
                    │        Router (192.168.10.1)       │
                    │     Gateway, VPN, Port Forwarding  │
                    └─────────────┬───────────────────────┘
                                  │
                    ┌─────────────▼───────────────────────┐
                    │      Infrastructure VLAN 10        │
                    │        192.168.10.0/24             │
                    └─────────────┬───────────────────────┘
                                  │
        ┌─────────────┬───────────┼───────────┬─────────────┐
        │             │           │           │             │
   ┌────▼────┐   ┌───▼───┐   ┌───▼───┐   ┌──▼────┐   ┌───▼───┐
   │NasDogg  │   │NucDogg│   │WorkDogg│   │ZenDogg│   │ Others│
   │ .40     │   │ .50   │   │ .51   │   │ .52   │   │       │
   │DNS,NAS  │   │Manager│   │Worker │   │Control│   │       │
   └─────────┘   └───────┘   └───────┘   └───────┘   └───────┘
```

---

## 📋 Host IP Assignments

| **Device** | **IP Address** | **Role** | **Key Services** |
|------------|---------------|----------|------------------|
| **NasDogg** | 192.168.10.40 | Storage & DNS | DNS Server, File Storage, Backup |
| **NucDogg** | 192.168.10.50 | Swarm Manager | MCP Hub, Coordination, Core Services |
| **WorkDogg** | 192.168.10.51 | Swarm Worker | Development, Processing, Applications |
| **ZenDogg** | 192.168.10.52 | Control Station | Windows Interface, Admin Desktop |

---

## 🔌 Port Allocation Matrix

### **MCP Servers (8100-8199)**
| **Service** | **Host** | **Port** | **Purpose** | **External** |
|-------------|----------|----------|-------------|--------------|
| Planning Coordinator | NucDogg | **8100** | Central MCP coordination | ❌ |
| Docker Management | NucDogg | **8101** | Docker Swarm MCP | ❌ |
| System Monitoring | NucDogg | **8500** | Metrics & health checks | ❌ |

### **Web Interfaces (8200-8299)**
| **Service** | **Host** | **Port** | **Purpose** | **External** |
|-------------|----------|----------|-------------|--------------|
| API Gateway | NucDogg | **8200** | External API proxy | ✅ (3001) |
| Portainer | NucDogg | **8201** | Docker management UI | ✅ (3004) |
| Grafana | NucDogg | **8202** | Metrics dashboard | ✅ (3005) |

### **Application Services (8300-8399)**
| **Service** | **Host** | **Port** | **Purpose** | **External** |
|-------------|----------|----------|-------------|--------------|
| N8N Automation | WorkDogg | **8300** | Workflow automation | ✅ (3002) |
| Asana Proxy | NucDogg | **8301** | Asana API proxy | ❌ |
| GitHub Proxy | NucDogg | **8302** | GitHub API proxy | ❌ |
| Google Proxy | NucDogg | **8303** | Google API proxy | ❌ |

### **Development Environments (2200-2299)**
| **Service** | **Host** | **Port** | **Purpose** | **External** |
|-------------|----------|----------|-------------|--------------|
| CCN Dev SSH | NucDogg | **2200** | Claude CCN development | ❌ |
| CCW Dev SSH | WorkDogg | **2201** | Claude CCW development | ❌ |

### **Database Services (8600-8699)**
| **Service** | **Host** | **Port** | **Purpose** | **External** |
|-------------|----------|----------|-------------|--------------|
| Obsidian LiveSync | NasDogg | **8601** | CouchDB for Obsidian | ✅ (3003) |
| Prometheus | NucDogg | **8501** | Metrics database | ❌ |
| Loki | NucDogg | **8502** | Log aggregation | ❌ |

---

## 🌍 Domain Mapping

### **Internal Domains (*.doggpack.local)**
```
DNS Server: 192.168.10.40 (NasDogg)

Host Records:
nasdogg.doggpack.local    → 192.168.10.40
nucdogg.doggpack.local    → 192.168.10.50  
workdogg.doggpack.local   → 192.168.10.51
zendogg.doggpack.local    → 192.168.10.52

Service Records:
mcp.doggpack.local        → 192.168.10.50:8100
api.doggpack.local        → 192.168.10.50:8200
monitoring.doggpack.local → 192.168.10.50:8500
docker.doggpack.local     → 192.168.10.50:8201
n8n.doggpack.local        → 192.168.10.51:8300
obsidian.doggpack.local   → 192.168.10.40:8601
grafana.doggpack.local    → 192.168.10.50:8202
```

### **External Domains (*.doggpack.net)**
```
DNS Provider: Cloudflare

Base Records:
home.doggpack.net     → Dynamic IP (Proxied)
vpn.doggpack.net      → Dynamic IP (Not Proxied)

Service Records:
mcp.doggpack.net      → home.doggpack.net (Port 3001)
automation.doggpack.net → home.doggpack.net (Port 3002)
sync.doggpack.net     → home.doggpack.net (Port 3003)
docker.doggpack.net   → home.doggpack.net (Port 3004)
metrics.doggpack.net  → home.doggpack.net (Port 3005)
```

---

## 🔀 Port Forwarding Rules

### **Router → Internal Services**
| **External Port** | **Protocol** | **Internal IP** | **Internal Port** | **Service** |
|-------------------|--------------|-----------------|-------------------|-------------|
| **1194** | UDP | 192.168.10.1 | 1194 | OpenVPN Server |
| **3390** | TCP | 192.168.10.50 | 3389 | NucDogg RDP (Emergency) |
| **3391** | TCP | 192.168.10.51 | 3389 | WorkDogg RDP (Emergency) |
| **3392** | TCP | 192.168.10.52 | 3389 | ZenDogg RDP (Emergency) |
| **2222** | TCP | 192.168.10.50 | 22 | NucDogg SSH |
| **2223** | TCP | 192.168.10.51 | 22 | WorkDogg SSH |
| **3001** | TCP | 192.168.10.50 | 8200 | API Gateway |
| **3002** | TCP | 192.168.10.51 | 8300 | N8N Automation |
| **3003** | TCP | 192.168.10.40 | 8601 | Obsidian LiveSync |
| **3004** | TCP | 192.168.10.50 | 8201 | Portainer |
| **3005** | TCP | 192.168.10.50 | 8202 | Grafana |

---

## 🐳 Docker Networking

### **Overlay Networks**
| **Network Name** | **Subnet** | **Purpose** | **Encryption** |
|------------------|------------|-------------|----------------|
| **coordination_net** | 10.1.0.0/24 | MCP servers & core coordination | ✅ |
| **services_net** | 10.2.0.0/24 | Application services | ❌ |
| **development_net** | 10.3.0.0/24 | Isolated development environments | ❌ |
| **api_gateway_net** | 10.4.0.0/24 | External API proxy & ingress | ✅ |

### **Container IP Assignments**
| **Service** | **Network** | **Container IP** | **Host Port** |
|-------------|-------------|------------------|---------------|
| Planning Coordinator | coordination_net | 10.1.0.10 | 8100 |
| Docker Management | coordination_net | 10.1.0.30 | 8101 |
| System Monitoring | coordination_net | 10.1.0.20 | 8500 |
| API Gateway | api_gateway_net | 10.4.0.10 | 8200 |
| Portainer | coordination_net | 10.1.0.40 | 8201 |
| Prometheus | coordination_net | 10.1.0.50 | 8501 |
| Grafana | coordination_net | 10.1.0.60 | 8202 |
| Loki | coordination_net | 10.1.0.70 | 8502 |
| N8N | services_net | 10.2.0.10 | 8300 |
| Obsidian LiveSync | services_net | 10.2.0.20 | 8601 |
| CCN Dev Environment | development_net | 10.3.0.10 | 2200 |
| CCW Dev Environment | development_net | 10.3.0.20 | 2201 |
| Asana Proxy | api_gateway_net | 10.4.0.20 | 8301 |
| GitHub Proxy | api_gateway_net | 10.4.0.30 | 8302 |
| Google Proxy | api_gateway_net | 10.4.0.40 | 8303 |

---

## 🔐 Access Methods

### **VPN Access (Recommended)**
```bash
# 1. Connect to VPN
openvpn --config doggpack-admin.ovpn

# 2. Access services via internal domains
curl http://mcp.doggpack.local:8100/health
curl http://api.doggpack.local:8200/health
mstsc /v:nucdogg.doggpack.local
ssh user@nucdogg.doggpack.local -p 22
```

### **Direct External Access (Emergency)**
```bash
# Web services via external domains
curl https://mcp.doggpack.net/health
curl https://automation.doggpack.net
curl https://metrics.doggpack.net

# RDP via external ports
mstsc /v:home.doggpack.net:3390  # NucDogg
mstsc /v:home.doggpack.net:3391  # WorkDogg
mstsc /v:home.doggpack.net:3392  # ZenDogg

# SSH via external ports
ssh user@home.doggpack.net -p 2222  # NucDogg
ssh user@home.doggpack.net -p 2223  # WorkDogg
```

---

## 🔄 Service Dependencies

### **Deployment Order**
```
1. Docker Swarm Initialization
   └── Network Creation (overlay networks)

2. Foundation Services
   ├── Planning Coordinator (8100)
   ├── Docker Management (8101)
   └── System Monitoring (8500)

3. Gateway & Proxy
   ├── API Gateway (8200)
   ├── Traefik (80/443)
   └── External Proxies (8301-8303)

4. Application Services
   ├── N8N Automation (8300)
   ├── Obsidian LiveSync (8601)
   ├── Portainer (8201)
   └── Monitoring Stack (8501-8502, 8202)

5. Development Environments
   ├── CCN Dev Container (2200)
   └── CCW Dev Container (2201)
```

### **Service Communication Matrix**
```
✅ = Allowed Communication
❌ = Blocked Communication

                     │ MCP │ API │ Apps│ Dev │
────────────────────┼─────┼─────┼─────┼─────│
MCP Services        │ ✅  │ ✅  │ ✅  │ ✅  │
API Gateway         │ ✅  │ ✅  │ ✅  │ ❌  │
Application Services│ ✅  │ ✅  │ ✅  │ ❌  │
Development         │ ✅  │ ❌  │ ❌  │ ✅  │
```

---

## 🧪 Validation Commands

### **Network Connectivity**
```bash
# Test internal DNS resolution
nslookup mcp.doggpack.local
nslookup nucdogg.doggpack.local

# Test service connectivity
curl http://mcp.doggpack.local:8100/health
curl http://api.doggpack.local:8200/health
curl http://monitoring.doggpack.local:8500/health

# Test Docker networking
docker network ls | grep -E "(coordination|services|development|api_gateway)"
docker service ls | grep -E "(running|replicated)"
```

### **Port Conflict Detection**
```bash
# Scan for port conflicts on NucDogg
nmap -sS 192.168.10.50 -p 8000-8999

# Check listening ports
netstat -tulpn | grep LISTEN | grep -E ":(8[0-9]{3}|2[2-9][0-9]{2}|3[0-9]{3})"

# Verify Docker port mappings
docker ps --format "table {{.Names}}\t{{.Ports}}" | grep -E "8[0-9]{3}"
```

### **External Access Validation**
```bash
# Test external domains (from outside network)
curl https://mcp.doggpack.net/health
curl https://automation.doggpack.net
nslookup vpn.doggpack.net

# Test port forwarding
nmap -sS home.doggpack.net -p 3001-3005,2222-2223,3390-3392
```

---

## ⚠️ Conflict Prevention

### **Reserved Port Ranges**
- **System**: 22, 80, 443, 53, 1194, 3389, 2376-2377, 7946, 4789
- **MCP Services**: 8100-8199
- **Web Interfaces**: 8200-8299  
- **APIs**: 8300-8399
- **Development**: 8400-8499, 2200-2299
- **Monitoring**: 8500-8599
- **Databases**: 8600-8699
- **External Access**: 3000-3099

### **IP Range Allocations**
- **Host Network**: 192.168.10.0/24
- **Docker coordination_net**: 10.1.0.0/24
- **Docker services_net**: 10.2.0.0/24
- **Docker development_net**: 10.3.0.0/24
- **Docker api_gateway_net**: 10.4.0.0/24

---

## 🚨 Troubleshooting Quick Fixes

### **Service Won't Start**
```bash
# Check port conflicts
netstat -tulpn | grep <port>
docker ps | grep <port>

# Check Docker network
docker network inspect <network_name>
docker service logs <service_name>
```

### **Cannot Access Service**
```bash
# Check service health
curl http://<service_host>:<port>/health
docker service ps <service_name>

# Check DNS resolution
nslookup <domain> 192.168.10.40
ping <hostname>
```

### **External Access Fails**
```bash
# Check port forwarding
telnet home.doggpack.net <external_port>

# Check DNS propagation
nslookup <domain> 8.8.8.8
curl -I https://<domain>
```

---

**🎯 This reference ensures zero port conflicts and predictable networking for all DoggPack services!**

Print this guide and keep it handy during deployment and troubleshooting! 📋✨
