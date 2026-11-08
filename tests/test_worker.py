"""Unit tests for episodic-consolidation-worker."""
import unittest
from episodic_consolidation_worker.worker import EpisodicConsolidationWorker


class TestEpisodicConsolidationWorker(unittest.TestCase):
    def test_consolidation_rule_creation(self):
        worker = EpisodicConsolidationWorker(min_support=2, min_confidence=0.7)
        worker.record_experience("SyntaxError", "fix_missing_colon", True)
        worker.record_experience("SyntaxError", "fix_missing_colon", True)
        schemas = worker.consolidate()
        self.assertEqual(len(schemas), 1)
        self.assertEqual(schemas[0].recommended_action, "fix_missing_colon")

    def test_unsupported_experience_ignored(self):
        worker = EpisodicConsolidationWorker(min_support=3)
        worker.record_experience("TypeError", "cast_str", True)
        worker.record_experience("TypeError", "cast_str", True)
        schemas = worker.consolidate()
        self.assertEqual(len(schemas), 0)
