# GitHub-Orchestrated Foundation Deployment

## Workflow Architecture

```yaml
# .github/workflows/foundation-deployment.yml
name: Foundation Infrastructure Deployment

on:
  workflow_dispatch:
    inputs:
      deployment_plan:
        description: 'Deployment plan file path'
        required: true
        default: 'planning/deployment-plans/active/foundation-infrastructure-2025-08-02.yml'
      target_environment:
        description: 'Target environment'
        required: true
        default: 'development'
        type: choice
        options:
          - development
          - staging
          - production

  issue_comment:
    types: [created]

jobs:
  validate-deployment:
    if: startsWith(github.event.comment.body, '/deploy') || github.event_name == 'workflow_dispatch'
    runs-on: ubuntu-latest
    outputs:
      plan-valid: ${{ steps.validate.outputs.valid }}
      deployment-id: ${{ steps.create-id.outputs.id }}
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Create Deployment ID
        id: create-id
        run: |
          DEPLOYMENT_ID="deploy-$(date +%Y%m%d-%H%M%S)-${{ github.run_number }}"
          echo "id=$DEPLOYMENT_ID" >> $GITHUB_OUTPUT
          echo "🚀 Created deployment ID: $DEPLOYMENT_ID"
      
      - name: Validate Deployment Plan
        id: validate
        run: |
          PLAN_FILE="${{ github.event.inputs.deployment_plan || 'planning/deployment-plans/active/foundation-infrastructure-2025-08-02.yml' }}"
          
          if [ ! -f "$PLAN_FILE" ]; then
            echo "❌ Deployment plan not found: $PLAN_FILE"
            echo "valid=false" >> $GITHUB_OUTPUT
            exit 1
          fi
          
          # Validate YAML structure
          python tools/planning-validators/validate-deployment-plan.py "$PLAN_FILE"
          
          echo "✅ Deployment plan validated"
          echo "valid=true" >> $GITHUB_OUTPUT
      
      - name: Create Deployment Issue
        if: steps.validate.outputs.valid == 'true'
        uses: actions/github-script@v7
        with:
          script: |
            const deploymentId = '${{ steps.create-id.outputs.id }}';
            const planFile = '${{ github.event.inputs.deployment_plan || 'planning/deployment-plans/active/foundation-infrastructure-2025-08-02.yml' }}';
            
            const { data: issue } = await github.rest.issues.create({
              owner: context.repo.owner,
              repo: context.repo.repo,
              title: `🚀 Foundation Deployment: ${deploymentId}`,
              body: `
## Deployment Status: 🟡 IN PROGRESS

