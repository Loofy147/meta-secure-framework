import argparse
import inspect
import importlib.util
import sys
from sacef.framework import SelfAdversarialFramework
from sacef.logger import setup_logging
from sacef.reporter import generate_report, save_report_to_json
from utils.config_loader import load_config

def main():
    """
    Main execution entry point for the SACEF CLI.
    """
    parser = argparse.ArgumentParser(description="Self-Adversarial Code Evolution Framework (SACEF)")
    parser.add_argument("--target", required=True, help="Path to the Python file to analyze.")
    parser.add_argument("--output", help="Path to save the JSON report.")
    parser.add_argument("--log", help="Path to a file to write logs to.")
    parser.add_argument("--log-level", default="INFO", help="Set the logging level (e.g., DEBUG, INFO, WARNING).")

    args = parser.parse_args()

    # Set up the logger. This will be the single source of output.
    logger = setup_logging(args.log, args.log_level)

    logger.info("SACEF v4.0 - Enterprise Edition")
    logger.info("="*40)

    # Load configuration from config.yaml
    config = load_config()

    # Initialize the framework
    framework = SelfAdversarialFramework(config)

    # Run the self-attack first to ensure the framework is robust
    framework.self_attacker.run_full_self_attack()

    # Load the target file and find functions to analyze
    try:
        spec = importlib.util.spec_from_file_location("target_module", args.target)
        target_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(target_module)

        # Find all functions defined in the target module
        target_functions = [
            obj for name, obj in inspect.getmembers(target_module)
            if inspect.isfunction(obj) and obj.__module__ == "target_module"
        ]

        if not target_functions:
            logger.error("No functions found in the target file.")
            sys.exit(1)

    except FileNotFoundError:
        logger.error(f"Target file not found: {args.target}")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Error loading target file: {e}", exc_info=True)
        sys.exit(1)

    # Analyze each function
    for func in target_functions:
        framework.analyze_function(func)

    # Generate and (optionally) save the final report
    final_report = generate_report(framework.test_results, framework.vulnerabilities)

    if args.output:
        try:
            save_report_to_json(final_report, args.output)
            logger.info(f"JSON report saved to: {args.output}")
        except Exception as e:
            logger.error(f"Failed to save JSON report: {e}", exc_info=True)
    else:
        # If no output file is specified, print a summary to the log
        logger.info("="*40)
        logger.info("Analysis Complete - Summary Report")
        logger.info(f"  Functions Analyzed: {final_report['summary']['total_functions_analyzed']}")
        logger.info(f"  Vulnerabilities Found: {final_report['summary']['total_vulnerabilities_found']}")
        logger.info(f"  Total Duration: {final_report['summary']['total_duration']:.2f}s")
        logger.info("="*40)

    logger.info("SACEF execution complete.")

if __name__ == "__main__":
    main()
