"""
Day 13 (08-13)  模块导入 · venv · pip

今天的目标：能建虚拟环境、装包、写自己的模块并 import。
教程：https://liaoxuefeng.com/books/python/function/modules/index.html
      https://liaoxuefeng.com/books/python/function/install-modules/index.html

今天这些东西你在 JS 世界里全都有对应，对照着记会非常快：

    JS                              Python
    import x from "./x.js"      →   import x  /  from x import ...
    node_modules/               →   .venv/lib/.../site-packages/
    npm install express         →   pip install fastapi
    package.json (dependencies) →   requirements.txt
    npx / node                  →   python
    module.exports              →   不需要，文件里的东西默认就能被 import

唯一一个 Python 独有、必须搞懂的东西是 `if __name__ == "__main__"`。
Day 7 你照抄过它，今天把它彻底弄明白。
"""

# ============================================================
# 读一读（一）：import 的几种写法
# ============================================================

# 写法 1：import 整个模块，用的时候带前缀 ← 最推荐，一眼看出东西来自哪
import json
import random

print(random.randint(1, 6))
print(json.dumps({"a": 1}))

# 写法 2：从模块里挑几个东西出来，用的时候不带前缀
from pathlib import Path
from datetime import datetime

print(Path.cwd())
print(datetime.now())

# 写法 3：起别名，名字太长时用
import datetime as dt
print(dt.date.today())

# 写法 4：⚠️ 别用
# from math import *
# 为什么坏：谁知道它导进来了多少个名字？很容易悄悄覆盖你自己的变量。
#          比如你有个变量叫 pow，被 math.pow 覆盖了，你要查半天。

# 常见的坑：只 import 模块名，却想直接用里面的函数
import math
# print(sqrt(16))        ← NameError，因为 sqrt 在 math 里，不在当前文件
print(math.sqrt(16))     # 要带前缀
# 或者一开始就 from math import sqrt


# ============================================================
# 读一读（二）：标准库有什么
# ============================================================
# Python 号称 "batteries included"（自带电池），装好就有 200 多个模块。
# 你现在该知道这几个：

# --- random 随机 ---
print(random.randint(1, 100))                    # 1-100 的整数，两头都含
print(random.choice(["石头", "剪刀", "布"]))       # 随便挑一个
print(random.sample(range(1, 50), 5))            # 不重复地挑 5 个
nums = [1, 2, 3, 4, 5]
random.shuffle(nums)                             # 打乱原列表（跟 list.sort() 一样，直接改）
print(nums)

# --- math 数学 ---
print(math.pi, math.sqrt(2), math.ceil(3.2), math.floor(3.8))
# 注意 round() 是内置的，不用 import。而且它是"四舍六入五取偶"：
print(round(2.5), round(3.5))       # 2 4  ← 不是你以为的 3 4，别惊讶

# --- datetime 时间（Day 17 会细讲，今天先用起来）---
now = datetime.now()
print(now.strftime("%Y-%m-%d %H:%M:%S"))         # 格式化成字符串
print(now.isoformat())                            # 2026-08-13T10:30:00.123456
# 存进 JSON 就用 .isoformat() 或 .strftime()，Day 12 讲过 datetime 不能直接 dump

# --- os / sys 系统相关 ---
import os
import sys
print("Python 版本：", sys.version.split()[0])
print("当前目录：", os.getcwd())
print("这个文件的路径：", __file__)

# --- collections：更好用的容器 ---
from collections import Counter

# 还记得 Day 5/6/8 你写过三遍的词频统计吗？标准库里有现成的：
words = "hello world hello python world hello".split()
c = Counter(words)
print(c)                          # Counter({'hello': 3, 'world': 2, 'python': 1})
print(c.most_common(2))           # [('hello', 3), ('world', 2)]
print(c["hello"])                 # 3
print(c["不存在的词"])              # 0  ← 不会 KeyError，比 dict 省事

# 说明一下为什么前面几天让你手写：
#   手写过一遍，你才知道 Counter 在替你干什么，也才有能力判断它够不够用。
#   现在开始，这种活可以放心交给标准库了。

