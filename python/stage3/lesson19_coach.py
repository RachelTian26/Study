"""
第 19 课  工具主体：把零件拼成能用的东西

前四课你学了四个零件：
    第 15 课 类        → 用来表示"一节课""一道题""一次答题"
    第 16 课 时间      → 用来算"隔了多久没复习"
    第 17 课 HTTP      → 通往外面世界的路
    第 18 课 调大模型  → 让 AI 干活

这节课不学新语法，**只干一件事：把它们拼起来。**
今天结束时，你会有一个真的能跑的 coach.py（暂时不带 AI，第 20 课接）。

「读一读」的输出全部实测，读的是你自己那 13 篇 summary。
"""

import json
import re
from datetime import date
from pathlib import Path

# ============================================================
# 一、为什么这节重要
# ============================================================
"""
【对写 Python 的意义】

    前面每节课都是几十行的独立小程序，写完就扔。
    这节课开始，你要维护一个几百行、跨文件、有状态的东西。

    你会遇到一种新的困难：**不是"这行怎么写"，是"这段该放哪"。**
    这是从"会写代码"到"会做东西"之间那道坎，只能靠做真项目跨过去。

【对用好 AI 的意义】★ 这条值得认真读

    有一件事你在 calendar-app 里已经隐约感觉到了，今天说破：

        **你能把需求说多清楚，AI 就能帮你到多远。**

    "帮我做个复习工具" —— AI 会给你一坨能跑但不是你要的东西。
    "读 stage1/ 和 stage2/ 下所有 lessonNN_summary.md，
      提取「练习里你能直接回顾的点」表格里的每一行作为知识点，
      按学习日期算间隔，挑出最该复习的一节" —— 这才能用。

    差别不在措辞，在于**第二句话的人自己想清楚了数据长什么样**。
    今天你做的设计工作（数据结构、流程、边界情况），
    就是你以后向 AI 提需求时的底气。

    还有一条反过来的：**程序越大，AI 的错越难发现。**
    50 行的代码你一眼扫完。500 行的代码，AI 塞进去一个错误的边界判断，
    你可能三个星期后才发现题库里少了一半知识点。
    所以从今天起加一条习惯：**一次只改一个函数，改完立刻跑。**

【不学会的后果】

    第 20 课接不上 —— 那节课是往这个工具里接 AI，工具本身得先跑起来。
"""


# ============================================================
# 二、先讲人话
# ============================================================
"""
【一个工具由三层组成】

    做任何工具，先问自己这三个问题：

        1. 数据从哪来？        ← 读取层
        2. 数据长什么样？      ← 数据层
        3. 数据存哪去？        ← 存储层

    我们的复习教练：

        读取层   读 stage1/、stage2/ 下的 lessonNN_summary.md
                 从里面挖出「知识点」

        数据层   Lesson（一节课）、Question（一道题）、Record（一次答题）
                 ↑ 第 15 课你写过这三个类了

        存储层   coach_data/ 下的 JSON 文件
                 ↑ 第 12 课学的 json.dump / json.load

【为什么先想清楚再动手】

    盖房子的类比：数据结构是地基，功能是房间。
    地基改一次，上面所有房间都要重砌。

    具体到这个工具：如果你一开始把"知识点"设计成一个字符串，
    后来想加"这个知识点我答错过几次"，就得把所有用到它的地方全改一遍。
    一开始就设计成对象，加个字段就完事了。

【今天的目标不是写完，是跑通一条最细的线】

    ❌ 不要一口气写 300 行然后运行
    ✅ 先让"读到 13 个文件名"跑通 → 再让"读出标题"跑通 →
       再让"读出知识点"跑通 → 再存 JSON

    每一步都能看到东西，每一步都能 commit。
    这个习惯比今天写的任何一行代码都值钱。
"""


# ============================================================
# 三、读一读
# ============================================================

HERE = Path(__file__).parent
PY_ROOT = HERE.parent                    # python/ 目录
DATA_DIR = HERE / "coach_data"           # 工具产生的数据放这儿

