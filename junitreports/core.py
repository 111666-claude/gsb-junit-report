"""解析并合并 JUnit 报告。"""

import xml.etree.ElementTree as ET


class Counter:
    """记录比较次数。"""

    def __init__(self):
        self.scanned = 0


class Case:
    def __init__(self, classname, name, status, time, flaky=False):
        self.classname = classname
        self.name = name
        self.status = status
        self.time = time
        self.flaky = flaky


class Report:
    def __init__(self):
        self.cases = []
        self._index = {}


def _status(tc):
    for child in tc:
        if child.tag in ("failure", "error"):
            return "failed"
        if child.tag == "skipped":
            return "skipped"
    return "passed"


def parse(sources, counter):
    report = Report()
    merged = {}
    ever_failed = {}
    for src in sources:
        root = ET.fromstring(src)
        for suite in root.iter("testsuite"):
            for tc in suite.iter("testcase"):
                counter.scanned += 1
                key = (tc.get("classname", ""), tc.get("name", ""))
                if key in merged and merged[key].status == "failed":
                    ever_failed[key] = True
                else:
                    ever_failed.setdefault(key, False)
                case = Case(
                    key[0],
                    key[1],
                    _status(tc),
                    float(tc.get("time") or 0),
                )
                merged[key] = case
    for key, case in merged.items():
        case.flaky = ever_failed[key] and case.status == "passed"
        report.cases.append(case)
        report._index[key] = case
    return report


def lookup(report, classname, name, counter):
    counter.scanned += 1
    return report._index.get((classname, name))
