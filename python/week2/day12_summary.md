# Day 12 学习总结

## 学习目标与真正学会的内容

| 学习目标 | 真正学会的内容（含例子） |
| --- | --- |
| 学会 `JSON` 和 Python 的互转。 | `json.dumps(data)` 把 Python 的字典/列表变成字符串；`json.loads(text)` 把字符串变回字典/列表。 |
| 学会和文件打交道的 `dump`/`load`。 | `json.dump(data, f)` 把数据写进文件；`json.load(f)` 从文件读出来。 |
| 明白 `带 s` 和 `不带 s` 的区别。 | `dumps/loads` 处理字符串；`dump/load` 处理文件，记住这个规律很重要。 |
| 会处理中文 JSON。 | `json.dumps(data, ensure_ascii=False, indent=2)` 能让中文正常显示，写文件更容易看。 |
| 会处理 Python 和 JSON 的类型差异。 | Python 里的 `True` / `None`，JSON 里对应是 `true` / `null`；元组会变成列表。 |
| 会用 `try/except` 处理坏 JSON。 | 例如 `json.loads("{'title': 'x'}")` 会报 `JSONDecodeError`，这时可以捕获并提示。 |
| 会写 `load_json()` 和 `save_json()`。 | 这是今天最重要的两个函数，可以重复用在后面的通讯录、待办列表等项目里。 |
| 会把数据写进 JSON 文件保存。 | 程序重启后还能继续读取，不会一下子消失。 |
| 会做“结构化数据”的统计和筛选。 | 例如按 `activityType` 分组统计，按 `status` 过滤 `pending`，很常用。 |
| 会理解“数据存得住”的意义。 | 以前数据在内存里，一关闭程序就没了；JSON 让数据能保留到下一次运行。 |

## 练习里你能直接回顾的点

| 复习点 |
| --- |
| `json.dumps(obj)` 把字典转成字符串。 |
| `json.loads(text)` 把字符串转回字典。 |
| `json.dump(data, f)` 把数据直接写进文件。 |
| `json.load(f)` 从文件读取数据。 |
| `ensure_ascii=False` 让中文正常显示。 |
| `indent=2` 让 JSON 文件更好看。 |
| `JSONDecodeError` 是 JSON 格式错误时常见的异常。 |
| Python 中 `True/False/None` 转成 JSON 时分别变成 `true/false/null`。 |
| `tuple` 写进 JSON 后会变成 `list`。 |
| `load_json(path, default=[])` 可以避免“文件不存在时崩掉”。 |
| `save_json(data, path)` 适合把字典或列表保存成 JSON 文件。 |
| `setdefault()` 很适合做按日期或按类型分组统计。 |
| `find_events(events, keyword)` 能做大小写不敏感搜索。 |
| `CSV` 也能做表格保存，但它丢失了原来字典里的很多字段。 |

## 学习体会

- 今天最重要的不是“背几个函数”，而是学会了“把 Python 里的数据真正存起来”。 |
- `JSON` 让我们能把 `list` 和 `dict` 这样的数据保存到文件里，第二次运行时还能读回来。 |
- 这其实是程序从“临时计算”变成“有记忆”的关键一步。 |
- 学到 `dumps/loads` 和 `dump/load` 后，后面的很多项目都会直接用到。 |
- `True/False/None` 这种 Python 特有的东西，存成 JSON 以后会变成 `true/false/null`，这是常见坑。 |
- `JSONDecodeError` 很像今天学到的 `ValueError`，都是“格式不对”，只是它专门针对 JSON。 |
- `load_json` 设计成“文件不存在时返回默认值”，非常实用。这样程序不会因为缺文件直接崩掉。 |
- `events.json` 这种结构很像真实项目里常见的数据格式：列表里装字典，每个字典代表一条事件。 |
- `CSV` 是表格格式，适合展示和导出；`JSON` 更适合存结构化数据和嵌套数据。 |
- 今天的重点是：数据不只是看得见，还要“能保存、能读、能继续用”。 |

## 今天实践的代码

### 1. 字典转字符串，再转回来
```python
event = {
    "id": "e1",
    "title": "写数学作业",
    "duration": 60,
    "done": False,
    "tags": ["study", "homework"],
    "note": None,
}

text = json.dumps(event)
back = json.loads(text)

print(text)
print(back)
```

### 2. 中文 JSON 要加 `ensure_ascii=False`
```python
print(json.dumps({"名字": "小明"}, ensure_ascii=False, indent=2))
```

### 3. JSON 读取文件
```python
with open(events_path, encoding="utf-8") as f:
    events = json.load(f)

print(type(events), type(events[0]))
```

### 4. 按类型统计
```python
by_type = {}
for event in events:
    kind = event.get("activityType", "unknown")
    by_type.setdefault(kind, {"count": 0, "minutes": 0})
    by_type[kind]["count"] += 1
    by_type[kind]["minutes"] += event.get("duration", 0)
```

### 5. 过滤 pending 事项并保存
```python
pending_list = []
for event in events:
    if event.get("status") == "pending":
        pending_list.append(event)

with open("pending.json", "w", encoding="utf-8") as f:
    json.dump(pending_list, f, ensure_ascii=False, indent=2)
```

### 6. 自动生成新的事件 id
```python
existing_ids = []
for item in events:
    event_id = item.get("id", "")
    if event_id.startswith("e") and event_id[1:].isdigit():
        existing_ids.append(int(event_id[1:]))

next_num = max(existing_ids) + 1 if existing_ids else 1
new_id = f"e{next_num}"
```

### 7. 查找关键字并忽略大小写
```python
def find_events(events, keyword):
    keyword = keyword.lower()
    result = []

    for event in events:
        title = str(event.get("title", "")).lower()
        description = str(event.get("description", "")).lower()
        if keyword in title or keyword in description:
            result.append(event)

    return result
```

### 8. 读取 JSON 文件，文件不存在时返回默认值
```python
def load_json(path, default=None):
    path = Path(path)
    if not path.exists():
        return default

    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        print("JSON 格式错误，返回默认值")
        return default
```

### 9. 写 JSON 文件保存数据
```python
def save_json(data, path):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
```

### 10. CSV 导出和读取
```python
def to_csv(events, path):
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["date", "title", "startTime", "duration", "status"])
        for item in events:
            writer.writerow([
                item.get("date", ""),
                item.get("title", ""),
                item.get("startTime", ""),
                item.get("duration", 0),
                item.get("status", ""),
            ])
```

## 这一天最重要的提醒

- `json.dumps` 和 `json.loads` 处理的是字符串，不是文件。 |
- `json.dump` 和 `json.load` 处理的是文件，不是字符串。 |
- `ensure_ascii=False` 很重要，中文文件不然会变成 `\uXXXX`。 |
- `indent=2` 让 JSON 更好看，也方便查看。 |
- Python 里 `True/False/None` 和 JSON 里的 `true/false/null` 不一样。 |
- `load_json` 最重要的作用是“文件不存在也不要崩”，这是程序写得稳的体现。 |
- `save_json` 是把结构化数据保存成文件，让程序具有“持久化能力”。 |
- JSON 很适合保存 `dict` 和 `list`，而 CSV 更适合保存简单表格。 |
- 今天的真正意义在于：程序终于能把数据保存下来而不是只停留在内存里。 |

## 一句话总结

Day 12 的核心是：学会把 Python 里的字典、列表和其他数据，写进 JSON 文件，再从文件读回来，程序就能“保存状态”和“下次继续用”。
