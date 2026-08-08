"""
Day 6 (08-06)  函数 def

今天的目标：会写默认参数、返回多个值，知道什么时候该抽成函数。
教程：https://liaoxuefeng.com/books/python/function/index.html

    JS   function add(a, b) { return a + b }
    Py   def add(a, b): return a + b
"""

# ============================================================
# 读一读
# ============================================================

def greet(name):
    """打招呼。三引号里的话叫 docstring，是给人看的说明。"""
    return f"你好，{name}！"

print(greet("小明"))

# 没有 return 的函数返回 None
def say_hi():
    print("hi")

result = say_hi()
print(result)        # None

# 默认参数：调用时可以不传
def power(base, exp=2):
    return base ** exp

print(power(5))        # 25  用默认的 exp=2
print(power(5, 3))     # 125 传了就用传的

# 关键字参数：按名字传，顺序就不重要了。参数多的时候可读性好得多
def make_event(title, minutes=30, done=False):
    return {"title": title, "minutes": minutes, "done": done}

print(make_event("写作业"))
print(make_event("跑步", done=True))              # 跳过 minutes 直接指定 done
print(make_event(minutes=60, title="看书"))       # 顺序都能换

# 返回多个值：其实是打包成元组，Python 特色，很方便
def min_max(numbers):
    return min(numbers), max(numbers)

low, high = min_max([3, 8, 1, 9, 4])       # 直接拆开接收
print(low, high)

# 作用域：函数里面的变量出了函数就不存在了
def f():
    inside = "我只活在函数里"
    print(inside)

f()
# print(inside)      ← 取消注释会报 NameError

# 这就是为什么要用 return 把结果传出来，而不是指望函数内部的变量


# 为什么要写函数？看这个对比 ↓

# 不用函数（重复代码，改起来要改三处）
print(f"小明的平均分：{(90 + 85 + 78) / 3:.1f}")
print(f"小红的平均分：{(88 + 92 + 95) / 3:.1f}")

# 用函数（逻辑只有一份，改一次全对）
def average(scores):
    return sum(scores) / len(scores)

print(f"小明的平均分：{average([90, 85, 78]):.1f}")
print(f"小红的平均分：{average([88, 92, 95]):.1f}")

# 判断标准很简单：同样的逻辑写了第二遍，就该抽成函数了。


# ============================================================
# 练一练
# ============================================================

# --- 第 1 题 ---
# 写一个函数 is_even(n)，判断 n 是不是偶数，返回 True / False
# 然后用它输出 1-20 里所有的偶数
# TODO


# --- 第 2 题 ---
# 写一个函数 bmi(weight, height)，算 BMI（体重kg / 身高m 的平方）
# 返回两个值：BMI 数值（保留1位小数）和 胖瘦评价
#   低于 18.5 偏瘦 / 18.5-24 正常 / 24 以上 偏胖
# TODO


# --- 第 3 题 ---
# 写一个函数 count_words(text)，统计每个单词出现次数，返回字典
# （就是 Day 5 第 3 题，这次包成函数）
# 然后调用它测试两个不同的句子——体会一下包成函数后复用有多方便
# TODO


# --- 第 4 题 ---
# 写一个函数 grade(score)，输入分数返回等级 A/B/C/D/不及格
# 要求：如果分数不在 0-100 之间，返回 "无效分数"
# 然后用循环测试这些输入：[95, 83, 71, 65, 40, -5, 150]
# TODO


# --- 第 5 题 ---
# 写一个函数 fizzbuzz(n)，从 1 数到 n：
#   能被 3 整除输出 Fizz，能被 5 整除输出 Buzz
#   同时能被 3 和 5 整除输出 FizzBuzz，其他输出数字本身
# 这是最有名的面试题，写出来你就正式入门了
# TODO


# --- 第 6 题（挑战）---
# 把 Day 5 第 6 题的通讯录重写一遍，这次要求：
#   add_contact(book, name, phone)     添加
#   find_contact(book, name)           查询，找不到返回 None
#   delete_contact(book, name)         删除，返回是否删成功
#   show_all(book)                     打印全部
#   main()                             菜单循环
# 主程序里只调用这些函数，不写具体逻辑
# 这就是"函数式拆分"，Day 14 的项目会直接用上
# TODO


# ============================================================
# 自检
# ============================================================
# [ ] 定义函数用什么关键字？后面要加什么符号？
# [ ] 函数没有 return 会返回什么？
# [ ] 怎么让一个参数变成可选的？
# [ ] 怎么一次返回两个值，怎么接收？
# [ ] 什么信号说明"这段代码该抽成函数了"？
