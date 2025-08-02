# ADR-003: Containerized Isolated Development Environments

**Status**: Accepted  
**Date**: 2025-08-02  
**Deciders**: DoggPack AI Team  
**Technical Impact**: High  
**Business Impact**: Medium  

## Context and Problem Statement

Previous attempts at AI-led deployment with Claude Code have been plagued with sudo permission problems and security concerns when giving AI systems direct access to host systems. We need a development approach that:

- Eliminates sudo permission friction for AI-driven deployments
- Provides safe experimentation environments
- Maintains security isolation between development and production
- Enables easy rollback and recovery
- Supports the development of MCP coordination infrastructure

Additionally, we want both CCN and CCW to eventually have their own isolated development environments where they can safely execute deployment tasks without affecting the host systems.

## Decision Drivers

- **Security Isolation**: Development work must not risk production systems
- **Permission Simplicity**: Eliminate sudo-related deployment failures
- **Recovery Capability**: Easy rollback from any experimental changes
- **AI Safety**: Provide safe sandbox for AI-driven development
- **Bootstrap Requirements**: Need environments where CCN/CCW can build their own replacements
- **Future MCP Development**: Provide space to develop MCP coordination tools

## Considered Options

### Option 1: Service Account with Limited Sudo
**Description**: Create dedicated service accounts with specific sudo permissions

**Pros**:
- Direct host system access
- Fine-grained permission control
- Native performance
- Familiar Linux permission model

**Cons**:
- Complex sudo configuration
- Risk of privilege escalation
- Still requires host system changes
- Difficult to ensure complete isolation
- Previous failures with this approach

**Implementation Complexity**: High
**Risk Level**: High

### Option 2: Virtual Machines
**Description**: Full VMs for each Claude instance development environment

**Pros**:
- Complete isolation
- Full OS control
- Easy snapshots and rollback
- No host system risk

**Cons**:
- High resource overhead
- Complex networking setup
- Slow provisioning and startup
- Resource waste with multiple VMs
- Management complexity

**Implementation Complexity**: High
**Risk Level**: Low

### Option 3: Privileged Development Containers
**Description**: Docker containers with privileged access and Docker socket mounting

**Pros**:
- Good isolation from host system
- Full privileges within container boundary
- Fast provisioning and reset
- Can run Docker-in-Docker for development
- Easy to rebuild and deploy
- Resource efficient

**Cons**:
- Privileged containers have security implications
- Docker socket access provides host system access
- Need careful network configuration
- Container escape vulnerabilities possible

**Implementation Complexity**: Medium
**Risk Level**: Medium

### Option 4: Rootless Containers with User Namespaces
**Description**: Unprivileged containers using user namespace mapping

**Pros**:
- Strong security isolation
- No privileged access required
- Reduced attack surface
- Modern container security practices

**Cons**:
- More complex setup
- Some functionality limitations
- Not all tools work in rootless mode
- May complicate Docker-in-Docker scenarios

**Implementation Complexity**: High
**Risk Level**: Low

## Decision Outcome

**Chosen Option**: Privileged Development Containers with Safety Measures

**Rationale**:

Privileged development containers provide the optimal balance of functionality, security, and simplicity for our AI-driven development needs:

1. **Permission Elimination**: No sudo issues within containers
2. **Host Protection**: Container boundary provides isolation
3. **Development Functionality**: Can run Docker and all development tools
4. **Easy Recovery**: Container restart provides clean environment
5. **Resource Efficiency**: Much lighter than VMs
6. **AI-Friendly**: Claude instances can safely experiment

**Safety Measures**:
- Timeshift snapshots before development sessions
- Network isolation for development containers
- Regular container rebuilds from clean images
- Host system monitoring during development
- Emergency rollback procedures

### Consequences

**Positive**:
- Eliminated sudo permission issues for AI development
- Safe experimentation environment for CCN and CCW
- Fast container provisioning and reset capabilities
- Can develop MCP servers and coordination tools safely
- Host system protected by container isolation
- Easy to scale and replicate development environments

