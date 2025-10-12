from sacef.framework import SelfAdversarialFramework
from sacef.modules.genetic_fuzzer import GeneticFuzzer
from sacef.modules.ml_vulnerability_predictor import MLVulnerabilityPredictor
from tests.target_functions import vulnerable_multiply, safe_function
from utils.testing import TestRunner


def run_comprehensive_tests():
    """Run ALL tests including framework self-tests."""

    print("╔═══════════════════════════════════════════════════════════════╗")
    print("║  COMPREHENSIVE TESTING - Framework Testing Itself            ║")
    print("╚═══════════════════════════════════════════════════════════════╝")

    test_runner = TestRunner()

    # TEST 1: Basic functionality
    def test_genetic_fuzzer_basics():
        """Test that genetic fuzzer can find vulnerabilities."""
        fuzzer = GeneticFuzzer(population_size=20)

        def vuln_func(x):
            return x * 10**9

        attacks = fuzzer.evolve(vuln_func, generations=2)

        # Should find at least one high-fitness attack
        has_high_fitness = any(f > 50 for _, f in attacks)

        if has_high_fitness:
            print(f"    Found {len(attacks)} attacks, best fitness: {max(f for _, f in attacks):.1f}")

        return has_high_fitness

    test_runner.run_test("Genetic Fuzzer - Basic Functionality", test_genetic_fuzzer_basics)

    # TEST 2: Fuzzer robustness
    def test_genetic_fuzzer_robustness():
        """Test fuzzer with extreme inputs."""
        fuzzer = GeneticFuzzer()

        extreme_funcs = [
            lambda x: None,
            lambda x: float('inf'),
            lambda x: 1 / 0,  # Will raise exception
        ]

        crashes = 0
        for func in extreme_funcs:
            try:
                fuzzer.evolve(func, generations=1)
            except Exception as e:
                crashes += 1
                print(f"    Fuzzer crashed with: {type(e).__name__}")

        # Should handle most edge cases
        return crashes <= 1  # Allow 1 crash (div by zero)

    test_runner.run_test("Genetic Fuzzer - Robustness", test_genetic_fuzzer_robustness)

    # TEST 3: Mutation safety
    def test_mutation_safety():
        """Test that mutation doesn't cause overflow."""
        fuzzer = GeneticFuzzer()

        large_values = [10**15, 10**18, 2**60]
        overflows = 0

        for val in large_values:
            try:
                mutated = fuzzer._mutate(val)
                # Check if mutation caused significant growth
                if isinstance(mutated, (int, float)) and abs(mutated) > abs(val) * 100:
                    overflows += 1
            except:
                pass

        # Mutations should be safe
        return overflows == 0

    test_runner.run_test("Mutation - Overflow Safety", test_mutation_safety)

    # TEST 4: Fitness function edge cases
    def test_fitness_edge_cases():
        """Test fitness with edge case inputs."""
        fuzzer = GeneticFuzzer()

        edge_cases = [
            (None, lambda x: None),
            ("", lambda x: ""),
            ([], lambda x: []),
            (0, lambda x: 0),
        ]

        errors = 0
        for payload, func in edge_cases:
            try:
                fitness = fuzzer.evaluate_fitness(payload, func)
                # Fitness should be between 0 and 100
                if not (0 <= fitness <= 100):
                    errors += 1
            except Exception as e:
                errors += 1

        return errors == 0

    test_runner.run_test("Fitness Function - Edge Cases", test_fitness_edge_cases)

    # TEST 5: Full integration test
    def test_full_integration():
        """Test complete framework on vulnerable function."""
        framework = SelfAdversarialFramework()

        result = framework.analyze_function(vulnerable_multiply, verbose=False)

        # Should find at least one vulnerability
        found_vulns = result['vulnerabilities'] > 0

        if found_vulns:
            print(f"    Found {result['vulnerabilities']} vulnerabilities")

        return found_vulns

    test_runner.run_test("Integration - Complete Analysis", test_full_integration)

    # TEST 6: ML prediction
    def test_ml_prediction():
        """Test ML predictor."""
        predictor = MLVulnerabilityPredictor()

        # Extract features from vulnerable function
        features = predictor.extract_features(vulnerable_multiply)
        score = predictor.predict_score(features)

        # Should predict some risk (> 0.1)
        has_risk = score > 0.1

        if has_risk:
            print(f"    Predicted risk: {score:.1%}")

        return has_risk

    test_runner.run_test("ML Predictor - Risk Assessment", test_ml_prediction)

    # TEST 7: Safe function detection
    def test_safe_function_detection():
        """Test that safe functions have fewer vulnerabilities."""
        framework = SelfAdversarialFramework()

        result_vuln = framework.analyze_function(vulnerable_multiply, verbose=False)
        result_safe = framework.analyze_function(safe_function, verbose=False)

        # Safe function should have fewer or equal vulnerabilities
        is_discriminating = result_safe['vulnerabilities'] <= result_vuln['vulnerabilities']

        print(f"    Vulnerable: {result_vuln['vulnerabilities']}, Safe: {result_safe['vulnerabilities']}")

        return is_discriminating

    test_runner.run_test("Detection - Safe vs Vulnerable", test_safe_function_detection)

    # Print summary
    test_runner.report()

    return test_runner
