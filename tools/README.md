# DoggPack Development Tools

Utilities and tools for developing, testing, and managing the DoggPack infrastructure.

## Tool Categories

### Planning Validators
- **validate-deployment-plan.py**: Validate deployment plan structure
- **dependency-checker.py**: Check plan dependencies
- **plan-summarizer.py**: Generate plan summaries
- **adr-validator.py**: Validate ADR format and content

### Deployment Simulators
- **deployment-simulator.py**: Simulate deployments before execution
- **resource-calculator.py**: Calculate resource requirements
- **timeline-estimator.py**: Estimate deployment timelines
- **risk-assessor.py**: Assess deployment risks

### MCP Testing Tools
- **mcp-server-tester.py**: Test MCP server functionality
- **coordination-tester.py**: Test Claude coordination
- **connection-validator.py**: Validate MCP connections
- **performance-profiler.py**: Profile MCP performance

### Documentation Generators
- **diagram-generator.py**: Generate architecture diagrams
- **api-doc-generator.py**: Generate API documentation
- **changelog-generator.py**: Generate change logs
- **status-reporter.py**: Generate status reports

## Usage

```bash
# Validate a deployment plan
python tools/planning-validators/validate-deployment-plan.py \
       planning/deployment-plans/active/my-plan.yml

# Simulate a deployment
python tools/deployment-simulators/deployment-simulator.py \
       --plan planning/deployment-plans/active/my-plan.yml

# Test MCP server
python tools/mcp-testing-tools/mcp-server-tester.py \
       --server planning-coordinator

# Generate documentation
python tools/documentation-generators/api-doc-generator.py
```

## Tool Development

- Follow Python best practices
- Include comprehensive error handling
- Provide clear usage instructions
- Test tools thoroughly before use
- Document all tool options and parameters