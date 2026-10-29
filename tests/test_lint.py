import unittest

from model_tier_lint.lint import lint


class TestLint(unittest.TestCase):
    def test_valid(self):
        self.assertEqual(lint([{"model_id": "a", "tier": "T1"}]), [])

    def test_missing_model_id(self):
        self.assertTrue(any("model_id" in e for e in lint([{"tier": "T1"}])))

    def test_missing_tier(self):
        self.assertTrue(any("tier" in e for e in lint([{"model_id": "a"}])))

    def test_unknown_tier(self):
        self.assertTrue(any("unknown tier" in e for e in lint([{"model_id": "a", "tier": "T9"}])))

    def test_duplicate_model_id(self):
        errs = lint([{"model_id": "a", "tier": "T1"}, {"model_id": "a", "tier": "T2"}])
        self.assertTrue(any("duplicate" in e for e in errs))

    def test_custom_tiers(self):
        self.assertEqual(lint([{"model_id": "a", "tier": "legal-class"}], known_tiers={"legal-class"}), [])


if __name__ == "__main__":
    unittest.main()
