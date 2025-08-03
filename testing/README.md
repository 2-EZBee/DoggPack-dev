# DoggPack Testing

Testing framework and test suites for the DoggPack AI-centric infrastructure.

## Testing Structure

- **unit-tests/**: Unit tests for individual components
- **integration-tests/**: Integration tests for service interactions
- **deployment-tests/**: End-to-end deployment validation
- **load-tests/**: Performance and load testing

## Testing Philosophy

### AI-Driven Infrastructure Testing

Testing AI-driven infrastructure requires special considerations:

1. **Plan Validation**: Ensure deployment plans are syntactically correct
2. **Coordination Testing**: Verify Claude instances can coordinate effectively
3. **Isolation Testing**: Validate development environment isolation
4. **Rollback Testing**: Ensure rollback procedures work under stress
5. **Integration Testing**: Verify external API connections work correctly

### Test Categories

- **Static Analysis**: YAML/JSON validation, linting
- **Unit Tests**: Individual script and function testing
- **Integration Tests**: Multi-service interaction testing
- **E2E Tests**: Complete workflow validation
- **Chaos Tests**: Failure scenario testing

## Running Tests

```bash
# Run all tests
./testing/run-all-tests.sh

# Run specific test category
./testing/run-unit-tests.sh
./testing/run-integration-tests.sh
./testing/run-deployment-tests.sh

# Validate deployment plans
./testing/validate-deployment-plans.sh
```

## Test Development

- Follow the testing standards in each subdirectory
- Include both positive and negative test cases
- Test error handling and recovery scenarios
- Mock external dependencies where appropriate
- Document test assumptions and requirements