from collections import defaultdict
# Day 12 的 setdefault 分组，用 defaultdict 更干净：
by_type = defaultdict(list)              # 访问不存在的键时自动建一个空列表
for w in words:
    by_type[len(w)].append(w)
print(dict(by_type))


# ============================================================
# 读一读（三）：__name__ 到底是什么
# ============================================================

# 每个 Python 文件运行时，都有一个内置变量 __name__：
#   直接运行这个文件           → __name__ 是 "__main__"
#   这个文件被别人 import      → __name__ 是模块名（比如 "textstats"）

print(f"\n当前文件的 __name__ = {__name__!r}")
# 直接运行会打印 '__main__'

# 所以这个写法的意思是「只在我被直接运行时才执行」：
#
#     if __name__ == "__main__":
#         main()
#
# 为什么需要它：一个文件常常既想当"能跑的程序"，又想当"能被 import 的工具箱"。
# 没有这层保护，别人 import 你的文件时，你的 main() 会立刻跑起来 —— 一般不是他想要的。

# 我给你写了个示范模块 textstats.py，就在旁边。先做两件事：
#   1. 打开 textstats.py 读一遍，看它的结构
#   2. 在终端直接运行它：python week2/textstats.py   ← 会看到自测输出
# 然后看下面 import 它会发生什么：

import textstats

print("\n--- import textstats 之后 ---")
print("textstats 的版本：", textstats.VERSION)
print(textstats.summary("Python is fun and Python is fast"))
print(textstats.top_words("Python is fun and Python is fast", 2))
# 注意：上面 import 的时候，textstats.py 里 if __name__ 那段自测代码**没有**执行。
# 这就是那行 if 的作用。

# 为什么 import textstats 能找到它？
#   Python 找模块的顺序大致是：当前脚本所在的目录 → 标准库 → 已安装的第三方包。
#   textstats.py 和这个文件在同一个 week2/ 里，所以直接就找到了。
#   如果它在别的文件夹，就要用包（package）的写法，那是以后的事。


# ============================================================
# 读一读（四）：venv 和 pip（在终端做，不在这个文件里）
# ============================================================
"""
虚拟环境解决的问题，跟 node_modules 一样：
项目 A 要 requests 2.0，项目 B 要 requests 3.0，装在系统里就打架了。
虚拟环境 = 给每个项目一份独立的包目录。

━━━ 在终端里操作（Ctrl + 反引号 打开终端）━━━

1) 进到 python 目录
       cd /Users/tian/Downloads/Study/python

2) 建虚拟环境（只需做一次，会生成一个 .venv 文件夹）
       python3 -m venv .venv
   -m 的意思是"把 venv 当命令来跑"。.venv 这个名字是社区惯例。

3) 激活（每次开新终端都要做）
       source .venv/bin/activate
   成功的标志：命令行提示符前面多了 (.venv)
   退出用：deactivate

4) 确认你在虚拟环境里
       which python        → 应该指向 .../python/.venv/bin/python
       python --version    → 3.14.5

5) 装包试试
       pip install requests
       pip list                    看装了什么
       pip show requests           看某个包的详情

6) 记录依赖（相当于 package.json）
       pip freeze > requirements.txt
   别人拿到你的代码，一句话装齐：
       pip install -r requirements.txt

7) VS Code 要用这个环境：
       Cmd + Shift + P → 输入 "Python: Select Interpreter" → 选 .venv 那个
   选完右下角会显示 .venv，之后点运行按钮就用的是虚拟环境。

━━━ 几个提醒 ━━━

• .venv/ 不要提交到 git（跟 node_modules 一样）。
  python/.gitignore 我已经帮你写好了。
• requirements.txt 要提交。
• 忘了激活会怎样：pip install 装到系统 Python 里去了，
  然后 VS Code 里 import 报 ModuleNotFoundError，你会找半天。
  记住一个检查动作：看提示符有没有 (.venv)。
• Day 18 要用 requests，Day 22 要用 fastapi，届时都装在这个环境里。

━━━ 装完自测（在终端里跑）━━━

       python -c "import requests; print(requests.__version__)"

  python -c "代码" 是直接跑一行代码，不用建文件，试东西时很方便。
"""


