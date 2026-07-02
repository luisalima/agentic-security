"""Tests for the illustrative benchmark."""

from benchmark.run import run_benchmark


def test_memory_benchmark_corpus_exercises_memory_poisoning():
    results = run_benchmark()
    memory = next(item for item in results["summary"] if item["defense"] == "Memory")

    assert memory["detected"] > 0
    assert any(row["corpus"] == "memory poisoning" for row in results["attacks"])
