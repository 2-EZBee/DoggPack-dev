# DoggPack Planning Documentation

This directory contains all planning, architecture, and decision documentation for the DoggPack infrastructure project.

## Structure

- **architecture/**: Versioned architecture documentation
- **deployment-plans/**: Structured deployment plans with templates
- **specifications/**: Detailed specifications for services and integrations
- **decisions/**: Architecture Decision Records (ADRs)
- **research/**: Background research and analysis

## Planning Workflow

1. **Architecture Planning**: Document major architectural decisions in `decisions/`
2. **Deployment Planning**: Create structured plans in `deployment-plans/active/`
3. **Specification**: Detail service requirements in `specifications/`
4. **Validation**: Use planning validators to check consistency
5. **Approval**: Get formal approval before moving to implementation

## GitHub-Orchestrated Planning

The DoggPack ecosystem uses **GitHub as the coordination layer** for planning and deployment:

### **Planning Process**
```
CDTZ creates plan → GitHub PR → Review & validation → Approval → GitHub Actions deployment
```

### **Deployment Coordination**
```
CDTZ triggers → GitHub Actions → Repository dispatch → CCN/CCW execution → Progress tracking
```

### **Claude Instance Roles**
- **CDTZ (ZenDogg)**: Planning orchestration and GitHub coordination
- **CCN (NucDogg)**: Infrastructure deployment and Docker management
- **CCW (WorkDogg)**: Development environments and processing tasks

## Current Planning Focus

- GitHub-orchestrated deployment architecture
- Foundation infrastructure deployment
- Isolated development environment strategy
- Progressive enhancement to MCP coordination

## Active Work

- [Foundation Infrastructure Deployment Plan](./deployment-plans/active/)
- [MCP-Centric Architecture ADR](./decisions/001-mcp-centric-approach.md)
- [GitHub Orchestration Bootstrap ADR](./decisions/002-github-orchestration-bootstrap.md)

## Planning Templates

- [Deployment Plan Template](./deployment-plans/templates/deployment-plan-template.yml)
- [ADR Template](./decisions/template-adr.md)
- [Service Specification Template](./specifications/templates/)

See [current deployment plans](./deployment-plans/active/) for active work.