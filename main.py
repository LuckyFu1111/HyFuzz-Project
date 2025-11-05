from utils.logger import setup_logger
from utils.report_generator import generate_report
from utils.cli_selector import select_engine, select_generation
from utils.depth_selector import select_max_depth
from modules.port_scanner import scan_http_ports
from modules.service_detector import detect_http_service
from modules.cve_query import load_cve_database
from modules.vuln_orchestrator import perform_vulnerability_scan
from modules.fuzz_tester.boofuzz_fuzz import run_boofuzz
from modules.fuzz_tester.hypothesis_fuzz import run_hypothesis_fuzz
from modules.fuzz_tester.gan_model import load_fuzz_data, train_gan, generate_test_cases as generate_gan_cases
from modules.fuzz_tester.deepseek_generator import DeepSeekGenerator
from modules.fuzz_tester.generalization_tester import test_generated_cases
import os
import json
import argparse
import sys

def parse_arguments():
    """Parse command-line arguments for HyFuzz."""
    parser = argparse.ArgumentParser(
        description='HyFuzz: A Hybrid AI-Enhanced Vulnerability Detection Framework',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 main.py --targets 192.168.0.100
  python3 main.py --targets 192.168.0.0/24 --fuzzer hypothesis --ai-mode deepseek
  python3 main.py --targets 10.0.0.1 --fuzzer boofuzz --ai-mode gan --depth 3 --timeout 10
        """
    )

    parser.add_argument('--targets', '-t', type=str, required=False,
                        help='Target IP address or CIDR range (e.g., 192.168.0.100 or 192.168.0.0/24)')
    parser.add_argument('--fuzzer', '-f', type=str, choices=['boofuzz', 'hypothesis'],
                        help='Fuzzing engine to use: boofuzz or hypothesis')
    parser.add_argument('--ai-mode', '-a', type=str, choices=['none', 'gan', 'deepseek'],
                        help='AI-based test generation mode: none, gan, or deepseek')
    parser.add_argument('--depth', '-d', type=int, default=3,
                        help='Maximum fuzzing depth (default: 3)')
    parser.add_argument('--timeout', type=int, default=5,
                        help='Timeout per test in seconds (default: 5)')
    parser.add_argument('--interactive', '-i', action='store_true',
                        help='Use interactive mode for selecting options')

    args = parser.parse_args()

    # Validate arguments
    if not args.interactive and not args.targets:
        parser.error('--targets is required unless --interactive mode is used')

    return args

def main(target_ip, fuzz_choice=None, testgen_choice=None, max_depth=3):
    logger = setup_logger()
    logger.info("Starting intelligent HTTP vulnerability detection")

    # Use provided choices or fallback to interactive selection
    if fuzz_choice is None:
        fuzz_choice = select_engine()           # 1: BooFuzz, 2: Hypothesis
    if testgen_choice is None:
        testgen_choice = select_generation()   # 1: None, 2: GAN, 3: DeepSeek
    if max_depth is None:
        max_depth = select_max_depth()         # Let user choose the max fuzzing depth

    open_ports = scan_http_ports(target_ip)
    if not open_ports:
        logger.warning("No open HTTP ports found")
        return

    for port in open_ports:
        service = detect_http_service(target_ip, port)
        if service == "Unknown":
            logger.info(f"Port {port} service unknown, skipping")
            continue

        cve_list, vulnerability_found = perform_vulnerability_scan(target_ip, port, service, logger)

        new_cases = []
        if not vulnerability_found:
            logger.info(f"Port {port} no common vulnerabilities found, performing fuzz testing")

            fuzz_log = None
            anomaly_cases = []

            for depth in range(1, max_depth + 1):
                logger.info(f"Starting fuzz test at depth {depth}...")

                if fuzz_choice == 1:
                    fuzz_log = run_boofuzz(target_ip, port, depth=depth)
                elif fuzz_choice == 2:
                    # Pass depth explicitly, num_examples is base per depth
                    fuzz_log = run_hypothesis_fuzz(target_ip, port, num_examples=50, depth=depth)
                else:
                    logger.warning("Invalid fuzzing engine selection. Skipping fuzzing.")
                    break

                if fuzz_log:
                    anomaly_cases = load_fuzz_data(fuzz_log)
                    if anomaly_cases:
                        logger.info(f"Anomalies found at depth {depth}, stopping further fuzzing.")
                        break
                    else:
                        logger.info(f"No anomalies found at depth {depth}.")

            if fuzz_log and anomaly_cases:
                if testgen_choice == 2:
                    logger.info("Training GAN with fuzz data...")
                    generator, _ = train_gan(anomaly_cases)
                    output_path = generate_gan_cases(generator, num_cases=10)
                    logger.info(f"Generated new fuzz test cases using GAN written to: {output_path}")
                elif testgen_choice == 3:
                    logger.info("Generating test cases with DeepSeek...")
                    generator = DeepSeekGenerator()
                    generator.train_from_log()
                    output_path = generator.save_generated_cases(num_cases=10)
                    logger.info(f"Generated new fuzz test cases using DeepSeek written to: {output_path}")
                else:
                    logger.info("Raw fuzzing only. Skipping AI-based generation.")

                if testgen_choice in [2, 3]:
                    filepath = os.path.abspath(output_path)
                    if os.path.exists(filepath):
                        logger.info("Running generalization testing on generated fuzz cases...")
                        results = test_generated_cases(target_ip, port, filepath, logger)
                        result_path = os.path.join(os.path.dirname(filepath), "generalization_results.json")
                        with open(result_path, "w", encoding="utf-8") as f:
                            json.dump(results, f, indent=4)
                        logger.info(f"Generalization test results saved to {result_path}")
                    else:
                        logger.warning(f"Generated case file not found: {filepath}")
            else:
                logger.info("No anomaly cases found, skipping AI-based generation")

        generate_report(
            target_ip=target_ip,
            open_ports=open_ports,
            service=service,
            cve_list=cve_list,
            fuzz_results={"fuzz_cases": new_cases}
        )


if __name__ == "__main__":
    args = parse_arguments()

    # Map string choices to numeric codes
    fuzzer_map = {'boofuzz': 1, 'hypothesis': 2}
    ai_mode_map = {'none': 1, 'gan': 2, 'deepseek': 3}

    if args.interactive:
        # Interactive mode - use hardcoded default or prompt user
        target_ip = "192.168.25.133"
        main(target_ip)
    else:
        # CLI mode - use provided arguments
        target_ip = args.targets
        fuzz_choice = fuzzer_map.get(args.fuzzer) if args.fuzzer else None
        testgen_choice = ai_mode_map.get(args.ai_mode) if args.ai_mode else None
        max_depth = args.depth

        main(target_ip, fuzz_choice, testgen_choice, max_depth)
