"""固定场景，用来复现题面里的锚点。"""

import json

from . import core


def _line(obj):
    print(json.dumps(obj, ensure_ascii=False))


def suite(tests, body):
    return ('<testsuites><testsuite name="s" tests="%d">%s</testsuite></testsuites>'
            % (tests, body))


def run(name):
    if name == "retry":
        src = suite(1, '<testcase classname="a" name="t" time="1"><failure/></testcase>'
                       '<testcase classname="a" name="t" time="1"/>')
        report = core.parse([src], core.Counter())
        case = core.lookup(report, "a", "t", core.Counter())
        if case is None:
            _line({"status": "", "flaky": False})
            return 0
        _line({"status": case.status, "flaky": case.flaky})
        return 0
    if name == "skipped":
        src = suite(1, '<testcase classname="a" name="t" time="0"><skipped/></testcase>')
        report = core.parse([src], core.Counter())
        case = core.lookup(report, "a", "t", core.Counter())
        _line({"status": case.status if case else ""})
        return 0
    if name == "totals":
        src = suite(5, '<testcase classname="a" name="t1" time="0"/>'
                       '<testcase classname="a" name="t2" time="0"/>')
        report = core.parse([src], core.Counter())
        _line({"total": len(report.cases)})
        return 0
    if name == "work":
        body = "".join('<testcase classname="a" name="t%04d" time="0"/>' % i for i in range(800))
        report = core.parse([suite(800, body)], core.Counter())
        counter = core.Counter()
        for i in range(800):
            core.lookup(report, "a", "t%04d" % i, counter)
        _line({"cases": 800, "scanned": counter.scanned})
        return 0
    raise SystemExit("未知场景：" + name)
