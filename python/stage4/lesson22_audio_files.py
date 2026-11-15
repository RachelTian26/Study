"""
第 22 课  配音演员赛跑：给每句话掐秒表

今天你会做出：一场"配音演员赛跑"。
             6 个配音演员（有一个会冒泡泡，有一个是机器人，有一个会唱歌）抢着念同一句话，
             场记掐秒表，屏幕上排出名次，最后冠军亲口给你念一遍。

上一课招来了配音演员（say）。今天招第二个人：场记。
场记拿着秒表，量每句配音有多长。后面字幕组（第 23 课）要靠这些秒数排时间，
剪辑师（第 25 课）要靠它们决定每页画面放多久。

标 🔊 的只有 1 处会出声（冠军领奖）；其它全部存成文件。
秒数标了 🌐：同一台电脑上每次都一样，换台 Mac 或换系统版本可能差一点。
"""

import json
import subprocess
from pathlib import Path

# ============================================================
# 一、为什么这节重要
# ============================================================
"""
【对写 Python 的意义】
    上一课 Python 只会"喊人干活"。今天它还要"听人回话"：
    场记量完时长，把结果交回来，Python 拿到这个数，才能排名次、算总时长。
    只会喊不会听，导演就是个瞎指挥。

【对用好 AI 的意义】
    AI 写的"调命令拿结果"的代码，经常拿到结果就直接用，不检查命令有没有成功。
    今天 5.1 的坑就出在 Opus 写的真实脚本里。

【不学会的后果】
    第 23 课排字幕要每句的秒数，第 25 课剪视频也要。量不出秒数，流水线就转不起来。
"""


# ============================================================
# 二、先讲人话
# ============================================================
"""
【类比：场记递纸条】

    | 生活里（拍片剧组）                         | 代码里                             |
    |--------------------------------------------|------------------------------------|
    | 场记，拿秒表量每句话多长                   | ffprobe 命令                       |
    | 场记对着全场大喊"2.88 秒！"，导演没记下来 | subprocess.run(命令)               |
    | 场记把结果写在纸条上，递到导演手里         | capture_output=True, text=True     |
    | 纸条上写的字                               | r.stdout                           |
    | 把纸条上的"2.88"读成能做加法的数字        | float(r.stdout)                    |
    | 给每段录音贴编号 01、02、03，排得整整齐齐  | f"line{i:02d}.aiff"                |

    术语：
        stdout      标准输出。人话：程序正常要说的话，平时直接打到屏幕上。

【类比哪里不像】
    真的纸条你一眼就能看出是空白的。r.stdout 空了，Python 不会提醒你，
    它会拿着空纸条硬去读数字，然后报一个看不懂的错（5.1 就是这个坑）。

今天只有 3 个新东西：拿回纸条（capture_output）、读成数字（float）、给文件编号（:02d）。
"""


# ============================================================
# 三、读一读
# ============================================================

NAME = "Rachel"           # ← 换成你的名字
HERE = Path(__file__).parent
OUT = HERE / "lesson_out" / "lesson22"
RACE = OUT / "race"
RACE.mkdir(parents=True, exist_ok=True)     # 上一课照抄过的两行，3.4 再细说


def stopwatch(path):
    """场记的秒表：量一个音频有多少秒。先当黑盒用，3.2 和 3.3 把它拆开。"""
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                        "-of", "csv=p=0", str(path)], capture_output=True, text=True)
    return float(r.stdout)


# ---------- 3.1 先玩一下：配音演员赛跑 ----------

sentence = f"{NAME} is making a science video."
racers = ["Samantha", "Daniel", "Bubbles", "Zarvox", "Whisper", "Bad News"]

fastest_voice = ""
fastest_seconds = 999.0           # 先放一个超大的数，谁都比它快

for voice in racers:
    audio = RACE / (voice + ".aiff")
    subprocess.run(["say", "-v", voice, "-o", str(audio), sentence], check=True)
    seconds = stopwatch(audio)
    print(voice, "用了", round(seconds, 2), "秒")
    if seconds < fastest_seconds:
        fastest_seconds = seconds
        fastest_voice = voice

print("🏆 冠军是", fastest_voice)
# 🌐 你会看到（大致）：
#     Samantha 用了 2.0 秒
#     Daniel 用了 2.08 秒
#     Bubbles 用了 2.35 秒
#     Zarvox 用了 2.35 秒
#     Whisper 用了 2.55 秒
#     Bad News 用了 6.12 秒
#     🏆 冠军是 Samantha
#
# Bad News 为什么慢那么多？去 lesson_out/lesson22/race/ 双击 Bad News.aiff 听听，它是唱出来的。
# "Bad News" 名字中间有空格也没事：列表一格放一个，上一课 5.1 讲过。

