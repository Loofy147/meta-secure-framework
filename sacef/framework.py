import time
from typing import Callable, Dict

from sacef.core.context import TargetFunctionContext
from sacef.core.datastructures import Vulnerability, AttackVector, SeverityLevel
from sacef.modules.genetic_fuzzer import GeneticFuzzer
from sacef.modules.symbolic_path_explorer import SymbolicPathExplorer
from sacef.modules.quantum_superposition_tester import QuantumSuperpositionTester
from sacef.modules.ml_vulnerability_predictor import MLVulnerabilityPredictor
from sacef.self_attack import SelfAttackModule


class SelfAdversarialFramework:
    """Framework with self-testing capabilities."""

    def __init__(self):
        self.genetic_fuzzer = GeneticFuzzer()
        self.symbolic_explorer = SymbolicPathExplorer()
        self.quantum_tester = QuantumSuperpositionTester()
        self.ml_predictor = MLVulnerabilityPredictor()
        self.self_attacker = SelfAttackModule(self)

        self.vulnerabilities = []
        self.test_results = []

    def analyze_function(self, func: Callable, context: TargetFunctionContext = None, verbose: bool = True) -> Dict:
        """Analyze a function."""
        if verbose:
            print(f"\n{'='*70}")
            print(f"🔍 Analyzing: {func.__name__}")
            print(f"{'='*70}")

        vulns = []
        stats = {}
        start = time.time()

        try:
            # ML Prediction
            if verbose:
                print("\n[1/4] 🤖 ML Prediction")
            features = self.ml_predictor.extract_features(func)
            predicted = self.ml_predictor.predict_score(features)
            stats['predicted_risk'] = predicted
            if verbose:
                print(f"  Predicted risk: {predicted:.1%}")

            # Genetic Fuzzing
            if verbose:
                print("\n[2/4] 🧬 Genetic Fuzzing")
            evolved = self.genetic_fuzzer.evolve(func, context=context, generations=3)
            stats['attacks_found'] = len(evolved)
            if verbose:
                print(f"  Found {len(evolved)} attacks")

            for payload, fitness in evolved:
                if fitness > 40:
                    vuln = Vulnerability(
                        attack_vector=AttackVector.OVERFLOW if fitness > 60 else AttackVector.LOGIC_BYPASS,
                        severity=min(fitness / 100.0, 0.95),
                        severity_level=SeverityLevel.CRITICAL,
                        exploit_code=f"Payload: {repr(payload)[:60]}",
                        failure_trace=[f"Fitness: {fitness:.1f}"],
                        discovered_at=time.time(),
                        patch_suggestions=["Add validation"]
                    )
                    vulns.append(vuln)

            # Symbolic Execution
            if verbose:
                print("\n[3/4] 🔮 Symbolic Execution")
            paths = self.symbolic_explorer.explore_paths(func)
            if verbose:
                print(f"  Explored {len(paths)} paths")

            # Quantum Testing
            if verbose:
                print("\n[4/4] ⚛️  Quantum Testing")
            superposition = self.quantum_tester.create_input_superposition([int, str, type(None)])
            collapsed = self.quantum_tester.collapse_superposition(func, superposition, context=context)
            if verbose:
                print(f"  {len(collapsed)} states collapsed")

            for state_name, data in collapsed.items():
                if data.get('failure', 0) > 0:
                    vuln = Vulnerability(
                        attack_vector=AttackVector.TYPE_CONFUSION,
                        severity=0.6,
                        severity_level=SeverityLevel.HIGH,
                        exploit_code=f"State: {state_name}",
                        failure_trace=[f"{data['failure']} failures"],
                        discovered_at=time.time(),
                        patch_suggestions=["Add type checking"]
                    )
                    vulns.append(vuln)

            # ML Training
            self.ml_predictor.train(features, len(vulns))

            self.vulnerabilities.extend(vulns)

        except Exception as e:
            if verbose:
                print(f"\n❌ Error: {e}")

        result = {
            'function': func.__name__,
            'duration': time.time() - start,
            'vulnerabilities': len(vulns),
            'stats': stats
        }

        self.test_results.append(result)

        if verbose:
            print(f"\n✅ Complete: {len(vulns)} vulnerabilities found")

        return result
