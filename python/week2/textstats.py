"""
textstats —— 一个"给你读"的示范模块（Day 13 用）

这个文件是我写的，目的是让你看清一个模块长什么样：
    上面是常量和函数（给别人用的）
    下面是 if __name__ == "__main__" 保护的自测代码（只在直接运行这个文件时跑）

Day 13 的练习里，你要照这个样子写自己的 mytools.py。
"""

# 模块级常量，全大写是约定（Python 没有真正的常量，靠约定）
VERSION = "1.0"
STOP_WORDS = {"the", "is", "a", "and", "of", "to", "in", "it", "that"}


def word_list(text, skip_stop_words=False):
    """
    把文本切成小写单词列表，去掉标点。

    skip_stop_words=True 时过滤掉 the / is / a 这类没信息量的词。
    """
    words = []
    for raw in text.lower().split():
        word = "".join(ch for ch in raw if ch.isalpha())      # 只留字母
        if not word:
            continue
        if skip_stop_words and word in STOP_WORDS:
            continue
        words.append(word)
    return words


def count_words(text, skip_stop_words=False):
    """统计词频，返回 {单词: 次数}。"""
    counts = {}
    for word in word_list(text, skip_stop_words):
        counts[word] = counts.get(word, 0) + 1
    return counts


def top_words(text, n=5, skip_stop_words=True):
    """返回出现最多的 n 个词，格式 [(单词, 次数), ...]。"""
    counts = count_words(text, skip_stop_words)
    ranked = sorted(counts.items(), key=lambda kv: kv[1], reverse=True)
    return ranked[:n]


def summary(text):
    """返回一句话统计，字符数 / 单词数 / 不重复单词数。"""
    words = word_list(text)
    return f"{len(text)} 字符，{len(words)} 个单词，{len(set(words))} 个不重复单词"


# ============================================================
# 这一段只在「直接运行 textstats.py」时执行。
# 别的文件 import textstats 的时候，下面这些不会跑。
# ============================================================
if __name__ == "__main__":
    demo = """
    Python is powerful and Python is fast. It plays well with others and
    it runs everywhere. Python is friendly and easy to learn.
    """
    print(f"textstats v{VERSION} 自测")
    print(summary(demo))
    print("词频前 3：", top_words(demo, 3))
    print("不去停用词：", top_words(demo, 3, skip_stop_words=False))
