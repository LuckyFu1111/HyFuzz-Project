# Contributing to HyFuzz

We welcome contributions to HyFuzz! This document provides guidelines for contributing to the project.

## Getting Started

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/your-username/HyFuzz.git
   cd HyFuzz
   ```
3. **Create a new branch** for your feature or bug fix:
   ```bash
   git checkout -b feature/your-feature-name
   ```

## Development Setup

1. **Install Python 3.9+** (recommended: 3.10 or 3.11)

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Install development dependencies**:
   ```bash
   pip install pytest pytest-cov pytest-mock flake8 black isort mypy
   ```

## Coding Standards

### Code Style

- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) Python style guide
- Use **4 spaces** for indentation (not tabs)
- Maximum line length: **127 characters**
- Use **type hints** for function arguments and return values
- Write **docstrings** for all public modules, classes, and functions

### Code Formatting

Before submitting code, format it with:

```bash
# Format code with black
black modules/ utils/ main.py

# Sort imports with isort
isort modules/ utils/ main.py
```

### Linting

Check your code with:

```bash
# Run flake8
flake8 modules/ utils/ main.py

# Run pylint (optional)
pylint modules/ utils/ main.py
```

## Testing

### Running Tests

```bash
# Run all tests
pytest tests/

# Run with coverage
pytest tests/ --cov=modules --cov=utils --cov-report=html

# Run specific test file
pytest tests/test_config_loader.py -v
```

### Writing Tests

- Place tests in the `tests/` directory
- Name test files `test_*.py`
- Name test functions `test_*`
- Use descriptive test names that explain what is being tested
- Aim for >80% code coverage

Example test:

```python
import unittest
from modules.your_module import your_function

class TestYourFunction(unittest.TestCase):
    def test_basic_functionality(self):
        """Test that your_function works correctly."""
        result = your_function("input")
        self.assertEqual(result, "expected_output")
```

## Pull Request Process

1. **Update documentation** if you're changing functionality
2. **Add tests** for new features
3. **Run the test suite** and ensure all tests pass
4. **Update CHANGELOG.md** with your changes
5. **Commit your changes**:
   ```bash
   git add .
   git commit -m "feat: Add new vulnerability test for Apache"
   ```
6. **Push to your fork**:
   ```bash
   git push origin feature/your-feature-name
   ```
7. **Create a Pull Request** on GitHub

### Commit Message Format

We follow the [Conventional Commits](https://www.conventionalcommits.org/) specification:

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

**Examples:**
```
feat(fuzzer): Add support for MQTT protocol fuzzing
fix(scanner): Correct port timeout handling
docs(readme): Update installation instructions
test(config): Add tests for YAML configuration loading
```

## Adding New Features

### Adding a New Vulnerability Test

1. Create your test function in `modules/exp_tester.py`:
   ```python
   def test_your_vulnerability(target_ip, port):
       """Test for Your Vulnerability.

       Args:
           target_ip (str): Target IP address
           port (int): Target port

       Returns:
           bool: True if vulnerability found, False otherwise
       """
       try:
           # Your test logic here
           response = requests.get(f"http://{target_ip}:{port}/test")
           if "vulnerable" in response.text:
               return True
       except (requests.RequestException, requests.Timeout) as e:
           print(f"[WARN] Test failed: {e}", file=sys.stderr)
       return False
   ```

2. Update `modules/vuln_orchestrator.py` to call your test

3. Add unit tests in `tests/test_exp_tester.py`

### Adding a New Fuzzer

1. Create a new file in `modules/fuzz_tester/`
2. Implement the fuzzing interface
3. Update `main.py` to support the new fuzzer
4. Add configuration in `configs/config.yaml`
5. Write tests

## Security

- **Never commit sensitive data** (API keys, credentials, etc.)
- Use **environment variables** for sensitive configuration
- Follow **secure coding practices**
- Report security vulnerabilities privately to: yanlei.fu@fau.de

## Code Review Process

All submissions require review. We use GitHub pull requests for this purpose:

1. Maintainers will review your code
2. Address any requested changes
3. Once approved, your PR will be merged

## Questions?

- Open an issue for bugs or feature requests
- Contact maintainers at:
  - yanlei.fu@fau.de
  - loui.alsardy@fau.de

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing to HyFuzz! 🎉
