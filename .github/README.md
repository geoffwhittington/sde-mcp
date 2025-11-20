# GitHub Actions Workflows

This directory contains GitHub Actions workflows for CI/CD.

## Workflows

### `ci.yml` - Main CI Pipeline

Runs on every push and pull request:
- **Lint**: Checks code formatting (black, isort) and type checking (mypy)
- **Test**: Runs unit tests on Python 3.10, 3.11, and 3.12
- **Integration**: Runs integration tests (requires `OPENAI_API_KEY` secret)

### `test-prompt-mapping.yml` - Prompt-to-Tool Mapping Tests

Runs when CSV or test files change:
- Validates CSV structure
- Runs prompt-to-tool mapping tests
- Requires `OPENAI_API_KEY` secret

## Setting Up Secrets

To enable integration tests, add the OpenAI API key as a repository secret:

1. Go to **Settings** > **Secrets and variables** > **Actions**
2. Click **New repository secret**
3. Name: `OPENAI_API_KEY`
4. Value: Your OpenAI API key
5. Click **Add secret**

## Workflow Behavior

- **Pull Requests**: Integration tests are skipped for PRs from forks (security)
- **Main/Develop Branches**: Integration tests run if `OPENAI_API_KEY` is set
- **Missing Secret**: Tests are skipped gracefully with a warning message

## Manual Trigger

You can manually trigger workflows:
1. Go to **Actions** tab
2. Select the workflow
3. Click **Run workflow**

