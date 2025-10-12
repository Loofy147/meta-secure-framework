from typing import Callable

class TestRunner:
    """Runs comprehensive tests on the framework itself."""

    def __init__(self):
        self.tests_passed = 0
        self.tests_failed = 0
        self.results = []

    def run_test(self, test_name: str, test_func: Callable) -> bool:
        """Run a single test and record results."""
        print(f"\n[TEST] {test_name}")
        try:
            result = test_func()
            if result:
                print(f"  ✅ PASSED")
                self.tests_passed += 1
            else:
                print(f"  ❌ FAILED")
                self.tests_failed += 1
            self.results.append({'name': test_name, 'passed': result})
            return result
        except Exception as e:
            print(f"  ❌ EXCEPTION: {e}")
            self.tests_failed += 1
            self.results.append({'name': test_name, 'passed': False, 'error': str(e)})
            return False

    def report(self):
        """Print test summary."""
        total = self.tests_passed + self.tests_failed
        print(f"\n{'='*70}")
        print(f"TEST SUMMARY: {self.tests_passed}/{total} passed")
        print(f"{'='*70}")
