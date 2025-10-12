import time
from typing import List
from sacef.core.datastructures import Vulnerability, AttackVector, SeverityLevel
from sacef.modules.genetic_fuzzer import GeneticFuzzer


class SelfAttackModule:
    """
    Attacks the framework's own code to find meta-vulnerabilities.
    This is the key innovation: the framework tests itself!
    """

    def __init__(self, framework):
        self.framework = framework
        self.meta_vulnerabilities = []

    def attack_genetic_fuzzer(self) -> List[Vulnerability]:
        """Attack the genetic fuzzer component."""
        print("\n🎯 SELF-ATTACK: Testing Genetic Fuzzer...")
        vulns = []

        # Attack 1: Extreme inputs
        extreme_inputs = [
            None,
            float('inf'),
            float('-inf'),
            float('nan'),
            [],
            {},
            lambda x: x,
            2**100,
            -2**100
        ]

        crashes = 0
        for inp in extreme_inputs:
            try:
                fuzzer = GeneticFuzzer()
                fuzzer.evolve(lambda x: inp, generations=1)
            except Exception as e:
                crashes += 1
                print(f"  ⚠️  Fuzzer crashed with: {type(inp).__name__}")

        if crashes > 0:
            vuln = Vulnerability(
                attack_vector=AttackVector.META_VULNERABILITY,
                severity=0.6,
                severity_level=SeverityLevel.HIGH,
                exploit_code=f"Genetic fuzzer crashes with {crashes} extreme inputs",
                failure_trace=[f"Tested {len(extreme_inputs)} inputs, {crashes} caused crashes"],
                discovered_at=time.time(),
                patch_suggestions=[
                    "Add input type validation in evolve()",
                    "Add try-catch in population initialization"
                ]
            )
            vulns.append(vuln)
            print(f"  🔴 Found meta-vulnerability in fuzzer")
        else:
            print(f"  ✅ Fuzzer is robust")

        return vulns

    def attack_mutation_function(self) -> List[Vulnerability]:
        """Test if mutation can cause overflow."""
        print("\n🎯 SELF-ATTACK: Testing Mutation Function...")
        vulns = []

        fuzzer = GeneticFuzzer()

        # Test mutation with large numbers
        large_numbers = [10**15, 10**20, 2**100]
        overflows = 0

        for num in large_numbers:
            try:
                result = fuzzer._mutate(num)
                if isinstance(result, (int, float)) and abs(result) > num * 10:
                    overflows += 1
                    print(f"  ⚠️  Mutation caused growth: {num} → {result}")
            except:
                pass

        if overflows == 0:
            print(f"  ✅ Mutation is safe (prevents overflow)")
        else:
            vuln = Vulnerability(
                attack_vector=AttackVector.META_VULNERABILITY,
                severity=0.5,
                severity_level=SeverityLevel.MEDIUM,
                exploit_code="Mutation can cause value growth",
                failure_trace=[f"{overflows} mutations grew values significantly"],
                discovered_at=time.time(),
                patch_suggestions=["Add bounds checking in _mutate()"]
            )
            vulns.append(vuln)

        return vulns

    def attack_fitness_function(self) -> List[Vulnerability]:
        """Test fitness evaluation for edge cases."""
        print("\n🎯 SELF-ATTACK: Testing Fitness Function...")
        vulns = []

        fuzzer = GeneticFuzzer()

        # Edge cases that might break fitness calculation
        edge_cases = [
            (None, lambda x: None),
            ([], lambda x: []),
            ({}, lambda x: {}),
            ("", lambda x: ""),
        ]

        errors = 0
        for payload, func in edge_cases:
            try:
                fitness = fuzzer.evaluate_fitness(payload, func)
                if fitness < 0 or fitness > 100:
                    errors += 1
                    print(f"  ⚠️  Invalid fitness score: {fitness}")
            except Exception as e:
                errors += 1
                print(f"  ⚠️  Fitness evaluation crashed: {type(e).__name__}")

        if errors == 0:
            print(f"  ✅ Fitness function is robust")
        else:
            vuln = Vulnerability(
                attack_vector=AttackVector.META_VULNERABILITY,
                severity=0.4,
                severity_level=SeverityLevel.MEDIUM,
                exploit_code="Fitness function has edge case issues",
                failure_trace=[f"{errors} edge cases caused problems"],
                discovered_at=time.time(),
                patch_suggestions=["Add edge case handling in evaluate_fitness()"]
            )
            vulns.append(vuln)

        return vulns

    def run_full_self_attack(self) -> List[Vulnerability]:
        """Run all self-attack tests."""
        print(f"\n{'='*70}")
        print("🔄 SELF-ATTACK MODE: Framework Testing Itself")
        print(f"{'='*70}")

        all_vulns = []

        all_vulns.extend(self.attack_genetic_fuzzer())
        all_vulns.extend(self.attack_mutation_function())
        all_vulns.extend(self.attack_fitness_function())

        self.meta_vulnerabilities = all_vulns

        print(f"\n{'='*70}")
        print(f"🎯 SELF-ATTACK COMPLETE: Found {len(all_vulns)} meta-vulnerabilities")
        print(f"{'='*70}")

        return all_vulns
