# Release Process

This document describes the process for releasing new versions of the `airflow-provider-great-expectations` package to PyPI.

Releases are triggered by creating a GitHub Release. The workflow automatically publishes to PyPI when a release is created.

## Release Steps

### 1. Update Version

**Note**: This step is currently manual. There is no automation for version updates.

Update the version in `great_expectations_provider/__init__.py`:

```python
__version__ = "X.Y.Z"
```

Follow [Semantic Versioning](https://semver.org/):
- **MAJOR** version for incompatible API changes
- **MINOR** version for backwards-compatible functionality additions
- **PATCH** version for backwards-compatible bug fixes

### 2. Update CHANGELOG.md

Add a new entry to `CHANGELOG.md` with:
- Version number and date
- List of changes grouped by type (FEATURE, BUGFIX, MAINTENANCE, DOCUMENTATION, etc.)
- Links to relevant pull requests

Example:
```markdown
## 1.0.0 (2025-01-XX)
* [FEATURE] Description of new feature by @contributor in #123
* [BUGFIX] Description of bug fix by @contributor in #124
```

### 3. Commit and Merge Changes

Commit the version and changelog updates, then merge the PR to `main`:

```bash
git add great_expectations_provider/__init__.py CHANGELOG.md
git commit -m "chore: prepare release X.Y.Z"
git push origin <your-branch>
# Create PR and merge to main
```

**Important**: The version update must be merged to `main` before creating the tag.

### 4. Create Git Tag

After the PR is merged to `main`, create a git tag on the `main` branch matching the version:

```bash
git checkout main
git pull origin main
git tag -a vX.Y.Z -m "Release version X.Y.Z"
git push origin vX.Y.Z
```

**Important**: 
- The tag must be created on the `main` branch (after merging), not on a PR branch
- The tag name must match the version in `__init__.py` exactly (without the `v` prefix in the version file, but with `v` prefix in the tag)

### 5. Create GitHub Release

1. Go to the [GitHub Releases page](https://github.com/great-expectations/airflow-provider-great-expectations/releases)
2. Click "Draft a new release"
3. Select the tag you just created (e.g., `vX.Y.Z`)
4. Set the release title to the version (e.g., `X.Y.Z`)
5. Copy the changelog entry for this version into the release description
6. Click "Publish release"

### 6. Automated Publishing

Once the GitHub Release is created, the CI workflow will automatically:

1. **Verify Version**: Check that the version in `__init__.py` matches the release tag
2. **Build Package**: Create wheel and source distribution using `uv build`
3. **Publish to PyPI**: Upload to PyPI using `uv publish` with trusted publishing
4. **Deploy Documentation**: 
   - For stable releases (non-pre-release versions): Deploy to `latest` alias and set as default
   - For pre-releases: Deploy to `dev` branch

### 7. Verify Release

After the workflow completes:

1. Check the [PyPI project page](https://pypi.org/project/airflow-provider-great-expectations/) to confirm the new version is available
2. Verify the package can be installed:
   ```bash
   pip install airflow-provider-great-expectations==X.Y.Z
   ```
3. Check that documentation is updated at https://great-expectations.github.io/airflow-provider-great-expectations/latest

## Pre-Release Versions

For pre-release versions (alpha, beta, rc), the process is the same, but:

- Use version format like `1.0.0a1`, `1.0.0b1`, `1.0.0rc1`
- Documentation will be deployed to the `dev` branch instead of `latest`
- The version verification script will still check that the tag matches