# ---------- 3.1 找到所有 summary 文件 ----------

# Path.glob() 按模式找文件。* 匹配任意字符，** 匹配任意层目录
files = sorted(PY_ROOT.glob("stage[12]/lesson*_summary.md"))

print("找到", len(files), "个 summary")
# 输出：找到 13 个 summary

print([f.name for f in files[:3]])
# 输出：['lesson01_summary.md', 'lesson02_summary.md', 'lesson03_summary.md']

# ★ 为什么用 stage[12] 而不是 stage*：
#   [12] 表示"1 或 2 这一个字符"。用 stage* 的话，
#   等你写完 stage3 的 summary，它也会被扫进来 —— 那时候你还没学呢。
#   等你学完了，把它改成 stage[123] 就行。

print(files[0].relative_to(PY_ROOT))
# 输出：stage1/lesson01_summary.md
#       ★ relative_to() 把绝对路径变成相对的，存 JSON 时用它 ——
#         绝对路径带着 /Users/tian，换台电脑就废了


# ---------- 3.2 从文件名里抠出课号 ----------

# 文件名长这样：lesson07_summary.md，要拿到 7
name = files[6].name
print(name)
# 输出：lesson07_summary.md

# 办法一：字符串切片（脆，文件名一变就废）
print(int(name[6:8]))
# 输出：7

# 办法二：正则表达式（稳一点）
m = re.search(r"lesson(\d+)", name)
print(int(m.group(1)))
# 输出：7

# 正则你还没系统学过，这里只要记住这一个模式：
#     r"lesson(\d+)"    \d 是数字，+ 是"一个或多个"，() 是"把这段抓出来"
#     m.group(1)        拿到第一个括号里抓到的东西（字符串）
#     m 可能是 None（没匹配上），用之前要判断


# ---------- 3.3 ★ 解析 markdown 表格：这是今天的核心技术 ----------
"""
    你的 summary 里有这么一段（第 5 课那篇）：

        ## 练习里你能直接回顾的点

        | 复习点 |
        | --- |
        | 第 1 题：用 `.items()` 遍历字典并打印每条信息。 |
        | 第 2 题：计算总分、平均分、最高科目，并筛选低于 80 分的科目。 |

    我们要把每一行的内容抠出来，作为"知识点"喂给 AI 出题。

    思路（三步，全是第 8 课和第 10 课的东西）：
        1. 按行读文件
        2. 找到 "## 练习里你能直接回顾的点" 那一行，开始收集
        3. 遇到下一个 "## " 就停；中间以 | 开头的行，去掉两边的 | 再 strip
"""


def extract_table_rows(text, heading):
    """从 markdown 文本里，抠出某个二级标题下面表格的所有数据行。

    返回字符串列表。找不到该标题就返回空列表。
    """
    rows = []
    collecting = False
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("## "):
            # 碰到二级标题：是目标就开始收，是别的就停
            collecting = heading in stripped
            continue
        if not collecting or not stripped.startswith("|"):
            continue
        # 去掉首尾的 |，按 | 切成各列
        cells = [c.strip() for c in stripped.strip("|").split("|")]
        if not cells or not cells[0]:
            continue
        if set(cells[0]) <= {"-", " ", ":"}:      # | --- | 这种分隔行，跳过
            continue
        if cells[0] in ("复习点", "学习目标", "重要点"):   # 表头行，跳过
            continue
        rows.append(cells[0])
    return rows


text = files[4].read_text(encoding="utf-8")       # 第 5 课那篇
points = extract_table_rows(text, "练习里你能直接回顾的点")

print("\n第 5 课有", len(points), "个知识点")
# 输出：第 5 课有 6 个知识点

print(points[0])
# 输出：第 1 题：用 `.items()` 遍历字典并打印每条信息。

print(points[1])
# 输出：第 2 题：计算总分、平均分、最高科目，并筛选低于 80 分的科目。

