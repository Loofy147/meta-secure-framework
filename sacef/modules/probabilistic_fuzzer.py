import random
from typing import Callable, List, Dict, Any, Optional
from sacef.core.context import TargetFunctionContext

class ProbabilisticFuzzer:
    """Probabilistic fuzzing based on type distributions."""

    def __init__(self, fuzz_iterations: int = 100):
        self.fuzz_iterations = max(10, min(fuzz_iterations, 5000))

    def _generate_input(self, selected_type: type) -> Any:
        """Generates a random input based on the selected type."""
        if selected_type == int:
            return random.choice([
                random.randint(-100, 100),
                random.randint(1001, 2000),
                random.randint(-2**31, 2**31 - 1),
                0, 1, -1, 2**31-1, -2**31
            ])
        elif selected_type == str:
            base_strings = ["", "test", "bad", "' OR '1'='1", "<script>alert(1)</script>"]
            chosen_base = random.choice(base_strings)
            mutation = random.choice(['', ''.join(random.choice('abcdefghijklmnopqrstuvwxyz\x00\xff') for _ in range(random.randint(1,10)))])
            return chosen_base + mutation
        elif selected_type == type(None):
            return None
        elif selected_type == bool:
            return random.choice([True, False])
        elif selected_type == float:
            return random.uniform(-1e6, 1e6)
        return None

    def fuzz(self, target_func: Callable, type_distribution: Dict[type, float], context: Optional[TargetFunctionContext] = None) -> Dict:
        """
        Fuzzes the target function with probabilistically generated inputs.
        """
        results = {}
        types_to_fuzz = list(type_distribution.keys())
        weights = list(type_distribution.values())

        for _ in range(self.fuzz_iterations):
            selected_type = random.choices(types_to_fuzz, weights, k=1)[0]
            inp = self._generate_input(selected_type)

            type_name = selected_type.__name__
            if type_name not in results:
                results[type_name] = {'success': 0, 'failure': 0}

            try:
                target_func(inp)
                results[type_name]['success'] += 1
            except Exception as e:
                if context and any(isinstance(e, exp_type) for exp_type in context.expected_exceptions):
                    results[type_name]['success'] += 1  # Expected exception is a form of success
                else:
                    results[type_name]['failure'] += 1

        return results
