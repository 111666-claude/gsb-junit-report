# junit-report

把多份 JUnit XML 报告合并成一份汇总：按用例去重、按重试定结果、识别抖动，并按名字建索引。只用 Python 标准库。

```
python3 -m unittest discover -s tests
python3 -m junitreports --sample=retry
python3 -m junitreports --sample=skipped
python3 -m junitreports --sample=totals
python3 -m junitreports --sample=work
```

## 口径

- **状态**：用例没有子元素是 passed；子元素是 `failure` 或 `error` 是 failed；是 `skipped` 是 skipped。
- **重试**：同一个（classname, name）出现多次时，以最后一次的结果为准，只算一个用例。
- **抖动**：最后一次通过、但之前有过失败，算 flaky。
- **总数**：总用例数等于去重后的用例数，不看套件声明的 tests 属性。
- **查找**：按（classname, name）走索引，不逐条比较。

## 不变量

- 同一个（classname, name）在结果里只有一条用例。
- flaky 用例的最后一次结果一定是 passed。
- `scanned` 不随用例数乘查询次数放大：八百个用例查八百次的 `scanned` 不超过 6000。

## 输出契约

场景打印一行 JSON，键随场景而定。`--sample=work` 打印 `{"cases": N, "scanned": N}`。
