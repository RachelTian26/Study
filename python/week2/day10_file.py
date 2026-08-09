"""
Day 10 (08-10)  文件读写

今天的目标：会用 with open()，说清 r / w / a 的区别，知道路径为什么会找不到。
教程：https://liaoxuefeng.com/books/python/function/io/index.html

今天是这个月第一个"质变"的日子。
在这之前你写的程序一关就什么都没了 —— 列表、字典都活在内存里。
今天开始，程序能把东西写到硬盘上，断电都还在。

calendar-app 里的 data.db 干的就是这件事，只是它用数据库。原理是一样的。
"""

from pathlib import Path

# ============================================================
# 读一读
# ============================================================

# --- 先解决路径问题，不然下面全部报 FileNotFoundError ---
#
# 坑在这：open("data/notes.txt") 里的路径，不是相对于这个 .py 文件，
# 而是相对于"你运行命令时所在的目录"（叫工作目录 / cwd）。
# 你在 VS Code 里点运行，cwd 可能是 python/，也可能是 python/week2/，不一定。
#
# 所以专业做法是：以"这个文件自己的位置"为基准算路径。

HERE = Path(__file__).parent          # __file__ 是当前文件的路径，.parent 是它所在的文件夹
DATA = HERE / "data"                  # Path 对象用 / 拼路径，比字符串拼接干净，还跨系统

print("这个文件在：", HERE)
print("数据文件夹：", DATA)
print("文件夹存在吗：", DATA.exists())

# 记住这三行，后面每次读写文件都照抄。
# 你会在 Day 12、Day 14 反复用到它。


# --- 读整个文件 ---
notes_path = DATA / "notes.txt"

with open(notes_path, "r", encoding="utf-8") as f:
    content = f.read()

print(content)

# 逐个部件拆解上面这句：
#   with ... as f    用完自动关闭文件，哪怕中间报错也会关。不用 with 就得自己 f.close()
#   "r"              模式：read，只读
#   encoding="utf-8" 编码。**中文文件必须写**，不写在某些电脑上会乱码或报错
#   f                文件对象，只在 with 缩进块里能用
#
# 出了 with 的缩进，f 就关了：
# print(f.read())    ← 取消注释会报 ValueError: I/O operation on closed file


# --- 三种读法，用途不同 ---

with open(notes_path, encoding="utf-8") as f:      # "r" 是默认值，可以省
    whole = f.read()                                # 整个文件变成一个大字符串
print(f"整个文件 {len(whole)} 个字符")

with open(notes_path, encoding="utf-8") as f:
    lines = f.readlines()                           # 每行一个元素的列表
print(f"一共 {len(lines)} 行")
print(repr(lines[0]))       # repr() 把字符串原样打出来，能看见结尾的 \n
#   ↑ 注意每行末尾都有 "\n"，这是最常见的坑，处理时要 .strip()

with open(notes_path, encoding="utf-8") as f:
    for line in f:                                  # 直接遍历文件对象 ← 推荐
        print(line.strip())
# 为什么推荐：readlines() 会把整个文件塞进内存，遍历是一行一行读。
# 文件小无所谓，但读几百 MB 的日志时差别巨大。


# --- 写文件："w" 会清空原文件 ---
out_path = HERE / "output.txt"

with open(out_path, "w", encoding="utf-8") as f:
    f.write("第一行\n")               # write() 不会自动换行，要自己写 \n
    f.write("第二行\n")
    f.write(f"这行是算出来的：{2 ** 10}\n")

print(f"写完了，去看看 {out_path.name}")

# ⚠️ "w" 模式打开的瞬间文件就被清空了，哪怕你什么都没写。
# 真实项目里写错模式导致数据没了是很常见的事故，写之前多看一眼。

# 一次写多行：
with open(out_path, "w", encoding="utf-8") as f:
    f.writelines([f"第 {i} 行\n" for i in range(1, 4)])
    # writelines 也不自动加换行，得自己在每个元素里带上 \n

# print 也能写进文件（有时候比 write 顺手，因为它自动换行）
with open(out_path, "w", encoding="utf-8") as f:
    print("用 print 写的", file=f)
    print(f"{3.14159:.2f}", file=f)


# --- 追加："a" 在末尾接着写，不清空 ---
log_path = HERE / "log.txt"

with open(log_path, "a", encoding="utf-8") as f:
    f.write("又运行了一次\n")

# 每次运行这个文件，log.txt 就多一行。这就是日志的写法。
with open(log_path, encoding="utf-8") as f:
    print("现在 log.txt 有", len(f.readlines()), "行")


# --- 四种模式，记住这张表 ---
#   "r"   只读。文件不存在 → FileNotFoundError
#   "w"   只写。文件不存在就新建，**存在就清空**
#   "a"   追加。文件不存在就新建，存在就在末尾接着写
#   "x"   新建。文件已存在 → FileExistsError（想确保不覆盖时用）
#
# 加 "b" 是二进制（图片、视频），今天用不上，知道有就行：open(p, "rb")


# --- 文件存在吗？ ---
# 直接读不存在的文件会崩，读之前先判断（Day 11 会学更好的办法：try/except）
missing = DATA / "不存在的文件.txt"
if missing.exists():
    print("有这个文件")
