# HyFuzz: A Hybrid AI-Enhanced Vulnerability Detection Framework

**HyFuzz** is a modular two-stage vulnerability scanner that integrates deterministic CVE correlation with adaptive fuzz testing guided by machine learning. The system combines traditional signature-based methods with generative adversarial networks (GANs) and large language models (LLMs), enabling efficient detection of both known and previously undocumented vulnerabilities.

This repository provides the source code, evaluation scripts, and configuration files for the experiments presented in our IEEE RTSI 2025 submission.

---

## 📌 Overview

- **Stage 1:** CVE-based detection via banner fingerprinting and proof-of-concept (PoC) validation using Metasploit.
- **Stage 2:** Dynamic fuzzing with BooFuzz or Hypothesis, followed by optional payload corpus expansion using:
  - a fine-tuned GAN model, or
  - the zero-shot DeepSeek-r1 language model.
- **Output:** JSON and HTML reports including CVE hits, anomaly logs, and unique crash traces.

The architecture is protocol-agnostic and supports services such as HTTP, MQTT, Modbus, and CoAP.

---

## 📥 Installation

### Prerequisites
- Python 3.9+
- Docker (for PoC sandboxing)
- pip (Python package manager)

### Setup Instructions

```bash
# Clone the repository
git clone https://github.com/cs7org/HyFuzz.git
cd HyFuzz

# Install Python dependencies
pip install -r requirements.txt
```


## ▶️ Running the Scanner

### Command-Line Mode

```bash
# Basic usage with target IP
python3 main.py --targets 192.168.0.100 --fuzzer hypothesis --ai-mode none

# Advanced usage with all options
python3 main.py --targets 192.168.0.0/24 --fuzzer boofuzz --ai-mode deepseek --depth 5 --timeout 10

# Get help
python3 main.py --help
```

### Interactive Mode

```bash
# Run in interactive mode (prompts for all options)
python3 main.py --interactive
```

### Command-Line Options

| Argument       | Short | Description                              | Default |
|----------------|-------|------------------------------------------|---------|
| `--targets`    | `-t`  | Target IP or CIDR range                  | Required (unless `-i`) |
| `--fuzzer`     | `-f`  | Fuzzing engine: `boofuzz` or `hypothesis` | Interactive prompt |
| `--ai-mode`    | `-a`  | AI mode: `none`, `gan`, or `deepseek`    | Interactive prompt |
| `--depth`      | `-d`  | Maximum fuzzing depth                    | 3 |
| `--timeout`    |       | Timeout per test (seconds)               | 5 |
| `--interactive`| `-i`  | Use interactive mode                     | False |

### Configuration File

You can also use a configuration file for persistent settings:

```bash
# Edit the configuration
nano configs/config.yaml

# HyFuzz will automatically load configs/config.yaml if it exists
python3 main.py --targets 192.168.1.100
```

### Output and Results

Scan reports are saved in multiple formats:

- **`<target_ip>_report.json`** - Machine-readable JSON report
- **`<target_ip>_report.html`** - Human-readable HTML report with visualizations
- **`fuzz_output/fuzz.log`** - Detailed trace of fuzzing attempts
- **`generated_output/generated_cases.log`** - AI-generated test cases (if using GAN/DeepSeek)

## 📊 Reproducing Results

To replicate the experiments described in the paper:

- Launch three local servers using test images: Apache 2.4, Nginx 1.18, and IIS 10.

- Run HyFuzz against each server in all four configurations:
  - CVE-only
  - Baseline fuzzing
  - Fuzz + GAN
  - Fuzz + DeepSeek

- Compare detection time, crash discovery, and false-positive rate as described in Section IV of the paper.

See experiments/configs/ for example scripts.

## 🧪 Configuration

HyFuzz supports configuration via YAML or JSON files. The default configuration is located at `configs/config.yaml`.

```yaml
# Example configuration
fuzzing:
  engine: "hypothesis"
  max_depth: 3
  timeout: 5

ai_generation:
  mode: "none"  # Options: none, gan, deepseek

port_scanning:
  ports: [80, 443, 8080, 8443]
  timeout: 2
```

You can customize:
- Port scanning parameters
- Fuzzing engine and depth
- AI generation settings
- CVE database paths
- Report output formats
- Logging levels

See `configs/config.yaml` for all available options.

## 📚 Citation
If you use HyFuzz in your research, please cite:
```bash
@misc{Hyfuzz,
  author       = {Yanlei Fu and Loui Al Sardy},
  title        = {HyFuzz: A Hybrid AI-Enhanced Vulnerability Detection Framework},
  howpublished = {\url{https://github.com/cs7org/HyFuzz}},
  year         = {2025},
  note         = {Accessed: 2025-05-14}
}
```

## 📄 License
HyFuzz is released under the MIT License. See LICENSE for full terms.

## 🤝 Contributing
We welcome contributions! Please open an issue or submit a pull request. For feature requests or collaboration inquiries, feel free to reach out.

## 📬 Contact
✉️ yanlei.fu@fau.de
✉️ loui.alsardy@fau.de
🌐 https://github.com/cs7org/HyFuzz

## 🔎 Acknowledgements
Developed as part of the CS7 Lab (Computer Networks and Communication Systems) at Friedrich–Alexander University Erlangen–Nürnberg (FAU).
