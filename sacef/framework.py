import time
import logging
from typing import Callable, Dict, Any

from sacef.core.context import TargetFunctionContext
from sacef.core.datastructures import Vulnerability, AttackVector, SeverityLevel
from sacef.modules.genetic_fuzzer import GeneticFuzzer
from sacef.modules.symbolic_path_explorer import SymbolicPathExplorer
from sacef.modules.probabilistic_fuzzer import ProbabilisticFuzzer
from sacef.modules.ml_vulnerability_predictor import MLVulnerabilityPredictor
from sacef.modules.mutation_advisor import MutationAdvisor
from sacef.self_attack import SelfAttackModule


class SelfAdversarialFramework:
    """Framework with self-testing capabilities."""

    def __init__(self, config: Dict[str, Any] = None):
        if config is None:
            config = {}

        self.logger = logging.getLogger('sacef')
        self.genetic_fuzzer = GeneticFuzzer(config.get('genetic_fuzzer'))
        self.symbolic_explorer = SymbolicPathExplorer()
        self.probabilistic_fuzzer = ProbabilisticFuzzer()
        self.ml_predictor = MLVulnerabilityPredictor(config.get('ml_predictor'))
        self.self_attacker = SelfAttackModule(self)

        self.vulnerabilities = []
        self.test_results = []

    def analyze_function(self, func: Callable, context: TargetFunctionContext = None) -> Dict:
        """Analyze a function."""
        self.logger.info(f"Starting analysis of function: {func.__name__}")

        # Reset the fuzzer's state for the new analysis
        self.genetic_fuzzer.reset()

        vulns = []
        stats = {}
        start = time.time()

        try:
            # ML Prediction
            self.logger.info("Performing ML prediction...")
            features = self.ml_predictor.extract_features(func)
            predicted = self.ml_predictor.predict_score(features)
            stats['predicted_risk'] = predicted
            self.logger.info(f"Predicted risk: {predicted:.1%}")

            # Create the feedback loop
            mutation_strategies = self.ml_predictor.predict_mutation_strategy(features)
            advisor = MutationAdvisor(mutation_strategies)
            self.genetic_fuzzer.advisor = advisor # Inject the advisor into the fuzzer

            # Hybrid Fuzzing Loop (Concolic Execution)
            self.logger.info("Starting hybrid fuzzing (concolic execution)...")

            try:
                # Initial fuzzing to get interesting seeds
                initial_population = self.genetic_fuzzer.initialize_population()

                # Use the most promising seed for concolic exploration
                # We iterate through seeds because some types may not be compatible with the function signature
                import inspect
                arg_names = inspect.getfullargspec(func).args
                new_inputs = None

                for seed in initial_population:
                    seed_input = [seed] * len(arg_names) if arg_names else []
                    try:
                        new_inputs = self.symbolic_explorer.explore_path(func, seed_input)
                        if new_inputs or not arg_names:
                            # Found a valid path or function has no args, so we can stop searching for a seed
                            break
                    except TypeError:
                        # This seed type is not compatible, try the next one
                        continue

                if new_inputs:
                    self.logger.info(f"Concolic engine found new input: {new_inputs}")
                    # Add the new, path-aware input to the fuzzer's population
                    self.genetic_fuzzer.add_to_population(new_inputs)
            except Exception as e:
                self.logger.warning(f"Concolic exploration failed: {e}")

            # Run the genetic fuzzer with the (potentially) enriched population
            evolved = self.genetic_fuzzer.evolve(func, context=context, generations=3)
            stats['attacks_found'] = len(evolved)
            self.logger.info(f"Genetic fuzzer found {len(evolved)} potential attacks.")

            for payload, fitness in evolved:
                if fitness > 40:
                    attack_vector = AttackVector.LOGIC_BYPASS
                    if fitness > 90:
                        attack_vector = AttackVector.CODE_INJECTION
                    elif fitness > 75:
                        attack_vector = AttackVector.OVERFLOW

                    vuln = Vulnerability(
                        attack_vector=attack_vector,
                        severity=min(fitness / 100.0, 0.95),
                        severity_level=SeverityLevel.CRITICAL,
                        exploit_code=f"Payload: {repr(payload)[:60]}",
                        failure_trace=[f"Fitness: {fitness:.1f}"],
                        discovered_at=time.time(),
                        patch_suggestions=["Add validation"]
                    )
                    vulns.append(vuln)

            # Probabilistic Fuzzing
            self.logger.info("Starting probabilistic fuzzing...")
            type_distribution = {int: 0.4, str: 0.4, type(None): 0.1, bool: 0.1}
            fuzz_results = self.probabilistic_fuzzer.fuzz(func, type_distribution, context=context)
            self.logger.info(f"Fuzzed {self.probabilistic_fuzzer.fuzz_iterations} inputs.")

            for type_name, data in fuzz_results.items():
                if data.get('failure', 0) > 0:
                    self.logger.warning(f"Probabilistic fuzzer found {data['failure']} failures for type: {type_name}")
                    vuln = Vulnerability(
                        attack_vector=AttackVector.TYPE_CONFUSION,
                        severity=min(0.2 + (data['failure'] / self.probabilistic_fuzzer.fuzz_iterations), 0.8),
                        severity_level=SeverityLevel.HIGH,
                        exploit_code=f"Type: {type_name}",
                        failure_trace=[f"{data['failure']} failures out of {data['success'] + data['failure']} attempts"],
                        discovered_at=time.time(),
                        patch_suggestions=["Add type checking"]
                    )
                    vulns.append(vuln)

            # ML Training
            self.ml_predictor.train(features, len(vulns))

            self.vulnerabilities.extend(vulns)

        except Exception as e:
            self.logger.error(f"An unexpected error occurred during analysis: {e}", exc_info=True)

        result = {
            'function': func.__name__,
            'duration': time.time() - start,
            'vulnerabilities': len(vulns),
            'stats': stats
        }

        self.test_results.append(result)
        self.logger.info(f"Analysis of {func.__name__} complete. Found {len(vulns)} vulnerabilities.")

        return result