# ============================================================
# 练一练
# ============================================================

# --- 第 1 题 ---
# 用 random 写一个"猜数字"游戏，比 Day 3 那版进阶：
#   答案随机生成 1-100，最多猜 7 次
#   每次提示大了/小了，还剩几次
#   猜中或次数用完都要给结论
# 提示：math.log2(100) ≈ 6.6，所以 7 次是"二分法刚好够"，这个游戏是有解的
# TODO


# --- 第 2 题 ---
# 用 random.sample 写一个双色球选号：
#   从 1-33 里不重复选 6 个红球（排序后输出），从 1-16 里选 1 个蓝球
# 输出格式：红球 03 07 12 19 25 31 | 蓝球 08
# 提示：数字补零用 f"{n:02d}"
# TODO


# --- 第 3 题 ---
# 用 Counter 重写 Day 8 第 3 题的词频统计，读 data/article.txt，输出出现最多的 5 个词。
# 然后跟你 Day 8 手写的版本对比一下：代码少了多少行？
# 提示：读文件要用 Day 10 的 Path(__file__).parent
# TODO


# --- 第 4 题（今天最重要的一题）---
# 建一个你自己的模块 week2/mytools.py，把这个月写过的好东西都收进去：
#
#   load_json(path, default=None)      Day 12 写的
#   save_json(data, path)              Day 12 写的
#   safe_int(text, default=0)          Day 11 第 1 题写的
#   get_number(prompt, low, high)      Day 11 第 2 题写的
#   average(numbers)                   Day 6 写的
#   grade(score)                       Day 6/7 写的
#   mask_phone(phone)                  Day 8 第 4 题写的
#
# 要求：
#   [ ] 每个函数都有 docstring
#   [ ] 文件底部用 if __name__ == "__main__" 包一段自测，直接运行能看到每个函数的效果
#   [ ] 照着 textstats.py 的结构写
#
# 然后在这个文件里 import mytools，调用其中至少 3 个函数验证能用。
#
# 这个 mytools.py 不是练习，是你真的会一直用下去的东西 ——
# Day 14 通讯录、Day 20 待办工具都会 import 它。
# TODO


# --- 第 5 题 ---
# 在终端里把虚拟环境建起来，装上 requests，然后回到这个文件里写：
#   try: import requests 成功就打印版本号
#   except ModuleNotFoundError: 打印「还没装 requests，先激活 .venv 再 pip install」
# 提示：ModuleNotFoundError 是 ImportError 的子类
# 这题的意义：你会亲手体会一次"装了但 VS Code 找不到"，以后能自己排查
# TODO


# --- 第 6 题（挑战）---
# 给 textstats.py 加一个新函数（直接改我那个文件）：
#   longest_words(text, n=3)   返回最长的 n 个不重复单词
# 加完在这个文件里 import 进来测试。
#
# 顺便注意一件事：改完 textstats.py 之后，这个文件要重新运行才会用到新版本。
# Python 的 import 在一次运行里只加载一遍。
# TODO


# --- 第 7 题（挑战）---
# 读一读标准库里 pathlib 的官方文档，找出这三个问题的答案：
#   1. 怎么一次建好多层文件夹？（提示：mkdir 的某个参数）
#   2. 怎么读一个文件的全部内容，不用 with open？（提示：Path 有个 read_ 开头的方法）
#   3. path.parts 返回什么？
# https://docs.python.org/zh-cn/3/library/pathlib.html
#
# 这题练的不是语法，是"查官方文档"这个能力 —— 比查菜鸟教程更值得练。
# TODO


# ============================================================
# 自检
# ============================================================
# [ ] import x 和 from x import y 用的时候有什么区别？
# [ ] 为什么不要用 from x import *？
# [ ] __name__ 什么时候是 "__main__"？这个 if 保护的是什么？
# [ ] 虚拟环境解决什么问题？怎么知道自己在虚拟环境里？
# [ ] requirements.txt 相当于 JS 里的什么？.venv 相当于什么？
# [ ] import mytools 的时候，Python 去哪里找这个文件？
