import random
import time
from typing import Callable, List, Dict, Any, Tuple, Optional

class GeneticFuzzer:
    """Genetic fuzzer with self-attack protection."""

    def __init__(self, population_size=30, mutation_rate=0.3):
        self.population_size = max(5, min(population_size, 100))  # Bounds check
        self.mutation_rate = max(0.0, min(mutation_rate, 1.0))  # Bounds check
        self.generation = 0
        self.best_attacks = []
        self.total_evaluations = 0
        self.max_evaluations = 10000  # Prevent infinite loops

    def initialize_population(self) -> List[Any]:
        """Create diverse initial population with safety checks."""
        seeds = [
            0, 1, -1, 2**31-1, -2**31, 2**20,  # Safer large numbers
            10**6, 10**9,
            0.0, 1.0, -1.0,
            "", " ", "test", "\x00", "admin",
            "' OR '1'='1", "; DROP TABLE",
            [], [1], {}, None, True, False
        ]

        population = seeds[:self.population_size]

        while len(population) < self.population_size:
            try:
                base = random.choice(seeds)
                mutated = self._mutate(base)
                population.append(mutated)
            except:
                population.append(None)  # Fallback

        return population

    def _mutate(self, payload: Any) -> Any:
        """SAFE mutation with overflow protection."""
        if random.random() > self.mutation_rate:
            return payload

        try:
            if isinstance(payload, int):
                # SAFE: Prevent overflow in mutation itself
                if abs(payload) > 10**10:
                    return payload  # Don't mutate already large values

                ops = [
                    lambda x: x * 2 if abs(x) < 10**8 else x,
                    lambda x: x + 1,
                    lambda x: -x,
                ]
                return random.choice(ops)(payload)

            elif isinstance(payload, str):
                # SAFE: Prevent memory exhaustion
                if len(payload) > 1000:
                    return payload  # Don't grow already large strings

                return random.choice([
                    payload * 2 if len(payload) < 50 else payload,
                    payload + "\x00",
                    payload.upper() if payload else "X",
                    ""
                ])

            elif isinstance(payload, list):
                # SAFE: Limit list growth
                if len(payload) > 100:
                    return payload
                return payload * min(2, 3)

        except Exception:
            return payload  # Safe fallback

        return payload

    def evaluate_fitness(self, payload: Any, target_func: Callable) -> float:
        """Evaluate fitness with timeout and safety."""
        if self.total_evaluations >= self.max_evaluations:
            return 0.0  # Stop if too many evaluations

        fitness = 0.0
        self.total_evaluations += 1

        try:
            # Timeout simulation (in real code, use signal.alarm or threading.Timer)
            start = time.time()
            result = target_func(payload)
            duration = time.time() - start

            if duration > 1.0:  # Took too long
                return 0.0

            # Timing
            if duration > 0.01:
                fitness += 20

            # Large results
            if isinstance(result, (int, float)):
                try:
                    if abs(result) > 10**12:
                        fitness += 70
                    elif abs(result) > 10**9:
                        fitness += 60
                    elif abs(result) > 10**6:
                        fitness += 40

                    result_str = str(result)
                    if 'inf' in result_str.lower():
                        fitness += 75
                    elif 'nan' in result_str.lower():
                        fitness += 70
                except:
                    fitness += 30  # Conversion failed - interesting

            # Large structures
            if isinstance(result, (list, str, dict)):
                try:
                    size = len(result)
                    if size > 10**6:
                        fitness += 85
                    elif size > 10**4:
                        fitness += 50
                except:
                    pass

        except MemoryError:
            fitness = 100
        except (RecursionError, OverflowError):
            fitness = 95
        except ZeroDivisionError:
            fitness = 60
        except TypeError:
            fitness = 55
        except ValueError:
            fitness = 50
        except Exception:
            fitness = 35

        return min(fitness, 100.0)

    def evolve(self, target_func: Callable, generations: int = 5) -> List[Tuple[Any, float]]:
        """Run genetic algorithm with safety limits."""
        generations = min(generations, 10)  # Limit generations
        population = self.initialize_population()

        for gen in range(generations):
            # Evaluate all
            fitness_scores = []
            for p in population:
                try:
                    f = self.evaluate_fitness(p, target_func)
                    fitness_scores.append((p, f))
                except:
                    fitness_scores.append((p, 0))

            if not fitness_scores:
                break

            fitness_scores.sort(key=lambda x: x[1], reverse=True)

            # Track best
            if fitness_scores[0][1] > 35:
                self.best_attacks.append(fitness_scores[0])

            # Selection with safety
            elite_count = max(2, min(self.population_size // 5, len(fitness_scores)))
            elites = [p for p, f in fitness_scores[:elite_count]]
            survivors = [p for p, f in fitness_scores[:max(1, len(fitness_scores) // 2)]]

            if not survivors:
                break

            # Next generation
            next_gen = elites.copy()
            attempts = 0
            while len(next_gen) < self.population_size and attempts < 100:
                try:
                    parent = random.choice(survivors)
                    child = self._mutate(parent)
                    next_gen.append(child)
                except:
                    next_gen.append(None)
                attempts += 1

            population = next_gen
            self.generation = gen + 1

        # Remove duplicates safely
        unique = []
        seen = set()
        for payload, fitness in self.best_attacks:
            try:
                key = str(type(payload).__name__) + str(payload)[:50]
                if key not in seen:
                    seen.add(key)
                    unique.append((payload, fitness))
            except:
                pass

        return sorted(unique, key=lambda x: x[1], reverse=True)
