# AGENTS.md

本文件是仓库级操作手册，写给以后在这个仓库工作的 AI 或子代理。它是最高层约定，优先于各子目录里的说明。

## 0. 每次开始先读 `TODOS.md`

任何任务开始前，第一件事是读仓库根目录的 `TODOS.md`，再做别的。

- 它是本地待办清单，已被根 `.gitignore` 忽略，不会提交。别的电脑上的 clone 里可能没有这个文件，没有就跳过。
- 同学和 AI 共用这个文件。做完一项就把 `[ ]` 改成 `[x]`；发现新任务就加到对应分区；完成的项过几天挪到「已完成」并写上日期。
- 「学习任务」分区是同学自己的练习，AI 不代写，只能讲解、指路、review。「课程维护」分区是教练/AI 可以直接动手的。
- 永远不要 `git add` 这个文件。

## 1. 先理解这个仓库

这是一个个人学习仓库，不是单一大项目。它里面同时存在两条性质不同的主线，不要用同一种方式处理。

```text
Study/
├── python/                 Python 学习课程，仓库主线
│   ├── stage1/             第 1 阶段，已完成
│   ├── stage2/             第 2 阶段，已完成到第 13 课，第 14 课按计划跳过
│   ├── stage3/             第 3 阶段，第 15-20 课，当前进度以实际文件为准
│   ├── stage4/             第 4 阶段，第 21-27 课，科普视频机
│   ├── stage5/             第 5 阶段（选做），第 30-35 课，AI 小助理
│   ├── requirements.txt    Python 依赖清单
│   ├── ruff.toml           Ruff 规则与忽略项
│   ├── SUMMARY_TEMPLATE.md 每课学习总结模板
│   └── TEACHING_STYLE.md   讲课规则：写新课前必读
├── calendar-app/           独立全栈日历应用（整个目录仅本地，不进 Git）
│   ├── server/             Express + SQLite 后端
│   ├── src/                React + Vite 前端
│   ├── .env.sample         环境变量模板
│   ├── agent.md            产品设计文档，不是操作指令
│   └── deploy.md           服务器部署说明
├── day1/                   早期复盘文档，属于历史资料
├── TODOS.md                本地待办清单，不提交，每次开始先读
└── README.md               根说明，信息很少，不要把它当成完整背景
```

开始任何任务前，先按需读：

- 改课程材料：`python/README.md`、对应 `python/stageN/README.md`、`python/TEACHING_STYLE.md`。
- 改日历应用：`calendar-app/README.md`、`calendar-app/agent.md`、`calendar-app/deploy.md`。整个目录仅本地开发，已被根 `.gitignore` 忽略。
- 改学习总结或进度元数据：`python/SUMMARY_TEMPLATE.md`、`python/stage3/lessons_seed.json`。

## 2. 两条主线的工作边界

### 2.1 Python 学习课程

这是教学仓库，仓库所有者是学习者。代理在这里的角色是教练和审阅者，不是替写答案的人。

- 用户没有明确要答案时，不要直接替他完成 `练一练` 或 `自检`。优先解释原理、指路、看报错、review 用户已经写完的代码。
- 如果用户主动要求写参考实现或生成新的课程材料，可以写，但要保持现有课程结构。
- 新增课时时，沿用 `stageN/lessonNN_*.py` 命名，保留固定六段结构：为什么重要、先讲人话、读一读、练一练、问 AI、自检。
- 写课必须遵守 `python/TEACHING_STYLE.md`：读者是 14 岁中学生，每课最多 3 个新东西，前 10 分钟能玩出结果，每个新概念用生活对照表类比，不用 lambda 等紧凑写法。
- 课程示例里的“输出”标注应当真实可运行，不要编造输出。
- 新学习记录按 `python/SUMMARY_TEMPLATE.md` 写；当新课时进入历史记录时，同步更新 `python/stage3/lessons_seed.json` 里的 `lessons` 条目。
- 不要根据当前日期随意推断课程进度。以文件、README 和 `lessons_seed.json` 里实际记录为准。

### 2.2 calendar-app 应用

这是本机开发项目，**整个 `calendar-app/` 目录都由根 `.gitignore` 忽略，任何文件都不进入 Git**。可以按正常工程方式在本机修改，但不要创建提交。技术栈：