**Deployment ID**: \`${deploymentId}\`
**Plan**: \`${planFile}\`
**Triggered by**: @${context.actor}
**Environment**: ${{ github.event.inputs.target_environment || 'development' }}

## Tasks

### Phase 1: Preparation
- [ ] **CCN**: Validate NucDogg prerequisites
- [ ] **CCW**: Validate WorkDogg prerequisites  
- [ ] **Timeshift**: Create system snapshots

### Phase 2: Foundation Infrastructure
- [ ] **CCN**: Initialize Docker Swarm
- [ ] **CCN**: Create foundation networks and secrets
- [ ] **CCN**: Deploy MCP coordination servers

### Phase 3: Development Environments  
- [ ] **CCW**: Build isolated development containers
- [ ] **CCN**: Configure inter-service networking
- [ ] **Both**: Validate Claude MCP connections

### Phase 4: Validation
- [ ] **CCN**: End-to-end workflow testing
- [ ] **CCW**: External API connectivity testing
- [ ] **CDTZ**: Final coordination validation

## Instructions for CCN/CCW

**CCN (NucDogg)**: Watch this issue and execute tasks assigned to CCN
**CCW (WorkDogg)**: Watch this issue and execute tasks assigned to CCW

Comment with your progress using:
- \`/task-complete <task-name>\` when you finish a task
- \`/task-failed <task-name> <reason>\` if a task fails
- \`/status\` for current status

## Rollback

If anything goes wrong, comment \`/rollback\` to trigger emergency rollback procedures.
              `,
              labels: ['deployment', 'in-progress', 'foundation']
            });
            
            // Set repository variable for tracking
            await github.rest.actions.createRepoVariable({
              owner: context.repo.owner,
              repo: context.repo.repo,
              name: 'ACTIVE_DEPLOYMENT_ISSUE',
              value: issue.data.number.toString()
            });

  assign-tasks:
    needs: validate-deployment
    if: needs.validate-deployment.outputs.plan-valid == 'true'
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Notify CCN (NucDogg)
        uses: actions/github-script@v7
        with:
          script: |
            // Create a repository dispatch event that CCN will listen for
            await github.rest.repos.createDispatchEvent({
              owner: context.repo.owner,
              repo: context.repo.repo,
              event_type: 'ccn-deployment-task',
              client_payload: {
                deployment_id: '${{ needs.validate-deployment.outputs.deployment-id }}',
                issue_number: process.env.ACTIVE_DEPLOYMENT_ISSUE,
                tasks: [
                  'validate_nucdogg_prerequisites',
                  'create_timeshift_snapshot',
                  'initialize_docker_swarm',
                  'create_foundation_networks',
                  'setup_secrets_management',
                  'deploy_coordination_servers'
                ],
                machine: 'nucdogg'
              }
            });
      
      - name: Notify CCW (WorkDogg)  
        uses: actions/github-script@v7
        with:
          script: |
            await github.rest.repos.createDispatchEvent({
              owner: context.repo.owner,
              repo: context.repo.repo,
              event_type: 'ccw-deployment-task',
              client_payload: {
                deployment_id: '${{ needs.validate-deployment.outputs.deployment-id }}',
                issue_number: process.env.ACTIVE_DEPLOYMENT_ISSUE,
                tasks: [
                  'validate_workdogg_prerequisites',
                  'create_timeshift_snapshot',
                  'build_isolated_dev_environments',
                  'configure_claude_mcp_connections',
                  'validate_external_api_access'
                ],
                machine: 'workdogg'
              }
            });

  monitor-deployment:
    needs: [validate-deployment, assign-tasks]
    runs-on: ubuntu-latest
    
    steps:
      - name: Monitor Deployment Progress
        uses: actions/github-script@v7
        with:
          script: |
            // This job will run for up to 2 hours, checking progress
            const maxWaitTime = 2 * 60 * 60 * 1000; // 2 hours
            const checkInterval = 30 * 1000; // 30 seconds
            const startTime = Date.now();
            
            while (Date.now() - startTime < maxWaitTime) {
              // Check issue comments for completion status
              const { data: comments } = await github.rest.issues.listComments({
                owner: context.repo.owner,
                repo: context.repo.repo,
                issue_number: process.env.ACTIVE_DEPLOYMENT_ISSUE
              });
              
              // Look for completion or failure signals
              const latestComments = comments.slice(-10);
              const hasFailure = latestComments.some(c => c.body.includes('/task-failed'));
              const hasCompletion = latestComments.some(c => c.body.includes('🎉 Deployment Complete'));
              
              if (hasFailure) {
                console.log('❌ Deployment failed - triggering rollback');
                // Trigger rollback workflow
                break;
              }
              
              if (hasCompletion) {
                console.log('✅ Deployment completed successfully');
                break;
              }
              
              await new Promise(resolve => setTimeout(resolve, checkInterval));
            }
```

## CCN Local Task Execution

```bash
# Script that CCN runs locally to watch for GitHub tasks
# /home/claude/dogpack-task-listener.sh

#!/bin/bash
REPO="2-EZBee/DoggPack-dev"
MACHINE_ID="CCN"
GITHUB_TOKEN="your-github-token"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1"
}

