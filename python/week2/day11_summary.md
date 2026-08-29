# Day 11 学习总结

## 为什么学这个很重要

| 重要点 | 说明 |
| --- | --- |
| 程序经常出错 | 用户输入错误、文件不存在、格式不合法，这些都是真实生活里常见的问题。 |
| `try/except` 能保命 | 不学它，程序一遇到错误就直接崩掉，用户体验会很差。 |
| 让程序更稳 | `try/except` 的核心作用，是让程序在出错时“继续运行”，而不是直接停止。 |
| 适合处理真实数据 | 处理 CSV、文件、用户输入时，异常处理非常关键。 |
| 是可靠程序的基础 | 学会异常处理后，代码不只是“能跑”，而是“能面对真实数据也稳定”。 |
| 项目里会经常用到 | 以后做通讯录、日历、成绩处理、文件读取等，都会遇到这些问题。 |
| 从“会写功能”升级到“会写程序” | 这一步真正体现了“程序不只是能计算，还能应对异常”。 |

## 学习目标与真正学会的内容

| 学习目标 | 真正学会的内容（含例子） |
| --- | --- |
| 会写基本的 `try/except`。 | `try: int("abc") except ValueError as e: print(e)`，遇到异常时，不让程序直接崩掉。 |
| 会区分常见错误类型。 | `ValueError`：值不对；`TypeError`：类型不对；`KeyError`：字典没有这个键；`IndexError`：列表越界；`FileNotFoundError`：文件不存在。 |
| 会接住多种异常。 | `except (ValueError, TypeError) as e:` 能同时处理几种常见问题，代码更简洁。 |
| 会写 `else` 和 `finally`。 | `try` 里放可能出错的代码，`else` 里放没出错时要执行的内容，`finally` 里放收尾工作。 |
| 会理解“异常处理不是让错误消失”。 | 程序报错不是为了“掩盖”，而是为了“提前预料并体面处理”。 |
| 会写 `raise` 主动抛错。 | `raise ValueError("分数必须在 0-100 之间")`，把问题尽早暴露出来，方便排错。 |
| 会用自定义异常。 | `class ScoreError(Exception): pass`，更容易区分“这是我自己的业务规则错误”。 |
| 会用 `try/except` 做真实输入校验。 | `float(raw)` 能接受小数，`strip()` 能去掉空格，`0 <= value <= 100` 保证范围合法。 |
| 会把 `try/except` 用在文件读取和脏数据处理里。 | 读取文件时捕获 `FileNotFoundError`；处理 CSV 时跳过坏数据，保留有效数据。 |
| 会体会 Python 的 EAFP 风格。 | 先做事，出错再处理，通常比一大堆 `if` 判断更自然、更简洁。 |

## 练习里你能直接回顾的点

| 复习点 |
| --- |
| `safe_int(text, default=0)`：把字符串转整数，失败时返回默认值。 |
| `get_score(subject)`：把输入分数的校验逻辑由 `.isdigit()` 升级成 `try/except`。 |
| `read_file_safe(path)`：文件存在就读，不存在就打印提示并返回空字符串。 |
| 处理“脏”用户数据：缺 key 用 `.get()`，类型错误用 `try/except`。 |
| 解析 `scores.csv`：遇到空行、缺字段、非数字时跳过并说明原因。 |
| `parse_event(line)`：用 `raise` 主动抛错，明确告诉“哪里错了”。 |
| `except Exception as e`：拿到的是异常对象，`type(e).__name__` 能显示错误类型。 |
| `finally`：无论有没有错误，都执行收尾动作。 |

## 学习体会

- 今天最大的收获不是“记住几个错误名”，而是知道了“异常处理本质上是为了让程序更稳”。 |
- `try/except` 不是让程序忽略问题，而是让程序在知道问题之后继续往下走，或者给出更好的提示。 |
- 只要是“可能会出错、但值得继续尝试”的地方，就适合用 `try/except`。 |
- 不要写裸 `except:`，因为它会把很多本来应该立即发现的错误都吞掉，调试会很痛苦。 |
- `raise` 很重要：当输入明显不合理时，最好尽早报错，而不是偷偷返回 `None`。 |
- 读文件和处理 CSV 时，最常见的坑是“数据不完整”“非数字”“空行”，这些都应该被处理，而不是直接崩掉。 |
- 这一天真正学会的是：程序不只是“写出结果”，还要“能面对真实世界的数据”。 |
- `else` 和 `finally` 很有用，因为它们把“正常流程”和“收尾动作”分开了，代码会更清晰。 |

## 今天实践的代码

### 1. 最基础的 `try/except`
```python
try:
    n = int("abc")
except ValueError as e:
    print("转换失败，接住了", e)

print("程序还活着")
```

### 2. 一次接多种异常
```python
def safe_div(a, b):
    try:
        return a / b
    except ZeroDivisionError:
        print("不能除以 0")
        return None
    except TypeError:
        print("参数得是数字")
        return None
```

### 3. `safe_int()`：把字符串安全转换成整数
```python
def safe_int(text, default=0):
    try:
        return int(str(text).strip())
    except (TypeError, ValueError):
        return default
```

### 4. `get_score()`：数字输入校验
```python
def get_score(subject):
    while True:
        try:
            value = float(subject.strip())
            if 0 <= value <= 100:
                return value
            else:
                print("分数必须在 0 到 100 之间，原因：不在合法范围内")
                return None
        except ValueError:
            print("输入不是数字，原因：不能转成 float")
            return None
```

### 5. `read_file_safe()`：文件不在时也不崩
```python
def read_file_safe(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        print(f"文件不存在：{path}")
        return ""
```

### 6. 处理“脏数据”用户列表
```python
bad_count = 0
for user in users:
    name = user.get("name", "未知")
    age_str = user.get("age")

    try:
        age = int(age_str)
    except (TypeError, ValueError):
        age = 0
        bad_count += 1

    if name == "未知" or age == 0:
        bad_count += 1

    print(f"{name} - {age}")
```

### 7. `raise` 和自定义异常
```python
class ScoreError(Exception):
    pass


def check_score(score):
    if not 0 <= score <= 100:
        raise ScoreError(f"分数 {score} 不在 0-100")
    return score
```

### 8. `parse_event()`：主动抛错
```python
def parse_event(line):
    parts = line.split("|")
    if len(parts) != 4:
        raise ValueError("字段数不对，需要 4 段")

    date, title, start_time, duration_text = parts
    date_parts = date.split("-")
    if len(date_parts) != 3:
        raise ValueError("日期格式应为 YYYY-MM-DD")

    try:
        duration = int(duration_text)
    except ValueError:
        raise ValueError("duration 必须是数字")

    return {
        "date": date,
        "title": title,
        "startTime": start_time,
        "duration": duration,
    }
```

## 这一天最重要的提醒

- `try/except` 的重点是“抓住正确的异常”，不要写成什么都接。 |
- `ValueError` 和 `TypeError` 很容易混淆：一个是“值不对”，一个是“类型不对”。 |
- 真正能让程序变稳的，不是“写一个大大的 `try`”，而是“把危险代码放进最小范围”。 |
- `raise` 和 `return None` 的区别：前者明确告诉调用者“这里出问题了”，后者容易让错误被静悄悄吞掉。 |
- 今天的代码中最常见的两个能力是：处理输入、处理脏数据。 |
- 学会异常处理之后，你以后写程序时，遇到用户输入和文件数据，就不会那么容易崩掉了。 |
