# Changelog

All notable changes to the Agent Spreadsheet Protocol project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- CSV backend implementation for local file access
- Core protocol envelope and message handling
- SHEET_LIST handler for discovering available sheets
- READ_RANGE handler for reading cell ranges
- Handler registry system for extensibility
- JSON schemas for message validation
- Development and contribution guidelines
- Comprehensive documentation

### Planned

- Google Sheets backend
- Excel backend
- Airtable backend
- ACTION_PROPOSE handler for safe write operations
- ACTION_EXECUTE handler for performing approved writes
- ANOMALY_DETECT handler for outlier detection
- TREND_ANALYSIS handler
- Web UI dashboard
- Python SDK for agents
- JavaScript/Node.js SDK
- Go implementation

## [0.1.0] - 2026-01-28

### Added

- Initial project structure
- FastAPI server setup
- Basic CSV backend with range parsing
- Message envelope structure
- Handler registry
- Sample data (sales.csv)
- Specification document
- JSON schemas for core message types

---

## How to Update This File

When making releases or significant changes:

1. Add an `[Unreleased]` section at the top if not present
2. Create a new version header: `## [X.Y.Z] - YYYY-MM-DD`
3. Use these subsections (as applicable):
   - **Added** for new features
   - **Changed** for changes in existing functionality
   - **Deprecated** for soon-to-be removed features
   - **Removed** for now removed features
   - **Fixed** for bug fixes
   - **Security** for security fixes

Example:

```markdown
## [1.0.0] - 2026-02-01

### Added

- Google Sheets backend integration
- Web UI dashboard
- Rate limiting

### Changed

- Updated message envelope format
- Improved error handling

### Fixed

- Bug in range parsing with special characters
- Memory leak in CSV backend

### Security

- Added input validation for all handlers
```

---

## Release Notes

### Version 0.1.0 (Initial Release)

- Foundation: Core protocol infrastructure
- Implementation: CSV backend with read operations
- Documentation: Specification and development guides
- Status: Pre-release, working toward 1.0.0

**Next Release Target:** 0.2.0

- Expected features: Write operations and approval workflow
- Timeline: Q1 2026