# Function to check for new deployment tasks
check_for_tasks() {
    # Check for repository dispatch events
    curl -s -H "Authorization: token $GITHUB_TOKEN" \
         -H "Accept: application/vnd.github.v3+json" \
         "https://api.github.com/repos/$REPO/dispatches" | \
    jq -r '.[] | select(.event_type == "ccn-deployment-task") | .client_payload'
}

# Function to execute a deployment task
execute_task() {
    local task=$1
    local deployment_id=$2
    local issue_number=$3
    
    log "🎯 Executing task: $task"
    
    case $task in
        "validate_nucdogg_prerequisites")
            # Check Docker, resources, network connectivity
            if validate_prerequisites; then
                report_task_complete "$task" "$issue_number"
            else
                report_task_failed "$task" "Prerequisites not met" "$issue_number"
            fi
            ;;
            
        "initialize_docker_swarm")
            # Initialize Docker Swarm
            if docker swarm init --advertise-addr $(hostname -I | awk '{print $1}'); then
                # Get join token for WorkDogg
                JOIN_TOKEN=$(docker swarm join-token worker -q)
                
                # Comment the join token on the issue for CCW to use
                comment_on_issue "$issue_number" "🔗 Docker Swarm initialized. Join token: \`$JOIN_TOKEN\`"
                report_task_complete "$task" "$issue_number"
            else
                report_task_failed "$task" "Docker swarm initialization failed" "$issue_number"
            fi
            ;;
            
        "deploy_coordination_servers")
            # Deploy MCP coordination layer
            if deploy_mcp_servers; then
                report_task_complete "$task" "$issue_number"
            else
                report_task_failed "$task" "MCP server deployment failed" "$issue_number"
            fi
            ;;
    esac
}

# Function to report task completion
report_task_complete() {
    local task=$1
    local issue_number=$2
    
    comment_on_issue "$issue_number" "✅ **CCN**: Task completed: \`$task\`"
}

# Function to report task failure
report_task_failed() {
    local task=$1
    local reason=$2
    local issue_number=$3
    
    comment_on_issue "$issue_number" "❌ **CCN**: Task failed: \`$task\` - Reason: $reason"
}

# Function to comment on GitHub issue
comment_on_issue() {
    local issue_number=$1
    local comment=$2
    
    curl -X POST \
         -H "Authorization: token $GITHUB_TOKEN" \
         -H "Accept: application/vnd.github.v3+json" \
         "https://api.github.com/repos/$REPO/issues/$issue_number/comments" \
         -d "{\"body\": \"$comment\"}"
}

# Main execution loop
log "🤖 CCN task listener started"
while true; do
    # Check for new tasks every 30 seconds
    NEW_TASKS=$(check_for_tasks)
    
    if [ ! -z "$NEW_TASKS" ]; then
        # Process the tasks
        echo "$NEW_TASKS" | jq -r '.tasks[]' | while read task; do
            DEPLOYMENT_ID=$(echo "$NEW_TASKS" | jq -r '.deployment_id')
            ISSUE_NUMBER=$(echo "$NEW_TASKS" | jq -r '.issue_number')
            
            execute_task "$task" "$DEPLOYMENT_ID" "$ISSUE_NUMBER"
        done
    fi
    
    sleep 30
done
```

## CCW Isolated Environment Builder

```bash
# Script that CCW runs to build isolated development environments
# /home/claude/build-isolated-environments.sh

#!/bin/bash