# 🔊 冠军领奖：afplay 是 Mac 自带的"播放器"，用法和 say 一样，列表里写上要播的文件
subprocess.run(["afplay", str(RACE / (fastest_voice + ".aiff"))])
#
# 这段里只有 stopwatch() 是新的。下面把它拆开，看场记是怎么把秒数交给 Python 的。


# ---------- 3.2 拆开秒表（一）：让场记递纸条 ----------

samantha = RACE / "Samantha.aiff"

# 这是请场记量时长的"咒语"。每一格什么意思看下表，不用背，以后复制就行。
probe = ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "csv=p=0", str(samantha)]
#
#     | 这一格                             | 人话                               |
#     |------------------------------------|------------------------------------|
#     | "ffprobe"                          | 叫场记来（装 ffmpeg 时一起装好的） |
#     | "-v", "error"                      | 废话别说，出错才吭声               |
#     | "-show_entries", "format=duration" | 我只要"时长"这一项                 |
#     | "-of", "csv=p=0"                   | 只报数字，别带名字                 |
#     | str(samantha)                      | 量哪个文件                         |

# 不加 capture_output：场记对着屏幕大喊，Python 手里什么也没有
r = subprocess.run(probe)
print("Python 拿到了：", r.stdout)
# 屏幕上先冒出场记喊的：2.003991
# 输出：Python 拿到了： None

# 加上 capture_output=True, text=True：场记把结果写在纸条上，交给 Python
r = subprocess.run(probe, capture_output=True, text=True)
print("纸条内容是：[" + r.stdout + "]")
# 🌐 你会看到（大致）：
#     纸条内容是：[2.003991
#     ]
#
# 那个 ] 跑到了下一行：纸条最后带着一个换行，r.stdout 其实是 "2.003991\n"。
# 两个开关一起写：capture_output=True 是"写纸条"，text=True 是"用文字写"。
# 只写前一个，拿到的是 b'2.003991\n' 这种"字节"，后面用着麻烦。


# ---------- 3.3 拆开秒表（二）：纸条上的字不是数字 ----------

paper = r.stdout.strip()          # strip() 去掉两头的空白和换行，第 8 课学过
print("把 0.4 秒停顿加上去：", paper + "0.4")
# 🌐 你会看到（大致）：把 0.4 秒停顿加上去： 2.0039910.4
#
# 哈？2.0039910.4 是什么鬼。文字 + 文字 = 两段字粘在一起，不是做加法。
# 就像你在纸条"2.88"后面接着写"0.4"，写出来的是"2.880.4"，不是 3.28。

seconds = float(paper)            # float()：把文字读成小数
print("这回再加：", seconds + 0.4)
print("类型变了：", type(paper), "→", type(seconds))
# 🌐 你会看到（大致）：这回再加： 2.403991
# 输出：类型变了： <class 'str'> → <class 'float'>
#
# 现在回头看 stopwatch()，它就三步：念咒语、拿纸条、读成数字。黑盒拆完了。


# ---------- 3.4 文件夹和编号 ----------

# 赛跑时文件名用的是声音名。给剧本配音时，每句话没有名字，用编号。
# 编号要补零：line01、line02……line10。为什么？看文件名排队：
print(sorted(["line2.aiff", "line10.aiff", "line1.aiff"]))
# 输出：['line1.aiff', 'line10.aiff', 'line2.aiff']
#       ↑ line10 插到 line2 前面了！文件名是按一个字一个字比的，"1" 比 "2" 小。

# :02d 的意思：整数，不够两位前面补 0。像座位号 01、02……10
for n in [1, 2, 10]:
    print(f"line{n:02d}.aiff")
# 输出：line01.aiff
# 输出：line02.aiff
# 输出：line10.aiff

# 上一课照抄的 mkdir(parents=True, exist_ok=True)，两个开关是：
#     parents=True    外面的柜子（lesson_out、lesson22）没有，就一起做出来
#     exist_ok=True   抽屉已经有了，就直接用，不报错
# 不写 exist_ok=True，第二次运行就会报 FileExistsError。所以这两个开关一般一起写。


# ---------- 3.5 合起来：猜猜整个剧本要念多久 ----------

MY_GUESS = 8.0                    # ← 运行前先猜：3 句话一共要念几秒？改这个数

