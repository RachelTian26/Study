# Day 10 学习总结

## 学习目标与真正学会的内容

| 学习目标 | 真正学会的内容（含例子） |
| --- | --- |
| 学会解决文件路径问题。 | `HERE = Path(__file__).parent`，`DATA = HERE / "data"`，这样不管从哪个目录运行，程序都能找到文件。 |
| 学会用 `with open()` 读文件。 | `with open(path, "r", encoding="utf-8") as f:` 先打开文件，再读内容，读完后自动关闭。 |
| 认识三种常用读法。 | `f.read()` 读整个文件；`f.readlines()` 得到列表，每行一个元素；`for line in f:` 一行一行遍历，最常用。 |
| 学会判断和处理空行。 | `if not line.strip(): continue` 可以跳过空白行，避免输出多余空行。 |
| 学会写文件和追加文件。 | `"w"` 会覆盖原文件；`"a"` 会在末尾继续写，适合日志和记录。 |
| 理解常见打开模式。 | `"r"` 只读，`"w"` 写入并覆盖，`"a"` 追加，`"x"` 只新建，不覆盖。 |
| 会处理“脏数据” CSV。 | 读取 `scores.csv` 后，把缺列、空格、非数字数据筛掉，只处理完整且合法的数据。 |
| 会写一个统计单词频率的函数。 | `word_count(path, top_n=5)` 先拆词，再用字典计数，最后按次数排序。 |
| 体会“程序有记忆”的意思。 | 用 `run_log.txt` 记录每次运行次数，程序重启后还能继续往后记，不会从 1 又开始。 |

## 练习里你能直接回顾的点

| 复习点 |
| --- |
| 用 `Path(__file__).parent` 解决 `FileNotFoundError`。 |
| 用 `with open()` 读 `notes.txt`，并加上行号输出。 |
| 用 `line.strip()` 去掉换行符和前后空白。 |
| 用 `enumerate(f, start=1)` 给每行编号。 |
| 用 `with open(..., "w")` 把编号结果写到 `numbered.txt`。 |
| 用 `if not line.strip(): continue` 跳过空行。 |
| 用 `.split()` 和字典统计单词出现次数。 |
| 用 `.isdigit()` 检查分数是否是数字。 |
| 用 `"a"` 模式追加写日志。 |
| 读 CSV 并做合法性检查，能跳过坏数据。 |

## 学习体会

- 今天的重点不是“学一个新函数”，而是学会“把程序和硬盘连接起来”。 |
- 以前程序里的数据都在内存里，一关就没了；文件让数据能保留下来。 |
- `with open()` 很重要，因为它会自动关闭文件，避免忘记 `close()`。 |
- `w` 和 `a` 的区别非常关键：`w` 会覆盖，`a` 会追加，写错模式可能丢数据。 |
- 读 CSV 时，经常会遇到脏数据，程序必须一条条检查，不能盲目假设每行都正确。 |
- 统计词频时，`split()` 和字典是最经典的组合，很多文本处理问题都会用到。 |
- 代码写得规范一点，路径和编码都写清楚，后面就不会因为中文乱码或找不到文件而卡住。 |

## 今天实践的代码

### 1. 读取文件并计算行数、单词数、字符数
```python
with open(path, "r", encoding="utf-8") as f:
    content = f.read()

lines = content.splitlines()
words = content.split()
chars_no_space = "".join(content.split())

print(len(lines))
print(len(words))
print(len(chars_no_space))
```

### 2. 给每行编号并跳过空行
```python
with open(notes_path, "r", encoding="utf-8") as f:
    for line_no, line in enumerate(f, start=1):
        if not line.strip():
            continue
        print(f"{line_no:>2} | {line.strip()}")
```

### 3. 把编号结果写到一个新文件
```python
numbered_path = DATA / "numbered.txt"

lines_to_write = []
with open(notes_path, "r", encoding="utf-8") as f:
    for line_no, line in enumerate(f, start=1):
        if not line.strip():
            continue
        lines_to_write.append(f"{line_no:>2} | {line.strip()}\n")

with open(numbered_path, "w", encoding="utf-8") as f:
    f.writelines(lines_to_write)
```

### 4. 过滤坏数据，只处理合法分数
```python
with open(csv_path, "r", encoding="utf-8") as f:
    lines = f.readlines()

valid_students = []
for line_no, line in enumerate(lines[1:], start=2):
    line = line.strip()
    if not line:
        continue

    parts = [p.strip() for p in line.split(",")]
    if len(parts) != 4:
        print(f"第 {line_no} 行数据有问题，已跳过")
        continue

    name, chinese, math, english = parts
    if not chinese.isdigit() or not math.isdigit() or not english.isdigit():
        print(f"第 {line_no} 行数据有问题，已跳过")
        continue

    valid_students.append({
        "name": name,
        "chinese": int(chinese),
        "math": int(math),
        "english": int(english),
    })
```

### 5. 追加写日志，记录每次运行次数
```python
run_log_path = HERE / "run_log.txt"

if run_log_path.exists():
    with open(run_log_path, "r", encoding="utf-8") as f:
        count = len(f.readlines())
else:
    count = 0

count += 1

with open(run_log_path, "a", encoding="utf-8") as f:
    f.write(f"第 {count} 次运行\n")
```

### 6. 统计文章中出现次数最多的单词
```python
def word_count(path, top_n=5):
    with open(path, "r", encoding="utf-8") as f:
        content = f.read().lower()

    words = content.split()
    counts = {}

    for word in words:
        cleaned = word.strip(".,!?\"'()")
        if not cleaned:
            continue
        counts[cleaned] = counts.get(cleaned, 0) + 1

    ordered = sorted(counts.items(), key=lambda kv: kv[1], reverse=True)
    return ordered[:top_n]
```

## 这一天最重要的提醒

- `Path(__file__).parent` 很重要，能避免路径写错。 |
- `with open()` 比裸 `open()` 更稳，程序更安全。 |
- `"w"` 和 `"a"` 的区别必须记住：前者覆盖，后者追加。 |
- `line.strip()` 很常用，特别是在处理文本和文件时。 |
- 读文件时，别忘了 `encoding="utf-8"`，否则中文容易出问题。 |
- 文件不是“临时存储”，它能让程序保存记忆。 |
