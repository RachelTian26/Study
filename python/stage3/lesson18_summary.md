# 第 18 课学习总结：用 Python 调大模型

## 学到了什么

| 学习目标 | 真正学会的内容（举例） |
| --- | --- |
| 把问题交给 AI | 用 `messages` 清单装对话消息。每条消息用花括号 `{}` 写 `role`（谁在说）和 `content`（说什么）；整串消息用方括号 `[]` 装起来。 |
| 取出 AI 的回答 | `chat(messages)` 会发送请求；返回结果不一定成功。用 `response_content(result)` 安全地取回答，结果失败或格式不对时会得到 `None`。 |
| 比较提示词位置 | 同一句要求放在 `system` 或 `user` 中，再比较回答。我的 A 组把 API 比作餐厅服务员，B 组比作点餐窗口；两组都大约两句话，回答都用了生活中的比喻。一次实验只能说明这次看到的结果。 |
| 让对话接着前文聊 | API 不会自动记住上一轮。程序要把之前的 user 消息和 AI 实际回答的 assistant 消息都放回 `messages`，下一轮才能参考它们。 |
| 检查 AI 返回的 JSON | AI 不一定严格照要求返回 JSON。要先尝试解析，再检查结果是不是字典，以及需要的字段是否存在、是不是非空文字。 |
| 看请求是否可靠 | 请求可能超时、连不上或收到错误；需要看错误提示。`temperature` 会影响回答变化程度，但效果由模型决定，不是保证。 |

## 关键代码

### 1. 把问题和要求装进 `messages`

```python
messages = [
    {"role": "system", "content": "用日常生活中的比喻解释，最多两句话。"},
    {"role": "user", "content": "什么是 API？"},
]
```

外层方括号 `[]` 是装消息的清单；里面每个花括号 `{}` 是一条消息。`role` 写是谁说的，`content` 写说的话。

### 2. 安全地取回答

```python
result = chat(messages)
answer = response_content(result)
```

不要直接假设响应里一定有 `choices[0]["message"]["content"]`。使用 `response_content()`；请求失败或响应不完整时，它会返回 `None`，避免因缺少字段而报 `KeyError`。

### 3. 保存聊天上下文

```python
messages.append({"role": "user", "content": question})
result = chat(messages)
answer = response_content(result)

if answer is not None:
    messages.append({"role": "assistant", "content": answer})
```

每轮把用户的问题和 AI 实际回答都留在清单里，后面的请求才带得上聊天历史。

## 踩过的坑

| 报错 / 现象 | 原因 | 怎么改的 |
| --- | --- | --- |
| 刚开始分不清 `[]` 和 `{}` | 它们代表不同的结构：`[]` 装一串消息，`{}` 写一条消息里的字段和值 | 用“方括号装纸条，花括号写纸条内容”来记；再看 `messages = [{"role": ..., "content": ...}]` 这个例子 |
| 直接用 `result["choices"][0]...` 可能出错 | 请求可能失败，或者响应中缺少某些字段 | 使用 `response_content(result)` 安全地取回答 |
| 以为 AI 会自动记住之前说的话 | 单次 API 请求只会看到这次发送的 `messages` | 程序自己保存并带上之前的 user 和 assistant 消息 |
| 以为要求 JSON 后结果一定正确 | AI 可能多说文字、漏字段、返回空内容，或 JSON 不完整 | 尝试解析，并继续检查数据类型和必需字段 |

## 卡在哪（★ 必填，写真话）

- **卡了最久的地方**：一开始不知道 `messages` 外面为什么是方括号、每条消息里面为什么又是花括号。
- **卡了多久**：这次没有记录。
- **最后怎么通的**：用“方括号装一串纸条、花括号写一张纸条内容”的比喻理解后，能分清整串对话和单条消息。
- **现在还是不确定的**：还要继续练习 `role` 和 `content` 分别写什么，以及 `system` 和 `user` 的位置有什么不同。

## 明天要注意

- 不看例子，自己写一遍 `messages`，练习方括号、花括号、`role` 和 `content`。
- 再看一次第 2 题的 A/B 消息，确认自己能指出哪句话放在 `system`、哪句话放在 `user`。
- 运行实验时按屏幕上真正出现的回答记录观察；AI 每次可能说得不一样。

## 一句话总结

第 18 课学会了用 `messages` 把问题交给 AI、从响应里安全地取回答；想让聊天记住前文，就要自己带上历史，而 AI 返回的内容也要检查后才能交给程序使用。
