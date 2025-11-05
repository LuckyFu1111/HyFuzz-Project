# Changelog

All notable changes to HyFuzz will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Command-line argument parsing with argparse for flexible usage
- HTML report generation with professional styling and risk assessment
- Comprehensive YAML/JSON configuration file support
- Configuration loader with validation and default values
- Unit test suite with pytest framework
- GitHub Actions CI/CD pipeline for automated testing
- Type hints throughout the codebase
- Proper dependency versioning in requirements.txt
- CONTRIBUTING.md with development guidelines
- Code quality checks (flake8, black, isort)
- Security scanning with bandit in CI pipeline

### Changed
- Replaced unsafe `eval()` calls with `ast.literal_eval()` for security
- Improved exception handling in vulnerability tests (replaced bare `except:` with specific exceptions)
- Enhanced report generator to produce both JSON and HTML outputs
- Updated main.py to support both CLI and interactive modes
- Improved logging with better error messages

### Fixed
- Security vulnerability: eval() usage on untrusted log data
- Poor exception handling in exp_tester.py (8 instances)
- Missing version constraints in requirements.txt
- Hardcoded configuration values

### Security
- Fixed arbitrary code execution vulnerability in log parsing (CVE-candidate)
- Improved input validation throughout the codebase
- Added security scanning to CI/CD pipeline

## [0.1.0] - 2025-01-XX (Initial Release)

### Added
- Two-stage vulnerability detection framework
- CVE-based detection with PoC validation
- Support for BooFuzz and Hypothesis fuzzers
- GAN-based payload generation
- DeepSeek LLM integration (simulated)
- Port scanning and service detection
- Basic JSON report generation
- Support for HTTP, MQTT, Modbus, and CoAP protocols
- Nginx vulnerability tests (1.8 and 1.18)

---

## Legend

- **Added**: New features
- **Changed**: Changes in existing functionality
- **Deprecated**: Soon-to-be removed features
- **Removed**: Removed features
- **Fixed**: Bug fixes
- **Security**: Security fixes