build_isolated_dev_environment() {
    local deployment_id=$1
    local issue_number=$2
    
    log "🏗️ Building isolated development environments"
    
    # Create the isolated development stack
    cat > /tmp/isolated-dev-stack.yml << 'EOF'
version: '3.8'

services:
  claude-dev-ccn:
    image: ubuntu:22.04
    hostname: claude-dev-ccn
    restart: unless-stopped
    privileged: true
    volumes:
      - ccn_workspace:/workspace
      - ccn_shared_state:/shared_state
      - /var/run/docker.sock:/var/run/docker.sock
    environment:
      - INSTANCE_NAME=CCN
      - DEVELOPMENT_MODE=true
    command: >
      sh -c "
        apt-get update &&
        apt-get install -y curl wget git docker.io python3 python3-pip nodejs npm openssh-server &&
        
        # Install Claude Code in the container
        curl -fsSL https://anthropic.com/claude-code/install.sh | sh &&
        
        # Configure SSH access
        mkdir -p /home/claude/.ssh &&
        useradd -m -s /bin/bash claude &&
        echo 'claude:claude' | chpasswd &&
        
        # Start SSH service
        service ssh start &&
        
        # Keep container running
        tail -f /dev/null
      "
    networks:
      - development_net
    ports:
      - "2200:22"  # SSH access to CCN dev environment

  claude-dev-ccw:
    image: ubuntu:22.04
    hostname: claude-dev-ccw
    restart: unless-stopped
    privileged: true
    volumes:
      - ccw_workspace:/workspace
      - ccw_shared_state:/shared_state
      - /var/run/docker.sock:/var/run/docker.sock
    environment:
      - INSTANCE_NAME=CCW
      - DEVELOPMENT_MODE=true
    command: >
      sh -c "
        apt-get update &&
        apt-get install -y curl wget git docker.io python3 python3-pip nodejs npm openssh-server &&
        curl -fsSL https://anthropic.com/claude-code/install.sh | sh &&
        mkdir -p /home/claude/.ssh &&
        useradd -m -s /bin/bash claude &&
        echo 'claude:claude' | chpasswd &&
        service ssh start &&
        tail -f /dev/null
      "
    networks:
      - development_net  
    ports:
      - "2201:22"  # SSH access to CCW dev environment

volumes:
  ccn_workspace:
  ccn_shared_state:
  ccw_workspace:
  ccw_shared_state:

networks:
  development_net:
    driver: bridge
EOF

    # Deploy the isolated environments
    if docker stack deploy -c /tmp/isolated-dev-stack.yml isolated-dev; then
        comment_on_issue "$issue_number" "🏗️ **CCW**: Isolated development environments deployed successfully"
        
        # Wait for containers to be ready
        sleep 60
        
        # Test SSH access
        if ssh -o StrictHostKeyChecking=no claude@localhost -p 2200 "echo 'CCN dev environment ready'" && \
           ssh -o StrictHostKeyChecking=no claude@localhost -p 2201 "echo 'CCW dev environment ready'"; then
            report_task_complete "build_isolated_dev_environments" "$issue_number"
        else
            report_task_failed "build_isolated_dev_environments" "SSH access to containers failed" "$issue_number"
        fi
    else
        report_task_failed "build_isolated_dev_environments" "Container deployment failed" "$issue_number"
    fi
}
```

## CDTZ Orchestration

```javascript
// How CDTZ triggers and monitors the deployment

async function deployFoundationInfrastructure() {
    // 1. Trigger GitHub Action from CDTZ
    const deployment = await github.rest.actions.createWorkflowDispatch({
        owner: '2-EZBee',
        repo: 'DoggPack-dev',
        workflow_id: 'foundation-deployment.yml',
        ref: 'main',
        inputs: {
            deployment_plan: 'planning/deployment-plans/active/foundation-infrastructure-2025-08-02.yml',
            target_environment: 'development'
        }
    });
    
    console.log('🚀 Foundation deployment triggered');
    
    // 2. Monitor the deployment issue for progress
    const issueNumber = await getActiveDeploymentIssue();
    
    // 3. Watch for completion or failure
    while (true) {
        const status = await checkDeploymentStatus(issueNumber);
        
        if (status.completed) {
            console.log('✅ Foundation deployment completed successfully!');
            break;
        } else if (status.failed) {
            console.log('❌ Foundation deployment failed');
            // Optionally trigger rollback
            break;
        }
        
        await sleep(30000); // Check every 30 seconds
    }
}
```
