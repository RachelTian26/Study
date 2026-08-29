# Day 13 学习总结

## 为什么学这个很重要

| 重要点 | 说明 |
| --- | --- |
| 模块是代码复用的基础 | 把常用功能拆出去，再用 `import` 调用，代码会更清晰，也更容易维护。 |
| `import` 是程序之间的连接方式 | 你以后写项目时，不可能所有代码都堆在一个文件里。模块化是必须掌握的能力。 |
| `__name__ == "__main__"` 很关键 | 它是 Python 中最重要的“区分入口”和“可导入模块”的机制。 |
| 虚拟环境解决依赖冲突 | 不同项目可能需要不同版本的库，虚拟环境让每个项目独立运行。 |
| `pip` 是 Python 的包管理器 | 以后安装 `requests`、`fastapi`、`pandas` 等都离不开它。 |
| 这是“工程化思维”的开始 | 学会模块导入和环境管理，才真正开始像写真实项目。 |
| 以后项目都会用到 | `mytools.py` 这种通用工具文件，后面通讯录、待办、日历都会直接复用。 |

## 学习目标与真正学会的内容

| 学习目标 | 真正学会的内容（含例子） |
| --- | --- |
| 会写和使用模块。 | `import textstats` / `import mytools`，把功能拆到另一个文件中。 |
| 会看懂 `__name__`。 | 直接运行文件时 `__name__ == "__main__"`；被导入时它是模块名。 |
| 会区分“运行”和“导入”。 | 直接运行 `python file.py` 时会跑自测；别人 `import` 时不会。 |
| 会写 `if __name__ == "__main__":`。 | 这是模块文件的标准入口保护语句，避免导入时执行测试代码。 |
| 会用 `import x` 和 `from x import y`。 | `import math` 用 `math.sqrt()`；`from math import sqrt` 直接用 `sqrt()`。 |
| 会知道 `from x import *` 不推荐。 | 它会导入很多名字，容易覆盖你自己的变量，代码不清晰。 |
| 会理解 Python 的模块查找路径。 | 当前目录、标准库、安装的第三方包，这些位置会被 Python 依次检查。 |
| 会建立虚拟环境。 | `python3 -m venv .venv`，相当于给项目单独装一个包环境。 |
| 会激活虚拟环境。 | `source .venv/bin/activate`，之后 `python` 和 `pip` 都会走这个环境。 |
| 会安装第三方库。 | `pip install requests`，安装库后才可以 `import requests`。 |
| 会写通用工具模块。 | `mytools.py` 中放 `load_json`、`save_json`、`safe_int` 等常用函数。 |
| 会处理“装了但没找到”的问题。 | 如果 `import requests` 报错，可能是没激活 `.venv`，或者没装成功。 |

## 练习里你能直接回顾的点

| 复习点 |
| --- |
| `import math` 要用 `math.sqrt()`。 |
| `from math import sqrt` 可以直接用 `sqrt()`。 |
| `if __name__ == "__main__":` 只在直接运行时执行。 |
| `textstats.py` 是标准的“模块写法示范”。 |
| `mytools.py` 应该像工具箱一样，收集常见函数。 |
| `load_json()` 和 `save_json()` 是以后项目里最常用的两个函数。 |
| `safe_int()` 让字符串转整数更稳，不会因为脏输入直接崩。 |
| `get_number()` 能反复让用户输入合法数字。 |
| `average()` 和 `grade()` 是统计与评分中常用的函数。 |
| `mask_phone()` 能把手机号中间隐藏，适合隐私保护。 |
| `requests` 是第三方库，装在虚拟环境里，别装到系统 Python。 |
| `pip freeze > requirements.txt` 可以记录项目依赖。 |
| `Path(__file__).parent` 能获取当前文件的目录。 |

## 学习体会

- 今天最重要的收获，不只是“会 import 一个模块”，而是知道了“程序可以拆成多个模块，互相协作”。 |
- `__name__ == "__main__"` 是 Python 中最常见的一个分界点：它让一个文件既能跑程序，又能被别的文件当工具箱使用。 |
- 以前你看到 `import` 可能觉得只是“写法”，今天真正理解了它的意义：把功能分层、组织代码、复用能力。 |
- 虚拟环境的意义很像 `node_modules`：每个项目都有自己的依赖，不会互相污染。 |
- `pip` 不是“装包工具”，而是“项目依赖管理工具”。学会它，后面做任何 Python 项目都更省心。 |
- `mytools.py` 这类文件其实不是“作业”，而是一个真正会长期用的工具库。以后做通讯录、待办、日历时，它都会被复用。 |
- 这一天的重点其实是工程思维：代码不只是能“跑”，还要“可维护、可复用、可扩展”。 |
- 只要一个项目需要处理用户输入、存文件、统计数据、做通用函数，模块化就会发挥作用。 |
- 学会 `venv` 和 `pip` 之后，Python 的开发环境就不是“随便开一个 Python 就行”，而是“为项目准备独立环境”。 |

## 今天实践的代码

### 1. `import` 和 `from ... import ...`
```python
import json
import random

print(random.randint(1, 6))
print(json.dumps({"a": 1}))
```

```python
from pathlib import Path
from datetime import datetime

print(Path.cwd())
print(datetime.now())
```

### 2. `__name__` 的区别
```python
print(__name__)
```

- 直接运行这个文件：`__name__ == "__main__"`
- 被别的文件import：`__name__ == "textstats"` 或其他模块名

### 3. `if __name__ == "__main__":` 的写法
```python
if __name__ == "__main__":
    print("我只在直接运行时才执行")
```

### 4. `textstats.py` 里的标准模块结构
```python
VERSION = "1.0"


def summary(text):
    """返回一句话统计。"""
    return "..."


if __name__ == "__main__":
    print(summary("Python is fun"))
```

### 5. `mytools.py` 的通用工具库思路
```python
def load_json(path, default=None):
    """读取 JSON 文件。文件不存在时返回默认值。"""
    ...


def save_json(data, path):
    """把数据保存成 JSON 文件。"""
    ...


def safe_int(text, default=0):
    """安全转整数。"""
    ...
```

### 6. venv 和 pip 的典型流程
```bash
cd /Users/tian/Downloads/Study/python
python3 -m venv .venv
source .venv/bin/activate
pip install requests
python -c "import requests; print(requests.__version__)"
```

### 7. 请求第三方库时的错误处理方式
```python
try:
    import requests
    print("requests 版本：", requests.__version__)
except ModuleNotFoundError:
    print("还没装 requests，先激活 .venv 再 pip install requests")
```

## 这一天最重要的提醒

- `import` 不是语法炫技，而是让程序分层、复用、扩展。 |
- `if __name__ == "__main__"` 是模块文件的门禁，防止导入时副作用执行。 |
- `venv` 的作用和 `node_modules` 很像：让每个项目有自己的独立依赖。 |
- `pip install` 一定记得在对应 `.venv` 里执行，不然容易装到错误的 Python。 |
- 一个真正写得好的模块，不是“会跑”，而是“以后能拿来直接复用”。 |
- `mytools.py` 就是你第一步进入“工程化编程”的文件，它会一直陪着你走后面的项目。 |

## 一句话总结

Day 13 的核心是：学会把代码拆成模块、用 `__name__` 控制入口、学会用虚拟环境和 `pip` 安装依赖，并把常用函数整理进自己的 `mytools.py`，让程序从“会写脚本”走向“会写工具”。
