# SACEF - Self-Adversarial Code Evolution Framework

SACEF is an enterprise-grade, self-improving security framework designed to proactively identify and mitigate vulnerabilities in Python applications. By leveraging a unique combination of genetic fuzzing, symbolic execution, and machine learning, SACEF not only finds bugs in your code but also in itself, creating a continuously hardening security analysis engine.

## Vision

To provide a fully autonomous, self-improving security partner that integrates seamlessly into the software development lifecycle, enabling organizations to build more secure and resilient applications with confidence. SACEF is designed to be the proactive, intelligent layer of defense that anticipates threats before they become vulnerabilities.

## Key Features

-   **Hybrid Fuzzing Engine:** Combines a genetic algorithm with a concolic execution engine (`SymbolicPathExplorer`) to discover complex vulnerabilities that traditional fuzzers miss.
-   **ML-Guided Mutations:** Employs a machine learning model (`MLVulnerabilityPredictor`) to predict code weaknesses and guide the fuzzer's mutation strategies, creating an intelligent feedback loop.
-   **Self-Adversarial Analysis:** SACEF is the security tool that audits itself. It uses its own fuzzing engine to dynamically find vulnerabilities in its internal components, ensuring its own robustness.
-   **Probabilistic Type Fuzzing:** A configurable fuzzer that uses probabilistic input generation to efficiently find type-related vulnerabilities.
-   **Enterprise-Ready Tooling:** Features structured JSON reporting, configurable logging, and a professional command-line interface (CLI) for easy integration into CI/CD pipelines and security dashboards.

## Getting Started

### Installation

1.  Clone the repository:
    ```bash
    git clone https://github.com/your-repo/sacef.git
    cd sacef
    ```

2.  Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3.  Install the framework as a runnable package:
    ```bash
    pip install .
    ```

## Usage

SACEF is controlled through a command-line interface. The primary entry point is the `sacef` command.

### Basic Analysis

To analyze a Python file, use the `--target` argument:

```bash
sacef --target /path/to/your/code.py
```

### Advanced Usage

-   **JSON Reporting:** To save the analysis results to a JSON file, use the `--output` argument:
    ```bash
    sacef --target /path/to/your/code.py --output results.json
    ```

-   **Logging:** Control the logging verbosity with the `--log` argument. To write logs to a file, specify a path:
    ```bash
    sacef --target /path/to/your/code.py --log sacef.log
    ```

-   To set the logging level (e.g., to `DEBUG` for more detail):
    ```bash
    sacef --target /path/to/your/code.py --log-level DEBUG
    ```

## Configuration

The framework's behavior can be fine-tuned through the `config.yaml` file in the root directory. This file allows you to configure parameters for the `GeneticFuzzer` and the `MLVulnerabilityPredictor`, such as population size, mutation rates, and ML model weights. This eliminates the need for hardcoded values and allows for environment-specific tuning.
