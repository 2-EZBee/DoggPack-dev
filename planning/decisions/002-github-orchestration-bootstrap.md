# ADR-002: GitHub Actions for Infrastructure Deployment Bootstrap

**Status**: Accepted  
**Date**: 2025-08-02  
**Deciders**: DoggPack AI Team  
**Technical Impact**: High  
**Business Impact**: Medium  

## Context and Problem Statement

While our long-term vision is MCP-centric infrastructure coordination, we face a bootstrap problem: the MCP coordination infrastructure doesn't exist yet, and we need a way for CDTZ (ZenDogg) to orchestrate deployments on CCN (NucDogg) and CCW (WorkDogg) during the initial setup phase.

Additionally, previous attempts at AI-led deployment with Claude Code have been plagued with sudo permission problems and the complexity of setting up secure service accounts before we have the infrastructure to manage them.

We need a bootstrap strategy that:
- Allows CDTZ to maintain control and orchestration
- Avoids sudo permission issues during deployment
- Uses existing infrastructure (GitHub, Claude Code already installed)
- Provides a clear evolution path to pure MCP coordination
- Enables building isolated development environments safely

## Decision Drivers

- **ZenDogg Control Preference**: User wants to orchestrate everything from CDTZ when possible
- **Sudo Permission Issues**: Previous deployments failed due to permission complexity
- **Existing Infrastructure**: Claude Code already installed on all machines with GitHub access
- **Bootstrap Challenge**: Need coordination before coordination infrastructure exists
- **Isolated Environment Goals**: Want to build safe development containers for future work
- **Evolution Path**: Must provide clear progression to MCP-only coordination

## Considered Options

### Option 1: Direct SSH Coordination
**Description**: CDTZ executes commands on remote machines via SSH

**Pros**:
- Direct control from ZenDogg
- No intermediate services required
- Familiar SSH patterns
- Can start immediately

**Cons**:
- SSH key management complexity
- Sudo permission issues persist
- Security implications of SSH automation
- No coordination state management
- Difficult error handling and rollback

**Implementation Complexity**: Medium
**Risk Level**: High

### Option 2: Custom Bootstrap Service
**Description**: Build temporary coordination service just for bootstrap

**Pros**:
- Tailored to bootstrap needs
- Can avoid sudo issues with proper design
- Direct control from CDTZ

**Cons**:
- Additional development effort
- Temporary infrastructure that gets discarded
- Still requires initial deployment of the bootstrap service
- Doesn't leverage existing infrastructure

**Implementation Complexity**: High
**Risk Level**: Medium

### Option 3: GitHub Actions Orchestration
**Description**: Use GitHub Actions as coordination hub with existing Claude Code instances

**Pros**:
- Leverages existing GitHub MCP integration
- Uses already-installed Claude Code instances
- CDTZ maintains orchestration control
- Built-in audit trail and monitoring
- No sudo issues (containers handle privileges)
- Can build isolated environments safely
- Clear evolution path to MCP coordination

**Cons**:
- Requires internet connectivity for coordination
- GitHub rate limits and dependencies
- More complex than direct approaches
- Need to build task coordination patterns

**Implementation Complexity**: Medium
**Risk Level**: Low

## Decision Outcome

**Chosen Option**: GitHub Actions Orchestration

**Rationale**:

GitHub Actions provides the optimal balance of control, safety, and evolution path:

1. **ZenDogg Control**: CDTZ can trigger and monitor deployments through GitHub Actions
2. **Permission Safety**: Isolated containers eliminate sudo permission issues
3. **Existing Infrastructure**: Uses Claude Code already installed and GitHub MCP already configured
4. **Bootstrap Solution**: Solves the coordination problem without requiring coordination infrastructure
5. **Evolution Path**: GitHub remains useful for CI/CD even after MCP coordination is established
6. **Audit Trail**: Complete deployment history and coordination logs

### Consequences

