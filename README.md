# SACEF - Self-Adversarial Code Evolution Framework

This project contains SACEF, a sophisticated framework designed to find vulnerabilities in Python code through a variety of advanced techniques, including genetic fuzzing, symbolic path exploration, and quantum-inspired testing. A key feature of SACEF is its self-adversarial nature, meaning it actively tests and attacks its own components to identify meta-vulnerabilities and ensure its own robustness.

## Project Structure

The framework has been refactored from a single script into a modular and scalable project structure:

-   `main.py`: The main entry point to run the complete analysis, including all tests, self-attacks, and reporting.
-   `sacef/`: The core source code for the framework.
    -   `core/`: Contains core components like data structures.
    -   `modules/`: Houses the various analysis modules (Genetic Fuzzer, Symbolic Path Explorer, etc.).
    -   `framework.py`: The main `SelfAdversarialFramework` class that orchestrates the analysis.
    -   `self_attack.py`: The `SelfAttackModule` responsible for testing the framework itself.
-   `tests/`: Contains the testing suite for the framework.
    -   `test_framework.py`: The comprehensive test suite that validates the framework's functionality.
    -   `target_functions.py`: A collection of vulnerable and safe functions used for testing.
-   `utils/`: Contains utility classes and functions, such as the `TestRunner`.

## How to Run

To run the full SACEF analysis, simply execute the `main.py` script from the root directory of the project:

```bash
python3 main.py
```

This will perform the following phases:
1.  **Framework Self-Validation:** Runs a comprehensive test suite on the framework's components.
2.  **Self-Attack Mode:** The framework attacks its own code to find meta-vulnerabilities.
3.  **Target Analysis:** Analyzes a set of predefined target functions.
4.  **Comprehensive Reporting:** Outputs a final report with statistics and a JSON summary.
