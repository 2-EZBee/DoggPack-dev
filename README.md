# DoggPack Development

AI-centric infrastructure for the DoggPack ecosystem, enabling **natural language infrastructure management** through coordinated Claude instances.

## 🎯 **Vision**

Transform infrastructure management from manual configuration to **conversational orchestration**:

```
"Deploy N8N automation with GitHub integration" → AI coordinates deployment across machines
```

## 🏗️ **Architecture Overview**

The DoggPack ecosystem uses a **GitHub-orchestrated, MCP-centric architecture** where:

- **CDTZ (ZenDogg)**: Planning and coordination through GitHub Actions
- **CCN (NucDogg)**: Infrastructure management and core services  
- **CCW (WorkDogg)**: Development workloads and processing
- **GitHub**: Coordination hub for deployment orchestration

### **Current Phase: GitHub-Orchestrated Bootstrap**
```
CDTZ → GitHub Actions → CCN/CCW → Isolated Environments → Pure MCP
```

1. **CDTZ triggers** deployment via GitHub Actions
2. **GitHub coordinates** task assignment to CCN/CCW
3. **CCN/CCW execute** tasks and report progress
4. **Isolated environments** built for future MCP coordination

## 🚀 **Quick Start**

### **Prerequisites**
- Fresh Ubuntu 22.04 LTS on NucDogg and WorkDogg
- Claude Code installed on both machines
- Docker installed and configured
- GitHub repository access configured

### **Deploy Foundation Infrastructure**

**From CDTZ (ZenDogg):**
```
"Deploy the foundation infrastructure using the GitHub-orchestrated workflow"
```

**Or manually trigger:**
1. Go to [Actions tab](../../actions)
2. Select "Foundation Infrastructure Deployment"
3. Click "Run workflow"
4. Monitor progress in the created deployment issue

### **Development Workflow**

1. **Plan**: Create deployment plans in `planning/deployment-plans/active/`
2. **Review**: Use GitHub PRs for plan validation
3. **Deploy**: Trigger via GitHub Actions from CDTZ
4. **Monitor**: Track progress through deployment issues
5. **Evolve**: Transition to direct MCP coordination

## 📋 **Project Structure**

```
DoggPack-dev/
├── planning/                    # 📋 Architecture & Deployment Planning
│   ├── architecture/            # Versioned architecture docs
│   ├── deployment-plans/        # Structured deployment plans
│   ├── decisions/              # Architecture Decision Records (ADRs)
│   └── specifications/         # Service and integration specs
├── implementation/             # 🚀 Infrastructure Code
│   ├── infrastructure/         # Docker, MCP servers, scripts
│   ├── applications/           # Windows control app, dashboards
│   └── workflows/             # N8N templates, GitHub Actions
├── .github/                   # 🤖 GitHub Automation
│   ├── workflows/             # Deployment orchestration
│   └── ISSUE_TEMPLATE/        # Planning and deployment templates
└── documentation/             # 📚 User & Developer Guides
```

## 🤖 **Claude Instance Coordination**

### **Current Coordination Model**
- **Planning**: CDTZ creates deployment plans and triggers GitHub Actions
- **Execution**: CCN/CCW receive tasks via GitHub repository dispatch events
- **Monitoring**: All instances monitor GitHub issues for progress updates
- **Communication**: GitHub comments and issue updates

### **Task Assignment Pattern**
```yaml
CDTZ: Planning, orchestration, monitoring
CCN:  Docker Swarm, core services, NucDogg infrastructure
CCW:  Development environments, processing, WorkDogg workloads
```

## 📈 **Evolution Roadmap**

### **Phase 1: GitHub Bootstrap** (Current)
- ✅ Repository structure and planning templates
- 🚧 GitHub Actions coordination workflows
- 🚧 Foundation infrastructure deployment
- 🚧 Isolated development environments

### **Phase 2: Hybrid Coordination** (Next)
- MCP servers deployed in isolated environments
- GitHub + MCP coordination working together
- Enhanced Claude instance communication
- Windows control application for CDTZ

### **Phase 3: Pure MCP** (Future)
- Direct MCP coordination between Claude instances
- Natural language → infrastructure without GitHub intermediary
- Advanced AI-driven optimization and self-healing
- Local AI model support

## 🛠️ **Development**

### **Start Development Session**
```bash
# On NucDogg and WorkDogg
./implementation/scripts/start-task-listener.sh

# Creates Timeshift snapshot and starts GitHub task monitoring
```

### **Create Deployment Plan**
```bash
# Copy template and customize
cp planning/deployment-plans/templates/deployment-plan-template.yml \
   planning/deployment-plans/active/my-deployment-$(date +%Y-%m-%d).yml

# Validate plan
python tools/planning-validators/validate-deployment-plan.py \
       planning/deployment-plans/active/my-deployment-*.yml
```

### **Monitor Active Deployments**
- Check [Issues](../../issues?q=is%3Aissue+is%3Aopen+label%3Adeployment) for active deployments
- Watch [Actions](../../actions) for workflow status
- Review deployment progress in issue comments

## 🔐 **Security Model**

### **Isolated Development Environments**
- All development happens in containers
- Host system protected by containerization
- Easy rollback through Timeshift snapshots
- Network isolation between development and production

### **Secrets Management**
- GitHub secrets for API tokens
- Docker secrets for container credentials
- No secrets in repository code
- Progressive enhancement to comprehensive secrets management

## 📊 **Status Dashboard**

### **Infrastructure Status**
- **NucDogg**: Ready for coordination layer deployment
- **WorkDogg**: Ready for development environment deployment
- **ZenDogg**: CDTZ configured for GitHub orchestration

### **Current Deployments**
- **Foundation Infrastructure**: Ready for deployment
- **N8N Automation Stack**: Planned
- **Knowledge Management**: Planned

### **Architecture Decisions**
- [ADR-001: MCP-Centric Approach](./planning/decisions/001-mcp-centric-approach.md)
- [ADR-002: GitHub Orchestration Bootstrap](./planning/decisions/002-github-orchestration-bootstrap.md)
- [ADR-003: Isolated Development Environments](./planning/decisions/003-isolated-development-environments.md)
- [ADR-006: Remove Portainer and Asana](./planning/decisions/006-remove-portainer-asana.md)

## 🤝 **Contributing**

### **Planning Contributions**
1. Create ADR for significant architectural decisions
2. Use deployment plan templates for new infrastructure
3. Validate plans with provided tools
4. Get approval through GitHub PR process

### **Implementation Contributions**
1. Follow deployment plans in `planning/deployment-plans/`
2. Test in isolated development environments
3. Document implementation in corresponding plan
4. Report completion through GitHub issue comments

## 📚 **Documentation**

- **User Guides**: [./documentation/user-guides/](./documentation/user-guides/)
- **Developer Guides**: [./documentation/developer-guides/](./documentation/developer-guides/)
- **API Reference**: [./documentation/api-reference/](./documentation/api-reference/)
- **Operations**: [./documentation/operations/](./documentation/operations/)

## 🎉 **Get Started**

Ready to deploy AI-driven infrastructure?

1. **Review** the [Foundation Deployment Plan](./planning/deployment-plans/active/)
2. **Trigger** deployment from CDTZ or GitHub Actions
3. **Monitor** progress through deployment issues
4. **Evolve** to direct MCP coordination

---

*The future of infrastructure is conversational. Let's build it together.*