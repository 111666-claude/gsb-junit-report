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
        self._had_failure = False


class Report:
    def __init__(self):
        self.cases = []
        self.declared = 0
        self._index = {}


def _status_of(tc):
    status = "passed"
    for child in tc:
        if child.tag in ("failure", "error"):
            return "failed"
        if child.tag == "skipped":
            status = "skipped"
    return status


def parse(sources, counter):
    report = Report()
    for src in sources:
        root = ET.fromstring(src)
        for suite in root.iter("testsuite"):
            report.declared += int(suite.get("tests") or 0)
            for tc in suite.iter("testcase"):
                counter.scanned += 1
                status = _status_of(tc)
                classname = tc.get("classname", "")
                name = tc.get("name", "")
                time = float(tc.get("time") or 0)
                key = (classname, name)
                case = report._index.get(key)
                if case is None:
                    case = Case(classname, name, status, time)
                    report._index[key] = case
                    report.cases.append(case)
                else:
                    case._had_failure = case._had_failure or case.status == "failed"
                    case.status = status
                    case.time = time
                    case.flaky = status == "passed" and case._had_failure
    return report


def lookup(report, classname, name, counter):
    counter.scanned += 1
    return report._index.get((classname, name))