**Negative**:
- Privileged containers have inherent security risks
- Docker socket access provides potential host system access
- Need careful monitoring of container activities
- Container escape vulnerabilities need mitigation
- Network configuration complexity

**Neutral**:
- Different development patterns than direct host access
- Need container management and monitoring tools
- Development tools must work within container environment

## Implementation Plan

**Phase 1**: Basic Container Development Environments (Week 1)
- Create privileged development containers for CCN and CCW
- Mount Docker socket for Docker-in-Docker capability
- Configure network isolation and access controls
- Test basic development workflows

**Phase 2**: Safety and Monitoring (Week 2)
- Implement Timeshift integration for host snapshots
- Set up container activity monitoring
- Create emergency rollback procedures
- Establish container rebuild automation

**Phase 3**: MCP Development Integration (Week 3)
- Install Claude Code within development containers
- Configure MCP server development tools
- Set up inter-container networking for MCP coordination
- Test MCP server development and deployment

**Phase 4**: Production Integration (Week 4)
- Establish promotion process from development to production
- Create container-to-host deployment pipelines
- Implement security scanning and validation
- Document operational procedures

**Timeline**: 4 weeks for full implementation
**Resources Required**:
- Docker infrastructure on NucDogg and WorkDogg
- Timeshift configured for system snapshots
- Network isolation capabilities
- Monitoring tools for container activity

## Container Architecture

### **Development Container Specifications**
```yaml
services:
  claude-dev-ccn:
    image: ubuntu:22.04
    privileged: true
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
      - ccn_workspace:/workspace
      - ccn_shared_state:/shared_state
    environment:
      - INSTANCE_NAME=CCN
      - DEVELOPMENT_MODE=true
    networks:
      - isolated_dev_net
```

### **Safety Integrations**
- **Timeshift Snapshots**: Automatic snapshots before development sessions
- **Network Isolation**: Development containers on isolated networks
- **Activity Monitoring**: Container activity logging and alerting
- **Resource Limits**: CPU and memory constraints to prevent resource exhaustion

### **Access Patterns**
- **SSH Access**: For direct development work
- **Docker Socket**: For container development and deployment
- **Shared Volumes**: For persistent workspace and coordination
- **Network Access**: Controlled external connectivity

## Security Considerations

### **Risk Mitigation**
- **Host Monitoring**: Real-time monitoring of host system changes
- **Container Rebuilds**: Regular clean rebuilds from base images
- **Network Isolation**: Development traffic separated from production
- **Timeshift Recovery**: Quick rollback capability for any issues
- **Resource Limits**: Prevent resource exhaustion attacks

### **Acceptable Risk Level**
- Container escape vulnerabilities are mitigated by:
  - Regular security updates
  - Host system monitoring
  - Timeshift snapshots for recovery
  - Network isolation
  - Regular container rebuilds

## Validation Criteria

**Success Metrics**:
- Zero sudo permission issues during AI development
- Safe deployment of MCP coordination infrastructure
- Successful container-based development workflows
- Host system protection maintained during development
- Easy rollback and recovery procedures working
- CCN and CCW can develop and test safely

**Review Schedule**:
- 1-week review: Basic container functionality and safety
- 2-week review: MCP development integration success
- 4-week review: Production promotion process effectiveness

**Reconsideration Triggers**:
- Container security breaches or host system compromises
- Performance issues that can't be resolved
- Development workflow limitations that block progress
- Safety measures proving insufficient

## Related Decisions

- ADR-002: GitHub Orchestration Bootstrap (coordinates container deployments)
- ADR-001: MCP-Centric Architecture (target for development)
- ADR-004: Timeshift Integration for Safety

## References

- [Docker Security Best Practices](https://docs.docker.com/engine/security/)
- [Container Isolation and Security](https://docs.docker.com/engine/security/userns-remap/)
- [Docker-in-Docker Best Practices](https://jpetazzo.github.io/2015/09/03/do-not-use-docker-in-docker-for-ci/)
- [Linux Container Security](https://www.redhat.com/en/topics/security/container-security)
- [Timeshift System Snapshots](https://github.com/teejee2008/timeshift)