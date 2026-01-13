# CI Secrets Configuration

This document describes the secrets required to run integration tests in CI for the Great Expectations Airflow Provider.

## GX Cloud Test Organization

Integration tests run against the **GX-Airflow-Tests** organization in GX Cloud. This organization is managed by the Great Expectations team and should only contain test resources created by CI.

## Required GitHub Configuration

Configure these in GitHub repository settings under **Settings > Secrets and variables > Actions**.

### Variables

| Variable Name | Description |
|--------------|-------------|
| `GX_CLOUD_ORGANIZATION_ID` | The organization ID (visible in GX Cloud UI, URLs, or existing GitHub variables) |
| `GX_CLOUD_WORKSPACE_ID` | A workspace ID within the test organization |

### Secrets

| Secret Name | Description |
|------------|-------------|
| `GX_CLOUD_ACCESS_TOKEN` | API access token for authenticating with GX Cloud |

## Creating/Rotating Credentials

1. Get invited to the **GX-Airflow-Tests** organization by an existing member with admin access.
2. Log in to [GX Cloud](https://app.greatexpectations.io/) and navigate to **Tokens**.
3. On the Tokens page you can find all required values: organization ID, workspace ID, and create user or organization access tokens.
4. Update the GitHub variables and secrets accordingly.

## GitHub Environments

The CI workflow uses two GitHub environments to control access to secrets:

- **internal**: Used for PRs from branches within the repository (has access to secrets)
- **external**: Used for PRs from forks (requires manual approval before secrets are accessible)

This protects secrets from being exposed in PRs from untrusted forks.

## Security Notes

- **Never commit credentials** to the repository.
- Access tokens should be rotated periodically.
- Only grant access to the test organization to maintainers who need it.
