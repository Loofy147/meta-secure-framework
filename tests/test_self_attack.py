import unittest
from unittest.mock import MagicMock
from sacef.framework import SelfAdversarialFramework
from sacef.self_attack import SelfAttackModule

class TestSelfAttackModule(unittest.TestCase):

    def test_self_attack_finds_mocked_vulnerability(self):
        # Create a mock framework instance
        framework = SelfAdversarialFramework()

        # Mock the symbolic explorer to raise an exception for a specific payload
        def mock_explore_path(func, payload_list):
            if payload_list and payload_list[0] == "crash":
                raise ValueError("Symbolic explorer crash")

        framework.symbolic_explorer.explore_path = MagicMock(side_effect=mock_explore_path)

        # Mock the genetic fuzzer to return the "crash" payload
        framework.genetic_fuzzer.evolve = MagicMock(return_value=[("crash", 95.0)])

        # Initialize the self-attack module with the mocked framework
        self_attacker = SelfAttackModule(framework)

        # Run the self-attack
        meta_vulnerabilities = self_attacker.attack_symbolic_explorer()

        # Verify that the vulnerability was found
        self.assertEqual(len(meta_vulnerabilities), 1)
        self.assertEqual(meta_vulnerabilities[0].attack_vector.name, "META_VULNERABILITY")
        self.assertIn("Symbolic explorer crashed with payload: 'crash'", meta_vulnerabilities[0].exploit_code)

if __name__ == '__main__':
    unittest.main()
