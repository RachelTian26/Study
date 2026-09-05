# Day 6 学习总结

## 学习目标与真正学会的内容

| 学习目标 | 真正学会的内容（含例子） |
| --- | --- |
| 学会用 `def` 定义函数。 | `def greet(name):` 开始定义一个函数，函数名后面加小括号和冒号。 |
| 认识函数可以避免重复代码。 | 把计算平均分的逻辑写成 `average(scores)`，就不用为小明和小红重复写同样的计算。 |
| 会写默认参数。 | `def power(base, exp=2):` 当调用 `power(5)` 时，`exp` 自动是 `2`。 |
| 会返回多个值。 | `def min_max(numbers): return min(numbers), max(numbers)`，调用时可以写 `low, high = min_max(...)`。 |
| 理解函数内部变量的作用域。 | 函数里面的 `inside = "..."` 只在函数里有效，函数外面不能访问。 |
| 了解函数需要 `return` 才能把结果传出来。 | `say_hi()` 只打印 `hi`，但没有 `return`，所以 `result = say_hi()` 结果是 `None`。 |
| 注意输出结果时要用 `print()` 或把值返回后再打印。 | 如果只是写完计算，没写 `print()`，程序不会显示结果。 |

## 练习里你能直接回顾的点

| 复习点 |
| --- |
| 用 `is_even(n)` 判断偶数，复用函数逻辑。 |
| 写 `bmi(weight, height)` 返回 BMI 和评价，并测试多个人的数据。 |
| 把 Day 5 的单词统计逻辑包装成 `count_words(text)` 函数。 |
| 写 `grade(score)` 判断分数等级，并处理无效分数。 |
| 实现 `fizzbuzz(n)`，练习条件判断和取余运算。 |
| 用 `add_contact`、`find_contact`、`delete_contact`、`show_all` 拆分通讯录功能。 |

## 练习代码示例

### 判断偶数
```python
def is_even(n):
    return n % 2 == 0

for i in range(1, 21):
    if is_even(i):
        print(i, end=" ")
```

### BMI 计算
```python
def bmi(weight, height):
    bmi_value = weight / (height ** 2)
    if bmi_value < 18.5:
        result = "偏瘦"
    elif bmi_value < 24:
        result = "正常"
    else:
        result = "偏胖"
    return round(bmi_value, 1), result
```

### 统计单词出现次数
```python
def count_words(text):
    words = text.split()
    counts = {}
    for word in words:
        counts[word] = counts.get(word, 0) + 1
    return counts
```

### 分数等级判断
```python
def grade(score):
    if score < 0 or score > 100:
        return "无效分数"
    elif score >= 90:
        return "A"
    elif score >= 80:
        return "B"
    elif score >= 70:
        return "C"
    elif score >= 60:
        return "D"
    else:
        return "不及格"
```

### FizzBuzz
```python
def fizzbuzz(n):
    for i in range(1, n + 1):
        if i % 3 == 0 and i % 5 == 0:
            print("FizzBuzz")
        elif i % 3 == 0:
            print("Fizz")
        elif i % 5 == 0:
            print("Buzz")
        else:
            print(i)
```

### 通讯录拆分函数
```python
def add_contact(book, name, phone):
    book[name] = phone

def find_contact(book, name):
    return book.get(name)

def delete_contact(book, name):
    if name in book:
        del book[name]
        return True
    return False

def show_all(book):
    if not book:
        print("通讯录为空")
    else:
        print("姓名      | 电话")
        print("---------|----------------")
        for name, phone in book.items():
            print(f"{name:<8} | {phone}")
```

## 学习体会

- 输出的时候如果要显示多条结果，应该用 `for` 循环逐行输出，这样结果更清楚。 |
- 输出格式不好看时要优化，比如在 `show_all` 里用表头和竖线分隔。 |
- 定义数组（列表）时，可以给出清楚的变量名，让意思更易理解。 |
- 定义的时候先想好内容和名字，代码看起来会更好。 |
