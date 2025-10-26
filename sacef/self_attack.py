import time
import logging
from typing import List, Callable
from sacef.core.datastructures import Vulnerability, AttackVector, SeverityLevel

class SelfAttackModule:
    """
    Attacks the framework's own code to find meta-vulnerabilities.
    This module uses the framework's own tools to test itself.
    """

    def __init__(self, framework):
        self.framework = framework
        self.meta_vulnerabilities = []
        self.logger = logging.getLogger('sacef')

    def _target_symbolic_explorer(self, payload: bytes):
        """
        A wrapper to make the symbolic explorer a valid fuzzing target.
        This will be attacked by the genetic fuzzer.
        """
        try:
            # The symbolic explorer expects a function and an input list.
            # We'll create a dummy function and feed the fuzzer's payload to it.
            dummy_func = lambda x: x
            self.framework.symbolic_explorer.explore_path(dummy_func, [payload])
        except TypeError as e:
            # A TypeError is a common failure mode for the explorer, so we'll
            # raise a more specific exception to be caught by the fuzzer.
            if "must be a list" in str(e):
                raise ValueError("Symbolic explorer failed with non-list input")
        except Exception:
            # Re-raise any other exceptions to be caught by the fuzzer.
            raise

    def attack_symbolic_explorer(self) -> List[Vulnerability]:
        """
        Uses the GeneticFuzzer to find vulnerabilities in the SymbolicPathExplorer.
        """
        self.logger.info("Starting self-attack on Symbolic Path Explorer...")

        # We use the framework's own fuzzer to attack one of its components.
        fuzzer = self.framework.genetic_fuzzer
        fuzzer.reset()

        # The `evolve` method will call `_target_symbolic_explorer` with many
        # different payloads, trying to find inputs that cause it to crash.
        evolved_attacks = fuzzer.evolve(self._target_symbolic_explorer, generations=5)

        vulns = []
        if evolved_attacks:
            # The fuzzer found inputs that crashed the symbolic explorer.
            # We'll report the most effective one as a meta-vulnerability.
            best_payload, best_fitness = evolved_attacks[0]
            vuln = Vulnerability(
                attack_vector=AttackVector.META_VULNERABILITY,
                severity=min(best_fitness / 100.0, 0.8),
                severity_level=SeverityLevel.HIGH,
                exploit_code=f"Symbolic explorer crashed with payload: {repr(best_payload)}",
                failure_trace=[f"Fitness score: {best_fitness:.1f}"],
                discovered_at=time.time(),
                patch_suggestions=["Add more robust input validation in SymbolicPathExplorer."]
            )
            vulns.append(vuln)
            self.logger.critical("Meta-vulnerability found in Symbolic Path Explorer!")
        else:
            self.logger.info("Symbolic Path Explorer appears robust after self-attack.")

        return vulns

    def run_full_self_attack(self) -> List[Vulnerability]:
        """Run all self-attack tests."""
        self.logger.info("Starting full self-attack mode.")

        all_vulns = []
        all_vulns.extend(self.attack_symbolic_explorer())
        self.meta_vulnerabilities = all_vulns

        self.logger.info(f"Self-attack complete. Found {len(all_vulns)} meta-vulnerabilities.")

        return all_vulns
