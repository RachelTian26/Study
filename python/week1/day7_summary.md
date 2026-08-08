# Day 7 学习总结

## 学习目标与真正学会的内容

| 学习目标 | 真正学会的内容（含例子） |
| --- | --- |
| 会把前面学的函数、列表、字典、循环、条件、输入输出等知识点组合起来。 | 用 `main()` 控制程序流程，把录入、打印成绩表、统计总结等步骤拆成不同函数。 |
| 会定义函数并让它们各司其职。 | `get_score()` 负责输入一个合法分数，`input_one_student()` 负责录入一个学生，`print_table()` 负责打印成绩表。 |
| 会做输入合法性检查。 | `get_score()` 判断输入是否是数字并且在 `0-100` 之间，非法时提示重输，不让程序崩。 |
| 会用循环实现多次录入和多条输出。 | `while` 循环让用户可以一个接一个录学生，`for` 循环让成绩表、总结结果逐行输出。 |
| 会用 `if` 判断处理不同情况。 | 根据平均分用 `grade()` 返回 `A/B/C/D/F`，根据是否有学生决定是打印表格还是输出“没有数据”。 |
| 会把输出格式化成表格形式。 | 用 `f"{value:>6}"` 和 `f"{name:<8}"` 控制列宽，让成绩表对齐好看。 |

## 练习里你能直接回顾的点

| 复习点 |
| --- |
| `get_score(subject)`：输入一科分数并检查是否合法。 |
| `input_one_student()`：输入姓名和三科分数，返回一个学生字典。 |
| `total(student)` 和 `average(student)`：计算总分和平均分。 |
| `print_table(students)`：打印成绩表，按列对齐显示姓名、三科、总分、平均分、等级。 |
| `print_summary(students)`：打印班级统计结果。 |
| `main()`：主流程里先读取学生，再判断是否为空，最后输出表格和总结。 |

## 学习体会

- 这一天学会了把不同知识点穿起来，一个完整程序里既有函数，也有列表、字典、循环、条件和输入输出。 |
- 定义函数时要让每个函数只做一件事，程序结构会更清楚，调试也更简单。 |
- 输入输出时，必须检查用户输入是否合法，尤其是分数是否是数字且在 `0-100`。 |
- 循环的时候，`else` 不能放条件；`else` 是循环结束后的补充代码，条件判断要写在 `if` 里。 |
- 输出结果时，表格格式要提前想好，列宽和对齐会让结果看起来更专业。 |

## 今天实践的代码

### 输入分数并检查合法性
```python
def get_score(subject):
    while True:
        if subject == "chinese":
            score = input("请输入语文成绩（0-100）：")
        elif subject == "math":
            score = input("请输入数学成绩（0-100)：")
        else:
            score = input("请输入英语成绩（0-100)：")

        if score.isdigit() and 0 <= int(score) <= 100:
            return int(score)
        print("输入无效，请重新输入！")
```

### 录入一个学生
```python
def input_one_student():
    name = input("请输入学生姓名（直接回车结束录入）：")
    if name == "":
        return None
    student = {
        "name": name,
        "chinese": get_score("chinese"),
        "math": get_score("math"),
        "english": get_score("english")
    }
    print(f"已录入学生：{student['name']}，语文：{student['chinese']}，数学：{student['math']}，英语：{student['english']}")
    return student
```

### 打印成绩表
```python
def print_table(students):
    print(f"{'姓名':<8} {'语文':>5} {'数学':>5} {'英语':>5} {'总分':>5} {'平均分':>6} {'等级':<4}")
    print("-" * 50)
    for student in students:
        print(f"{student['name']:<8} {student['chinese']:>5} {student['math']:>5} {student['english']:>5} {total(student):>5} {average(student):>6.1f} {grade(average(student)):<4}")
```

### 主流程
```python
def main():
    students = [
        {"name": "小明", "chinese": 90, "math": 85, "english": 78},
        {"name": "小红", "chinese": 88, "math": 92, "english": 95},
        {"name": "小刚", "chinese": 80, "math": 70, "english": 60}
    ]
    while True:
        student = input_one_student()
        if student is None:
            break
        students.append(student)

    if not students:
        print("没有数据")
        return

    print_table(students)
    print_summary(students)
```

## 以后 summary 也要加代码示例

- 以后每次写总结，都把今天实践的关键代码放进去，帮助自己快速回顾。 |
