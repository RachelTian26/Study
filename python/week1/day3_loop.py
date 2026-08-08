"""
Day 3 (08-03)  循环 for · while · range

今天的目标：会用 break / continue，能写嵌套循环。
教程：https://liaoxuefeng.com/books/python/basic/loop/index.html

循环是编程里最重要的东西之一。今天多写几遍，写到不用想。
"""

# ============================================================
# 读一读
# ============================================================

# range(5) 生成 0,1,2,3,4 —— 注意不包含 5！
for i in range(5):
    print(f"第 {i} 次")

print("---")

# range(起点, 终点) —— 包含起点，不含终点
for i in range(1, 6):
    print(i)   # 1 2 3 4 5

print("---")

# range(起点, 终点, 步长)
for i in range(0, 10, 2):
    print(i)   # 0 2 4 6 8

# 倒着数：步长给负数
for i in range(5, 0, -1):
    print(i)   # 5 4 3 2 1

print("---")

# for 也能直接遍历字符串、列表等
for ch in "Python":
    print(ch)

print("---")

# while：条件为真就一直转
count = 0
while count < 3:
    print(f"count 现在是 {count}")
    count += 1      # 千万别忘了这行！忘了就是死循环（真卡住了按 Ctrl+C）

print("---")

# break：立刻跳出整个循环
for i in range(10):
    if i == 4:
        break
    print(i)     # 0 1 2 3

print("---")

# continue：跳过这一轮，继续下一轮
for i in range(6):
    if i % 2 == 0:
        continue
    print(i)     # 1 3 5

print("---")

# 嵌套循环：循环里面套循环。外层转一次，内层转一整轮
for i in range(1, 4):
    for j in range(1, 4):
        print(f"{i}x{j}={i*j}", end="  ")   # end="  " 表示不换行，用空格结尾
    print()   # 空的 print() 就是换行


# ============================================================
# 练一练
# ============================================================

# --- 第 1 题 ---
# 用循环输出 1 到 100 所有数字的和（答案是 5050）
# TODO
sum = 0
for i in range(1, 101):
    # sum = 0
    # print(f"sum = {sum}, i = {i}")
    sum += i
print(sum)
assert sum == 5050, "答案不对"

# --- 第 2 题 ---
# 输出 1-50 之间所有能被 7 整除的数
# TODO
for i in range(1, 51):
    if i % 7 == 0:
        print(i)


# --- 第 3 题 ---
# 把昨天的"猜数字"改成真正的游戏：
#   answer = 42
#   用 while 循环让用户一直猜，猜对了输出"猜对了"并用 break 退出
#   猜大猜小都给提示
#   顺便记一下猜了几次，最后输出"你一共猜了 N 次"
# TODO
# answer = 42
# guess = int(input("猜一个数字"))
# while guess != answer:
#     if guess > answer:
#         print("太大了")
#     else:
#         print("太小了")
#     guess = int(input("再猜一个数字"))
# print("猜对了！it is number answer " + str(answer))


# --- 第 4 题 ---
# 用嵌套循环打印这个图形（5 行）：
# *
# **
# ***
# ****
# *****
# 提示："*" * 3 会得到 "***"，这题其实一层循环就够，但两种都试试
# TODO
for i in range(1, 6):
    print("*" * i)


# --- 第 5 题 ---
# 打印完整的 9x9 乘法表，要求对齐好看
# 提示：f"{值:>4}" 表示右对齐占 4 个字符宽
# TODO
for i in range(1, 10):
    for j in range(1, i + 1):
        print(f"{j}x{i}={i*j:>2}", end="  ")
    print()

# --- 第 6 题（挑战）---
# 让用户不停输入数字，输入 0 就停止
# 停止后输出：一共输入了几个数、它们的和、平均值
# 提示：先想清楚"在循环外面"要准备哪些变量
# TODO
input_count = 0
input_sum = 0
input_avg = 0
while True:
    input_num = int(input("请输入一个数字(输入0结束): "))
    if input_num == 0:
        break
    input_count += 1
    input_sum += input_num
if input_count > 0:
    input_avg = input_sum / input_count
else:
    input_avg = 0
print(f"一共输入了{input_count}个数, 它们的和是{input_sum}, 平均值是{input_avg:.2f}")


# ============================================================
# 自检
# ============================================================
# [ ] range(3) 包含 3 吗？range(1, 4) 生成哪几个数？ 不包含3， 生成123
# [ ] break 和 continue 差在哪？ break 是跳出整个循环，continue 是跳过本次循环，继续下一轮
# [ ] while 循环里忘了改变量会怎样？怎么强制停下来？ conmmand+c
# [ ] 嵌套循环里，内层跑完一轮外层才动一次——对吗？ yes
