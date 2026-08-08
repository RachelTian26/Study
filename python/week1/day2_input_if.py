"""
Day 2 (08-02)  输入 · 运算 · 条件判断

今天的目标：if/elif/else 写熟，牢记 input() 拿到的永远是字符串。
教程：https://liaoxuefeng.com/books/python/basic/branch/index.html

注意：这个文件里有 input()，运行后要在下面的终端里打字然后按回车。
"""

# ============================================================
# 读一读
# ============================================================

# input() 会暂停程序，等你打字。括号里的话是提示语。
# 关键：input() 的结果永远是字符串！哪怕你输入 15，拿到的也是 "15"
age_text = input("你几岁了？")
print(f"你输入的是 {age_text}，类型是 {type(age_text)}")

# 想当数字用就得转
age = int(age_text)

# 也可以一步写完（常见写法）
# age = int(input("你几岁了？"))

# 条件判断。注意三件事：
#   1. 条件后面有冒号 :
#   2. 里面的代码要缩进（4 个空格，VS Code 按 Tab 会自动变成 4 空格）
#   3. 是 elif 不是 else if
if age < 13:
    print("小学生")
elif age < 16:
    print("初中生")
elif age < 19:
    print("高中生")
else:
    print("成年人")

# 比较运算符：==  !=  >  <  >=  <=
# 注意 == 是比较，= 是赋值。Python 没有 JS 的 ===
print(3 == 3.0)   # True，Python 里整数和小数可以直接比

# 逻辑运算：and / or / not（JS 里是 && || !）
score = 85
if score >= 60 and score < 90:
    print("及格了，但还能再高")

# 这种链式写法 Python 独有，很好用：
if 60 <= score < 90:
    print("同一个意思，写法更清爽")

# 常用运算符
print(10 / 3)   # 3.333...  除法，结果一定是小数
print(10 // 3)  # 3         整除，砍掉小数
print(10 % 3)   # 1         取余数，判断奇偶/整除时超常用
print(2 ** 10)  # 1024      幂运算


# ============================================================
# 练一练
# ============================================================

# --- 第 1 题 ---
# 让用户输入一个数字，判断是奇数还是偶数，输出结果
# 提示：用 % 2
# TODO
input_num = int(input("请输入一个数字: "))
if input_num % 2 == 0:
    print(f"{input_num} even")
else:
    print(f"{input_num} odd")
    

# --- 第 2 题 ---
# 让用户输入分数（0-100），按下面的规则输出等级：
#   90 及以上 → A
#   80-89     → B
#   70-79     → C
#   60-69     → D
#   60 以下   → 不及格
# TODO
level = int(input("enter score"))
if level >= 90:
    print("A")
elif level >= 80:
    print("B")
elif level >= 70:
    print("C")
elif level >= 60:
    print("D")
else:
    print("不及格")

# --- 第 3 题 ---
# 让用户输入两个数字，输出较大的那个
# 先自己用 if 写一遍，写完之后再查一下 max() 函数，对比一下
# TODO
number = int(input("number1"))
number2= int(input("number2"))
if number > number2:
    print(f"较大的数字是{number}")
else:
    print(f"较大的数字是{number2}")

# --- 第 4 题 ---
# 简易闰年判断：让用户输入年份，判断是不是闰年
# 规则：能被 4 整除但不能被 100 整除，或者能被 400 整除
# 提示：这题需要 and / or 配合括号，先在纸上把逻辑写清楚
# TODO
runian = int(input("give a year"))
if (runian % 4 == 0 and runian % 100 != 0) or (runian % 400 == 0):
    print(f"{runian}是闰年)")
else:
    print(f"{runian}不是闰年")


# --- 第 5 题（有点难，值得挑战）---
# 做一个"猜数字"的单次版本：
#   程序里先定义一个答案 answer = 42
#   让用户输入一个数字
#   如果猜大了输出"太大了"，猜小了输出"太小了"，猜对了输出"猜对了！"
# （明天学了循环，就能改成一直猜到对为止）
# TODO
answer = 42
guess = int(input("猜一个数字"))
if guess > answer:
    print("太大了")
elif guess < answer:
    print("太小了")
else:
    print("猜对了！")
    

# ============================================================
# 自检
# ============================================================
# [ ] input() 返回什么类型？想要数字怎么办？
# [ ] Python 里"否则如果"怎么写？
# [ ] if 后面忘了冒号会报什么错？（故意试一次，认识这个错误）
# [ ] 10 / 3 和 10 // 3 差在哪？