VOICES = OUT / "voices"
VOICES.mkdir(parents=True, exist_ok=True)
script = json.loads((HERE / "script_demo.json").read_text(encoding="utf-8"))

total = 0.0
for i, line in enumerate(script["lines"], start=1):
    audio = VOICES / f"line{i:02d}.aiff"
    subprocess.run(["say", "-v", "Samantha", "-o", str(audio), line["en"]], check=True)
    seconds = stopwatch(audio)
    total = total + seconds
    print(f"第 {i} 句 {seconds:.2f} 秒  {line['zh']}")
print(f"总共 {total:.2f} 秒")

miss = total - MY_GUESS
if miss < 0:
    miss = -miss                  # 猜多了也算差距，变成正数
print(f"你猜 {MY_GUESS} 秒，差了 {miss:.2f} 秒")
if miss < 1:
    print("🎯 神预测！你已经能当场记了")
else:
    print("再听几遍配音，培养一下'秒感'")
# 🌐 你会看到（大致）：
#     第 1 句 2.89 秒  9 月 15 日在 10 月 1 日前面吗？
#     第 2 句 2.83 秒  把它们当字符串比，Python 说不是。
#     第 3 句 2.76 秒  先把它们变成日期对象，再比较。
#     总共 8.48 秒
#     你猜 8.0 秒，差了 0.48 秒
#     🎯 神预测！你已经能当场记了
#
# 去 lesson_out/lesson22/voices/ 看看：line01～line03 按顺序排好了。
# 这段有个隐患：stopwatch() 默认场记每次都量得出来。5.1 看看量不出来会怎样。


# ============================================================
# 四、练一练  ★ 这部分你手写，我不代写
# ============================================================

# --- 第 1 题：办你自己的赛跑（5 分钟） ---
# 改 3.1：往 racers 里加两个选手（Junior、Superstar、Trinoids 随便挑），
# 再把 sentence 换成一句绕口令，比如 "She sells seashells by the seashore."
# 做完的样子：排行榜多了两行，冠军可能换人了，最后冠军念的是你的绕口令。
# 卡住了看这里：所有声音名在终端里敲 say -v '?' 能看到，名字要一字不差。
# TODO


# --- 第 2 题：在 audio.py 里写 duration_of(path) ---
# 打开上一课写的 audio.py，加一个函数：
#     duration_of(path)   量一个音频多少秒，返回数字；量不出来返回 None
# 做完的样子：
#     duration_of(一个存在的 .aiff)   → 2.003991 这样的数字
#     duration_of("没有这个文件.aiff") → None，而且程序不报错
# 卡住了看这里：stopwatch() 就是起点。"量不出来"怎么判断？看 5.1 最后那段。
# TODO（写在 audio.py 里）


# --- 第 3 题：在 audio.py 里写 speak_all(lines, folder) ---
#     lines   剧本里的 lines 列表，每项是 {"en": ..., "zh": ...}，用 "en" 配音
#     folder  音频存到哪个文件夹（Path）
# 要求：
#   [ ] folder 不存在就建（3.4）
#   [ ] 文件名是 line01.aiff、line02.aiff……（3.4 的 :02d）
#   [ ] 用上一课的 speak() 配音，用第 2 题的 duration_of() 量时长
#   [ ] 返回列表，每句一个字典：[{"audio": 路径, "seconds": 秒数}, ...]
# 做完的样子：给它 2 句台词，返回一个长度为 2 的列表，打印出来能看到两个路径和两个秒数。
# 卡住了看这里：3.5 的循环几乎就是它。先建一个空列表，每配好一句就 append 一个字典。
# TODO（写在 audio.py 里）


# --- 第 4 题：给整个剧本配音 ---
# 在 audio.py 的 if __name__ == "__main__": 里：
# 读 script_demo.json，调用 speak_all(剧本的 lines, video_out/voices 文件夹)，
# 再打印每句秒数和总时长。
# 做完的样子：和 3.5 打印的差不多，"第 1 句 2.89 秒……总共 8.48 秒"。
# 卡住了看这里：读 JSON 和打印都照 3.5。
#   如果某句 seconds 是 None，加总时会报错，想想怎么跳过它，并打印一句提醒。
# TODO（写在 audio.py 里）


