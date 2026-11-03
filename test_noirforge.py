import os
import tempfile
import unittest

from noirforge import db
from noirforge.generator import FALSE_CLUE, TRUE_CLUE, generate_case
from noirforge.render import render_case


class GeneratorTests(unittest.TestCase):
    def test_deterministic(self):
        self.assertEqual(generate_case(42), generate_case(42))

    def test_different_seeds_differ(self):
        self.assertNotEqual(generate_case(1), generate_case(2))

    def test_exactly_one_culprit(self):
        for seed in range(200):
            case = generate_case(seed, 3 + seed % 4)
            self.assertEqual(sum(s.is_culprit for s in case.suspects), 1)

    def test_clue_structure(self):
        for seed in range(200):
            case = generate_case(seed, 3 + seed % 4)
            names = {s.name for s in case.suspects}
            true = [c for c in case.clues if c.kind == TRUE_CLUE]
            false = [c for c in case.clues if c.kind == FALSE_CLUE]
            self.assertEqual(len(true), 3)
            self.assertTrue(all(c.points_to == case.culprit.name for c in true))
            self.assertTrue(all(c.points_to in names for c in false))
            self.assertTrue(all(c.points_to != case.culprit.name for c in false))
            self.assertTrue(all(c.explanation for c in false))

    def test_names_are_unique(self):
        case = generate_case(7, 6)
        names = [s.name for s in case.suspects] + [case.victim_name]
        self.assertEqual(len(names), len(set(names)))

    def test_no_unformatted_templates(self):
        for seed in range(200):
            text = render_case(generate_case(seed), reveal=True)
            self.assertNotIn("{", text)

    def test_invalid_suspect_count(self):
        for n in (0, 2, 7):
            with self.assertRaises(ValueError):
                generate_case(1, n)


class RenderTests(unittest.TestCase):
    def test_solution_hidden_by_default(self):
        case = generate_case(5)
        hidden = render_case(case)
        self.assertNotIn("## Solução", hidden)
        self.assertNotIn(case.twist, hidden)
        self.assertIn("## Solução", render_case(case, reveal=True))


class DatabaseTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.conn = db.connect(os.path.join(self.tmp.name, "t.db"))

    def tearDown(self):
        self.conn.close()
        self.tmp.cleanup()

    def test_roundtrip(self):
        case = generate_case(99, 5)
        case_id = db.save_case(self.conn, case)
        self.assertEqual(db.load_case(self.conn, case_id), case)

    def test_save_is_idempotent(self):
        case = generate_case(11)
        self.assertEqual(db.save_case(self.conn, case), db.save_case(self.conn, case))
        self.assertEqual(len(db.list_cases(self.conn)), 1)

    def test_delete_cascades(self):
        case_id = db.save_case(self.conn, generate_case(3))
        self.assertTrue(db.delete_case(self.conn, case_id))
        self.assertIsNone(db.load_case(self.conn, case_id))
        left = self.conn.execute("SELECT COUNT(*) FROM suspects").fetchone()[0]
        self.assertEqual(left, 0)

    def test_stats(self):
        for seed in range(1, 11):
            db.save_case(self.conn, generate_case(seed))
        s = db.stats(self.conn)
        self.assertEqual(s["total"], 10)
        self.assertTrue(s["weapons"])
        self.assertTrue(s["culprit_relations"])


if __name__ == "__main__":
    unittest.main()
