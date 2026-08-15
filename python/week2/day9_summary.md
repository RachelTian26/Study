# Day 9 学习总结

## 学习目标与真正学会的内容

| 学习目标 | 真正学会的内容（含例子） |
| --- | --- |
| 复习 `def` 函数的定义和调用。 | `def get_score(subject):` 之后在函数里写逻辑，再用 `return` 把结果返回出来。 |
| 继续巩固 `if` / `elif` / `else` 判断。 | `grade(avg)` 里根据分数区间返回 `A/B/C/D/F`。 |
| 练习循环和累计变量。 | `for student in students:` 用来遍历学生列表，`total += s` 用来累计总分。 |
| 学会写函数时要注意返回值。 | 如果函数里只写 `print(...)`，外面拿到的值还是 `None`，不会有输出。 |
| 学会检查输入是否合法。 | `get_score()` 里用 `float()` 转换，并检查是否在 `0-100` 之间。 |
| 认识字符串和数字转换的关键点。 | `input()` 读出来是字符串，计算前要先转成 `int()` 或 `float()`。 |
| 学会用 `len()` 统计长度。 | `len(scores)` 可以看列表里有多少个元素，`len(text)` 可以看字符串有多少个字符。 |
| 理解列表处理和去重。 | 用 `if num not in result:` 把重复值过滤掉，保留第一次出现的顺序。 |
| 理解统计词频的思路。 | 先 `split()`，再用字典 `counts[word] = counts.get(word, 0) + 1` 统计次数。 |
| 练习 f-string 对齐输出。 | `f"{name:<8} {score:>5.1f}"` 可以让输出对齐更整齐。 |

## 练习里你能直接回顾的点

| 复习点 |
| --- |
| 写 `get_score(subject)`：输入分数，处理非法输入，返回合法分数。 |
| 写 `grade(avg)`：根据分数区间返回等级。 |
| 写 `print_summary(students)`：统计总人数、各科平均分和最高分学生。 |
| 统计词频：先分词，再用字典累计每个词出现次数。 |
| 去重：保留第一次出现的元素，重复的跳过。 |
| `len()` 的用途：统计列表长度、字符串长度，计算平均时常用 `len(scores)`。 |
| 列表推导式：`[num ** 2 for num in range(1, 21) if num % 2 == 0]`。 |
| 字符串拼接：`"、".join(names)`。 |
| 处理空列表：避免 `len(scores) == 0` 时除以 0。 |

## 学习体会

- 今天这一天不学新语法，主要是把前几天的内容再捡起来做一遍，感觉像“把知识重新装回脑子里”。 |
- 函数是最重要的部分：写函数时一定要先想清楚它要做什么，最后要不要 `return`。 |
- 只写 `print()` 常常不够，因为外面拿到的还是没有返回值。 |
- `if` 和 `for` 组合起来，用于统计、筛选和判断，是最常见的写法。 |
- `len()` 也是非常重要的基础函数：知道列表或字符串有多少个元素，很多统计题都离不开它。 |
- 输入来自用户时，往往是字符串，计算前一定要转成数字，不然就会出错。 |
- 代码写得越规范，越容易看懂和调试。比如避免用 `sum` 这种内置函数名作为变量名。 |

## 今天实践的代码

### 1. 输入分数并检查合法性
```python
def get_score(subject):
    while True:
        score_str = input(f"请输入{subject}成绩（0-100）：")
        try:
            score = float(score_str)
            if 0 <= score <= 100:
                return score
            else:
                print("分数必须在 0 到 100 之间，请重新输入。")
        except ValueError:
            print("输入无效，请输入一个数字。")
```

### 2. 根据平均分返回等级
```python
def grade(avg):
    if avg >= 90:
        return "A"
    elif avg >= 80:
        return "B"
    elif avg >= 70:
        return "C"
    elif avg >= 60:
        return "D"
    else:
        return "F"
```

### 3. 统计全班结果
```python
def print_summary(students):
    if not students:
        print("没有学生数据")
        return

    total_students = len(students)
    chinese_total = 0
    math_total = 0
    english_total = 0
    max_score = 0
    max_student = ""

    for student in students:
        chinese_total += student["chinese"]
        math_total += student["math"]
        english_total += student["english"]

        total = student["chinese"] + student["math"] + student["english"]
        if total > max_score:
            max_score = total
            max_student = student["name"]

    print("总人数:", total_students)
    print("语文平均分:", chinese_total / total_students)
    print("数学平均分:", math_total / total_students)
    print("英语平均分:", english_total / total_students)
    print("最高分学生:", max_student, max_score)
```

### 4. 统计单词出现次数
```python
text = "the quick brown fox jumps over the lazy dog the end"
words = text.split()
counts = {}
for word in words:
    counts[word] = counts.get(word, 0) + 1
print(counts)
```

### 5. 去重并保持第一次出现顺序
```python
numbers = [3, 7, 3, 1, 7, 9]
result = []
for num in numbers:
    if num not in result:
        result.append(num)
print(result)
```

### 6. 列表推导式做偶数平方
```python
squares = [num ** 2 for num in range(1, 21) if num % 2 == 0]
print(squares)
```

## 这次复习最重要的提醒

- 定义函数时，函数体要有缩进。 |
- `return` 很关键：函数不返回值，外面就拿不到结果。 |
- 只写 `print()`，常常只是“显示”，不是“传值”。 |
- `len()` 常用于统计长度，比如 `len(scores)`、`len(text)`。 |
- 读入的数据基本都是字符串，记得转换成 `int` 或 `float`。 |
- `for` 循环和 `if` 条件是最常用的组合，今天很多题都用了它。 |
