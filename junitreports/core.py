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
        self.declared = 0


def parse(sources, counter):
    report = Report()
    for src in sources:
        root = ET.fromstring(src)
        for suite in root.iter("testsuite"):
            report.declared += int(suite.get("tests") or 0)
            for tc in suite.iter("testcase"):
                counter.scanned += 1
                status = "passed"
                for child in tc:
                    if child.tag in ("failure", "error"):
                        status = "failed"
                case = Case(
                    tc.get("classname", ""),
                    tc.get("name", ""),
                    status,
                    float(tc.get("time") or 0),
                )
                report.cases.append(case)
    return report


def lookup(report, classname, name, counter):
    for case in report.cases:
        counter.scanned += 1
        if case.classname == classname and case.name == name:
            return case
    return None
