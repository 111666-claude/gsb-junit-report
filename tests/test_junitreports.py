import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from junitreports import core

ONE = ('<testsuites><testsuite name="s" tests="1">'
       '<testcase classname="a" name="t" time="0.5"/></testsuite></testsuites>')


class JunitReportTest(unittest.TestCase):
    def test_single_case(self):
        report = core.parse([ONE], core.Counter())
        self.assertEqual(len(report.cases), 1)

    def test_case_fields(self):
        case = core.parse([ONE], core.Counter()).cases[0]
        self.assertEqual((case.classname, case.name), ("a", "t"))

    def test_passed_status(self):
        self.assertEqual(core.parse([ONE], core.Counter()).cases[0].status, "passed")

    def test_lookup_finds(self):
        report = core.parse([ONE], core.Counter())
        self.assertIsNotNone(core.lookup(report, "a", "t", core.Counter()))

    def test_lookup_missing(self):
        report = core.parse([ONE], core.Counter())
        self.assertIsNone(core.lookup(report, "z", "z", core.Counter()))

    def test_counter_counts(self):
        counter = core.Counter()
        core.parse([ONE], counter)
        self.assertGreater(counter.scanned, 0)


if __name__ == "__main__":
    unittest.main()
