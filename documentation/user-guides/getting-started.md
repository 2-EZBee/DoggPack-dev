# Getting Started with DoggPack Development

Welcome to the DoggPack AI-centric infrastructure! This guide will help you understand and use the repository for planning, developing, and deploying AI-coordinated infrastructure.

## Quick Overview

DoggPack is a revolutionary approach to infrastructure management where Claude instances coordinate to deploy and manage services through natural language interactions. The system consists of:

- **CDTZ (ZenDogg)**: Planning and coordination interface
- **CCN (NucDogg)**: Infrastructure management and core services  
- **CCW (WorkDogg)**: Development workloads and processing

All coordination happens through **Model Context Protocol (MCP)** servers, enabling natural language infrastructure management.

## Repository Structure

```
DoggPack-dev/
├── planning/           📋 Planning & Architecture
│   ├── architecture/   🏗️ Architecture documentation
│   ├── deployment-plans/ 📋 Structured deployment plans
│   ├── decisions/      📝 Architecture Decision Records (ADRs)
│   └── specifications/ 📄 Technical specifications
├── implementation/     🚀 Implementation Code
│   ├── infrastructure/ 🏗️ Docker, MCP servers, scripts
│   ├── applications/   💻 Custom applications
│   └── workflows/      🔄 Automation workflows
├── documentation/      📚 User and developer guides
├── testing/           🧪 Test suites
├── tools/             🔧 Development and validation tools
└── .github/           🤖 Workflows and issue templates
```

## Getting Started Workflows

### 1. **Understanding the Current State**

Start by reviewing the current architecture and plans:

```bash
# Clone the repository
git clone https://github.com/2-EZBee/DoggPack-dev.git
cd DoggPack-dev

# Review the main architecture
cat planning/architecture/v1.0/ai-centric-architecture.md

# Check current deployment plans
ls planning/deployment-plans/active/

# Review architectural decisions
ls planning/decisions/
```

### 2. **Planning a New Deployment**

When you want to deploy a new service or modify infrastructure:

```bash
# Create a new deployment plan
cp planning/deployment-plans/templates/deployment-plan-template.yml \
   planning/deployment-plans/active/my-service-$(date +%Y-%m-%d).yml

# Edit the plan with your requirements
nano planning/deployment-plans/active/my-service-*.yml

# Validate the plan
python tools/planning-validators/validate-deployment-plan.py \
       planning/deployment-plans/active/my-service-*.yml

# Create a planning issue
gh issue create --template deployment-plan.md --title "Deploy My Service"
```

### 3. **Making Architecture Decisions**

For significant architectural changes:

```bash
# Create an ADR based on the template
cp planning/decisions/template-adr.md \
   planning/decisions/004-my-decision.md

# Edit with your decision context and options
nano planning/decisions/004-my-decision.md

# Create an architecture decision issue
gh issue create --template architecture-decision.md --title "Architecture: My Decision"

# Submit for review
git checkout -b decision/my-decision
git add planning/decisions/004-my-decision.md
git commit -m "ADR-004: My architectural decision"
git push origin decision/my-decision
gh pr create --title "ADR-004: My Decision" --body "Architecture decision for review"
```

## Understanding DoggPack Coordination

### **How Claude Instances Work Together**

The DoggPack system uses a sophisticated coordination model:

1. **CDTZ (Planning)**: Creates deployment plans and coordinates overall strategy
2. **CCN (Infrastructure)**: Manages core infrastructure, Docker Swarm, networking
3. **CCW (Processing)**: Handles development environments and specialized processing

### **MCP-Based Communication**

All Claude instances communicate through standardized MCP servers:

- **Planning Coordinator**: Manages deployment state and coordination
- **Docker Management**: Controls container orchestration
- **System Monitoring**: Tracks system health and performance
- **API Gateway**: Handles external service integration

### **GitHub Orchestration**

Deployments are triggered and coordinated through GitHub:

