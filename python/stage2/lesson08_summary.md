# Day 8 学习总结

## 学习目标与真正学会的内容

| 学习目标 | 真正学会的内容（含例子） |
| --- | --- |
| 学会用字符串做基本处理。 | 用 `s[0]`、`s[-1]`、`s[7:]`、`s[::-1]` 访问字符串中的内容。 |
| 认识字符串是不可变的。 | 不能直接写 `s[0] = "h"`，要重新生成一个新字符串，比如 `s2 = "h" + s[1:]`。 |
| 会用 `strip()` 去掉多余空白。 | `"  Rachel  ".strip()` 可以得到 `"Rachel"`。 |
| 会用 `split()` 把字符串切成列表。 | `"a,b,c".split(",")` 会得到 `['a', 'b', 'c']`。 |
| 会用 `join()` 把列表拼回字符串。 | `"-".join(["2026", "08", "08"])` 会得到 `"2026-08-08"`。 |
| 会用 `replace()` 做替换。 | `"我爱Java".replace("Java", "Python")` 会得到 `"我爱Python"`。 |
| 会用大小写和判断方法处理字符串。 | `"Python".upper()`、`"Python".lower()`、`"hello world".title()`，以及 `.startswith()`、`.endswith()`。 |
| 会用 `f-string` 做对齐和格式化。 | `f"{name:<8} {price:>6.2f}"` 可以让输出更整齐。 |

## 练习里你能直接回顾的点

| 复习点 |
| --- |
| 用 `strip()` 去掉字符串前后空格和换行。 |
| 用 `split()` 按逗号或空格拆分一行文本。 |
| 用列表推导式把拆分后的每一段再做 `strip()`。 |
| 用 `join()` 把多个部分拼成一个完整字符串。 |
| 用 `replace()` 删除指定字符或替换内容。 |
| 用 `lower()` 先统一大小写，再统计单词。 |
| 用 `f-string` 做对齐、保留小数位、千位分隔。 |

## 学习体会

- 今天学到的内容很实用，因为以后读文件、处理用户输入、解析数据，基本都是在处理字符串。 |
- 字符串和列表有些地方很像，但最重要的区别是：字符串不能直接修改，必须重新生成新字符串。 |
- `strip()`、`split()`、`join()`、`replace()` 这几个方法经常一起用，特别适合处理一行文本。 |
- `f-string` 不只是输出值，还能帮我们把结果排好看，适合做表格或小票。 |
- 以后遇到“字符串数据”时，先想清楚：要不要拆、要不要整理、要不要格式化。 |

## 今天实践的代码

### 处理一行文本
```python
line = "  小明 , 90 , 85 , 78  \n"

parts = line.strip().split(",")
parts = [p.strip() for p in parts]
print(parts)
```

### 替换内容
```python
text = "我爱Java"
print(text.replace("Java", "Python"))
```

### 统计单词
```python
text = "Hello hello world hello Python"
words = text.lower().split()

counts = {}
for word in words:
    counts[word] = counts.get(word, 0) + 1

print(counts)
```

### 格式化输出
```python
name = "小明"
price = 12.5
print(f"{name:<8} {price:>6.2f}")
```
