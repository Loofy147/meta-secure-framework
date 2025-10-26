import unittest
from sacef.modules.probabilistic_fuzzer import ProbabilisticFuzzer
from sacef.core.context import TargetFunctionContext

class TestProbabilisticFuzzer(unittest.TestCase):

    def test_fuzzer_identifies_failures(self):
        fuzzer = ProbabilisticFuzzer(fuzz_iterations=200)

        def faulty_function(x):
            if isinstance(x, int) and x > 1000:
                raise ValueError("Value too large")
            if isinstance(x, str) and "bad" in x:
                raise TypeError("Bad string")

        type_distribution = {int: 0.5, str: 0.5}
        results = fuzzer.fuzz(faulty_function, type_distribution)

        self.assertIn('int', results)
        self.assertIn('str', results)
        self.assertGreater(results['int']['failure'], 0)
        self.assertGreater(results['str']['failure'], 0)
        self.assertGreater(results['int']['success'], 0)
        self.assertGreater(results['str']['success'], 0)

    def test_fuzzer_respects_context(self):
        fuzzer = ProbabilisticFuzzer(fuzz_iterations=100)

        def function_with_expected_exceptions(x):
            if isinstance(x, int):
                raise ValueError("Expected integer failure")

        context = TargetFunctionContext(expected_exceptions=[ValueError])
        type_distribution = {int: 1.0}
        results = fuzzer.fuzz(function_with_expected_exceptions, type_distribution, context)

        self.assertIn('int', results)
        self.assertEqual(results['int']['failure'], 0)
        self.assertGreater(results['int']['success'], 0)

if __name__ == '__main__':
    unittest.main()