else:
    print("没有这个文件，跳过")

# Path 还有一堆好用的东西：
print(notes_path.name)        # notes.txt      文件名
print(notes_path.stem)        # notes          不含后缀
print(notes_path.suffix)      # .txt           后缀
print(notes_path.exists())    # True

# 列出文件夹里所有 .txt：
for p in DATA.glob("*.txt"):
    print("找到：", p.name)


# --- 真实场景：读 CSV 并解析 ---
# data/scores.csv 是一份"脏"数据，故意留了空行、多余空格、缺列、非数字
# 今天先用最朴素的办法读，Day 11 学了异常处理再来收拾这些坑

csv_path = DATA / "scores.csv"

with open(csv_path, encoding="utf-8") as f:
    lines = f.readlines()

header = lines[0].strip().split(",")
print("表头：", header)

for line in lines[1:]:
    line = line.strip()
    if not line:              # 跳过空行 —— 空字符串是 False，这个技巧很常用
        continue
    parts = [p.strip() for p in line.split(",")]
    print(parts)
# ↑ 跑一遍看输出，注意"小美"那行的 abc 和"小强"那行只有 3 段。
# 现在还不用管它们，但先看清楚真实数据有多脏。

# 顺便说一句：Python 有专门的 csv 模块，能处理逗号在引号里之类的怪情况。
# 今天故意手写，因为手写一遍你才知道 csv 模块在替你干什么。


# ============================================================
# 练一练
# ============================================================

# 所有题目都用文件开头的 HERE / DATA 来拼路径，别写死路径

# --- 第 1 题 ---
# 读 data/article.txt，输出：
#   一共多少行、多少个单词、多少个字符（不含空白）
# 提示：单词数可以把整个文件 .split() 之后数长度
# TODO


# --- 第 2 题 ---
# 读 data/notes.txt，给每行加上行号后打印，格式：
#   1 | 今天开始学文件读写。
#   2 | 文件就是硬盘上的一段文字...
# 要求：跳过空行，行号右对齐占 2 格
# 提示：enumerate(f, start=1) 可以让计数从 1 开始
# TODO


# --- 第 3 题 ---
# 把第 2 题的结果**写进**一个新文件 numbered.txt，而不是打印
# 写完后自己打开文件确认一下
# 提示：一个 with 读，一个 with 写；或者先读进列表再写
# TODO


# --- 第 4 题 ---
# 读 data/scores.csv，只处理"格式完整且三科都是数字"的行，
# 把其他行跳过并打印一句「第 N 行数据有问题，已跳过」。
# 然后输出一张成绩表（可以直接搬 Day 7 的 print_table 思路），
# 并算出各科平均分。
#
# 这题是 Day 7 那个你没写完的 print_summary 的第二次机会 ——
# 这次数据来自文件，不用手输了。
# 提示：判断"是不是数字"先用 .isdigit()，Day 11 会有更好的写法
# TODO


# --- 第 5 题 ---
# 做一个"运行记录器"：每次运行这个文件，就往 run_log.txt 追加一行，
# 内容是「第 N 次运行」，N 要接着上次的数往下数。
# 提示：先读文件数一下已经有几行（文件可能还不存在，要判断），再追加
# 这题的核心是体会 "a" 模式和 "程序有记忆" 是什么意思
# TODO


# --- 第 6 题（挑战）---
# 写一个函数 word_count(path, top_n=5)：
#   读指定文件，统计单词出现次数，返回出现最多的 top_n 个
#   返回格式 [("python", 5), ("is", 4), ...]
# 用 data/article.txt 测试
# 提示：统计还是 .get(词, 0) + 1；排序可以用
#       sorted(counts.items(), key=lambda kv: kv[1], reverse=True)
#       lambda 是"一次性小函数"，key= 告诉 sorted 按什么排。
#       看不懂就先照抄，Day 13 之后再回来理解
# TODO


# --- 第 7 题（挑战）---
# 把 Day 7 的成绩统计器改造一下：录入完成后，把成绩表存进 grades.txt，
# 下次运行时先读这个文件，把之前录的人显示出来，然后可以继续加人。
#
# 这就是 Day 14 通讯录项目的雏形，只是那时候会用 JSON 存。
# 提示：存的时候一行一个学生，用 | 或 , 分隔；读的时候 split 回来
# TODO


# ============================================================
# 自检
# ============================================================
# [ ] 为什么要用 with open() 而不是直接 open()？
# [ ] "w" 和 "a" 的区别？哪个会让你丢数据？
# [ ] 读中文文件不写 encoding="utf-8" 会怎样？
# [ ] readlines() 拿到的每行末尾有什么？怎么去掉？
# [ ] f.read() / f.readlines() / for line in f 分别什么时候用？
# [ ] Path(__file__).parent 是什么意思？为什么不直接写 "data/x.txt"？


# ============================================================
# 收尾
# ============================================================
# 这个文件跑完会在 week2/ 里生成 output.txt、log.txt 和你练习产出的文件。
# 都是练习产物，不用管，也不用提交到 git（week2/.gitignore 已经帮你排除了）。
