# Infrastructure Scripts

## Deployment Scripts

- `deploy-foundation.sh` - Deploy foundation infrastructure
- `setup-environment.sh` - Initial environment setup
- `setup-service-accounts.sh` - Configure service accounts and secrets

## Management Scripts

- `health-check.sh` - Comprehensive system health check
- `backup.sh` - Create system backups
- `rollback.sh` - Rollback to previous state
- `logs.sh` - Collect and analyze logs

## Automation Scripts

- `task-listener.sh` - Listen for GitHub deployment tasks
- `timeshift-automation.sh` - Automated snapshot management
- `monitoring-setup.sh` - Configure monitoring and alerting

## Usage

All scripts should be run from the repository root:

```bash
./implementation/infrastructure/scripts/script-name.sh
```