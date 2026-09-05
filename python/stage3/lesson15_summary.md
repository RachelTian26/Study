# 第 15 课学习总结

## 为什么学这个很重要

| 重要点 | 说明 |
| --- | --- |
| 类是把数据和规则放在一起 | 以前用字典装数据，但类还能规定“这个东西应该有什么字段、能做什么操作”。 |
| 对象是类的具体实例 | `Student` 是模板，`s1 = Student("小明", [90, 85, 88])` 就是一个具体对象。 |
| `self` 很关键 | 它代表“当前这个对象自己”，所有实例属性都要通过 `self` 来访问。 |
| `__init__` 是初始化入口 | 它在对象创建时自动调用，用来给对象赋值。 |
| `__repr__` 让输出更容易看 | 不写它时，打印对象会出现一串地址；写了之后会更清晰。 |
| 可变默认参数是经典坑 | `scores=[]` 这种写法会让多个对象共用同一个列表，最后容易出 bug。 |
| 这节课是“写真实项目”的起点 | 后面的课程里会用类来表示题目、记录、课程对象，代码会更清晰。 |
| 类比字典更适合“有规则”的数据 | 只存数据可以用字典，但一旦有“算平均分”“判断答题”“生成标题”这样的行为，类更合适。 |

## 学习目标与真正学会的内容

| 学习目标 | 真正学会的内容（含例子） |
| --- | --- |
| 会写最简单的类。 | `class Student: ...`，`__init__` 里给对象赋值。 |
| 会理解 `self`。 | `self.name`、`self.scores`，都是“当前对象自己的属性”。 |
| 会用 `__repr__`。 | `print(s1)` 会显示成 `Student('小明', 平均 87.66)`，比一串内存地址好看很多。 |
| 会知道类属性和实例属性的区别。 | `Question.total` 是类属性，所有对象共用；`self.text` 是实例属性。 |
| 会理解可变默认参数的坑。 | `scores=[]` 会共享；正确写法是 `scores=None`，再在函数里判断。 |
| 会写 `Lesson` 这种工具类。 | 课号、标题、卡点、路径等都可以封装到对象中。 |
| 会写 `Question` 类。 | 用 `strip()` 和 `lower()` 统一大小写和空格，然后判断是否相等。 |
| 会用类把“数据”和“行为”放在一起。 | `average()`、`best()`、`check()`，这些都属于对象的方法。 |

## 练习里你能直接回顾的点

| 复习点 |
| --- |
| `self` 是对象本身，不用手动传。 |
| `__init__` 是在对象创建时自动执行的。 |
| `print(obj)` 时，Python 会调用 `__repr__`。 |
| `scores=[]` 是错的，`scores=None` 才是安全的。 |
| `if not self.scores:` 可以判断列表是否为空。 |
| `sum(scores) / len(scores)` 可以算平均分。 |
| `max(scores)` 找最高分。 |
| `strip()` 去掉两边空格；`lower()` 统一成小写。 |
| `Question.check()` 里要先清洗用户输入，再比较答案。 |
| `Lesson.stage()` 可以根据课号返回第几阶段。 |
| 类适合放“规则”和“方法”，字典适合放“原始数据”。 |

## 学习体会

- 这节课最重要的收获不是“会写 class”，而是知道了“为什么需要类”。
- 以前我会用字典存很多信息，但类让这些信息更有规则，不容易乱用。 |
- `self` 一开始最容易混，但真正理解之后，类就像一个“真实的东西”，不是一堆乱放的变量。 |
- 我现在觉得类最像“模板”，比如学生表、题目卡、课程记录，它们都有固定字段和固定操作。 |
- `__repr__` 这个方法很实用，因为调试时看对象的输出比看一串地址容易多了。 |
- 可变默认参数是最值得记住的坑。它看起来不明显，但一不注意就会出非常隐蔽的 bug。 |
- 第 4 题和第 5 题让我明白：真正判断“对不对”，不一定只看字符串完全相等，很多时候还要看语义。 |
- 这节课最像“从写脚本进入写工具”的一课。以后如果做项目，类会让代码更清晰，也更容易维护。 |

## 今天实践的代码

### 1. `Student` 类
```python
class Student:
    def __init__(self, name, scores):
        self.name = name
        self.scores = scores

    def average(self):
        if not self.scores:
            return 0
        return sum(self.scores) / len(self.scores)

    def best(self):
        if not self.scores:
            return None
        return max(self.scores)

    def __repr__(self):
        return f"Student('{self.name}', 平均 {self.average()})"
```

### 2. 可变默认参数的坑
```python
class BadRecord:
    def __init__(self, name, tags=[]):
        self.name = name
        self.tags = tags
```

这样写会让多个对象共享同一个列表。

正确写法：
```python
class GoodRecord:
    def __init__(self, name, tags=None):
        self.name = name
        self.tags = tags if tags is not None else []
```

### 3. `Question` 类
```python
class Question:
    def __init__(self, text, answer, source_lesson):
        self.text = text
        self.answer = answer
        self.source_lesson = source_lesson

    def check(self, user_input):
        cleaned_user = str(user_input).strip().lower()
        cleaned_answer = str(self.answer).strip().lower()
        return cleaned_user == cleaned_answer
```

### 4. 第 5 题的思考
```python
# 参考答案：去掉两头空白
# 用户答案：删除首尾空格
# 这两个意思相同，但字符串不一样。
```

这说明“简单的字符串比较”不够用，真实场景可能需要更宽松的判断方法，例如：
- 关键词匹配
- 让 AI 判断语义
- 改成选择题

## 这一天最重要的提醒

- `self` 不是神秘魔法，它只是当前对象这个变量。 |
- `__init__` 和 `__repr__` 这两种方法，都是 Python 里很常见的“魔术方法”。 |
- 凡是参数里出现 `[]` / `{}` / `set()`，都要特别警惕。 |
- 类不是为了炫技，而是为了让代码更清晰、更可维护。 |
- 写类的时候要先想清楚：这个东西有什么属性？有什么行为？ |
- 现实里，很多数据其实更适合用类来组织，而不是堆在字典里。 |

## 最后一段：我的真实体会

这一节课最难的不是语法，而是“把抽象的概念真正理解成能用的思维”。一开始我会觉得 `self` 很绕，`__init__` 也只会照抄；但后来我发现，类其实就是把数据和规则放在一起，像一个学生对象、一个题目对象、一个课程对象。最让人受益的地方，是我开始意识到“不是所有东西都适合用字典存”，有些东西需要对象来管理。最重要的坑是可变默认参数，因为它看起来没问题，但运行时就会悄悄串数据。下一步我想继续练习把课程、题目、记录都做成对象，这样以后写项目会更顺手。

## 一句话总结

第 15 课的核心是：学会把“数据”和“行为”放进类里，用对象来组织信息，并且知道 `self`、`__init__`、`__repr__` 和可变默认参数这些关键点，才能写出更稳定、更可维护的 Python 代码。