**Positive**:
- CDTZ maintains orchestration control from ZenDogg
- Eliminated sudo permission issues through containerization
- Leverages existing, tested infrastructure (GitHub, Claude Code)
- Provides complete audit trail of all deployments
- Enables safe building of isolated development environments
- Creates foundation for pure MCP coordination
- Supports both manual and AI-triggered deployments

**Negative**:
- Requires internet connectivity for coordination
- Dependency on GitHub service availability
- More complex coordination patterns than direct methods
- Need to build GitHub Actions workflows and task listeners
- Temporary dual-coordination model during transition

**Neutral**:
- GitHub becomes permanent part of CI/CD infrastructure
- Need to learn GitHub Actions patterns for infrastructure
- Different coordination model than pure MCP approach

## Implementation Plan

**Phase 1**: GitHub Actions Foundation (Week 1)
- Create GitHub Actions workflows for deployment coordination
- Build task listener scripts for CCN and CCW
- Implement GitHub issue-based progress tracking
- Test basic coordination patterns

**Phase 2**: Foundation Infrastructure Deployment (Week 2)
- Deploy isolated development environments using GitHub coordination
- Build MCP servers inside isolated containers
- Establish Docker Swarm and networking foundation
- Validate external API access through containers

**Phase 3**: Hybrid Coordination (Week 3)
- MCP servers operational in isolated environments
- Both GitHub and MCP coordination working
- Begin transitioning simple tasks to MCP coordination
- Maintain GitHub for complex deployment orchestration

**Phase 4**: MCP Migration (Week 4+)
- Gradually move coordination tasks to pure MCP
- GitHub Actions become CI/CD and emergency backup
- CDTZ coordinates primarily through MCP tools
- GitHub remains for repository management and workflows

**Timeline**: 4+ weeks with gradual evolution
**Resources Required**:
- GitHub repository with Actions enabled
- Claude Code instances with GitHub MCP access
- Docker on both target machines
- Network connectivity for GitHub API access

## Coordination Architecture

### **Bootstrap Flow**
```
CDTZ (Planning) → GitHub Actions (Coordination) → CCN/CCW (Execution)
     ↓                    ↓                           ↓
Trigger workflow → Repository dispatch → Task listeners
     ↓                    ↓                           ↓
Monitor progress ← GitHub issues ← Progress reports
```

### **Task Assignment Pattern**
```yaml
CDTZ: Workflow triggering, progress monitoring, deployment approval
GitHub: Task dispatch, progress tracking, coordination state
CCN: NucDogg infrastructure, Docker Swarm, core services
CCW: WorkDogg environments, development containers, processing
```

### **Evolution Path**
```
GitHub-Only → GitHub + MCP → MCP + GitHub backup → Pure MCP
```

## Validation Criteria

**Success Metrics**:
- CDTZ can trigger deployments and monitor progress from ZenDogg
- Zero sudo permission issues during deployment
- Isolated development environments built successfully
- Complete audit trail of all deployment activities
- CCN and CCW coordinate effectively through GitHub
- Smooth evolution to MCP coordination when ready

**Review Schedule**:
- 1-week review: Assess GitHub Actions coordination effectiveness
- 2-week review: Evaluate isolated environment deployment success
- 4-week review: Plan MCP coordination transition

**Reconsideration Triggers**:
- GitHub rate limiting blocking deployments
- Internet connectivity requirements causing issues
- Inability to build isolated environments safely
- GitHub Actions proving insufficient for coordination needs

## Related Decisions

- ADR-001: MCP-Centric Architecture (long-term target)
- ADR-003: Isolated Development Environment Design
- ADR-004: Timeshift Integration for Deployment Safety

## References

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [GitHub MCP Server](https://github.com/modelcontextprotocol/servers/tree/main/src/github)
- [Repository Dispatch Events](https://docs.github.com/en/rest/repos/repos#create-a-repository-dispatch-event)
- [Docker in Docker Best Practices](https://docs.docker.com/engine/security/)
- [Claude Code GitHub Integration](https://docs.anthropic.com/claude-code)