- 前端：React 19、Vite
- 后端：Express、better-sqlite3
- 认证：JWT、bcryptjs
- AI：火山引擎方舟 API

服务端由 `calendar-app/server/index.cjs` 启动并提供 API 和构建后的静态文件；`calendar-app/server/db.cjs` 负责 SQLite 初始化和迁移。

修改数据库结构时，先在 `db.cjs` 的迁移逻辑里处理兼容，不要只在现有空库上测试。`server/data.db` 是本地数据，不要提交，也不要无备份地删除或覆盖。

## 3. 常用命令

### 3.1 Python

```bash
cd ~/Downloads/Study/python
python3 -m ruff check .
python3 -m ruff check stageN/ --fix   # 只用于安全的格式类修复，逻辑错误不要依赖 --fix
python3 -m pip install -r requirements.txt   # 缺依赖时再装
python3 <对应的 lessonNN_*.py>               # 运行单个课程文件时，注意它声明的相对路径要求
```

Python 学习代码默认直接用系统 `python3`，不需要激活 `python/.venv`。`python/.venv` 和 `python/.ruff_cache` 都是本地产物，已被忽略。

### 3.2 calendar-app

```bash
cd ~/Downloads/Study/calendar-app
npm install
npm run lint
npm run build

# 本地完整运行：构建静态文件并启动后端，默认 http://localhost:8080
npm start

# 或开发模式：Vite 在 5173，代理 /api 到 8080，后端需要另外开一个终端
npm run server
npm run dev
```

健康检查：

```bash
curl -s http://localhost:8080/api/health
```

不配置 `AI_API_KEY` 时，AI 排程功能不可用，但应用仍应能正常启动和登录。不要因为本地没配密钥就删掉或破坏 AI 降级逻辑。

## 4. 密钥、本地文件和 Git 安全

以下文件或目录绝不能提交到 Git，也不要读取真实值写进任何文档里：

- `calendar-app/` 整个目录：仅本机开发，根 `.gitignore` 已忽略，不能用 `git add -f` 强制加入。
- `TODOS.md`：仅本机待办，已忽略。
- `python/.env`、`python/.venv/`、`python/stage3/coach_data/`、`__pycache__/`、`python/.ruff_cache/`。
- 在同学明确表示同步前，`python/stage4/`、`python/stage5/` 也按路径排除，不提交。

`.env.sample` 如果提交，只能放明显占位值，例如 `AI_API_KEY=your-ark-api-key`、`APP_PASSWORD=your-admin-password`、`JWT_SECRET=your-random-secret`。不能放真实密钥或任何看起来可用的默认密码。

新增环境变量时，同时更新对应的本地说明和读取逻辑。Python 课程相关提交范围以 `python/` 内说明为准；`calendar-app/.env.sample` 只用于本机，不进入 Git。

提交前必须做：

```bash
git status --short
git diff --cached --check
git diff --cached --name-only
```

不要盲目使用 `git add -A` 或 `git add .`。确认改动范围后再按路径添加。如果对某文件是否含敏感信息有疑问，先检查差异，不要直接提交。

## 5. 提交约定

- 远程仓库：`git@github.com:RachelTian26/Study.git`，主分支 `main`。
- 提交要小、要围绕单一主题。不要在一次提交里混入 Python 课程、stage4/stage5 和仓库文档；`calendar-app/` 不提交。
- Python 学习记录按课程提交，例如 `lesson15: 类和对象`。
- `calendar-app/` 整个目录不进 Git；不要为它创建提交。
- 文档或仓库级改动单独提交，例如 `docs: add AGENTS.md`。
- 提交后不要未经确认就重写已经推送到远程的历史。

## 6. 完成一次改动前自检

- 我只修改了和任务相关的文件。
- Python 相关改动已经跑过对应文件或至少 `python3 -m ruff check`。
- 本次暂存区没有包含 `calendar-app/`、`python/stage4/`、`python/stage5/` 或任何 `.env`/数据库/真实密钥。
- 没有把 `.env`、数据库、部署脚本、真实密钥写进暂存区。
- 如果有结构、命令、环境变量或工作流变化，顺手更新本文件和相应 README。