# 扫一遍全部 13 篇，看看数据够不够：
total = 0
missing = []
for f in files:
    n = len(extract_table_rows(f.read_text(encoding="utf-8"), "练习里你能直接回顾的点"))
    total += n
    if n == 0:
        missing.append(f.name)

print("\n13 篇一共", total, "个知识点")
# 输出：13 篇一共 95 个知识点

print("没有这一节的:", missing)
# 输出：没有这一节的: ['lesson01_summary.md']
#
# ★★ 这就是真实数据的样子 —— 不整齐。
#    第 1 课那篇你没写「练习里你能直接回顾的点」这一节。
#    你的程序**必须能接受这种不整齐**，不能因为一个文件缺一节就崩。
#
#    这一点比什么语法都重要：教程里的数据永远是干净的，
#    真实数据永远是脏的。第 10 课那个故意弄脏的 scores.csv 就是在练这个。


# ---------- 3.4 学习日期从哪来 ----------
"""
    要算"隔了多久没复习"，得知道每节课是哪天学的。三个来源：

    ❌ 文件修改时间（f.stat().st_mtime）
       不行。你改一次错别字，日期就变了。我批量改文件名时已经把它们全刷成今天了。

    ⚠ git 提交记录
       准，但要调 git 命令（subprocess），而且文件改过名之后要 --follow。
       能用，但对现在的你有点绕。

    ✅ 自己记一份
       我已经从 git 里把真实日期翻出来了，存在 lessons_seed.json 里。
       工具读它就行，以后学完新课自己加一条。

    ★ 这是个真实的工程判断：**能查的数据不一定要实时去查。**
      一份手工维护的小文件，往往比一个"聪明"的自动方案更可靠。
"""

seed_path = HERE / "lessons_seed.json"
seed = json.loads(seed_path.read_text(encoding="utf-8"))

print("\n种子文件里有", len(seed["lessons"]), "节课")
# 输出：种子文件里有 17 节课

first = seed["lessons"][0]
print(first["num"], first["title"], first["learned"])
# 输出：1 变量 · 输出 · 数据类型 2026-08-08

# 配合第 16 课的日期计算：
learned = date.fromisoformat(first["learned"])
print("距今", (date.today() - learned).days, "天")
# 🌐 这个数字每天都在变，你跑出来跟我不一样是正常的


# ---------- 3.5 存储：读写 JSON ----------

DATA_DIR.mkdir(exist_ok=True)            # 目录不存在就建，存在也不报错

demo_file = DATA_DIR / "demo.json"