```bash
# Trigger a deployment
gh workflow run foundation-deployment.yml \
   -f deployment_plan=planning/deployment-plans/active/foundation-infrastructure-2025-08-02.yml \
   -f target_environment=development

# Monitor progress in the created issue
gh issue list --label deployment
```

## Key Concepts

### **AI-First Infrastructure**

Traditional infrastructure management adds AI as a helper. DoggPack inverts this:

- **Describe what you want** in natural language
- **AI generates the technical implementation**
- **Humans approve and monitor** strategic decisions
- **Systems self-optimize** based on AI analysis

### **Isolated Development Environments**

Each Claude instance operates in isolated Docker containers with:

- **Full development tools** (Node.js, Python, Claude Code)
- **Docker access** for container management
- **External API connectivity** through secure gateways
- **Shared state coordination** through MCP servers

### **Natural Language Deployments**

Instead of writing YAML configurations manually:

1. **Describe your needs**: "I want to deploy a Node.js API with Redis caching"
2. **AI generates plans**: Claude creates deployment specifications
3. **Review and approve**: Human oversight for critical decisions
4. **Automated execution**: Coordinated deployment across instances

## Common Tasks

### **Reviewing System Status**

```bash
# Check deployment plans
find planning/deployment-plans/active/ -name "*.yml" | head -5

# Review recent decisions
ls -la planning/decisions/ | tail -5

# Check for active deployments
gh issue list --label deployment --state open
```

### **Contributing to Architecture**

```bash
# Start a feature branch
git checkout -b feature/my-enhancement

# Add your changes to the appropriate directory
# - planning/ for architectural changes
# - implementation/ for code
# - documentation/ for guides

# Validate your changes
python tools/planning-validators/validate-deployment-plan.py path/to/plan.yml

# Submit for review
git add .
git commit -m "Add: my enhancement description"
git push origin feature/my-enhancement
gh pr create --title "Enhancement: My Feature" --body "Description of changes"
```

### **Understanding Dependencies**

The DoggPack system has a dependency hierarchy:

1. **Foundation Infrastructure** (Docker Swarm, MCP servers)
2. **Core Services** (Monitoring, API Gateway)
3. **Application Services** (N8N, Obsidian, etc.)
4. **Specialized Services** (AI workloads, media processing)

Each deployment plan specifies its dependencies to ensure proper ordering.

## Troubleshooting

### **Plan Validation Errors**

```bash
# Run the validator for detailed error messages
python tools/planning-validators/validate-deployment-plan.py my-plan.yml

# Common issues:
# - Missing required sections
# - Invalid Claude instance assignments
# - Malformed YAML
# - Circular dependencies
```

### **GitHub Workflow Issues**

```bash
# Check workflow runs
gh run list

# View specific run details
gh run view <run-id>

# Check repository dispatch events
gh api repos/2-EZBee/DoggPack-dev/dispatches
```

### **Understanding MCP Communication**

MCP servers provide standardized interfaces for AI-infrastructure interaction:

- **Tools**: Specific functions (create container, check status, etc.)
- **Resources**: Data sources (deployment state, system metrics)
- **Prompts**: Reusable AI prompts for common tasks

## Next Steps

1. **Review the foundation deployment plan**: `planning/deployment-plans/active/foundation-infrastructure-2025-08-02.yml`
2. **Understand the MCP architecture**: `planning/architecture/v1.0/ai-centric-architecture.md`
3. **Examine coordination patterns**: `planning/architecture/v1.0/github-orchestrated-deployment.md`
4. **Try creating a simple deployment plan** using the template
5. **Join the coordination workflow** by participating in deployment issues

## Resources

- **Architecture Documentation**: `/planning/architecture/v1.0/`
- **Deployment Templates**: `/planning/deployment-plans/templates/`
- **Tool Reference**: `/tools/planning-validators/`
- **Issue Templates**: `/.github/ISSUE_TEMPLATE/`
- **Workflow Documentation**: `/.github/workflows/`

The DoggPack ecosystem represents a fundamental shift toward AI-first infrastructure management. Welcome to the future of intelligent systems coordination!