# --- 第 5 题（挑战，可跳过）：卡点配音 ---
# 拍视频常常要"这句话正好卡在几秒"。上一课学过 say 的 -r（语速）。
# 让 Samantha 念 3.1 的 sentence，写个 for 循环，语速从 40 试到 200，每次加 10，
# 每个语速都量一下，自动找出念得最接近 2.5 秒的那个语速。
# 做完的样子：打印每个语速的秒数，最后一行像 "语速 50 时是 2.59 秒，最接近 2.5 秒"。
#   你会发现一件怪事：语速改了好几次，秒数却一动不动，然后突然一跳。
#   这台 Mac 上实测是这样：say 的语速是"分档"的。把你看到的规律写在下面。
# 卡住了看这里：找"最接近"和 3.1 找"最快"是一个套路，只是比的东西换成"离 2.5 秒差多少"，
#   差多少怎么变成正数，看 3.5 的 miss。range 可以写第三个数当步长：range(40, 201, 10)。
# 我发现的规律：
# TODO


# ============================================================
# 五、问 AI
# ============================================================

# ---------- 5.1 找坑：Opus 的场记不检查纸条 ----------
"""
    打开 reading/build_audio.py，第 49～51 行是 Opus 写的量时长函数：

        def dur(path):
            r = subprocess.run(["ffprobe", ..., path], capture_output=True, text=True)
            return float(r.stdout.strip())

    眼熟吗？它和我们的 stopwatch() 一样：拿到纸条就直接 float()，从不看场记有没有量成功。
    平时没事，因为文件都在。可如果配音那一步失败了、文件没生成，会怎样？
"""

missing = VOICES / "line99.aiff"          # 这个文件不存在
try:
    stopwatch(missing)
except ValueError as e:
    print("ValueError:", e)
# 输出：ValueError: could not convert string to float: ''
#
# 不接住的话就是一屏红字，最后一行是这句。
# 人话："我没法把空字符串 '' 变成数字"。它完全没说"文件不存在"，你会一头雾水。

# 为什么？看看场记交回来的东西：
r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                    "-of", "csv=p=0", str(missing)], capture_output=True, text=True)
print("成绩单:", r.returncode)
print("纸条内容是：[" + r.stdout + "]")
print("错误纸条里写着 No such file 吗？", "No such file" in r.stderr)
# 输出：成绩单: 1
# 输出：纸条内容是：[]
# 输出：错误纸条里写着 No such file 吗？ True
#
# 场记其实抱怨了"找不到文件"，可这句被收进了 r.stderr（错误纸条），屏幕上看不到。
# 所以：读纸条之前，先看成绩单；成绩单不是 0，或者纸条是空的，就别 float()。

text = r.stdout.strip()
if r.returncode != 0 or text == "":
    seconds = None
    print(f"⚠ 量不出 {missing.name} 的时长，先检查文件在不在")
else:
    seconds = float(text)
print("seconds =", seconds)
# 输出：⚠ 量不出 line99.aiff 的时长，先检查文件在不在
# 输出：seconds = None
#
# ★ 量不出来就给 None，让调用的人自己决定怎么办（跳过、重配、报错），
#   而不是冒出一个看不懂的 ValueError。第 2 题的 duration_of 就照这个写。

# ---------- 5.2 去问 ----------
"""
【模板】
    这是一段量音频时长的 Python 代码：（贴上 stopwatch）
    如果音频文件不存在，它会报什么错？为什么这个报错让人看不出真正原因？
    告诉我应该检查哪两样东西，不要直接给我改好的代码。

    ↑ 好在哪：先问"会怎样""为什么"，逼 AI 推演出错过程；
      "检查哪两样东西"给了方向，你拿到提示后自己写 duration_of，才是真学会。
      写完再问它："我的 duration_of 还有没有漏掉的情况？"
"""


# ============================================================
# 六、自检
# ============================================================
# [ ] 用剧组的话说：ffprobe 是谁？capture_output=True 像什么？r.stdout 是什么？
# [ ] "2.88" + "0.4" 得到什么？怎样才能得到 3.28？
# [ ] 为什么文件名要写成 line01 而不是 line1？
# [ ] 3.1 里 fastest_seconds 一开始为什么放 999.0？放 0 会怎样？
# [ ] 如果文件不存在，stopwatch() 会报什么错？你的 duration_of 会怎样？


if __name__ == "__main__":
    print("\n" + "=" * 50)
    print("第 22 课「读一读」跑完了。")
    print(f"今天你做到了：办了一场配音演员赛跑，冠军是 {fastest_voice}；还量出了整个剧本多长。")
    print("下一课：拿这些秒数排时间轴，做出像卡拉 OK 一样的字幕。")