def save_json(data, path):
    """把数据存成 JSON。中文不转义，缩进 2 空格。"""
    path.write_text(
        json.dumps(data, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def load_json(path, default=None):
    """读 JSON。文件不存在或坏了，返回 default 而不是崩掉。"""
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        print(f"⚠ {path.name} 内容坏了，当作空的处理")
        return default


save_json({"测试": [1, 2, 3]}, demo_file)
print("\n读回来:", load_json(demo_file))
# 输出：读回来: {'测试': [1, 2, 3]}

print("文件不存在时:", load_json(DATA_DIR / "根本没有.json", default={}))
# 输出：文件不存在时: {}

# ★ 这两个函数你第 13 课已经写进 mytools.py 了。
#   这里我用 Path 的 write_text/read_text 重写了一遍 —— 比 with open() 更短。
#   注意 ensure_ascii=False，不加的话中文会存成 你好（第 12 课讲过）。


# ---------- 3.6 ★ 坑：id 该怎么生成 ----------

# 最常见的错误写法（AI 尤其爱写这个）：
items = [{"id": 1, "t": "a"}, {"id": 2, "t": "b"}, {"id": 3, "t": "c"}]

new_id = len(items) + 1
print("\n新 id:", new_id)
# 输出：新 id: 4        ← 看起来没问题

# 但删掉中间一条之后：
items.pop(1)                             # 删掉 id=2 那条
new_id = len(items) + 1
print("删了一条之后的新 id:", new_id)
# 输出：删了一条之后的新 id: 3
#       ↑ 已经有 id=3 了！**id 撞了。**

# 正确写法之一：取当前最大值 + 1
def next_id(items):
    """生成下一个不重复的 id。空列表时返回 1。"""
    return max((item["id"] for item in items), default=0) + 1


print("正确的新 id:", next_id(items))
# 输出：正确的新 id: 4

# max(..., default=0) 里的 default 是空列表时的返回值 ——
# 不写的话空列表会抛 ValueError。

# 【为什么这个坑值得单独讲】
#   跟第 16 课那个字符串算日期一样：**它在大部分时候是对的。**
#   只要你没删过东西，len+1 永远正确。测试也能过。
#   等你用了两个月、删过几条记录之后，才开始出现"两条记录 id 一样"的诡异 bug。
#
#   ★ 这类 bug 的共同特征：**触发条件是"用久了"，而不是"输入错了"。**
#     这正是 AI 最容易漏、你也最难测出来的一类。


# ---------- 3.7 把 3.1-3.5 串起来 ----------

def load_all_lessons():
    """读种子文件 + 扫 summary，拼出完整的课程列表。"""
    seed = json.loads((HERE / "lessons_seed.json").read_text(encoding="utf-8"))
    result = []
    for item in seed["lessons"]:
        path = PY_ROOT / item["summary"]
        points = []
        if path.exists():
            points = extract_table_rows(
                path.read_text(encoding="utf-8"), "练习里你能直接回顾的点"
            )
        result.append({
            "num": item["num"],
            "title": item["title"],
            "learned": item["learned"],
            "points": points,
        })
    return result


lessons = load_all_lessons()
print("\n装载了", len(lessons), "节课")
# 输出：装载了 17 节课

print("有知识点的:", sum(1 for x in lessons if x["points"]), "节")
# 输出：有知识点的: 14 节

# 按知识点数量排个序看看
top = sorted(lessons, key=lambda x: len(x["points"]), reverse=True)[:3]
print([(x["num"], len(x["points"])) for x in top])
# 输出：[(12, 14), (13, 13), (15, 11)]
#       ↑ (课号, 知识点数)。第 12 课的 summary 你写得最全，所以素材最多 ——
#         summary 写得越认真，这个工具出的题就越好。这是它的正反馈

# 清理掉刚才的演示文件
demo_file.unlink(missing_ok=True)


# ============================================================
# 四、练一练  ★ 这部分你手写，我不代写
# ============================================================
"""
今天的练习跟前几课不一样：**你要在旁边新建一个 coach.py，把工具真的写出来。**
这个文件不是练习，是你之后会一直用、一直改的东西。

顺序很重要，一题一题来，每题写完立刻运行看效果。
不要跳到第 5 题去写主程序 —— 前面没跑通，主程序一定是坏的。
"""

# --- 第 1 题：搭骨架 ---
# 新建 stage3/coach.py，先写好结构（照 textstats.py 的样子）：
#   文件顶部：docstring 说明这是干什么的
#   常量：HERE、PY_ROOT、DATA_DIR
#   底部：if __name__ == "__main__": main()
#   main() 里先只写一行 print("复习教练启动")
# 跑一遍，看到那句话就算过。
# ★ 别小看这一步。先让一个空壳跑起来，比写完 300 行再调试轻松十倍。
# TODO


# --- 第 2 题：数据类 ---
# 把第 15 课第 3、4、6 题的三个类搬进 coach.py，按工具的真实需要改：
#
#   Lesson    num, title, learned(date对象), points(列表)
#             days_since()      距今多少天        ← 第 16 课
#             is_due(count)     该不该复习了      ← 第 16 课 3.9
#             pick_point()      随机挑一个知识点  ← random.choice
#
#   Question  text, answer, source_lesson
#             check(user_input)  判对错（先做字符串比较，第 20 课换成 AI 判）
#
#   Record    lesson_num, questions, answers
#             score()            返回 (对几道, 共几道)
#
# 要求：
#   [ ] 每个类都有 __repr__
#   [ ] Lesson 的 points 参数默认值**不能写成 []**（第 15 课 3.6）
#   [ ] 每个类都有 to_dict()，Lesson 还要有 from_dict()（第 15 课第 7 题）
# TODO


# --- 第 3 题：读取层 ---
# 在 coach.py 里写 load_lessons()，返回 Lesson 对象的列表。
# 直接用 3.7 的 load_all_lessons 思路，但要返回**对象**不是字典。
#
# 写完验证三件事：
#   [ ] 返回 17 个 Lesson（lessons_seed.json 里有几条就是几个）
#   [ ] 第 1 课的 points 是空列表，程序不崩
#   [ ] 随便打印一个 Lesson，__repr__ 好看
# TODO


# --- 第 4 题：挑课 ---
# 写 pick_lesson(lessons)：挑出今天最该复习的一节，返回 Lesson 或 None。
#
# 规则你自己定，但必须在 docstring 里写清楚。参考：
#   · 跳过 points 为空的（没素材，出不了题）
#   · 优先选逾期最久的
#   · 都不该复习就返回 None
#
# ★ 这题跟第 16 课第 5 题是同一道，那题做过就搬过来。
#   没做的话现在补 —— 这是工具的大脑。
# TODO


# --- 第 5 题：存储层 ---
# 写两个函数：
#   save_record(record)     把一次答题存进 coach_data/records.json（追加，不是覆盖）
#   load_records()          读出全部记录，文件不存在返回 []
#
# 要求：
#   [ ] id 用 3.6 的 next_id，不许用 len+1
#   [ ] 文件不存在、内容坏了都不能崩
#   [ ] 存的时候 ensure_ascii=False
#
# 测试方法：存两条 → 关掉程序 → 重新运行 → 读出来还是两条。
# ★ 这就是第 14 课（跳过的那节）本来要练的东西，这次换个更有用的场景补上
# TODO


# --- 第 6 题：串成主程序 ---
# 写 main()，把上面全接起来：
#
#   1. 载入所有课
#   2. 挑一节该复习的（没有就提示"今天没有需要复习的，去学新课吧"然后退出）
#   3. 从它的 points 里挑 3 个知识点
#   4. **暂时用手写的题目**（第 20 课换成 AI 出题）：
#      直接把知识点本身当题目问 "还记得这个吗？(y/n)"
#   5. 记录结果，存进 records.json
#   6. 打印本次得分
#
# 跑通它。丑没关系，能跑最重要。
# ★ 第 4 步的"占位实现"是个重要技巧：**先用假的把流程跑通，再换成真的。**
#   这样你能确定流程是对的，之后接 AI 出问题时就知道是 AI 那段的锅。
# TODO


# --- 第 7 题（挑战）---
# 3.5 的 save_json 有个隐患：如果程序在写文件的中途崩了（断电、Ctrl+C），
# 文件会变成半截的，下次读就坏了 —— 而你所有的答题记录都在里面。
#
# 查一下"原子写入"是怎么做的，回答（写注释里）：
#   1. 标准做法是什么？（提示：跟"先写到临时文件"有关）
#   2. Path.replace() 和 Path.rename() 有什么区别？
#   3. 你觉得这个工具有必要做原子写吗？说出你的判断和理由
#
# ★ 第 3 问才是重点。**不是所有隐患都值得修**，
#   工程判断的一半是"知道什么时候可以不管"。
# TODO


# ============================================================
# 五、问 AI
# ============================================================

# ---------- 5.1 找坑 ----------
"""
下面这段是"帮我写个存储答题记录的类"的典型 AI 产物。找出 5 个问题：

    import json

    class RecordStore:
        def __init__(self, path="records.json"):
            self.path = path
            self.records = []
            if os.path.exists(path):
                with open(path) as f:
                    self.records = json.load(f)

        def add(self, lesson_num, score):
            record = {
                "id": len(self.records) + 1,
                "lesson": lesson_num,
                "score": score,
                "date": str(datetime.now())
            }
            self.records.append(record)
            self.save()

        def save(self):
            with open(self.path, "w") as f:
                json.dump(self.records, f)

写下你找到的：
    1.
    2.
    3.
    4.
    5.

【方向提示】
    · 3.6 讲的那个（最经典）
    · 第 10 课反复强调的、open() 必须带的参数（这里缺了两处）
    · 第 12 课讲的、json.dump 处理中文要加的参数
    · 文件内容如果坏了会怎样？（3.5 的 load_json 就是防这个的）
    · 有两个模块用了但没 import

    加分题：默认参数 path="records.json" 是相对路径。
    从不同目录运行这个程序会发生什么？（第 10 课那个 FileNotFoundError 的坑）

【找完再往下】
把它发给 AI 问"有什么问题"。这次重点观察一件事：

    ★ **它会不会提 id 那个坑？**

    我的预期是：它大概率不会主动提，因为那段代码"看起来完全正常"。
    但如果你换个问法 —— "如果用户删除过记录，这段代码会出什么问题？" ——
    它多半立刻就能答对。

    这说明一件很重要的事：
    **AI 的能力上限很高，但它默认只回答你字面问的东西。**
    你问"有什么问题"，它扫一遍常见错误清单；
    你问"删除记录后会怎样"，它才真的去推演。

    **会提问的人从同一个 AI 那里能拿到多得多的东西。** 这就是"用好 AI"的含义。
"""

# ---------- 5.2 去问 ----------
"""
【模板 1 —— 让它审你的设计，不是你的代码】

    我要做一个复习工具，数据结构是这样设计的：

        Lesson  = {课号, 标题, 学习日期, 知识点列表}
        Record  = {课号, 题目列表, 我的答案列表, 日期}

    我想支持这些功能：挑该复习的课、出题、记录对错、下次优先考错过的。

    这个设计有什么会在三个月后坑到我的地方？不要给我代码，只说设计问题。

    ↑ **"三个月后"这个限定词是精髓。** 不加它，AI 会说些泛泛的好话；
      加了它，它才会去想"数据变多之后""需求变了之后"。

【模板 2 —— 让它扮演用户挑刺】

    你是一个 14 岁的学生，有人给你做了一个用 AI 出题帮你复习的命令行工具。
    你会在什么情况下用了两天就不想再用了？列 5 个最可能的原因。

    ↑ 这个视角能挖出技术思路挖不到的东西。
      **认真看它的回答 —— 里面很可能有你的工具真正的死因。**

【模板 3 —— 拆解一个你写不出来的功能】

    我想给工具加"优先考我答错过的知识点"。
    不要给我代码。把这个需求拆成 3-5 个我需要自己想清楚的问题，
    每个问题给我两个可选方案和各自的代价。

    ↑ 这是我最推荐的一个模板。**让 AI 帮你想问题，而不是帮你写答案。**
      问题想清楚了，代码你自己就能写；
      问题没想清楚，AI 给你的代码你也不知道对不对。

【做完记在 summary 里】
    · 模板 2 里，哪一条你觉得说到点子上了？你打算怎么防？
    · 「找坑」你找到几个？AI 提没提 id 那条？
"""


# ============================================================
# 六、自检
# ============================================================
# [ ] 一个工具的三层分别是什么？你的 coach.py 里各对应哪些函数？
# [ ] 为什么 id 不能用 len(列表) + 1？这个 bug 什么时候才会暴露？
# [ ] 13 篇 summary 里有一篇缺了「复习点」那一节，你的代码是怎么处理的？
# [ ] Path.glob("stage[12]/lesson*_summary.md") 里的 [12] 和 * 分别什么意思？
# [ ] 为什么学习日期不用文件修改时间？
# [ ] load_json 为什么要接 JSONDecodeError？不接会怎样？
# [ ] 「先用假的把流程跑通，再换成真的」这个做法好在哪？


if __name__ == "__main__":
    print("\n" + "=" * 50)
    print("第 19 课「读一读」跑完了。")
    print("现在去新建 coach.py，从第 1 题开始，一题一跑。")
