"""
Generate knowledge points for Week 12.
Modules:
- py-crewai (8) - CrewAI: multi-agent collaboration, task orchestration
- py-dify (8) - Dify: workflow engine, plugin system
- py-ragflow (8) - RAGFlow: document parsing, vector retrieval
- ts-nextjs (10) - Next.js: SSR/SSG, App Router, middleware, Server Components
- ts-trpc (8) - tRPC: end-to-end type safety, procedures
- ts-tauri (8) - Tauri: cross-platform desktop, IPC
- ts-shadcn (8) - shadcn/ui: component design, theming
- ts-bun (8) - Bun: runtime, bundler, test runner
- ai-prompt (8) - Prompt Engineering: system prompts, few-shot, chain-of-thought
- ai-architecture (6) - AI-Assisted Architecture: design decisions with AI

Output: web/backend/data/kp_week12.json
"""

import json
from pathlib import Path

ALL_KP = []


def add(week, module, title, explanation, code, game, quiz):
    ALL_KP.append({
        "week": week,
        "module": module,
        "title": title,
        "explanation": explanation,
        "code": code,
        "game": game,
        "quiz": quiz,
    })


def po(instructions, code, options, correct, explanation):
    return {"type": "predict_output", "title": "预测输出", "instructions": instructions,
            "content": {"code": code, "options": options, "correct": correct, "explanation": explanation}}


def fb(instructions, code_lines, bug_line, explanation):
    return {"type": "find_bug", "title": "找Bug", "instructions": instructions,
            "content": {"code_lines": code_lines, "bug_line": bug_line, "explanation": explanation}}


def fl(instructions, code, blanks, explanation):
    return {"type": "fill_blank", "title": "填空题", "instructions": instructions,
            "content": {"code": code, "blanks": blanks, "explanation": explanation}}


def co(instructions, lines, correct_order, explanation):
    return {"type": "code_order", "title": "代码排序", "instructions": instructions,
            "content": {"lines": lines, "correct_order": correct_order, "explanation": explanation}}


def quiz(q, opts, correct, explanation):
    return {"question": q, "options": opts, "correct": correct, "explanation": explanation}


# ============================================================
# WEEK 12: py-crewai (8 points)
# ============================================================

add(12, "py-crewai", "CrewAI 简介",
    "CrewAI 是一个多智能体协作框架。它让多个AI Agent像团队一样分工合作，每个Agent有自己的角色、目标和工具。",
    "from crewai import Agent\n\nresearcher = Agent(\n    role='研究员',\n    goal='收集和分析市场数据',\n    backstory='你是一位资深市场分析师',\n    verbose=True\n)\nprint(researcher.role)",
    po("这段代码输出什么？",
       "from crewai import Agent\n\nresearcher = Agent(\n    role='研究员',\n    goal='收集和分析市场数据',\n    backstory='你是一位资深市场分析师',\n    verbose=True\n)\nprint(researcher.role)",
       ["收集和分析市场数据", "研究员", "你是一位资深市场分析师", "True"],
       1, "researcher.role 获取Agent的角色名称，输出'研究员'。"),
    quiz("CrewAI 中 Agent 的 role 属性表示什么？",
         ["Agent的名字", "Agent在团队中的角色", "Agent的密码", "Agent的版本"],
         1, "role定义Agent在团队中的角色定位，如'研究员'、'写手'等。"))

add(12, "py-crewai", "定义 Task 任务",
    "Task 定义了Agent需要完成的具体工作。每个Task有描述、期望输出和负责的Agent。",
    "from crewai import Task\n\ntask = Task(\n    description='分析竞品的定价策略',\n    expected_output='一份详细的竞品分析报告',\n    agent=researcher\n)\nprint(task.description)",
    fl("填写任务描述",
       "from crewai import Task\n\ntask = Task(\n    ___='分析竞品的定价策略',\n    expected_output='一份详细的竞品分析报告',\n    agent=researcher\n)\nprint(task.description)",
       [{"position": 0, "answer": "description", "options": ["description", "name", "title", "content"]}],
       "Task的description参数描述任务的具体内容。"),
    quiz("Task 中 expected_output 的作用是什么？",
         ["删除任务", "描述期望的输出格式和内容", "创建Agent", "导入模块"],
         1, "expected_output告诉Agent期望什么样的输出结果，引导生成质量。"))

add(12, "py-crewai", "Crew 组建团队",
    "Crew 将多个Agent和Task组织在一起，定义协作流程。agents是团队成员，tasks是工作清单。",
    "from crewai import Crew\n\ncrew = Crew(\n    agents=[researcher, writer],\n    tasks=[research_task, write_task],\n    verbose=True\n)\nresult = crew.kickoff()\nprint(result)",
    co("排列代码到正确顺序",
       ["result = crew.kickoff()", "from crewai import Crew", "    tasks=[research_task, write_task],", "    agents=[researcher, writer],", "crew = Crew(", "    verbose=True", ")"],
       [1, 4, 3, 2, 5, 6, 0],
       "正确顺序：导入Crew -> 创建Crew对象 -> 配置agents和tasks -> 启动执行。"),
    quiz("crew.kickoff() 的作用是什么？",
         ["删除Crew", "启动团队协作执行所有任务", "创建Agent", "停止任务"],
         1, "kickoff()启动Crew，按照定义的流程执行所有任务。"))

add(12, "py-crewai", "Agent 使用工具",
    "Agent可以绑定工具（Tools）来执行具体操作，如搜索网页、读写文件、调用API等。",
    "from crewai import Agent\nfrom crewai_tools import SerperDevTool\n\nsearch_tool = SerperDevTool()\n\nagent = Agent(\n    role='搜索员',\n    goal='搜索最新资讯',\n    tools=[search_tool],\n    verbose=True\n)",
    fb("找出代码中的问题",
       ["from crewai import Agent", "from crewai_tools import SerperDevTool", "", "search_tool = SerperDevTool()", "", "agent = Agent(", "    role='搜索员',", "    goal='搜索最新资讯',", "    verbose=True", ")"],
       5, "Agent缺少tools参数，应该加上 tools=[search_tool]，否则Agent无法使用搜索工具。"),
    quiz("Agent 的 tools 参数有什么作用？",
         ["删除工具", "让Agent拥有执行具体操作的能力", "创建任务", "导出结果"],
         1, "tools给Agent提供实际操作能力，如搜索、文件读写、API调用等。"))

add(12, "py-crewai", "sequential 顺序流程",
    "Crew默认按sequential（顺序）模式执行任务。前一个任务的输出会作为上下文传递给下一个任务。",
    "from crewai import Crew, Process\n\ncrew = Crew(\n    agents=[researcher, writer],\n    tasks=[research_task, write_task],\n    process=Process.sequential,\n    verbose=True\n)\nresult = crew.kickoff()",
    po("research_task 和 write_task 的执行顺序是什么？",
       "from crewai import Crew, Process\n\ncrew = Crew(\n    agents=[researcher, writer],\n    tasks=[research_task, write_task],\n    process=Process.sequential,\n    verbose=True\n)\nresult = crew.kickoff()",
       ["同时执行", "先research_task再write_task", "先write_task再research_task", "随机顺序"],
       1, "sequential模式按tasks列表顺序执行，research_task先执行，结果传递给write_task。"),
    quiz("sequential 流程模式的特点是什么？",
         ["并行执行", "按顺序执行，前一个的输出是后一个的输入", "随机执行", "只执行第一个"],
         1, "sequential按顺序执行，每个任务可以利用前序任务的输出作为上下文。"))

add(12, "py-crewai", "hierarchical 管理流程",
    "hierarchical模式让Crew自动分配一个管理者Agent来协调其他Agent的工作。适合复杂项目。",
    "from crewai import Crew, Process\n\ncrew = Crew(\n    agents=[researcher, writer, reviewer],\n    tasks=[research_task, write_task, review_task],\n    process=Process.hierarchical,\n    manager_llm='gpt-4',\n    verbose=True\n)",
    fl("填写流程模式",
       "from crewai import Crew, Process\n\ncrew = Crew(\n    agents=[researcher, writer, reviewer],\n    tasks=[research_task, write_task, review_task],\n    process=Process.___,\n    manager_llm='gpt-4',\n    verbose=True\n)",
       [{"position": 0, "answer": "hierarchical", "options": ["hierarchical", "sequential", "parallel", "random"]}],
       "hierarchical模式自动创建管理者来协调团队。"),
    quiz("hierarchical 模式中 manager_llm 的作用是什么？",
         ["删除管理者", "指定管理者Agent使用的语言模型", "创建任务", "设置超时"],
         1, "manager_llm指定管理者Agent使用哪个LLM来做决策和协调。"))

add(12, "py-crewai", "Task 的 context 上下文",
    "Task可以通过context参数引用其他任务的输出，实现任务间的数据传递。这比让Agent自己记忆更可靠。",
    "from crewai import Task\n\nsummary_task = Task(\n    description='总结研究结果',\n    expected_output='简洁的摘要',\n    agent=writer,\n    context=[research_task]\n)",
    co("排列代码到正确顺序",
       ["    agent=writer,", "from crewai import Task", "summary_task = Task(", "    context=[research_task]", "    description='总结研究结果',", "    expected_output='简洁的摘要',", ")"],
       [1, 2, 4, 5, 0, 3, 6],
       "正确顺序：导入Task -> 创建Task -> 设置描述 -> 设置输出 -> 指定Agent -> 设置上下文 -> 闭合。"),
    quiz("Task 的 context 参数有什么作用？",
         ["删除任务", "引用其他任务的输出作为输入上下文", "创建Agent", "设置超时"],
         1, "context让当前任务能访问指定任务的输出，实现任务间数据传递。"))

add(12, "py-crewai", "CrewAI 的 memory 记忆",
    "CrewAI支持memory功能，让Agent在多次执行中积累经验。包括短期记忆、长期记忆和实体记忆。",
    "from crewai import Crew\n\ncrew = Crew(\n    agents=[researcher],\n    tasks=[task],\n    memory=True,\n    verbose=True\n)\nresult = crew.kickoff()",
    po("memory=True 的效果是什么？",
       "from crewai import Crew\n\ncrew = Crew(\n    agents=[researcher],\n    tasks=[task],\n    memory=True,\n    verbose=True\n)\nresult = crew.kickoff()",
       ["删除记忆", "Agent在多次执行中积累和利用经验", "禁用记忆", "报错"],
       1, "memory=True启用记忆功能，Agent可以利用之前执行中积累的经验。"),
    quiz("CrewAI 的 memory 包含哪几种？",
         ["只有一种", "短期、长期和实体记忆", "只有短期记忆", "没有记忆"],
         1, "CrewAI的memory包括短期记忆（当前任务）、长期记忆（跨任务）和实体记忆（关键实体）。"))


# ============================================================
# WEEK 12: py-dify (8 points)
# ============================================================

add(12, "py-dify", "Dify 平台简介",
    "Dify是一个开源的LLM应用开发平台。它提供可视化的Workflow编排、RAG引擎、Agent能力，让你不用写代码也能构建AI应用。",
    "import requests\n\nAPI_BASE = 'https://api.dify.ai/v1'\nAPI_KEY = 'app-xxxxxxxx'\n\nheaders = {\n    'Authorization': f'Bearer {API_KEY}',\n    'Content-Type': 'application/json'\n}\nprint('Dify API准备就绪')",
    po("这段代码输出什么？",
       "import requests\n\nAPI_BASE = 'https://api.dify.ai/v1'\nAPI_KEY = 'app-xxxxxxxx'\n\nheaders = {\n    'Authorization': f'Bearer {API_KEY}',\n    'Content-Type': 'application/json'\n}\nprint('Dify API准备就绪')",
       ["报错", "Dify API准备就绪", "API_KEY的值", "headers的内容"],
       1, "代码只是定义变量和打印字符串，输出'Dify API准备就绪'。"),
    quiz("Dify 平台的核心特点是什么？",
         ["只能写代码", "可视化编排LLM应用，降低开发门槛", "只能用于聊天", "需要训练模型"],
         1, "Dify提供可视化Workflow编排、RAG、Agent等功能，降低LLM应用开发门槛。"))

add(12, "py-dify", "调用 Dify Chat API",
    "Dify的Chat API用于对话类应用。发送用户消息，返回AI回复。支持多轮对话（通过conversation_id）。",
    "import requests\n\ndef chat(message, conversation_id=None):\n    url = f'{API_BASE}/chat-messages'\n    payload = {\n        'inputs': {},\n        'query': message,\n        'response_mode': 'blocking',\n        'conversation_id': conversation_id or '',\n        'user': 'user-001'\n    }\n    resp = requests.post(url, json=payload, headers=headers)\n    return resp.json()\n\nresult = chat('你好')\nprint(result['answer'])",
    fl("填写请求方法",
       "import requests\n\nurl = f'{API_BASE}/chat-messages'\npayload = {'query': '你好', 'user': 'user-001'}\nresp = requests.___(url, json=payload, headers=headers)\nprint(resp.json()['answer'])",
       [{"position": 0, "answer": "post", "options": ["post", "get", "put", "delete"]}],
       "Chat API使用POST方法发送消息。"),
    quiz("Dify Chat API 中 conversation_id 的作用是什么？",
         ["删除对话", "维持多轮对话上下文", "设置用户名", "创建应用"],
         1, "conversation_id关联对话历史，实现多轮对话。不传则开始新对话。"))

add(12, "py-dify", "Dify Workflow 工作流",
    "Dify的Workflow是可视化编排的AI工作流。由节点（Node）和连线（Edge）组成，支持条件分支、循环、并行等。",
    "# Dify Workflow 节点类型:\n# 1. Start - 开始节点\n# 2. LLM - 大语言模型节点\n# 3. Knowledge - 知识库检索\n# 4. Code - 代码执行\n# 5. IF/ELSE - 条件分支\n# 6. End - 结束节点\n\n# 通过API触发Workflow\nimport requests\n\nresp = requests.post(\n    f'{API_BASE}/workflows/run',\n    json={'inputs': {'query': '分析报告'}, 'user': 'user-001'},\n    headers=headers\n)\nprint(resp.json()['data']['outputs'])",
    co("排列Workflow节点到正确执行顺序",
       ["LLM - 大语言模型节点", "Start - 开始节点", "End - 结束节点", "Knowledge - 知识库检索", "IF/ELSE - 条件分支"],
       [1, 3, 0, 4, 2],
       "典型顺序：Start -> Knowledge检索 -> LLM处理 -> 条件判断 -> End。"),
    quiz("Dify Workflow 的作用是什么？",
         ["只能聊天", "可视化编排复杂的AI处理流程", "删除数据", "训练模型"],
         1, "Workflow让你用拖拽方式编排多个AI节点，构建复杂的处理流程。"))

add(12, "py-dify", "Dify 知识库（RAG）",
    "Dify内置RAG引擎。上传文档后自动切分、向量化，LLM节点可以通过Knowledge节点检索相关内容。",
    "import requests\n\n# 上传文档到知识库\ndef upload_document(dataset_id, file_path):\n    url = f'{API_BASE}/datasets/{dataset_id}/documents'\n    with open(file_path, 'rb') as f:\n        resp = requests.post(\n            url,\n            headers={'Authorization': f'Bearer {API_KEY}'},\n            files={'file': f},\n            data={'data': '{\"indexing_technique\":\"high_quality\"}'}\n        )\n    return resp.json()",
    fb("找出代码中的问题",
       ["import requests", "", "def upload_document(dataset_id, file_path):", "    url = f'{API_BASE}/datasets/{dataset_id}/documents'", "    with open(file_path, 'rb') as f:", "        resp = requests.get(", "            url,", "            headers={'Authorization': f'Bearer {API_KEY}'},", "            files={'file': f}", "        )", "    return resp.json()"],
       5, "第6行用了requests.get()，但上传文档应该用requests.post()。"),
    quiz("Dify 知识库的 RAG 流程是什么？",
         ["直接删除文档", "文档切分 -> 向量化 -> 检索相关片段 -> 喂给LLM", "只存储不检索", "手动搜索"],
         1, "RAG流程：文档自动切分为chunk，向量化存储，查询时检索相关片段作为LLM上下文。"))

add(12, "py-dify", "Dify Completion API",
    "Completion API用于文本生成类应用（非对话）。输入变量，返回生成的文本。适合文案生成、摘要等场景。",
    "import requests\n\ndef completion(inputs):\n    url = f'{API_BASE}/completion-messages'\n    payload = {\n        'inputs': inputs,\n        'response_mode': 'blocking',\n        'user': 'user-001'\n    }\n    resp = requests.post(url, json=payload, headers=headers)\n    return resp.json()\n\nresult = completion({'topic': '人工智能'})\nprint(result['answer'])",
    po("这段代码的目的是什么？",
       "import requests\n\ndef completion(inputs):\n    url = f'{API_BASE}/completion-messages'\n    payload = {\n        'inputs': inputs,\n        'response_mode': 'blocking',\n        'user': 'user-001'\n    }\n    resp = requests.post(url, json=payload, headers=headers)\n    return resp.json()\n\nresult = completion({'topic': '人工智能'})\nprint(result['answer'])",
       ["进行多轮对话", "根据输入变量生成文本", "上传文档", "删除数据"],
       1, "Completion API根据inputs中的变量生成文本，适合非对话场景。"),
    quiz("Chat API 和 Completion API 的区别是什么？",
         ["没有区别", "Chat用于对话（有上下文），Completion用于文本生成（无对话历史）", "Chat更快", "Completion更便宜"],
         1, "Chat API支持多轮对话，Completion API是一次性文本生成。"))

add(12, "py-dify", "Dify 插件系统",
    "Dify支持自定义插件（Tool Provider），让AI Agent能调用外部工具。插件定义了工具的名称、参数和执行逻辑。",
    "# Dify 自定义工具定义 (OpenAPI Schema)\ntool_schema = {\n    'name': 'weather_query',\n    'description': '查询指定城市的天气',\n    'parameters': {\n        'type': 'object',\n        'properties': {\n            'city': {\n                'type': 'string',\n                'description': '城市名称'\n            }\n        },\n        'required': ['city']\n    }\n}\nprint(tool_schema['name'])",
    fl("填写工具名称",
       "tool_schema = {\n    'name': '___',\n    'description': '查询指定城市的天气',\n    'parameters': {\n        'type': 'object',\n        'properties': {\n            'city': {'type': 'string', 'description': '城市名称'}\n        },\n        'required': ['city']\n    }\n}",
       [{"position": 0, "answer": "weather_query", "options": ["weather_query", "get_weather", "weather", "query"]}],
       "工具的name字段定义工具的标识名称。"),
    quiz("Dify 插件系统的作用是什么？",
         ["删除应用", "让AI Agent能调用外部工具和API", "创建数据库", "训练模型"],
         1, "插件系统让Agent具备调用外部工具的能力，如搜索、查询天气、发邮件等。"))

add(12, "py-dify", "Dify 流式输出",
    "将response_mode设为'streaming'可以获取流式输出，逐token返回结果，提升用户体感速度。",
    "import requests\n\ndef chat_stream(message):\n    url = f'{API_BASE}/chat-messages'\n    payload = {\n        'query': message,\n        'response_mode': 'streaming',\n        'user': 'user-001'\n    }\n    resp = requests.post(url, json=payload, headers=headers, stream=True)\n    for line in resp.iter_lines():\n        if line:\n            print(line.decode(), end='', flush=True)",
    co("排列代码到正确顺序",
       ["    for line in resp.iter_lines():", "def chat_stream(message):", "    resp = requests.post(url, json=payload, headers=headers, stream=True)", "import requests", "    url = f'{API_BASE}/chat-messages'", "            print(line.decode(), end='', flush=True)", "        if line:"],
       [3, 1, 4, 2, 0, 6, 5],
       "正确顺序：导入requests -> 定义函数 -> 构造URL -> POST请求 -> 逐行处理。"),
    quiz("流式输出(streaming)的好处是什么？",
         ["更准确", "用户可以逐token看到结果，体感更快", "更便宜", "更安全"],
         1, "流式输出让用户不用等全部生成完就能看到部分结果，体感速度更快。"))

add(12, "py-dify", "Dify 应用类型",
    "Dify支持多种应用类型：聊天助手、文本生成、Agent、Chatflow。每种类型适合不同的业务场景。",
    "# Dify 应用类型:\n# 1. 聊天助手 - 多轮对话\n# 2. 文本生成 - 一次性生成\n# 3. Agent - 自主使用工具\n# 4. Chatflow - 可视化对话流程\n\n# Agent类型可以自动选择工具\nimport requests\nresult = requests.post(\n    f'{API_BASE}/chat-messages',\n    json={'query': '北京天气怎么样', 'user': 'user-001'},\n    headers=headers\n)\nprint(result.json()['answer'])",
    po("如果应用是Agent类型，处理'北京天气怎么样'时Agent会怎么做？",
       "# Agent类型应用\nresult = requests.post(\n    f'{API_BASE}/chat-messages',\n    json={'query': '北京天气怎么样', 'user': 'user-001'},\n    headers=headers\n)\nprint(result.json()['answer'])",
       ["直接回答不知道", "自动调用天气工具查询后回答", "报错", "要求用户重新输入"],
       1, "Agent类型会自动判断需要调用天气工具，获取数据后再生成回答。"),
    quiz("Dify 的 Chatflow 和普通聊天助手的区别是什么？",
         ["没有区别", "Chatflow可以用可视化编排复杂的对话流程", "Chatflow更快", "聊天助手更灵活"],
         1, "Chatflow让你用可视化方式编排对话的每个步骤和分支逻辑。"))


# ============================================================
# WEEK 12: py-ragflow (8 points)
# ============================================================

add(12, "py-ragflow", "RAGFlow 简介",
    "RAGFlow是一个开源的RAG引擎，专注于文档解析和深度检索。它支持多种文档格式（PDF、Word、Excel等），提供精准的文档问答。",
    "import requests\n\nRAGFLOW_BASE = 'http://localhost:9380'\nAPI_KEY = 'ragflow-xxxxxxxx'\n\nheaders = {\n    'Authorization': f'Bearer {API_KEY}',\n    'Content-Type': 'application/json'\n}\nresp = requests.get(f'{RAGFLOW_BASE}/api/v1/datasets', headers=headers)\nprint(resp.json())",
    po("这段代码的目的是什么？",
       "import requests\n\nRAGFLOW_BASE = 'http://localhost:9380'\nAPI_KEY = 'ragflow-xxxxxxxx'\n\nheaders = {\n    'Authorization': f'Bearer {API_KEY}',\n    'Content-Type': 'application/json'\n}\nresp = requests.get(f'{RAGFLOW_BASE}/api/v1/datasets', headers=headers)\nprint(resp.json())",
       ["上传文档", "获取知识库列表", "删除数据", "创建用户"],
       1, "GET /api/v1/datasets 请求获取所有知识库(dataset)的列表。"),
    quiz("RAGFlow 的核心优势是什么？",
         ["只能处理文本", "深度文档解析和精准检索", "只能用于聊天", "需要训练模型"],
         1, "RAGFlow专注于文档解析质量（表格、图片、公式等）和检索精度。"))

add(12, "py-ragflow", "创建知识库 Dataset",
    "在RAGFlow中，Dataset（知识库）是文档的集合。创建时需要指定嵌入模型和分块方法。",
    "import requests\n\ndef create_dataset(name):\n    url = f'{RAGFLOW_BASE}/api/v1/datasets'\n    payload = {\n        'name': name,\n        'embedding_model': 'BAAI/bge-large-zh-v1.5',\n        'chunk_method': 'naive'\n    }\n    resp = requests.post(url, json=payload, headers=headers)\n    return resp.json()\n\nresult = create_dataset('产品文档库')\nprint(result['data']['name'])",
    fl("填写API方法",
       "import requests\n\nurl = f'{RAGFLOW_BASE}/api/v1/datasets'\npayload = {'name': '产品文档库'}\nresp = requests.___(url, json=payload, headers=headers)\nprint(resp.json()['data']['name'])",
       [{"position": 0, "answer": "post", "options": ["post", "get", "put", "delete"]}],
       "创建资源使用POST方法。"),
    quiz("创建Dataset时 chunk_method 的作用是什么？",
         ["删除文档", "指定文档如何被切分成小块", "设置颜色", "选择语言"],
         1, "chunk_method决定文档的分块策略，影响检索的精度和效率。"))

add(12, "py-ragflow", "上传文档到知识库",
    "RAGFlow支持上传多种格式的文档。上传后会自动解析、切分、向量化。",
    "import requests\n\ndef upload_doc(dataset_id, file_path):\n    url = f'{RAGFLOW_BASE}/api/v1/datasets/{dataset_id}/documents'\n    with open(file_path, 'rb') as f:\n        resp = requests.post(\n            url,\n            headers={'Authorization': f'Bearer {API_KEY}'},\n            files={'file': f}\n        )\n    return resp.json()\n\nresult = upload_doc('ds-001', '产品手册.pdf')\nprint(result)",
    fb("找出代码中的问题",
       ["import requests", "", "def upload_doc(dataset_id, file_path):", "    url = f'{RAGFLOW_BASE}/api/v1/datasets/{dataset_id}/documents'", "    with open(file_path, 'rb') as f:", "        resp = requests.get(", "            url,", "            headers={'Authorization': f'Bearer {API_KEY}'},", "            files={'file': f}", "        )", "    return resp.json()"],
       5, "第6行用了requests.get()，上传文档应该用requests.post()。"),
    quiz("RAGFlow 支持哪些文档格式？",
         ["只有TXT", "PDF、Word、Excel、PPT等多种格式", "只有PDF", "只有Markdown"],
         1, "RAGFlow支持PDF、Word、Excel、PPT、Markdown、TXT等多种文档格式。"))

add(12, "py-ragflow", "检索相关文档片段",
    "RAGFlow的检索API根据查询返回最相关的文档片段。支持多种检索策略：向量检索、全文检索、混合检索。",
    "import requests\n\ndef retrieve(dataset_ids, query):\n    url = f'{RAGFLOW_BASE}/api/v1/retrieval'\n    payload = {\n        'question': query,\n        'dataset_ids': dataset_ids,\n        'top_k': 5\n    }\n    resp = requests.post(url, json=payload, headers=headers)\n    return resp.json()\n\nresults = retrieve(['ds-001'], '产品价格是多少')\nfor chunk in results['data']['chunks']:\n    print(chunk['content'][:50])",
    co("排列代码到正确顺序",
       ["    for chunk in results['data']['chunks']:", "results = retrieve(['ds-001'], '产品价格是多少')", "def retrieve(dataset_ids, query):", "import requests", "    return resp.json()", "    resp = requests.post(url, json=payload, headers=headers)"],
       [3, 2, 5, 4, 1, 0],
       "正确顺序：导入 -> 定义函数 -> 发送请求 -> 返回结果 -> 调用函数 -> 遍历输出。"),
    quiz("top_k 参数的作用是什么？",
         ["删除结果", "返回最相关的前K个文档片段", "设置超时", "选择语言"],
         1, "top_k限制返回的最相关文档片段数量，平衡精度和性能。"))

add(12, "py-ragflow", "RAGFlow 的 chunk 分块",
    "文档上传后被自动切分为chunk（块）。分块质量直接影响检索效果。RAGFlow支持多种分块策略。",
    "# RAGFlow 分块策略:\n# naive - 通用分块\n# book - 书籍专用\n# paper - 论文专用\n# laws - 法律文件\n# qa - 问答对\n# table - 表格专用\n\nimport requests\n\nresp = requests.post(\n    f'{RAGFLOW_BASE}/api/v1/datasets',\n    json={'name': '论文库', 'chunk_method': 'paper'},\n    headers=headers\n)\nprint(resp.json()['data']['chunk_method'])",
    po("这段代码输出什么？",
       "import requests\n\nresp = requests.post(\n    f'{RAGFLOW_BASE}/api/v1/datasets',\n    json={'name': '论文库', 'chunk_method': 'paper'},\n    headers=headers\n)\nprint(resp.json()['data']['chunk_method'])",
       ["论文库", "paper", "naive", "报错"],
       1, "chunk_method被设为'paper'，所以输出'paper'。"),
    quiz("为什么不同文档类型需要不同的分块策略？",
         ["没有区别", "不同文档结构不同，合适的分块策略能提高检索质量", "只是为了好看", "随机选择"],
         1, "论文有摘要、正文结构，表格有行列结构，合适的分块策略保留文档语义完整性。"))

add(12, "py-ragflow", "RAGFlow 对话 API",
    "RAGFlow提供对话API，结合知识库检索和LLM生成回答。支持多轮对话和引用溯源。",
    "import requests\n\ndef chat(dataset_ids, question, session_id=''):\n    url = f'{RAGFLOW_BASE}/api/v1/chats'\n    payload = {\n        'question': question,\n        'dataset_ids': dataset_ids,\n        'stream': False\n    }\n    if session_id:\n        payload['session_id'] = session_id\n    resp = requests.post(url, json=payload, headers=headers)\n    return resp.json()\n\nresult = chat(['ds-001'], '退货政策是什么')\nprint(result['data']['answer'])",
    fl("填写流式参数",
       "import requests\n\npayload = {\n    'question': '退货政策是什么',\n    'dataset_ids': ['ds-001'],\n    '___': False\n}\nresp = requests.post(url, json=payload, headers=headers)",
       [{"position": 0, "answer": "stream", "options": ["stream", "flow", "async", "realtime"]}],
       "stream参数控制是否使用流式输出。"),
    quiz("RAGFlow 对话API的引用溯源是什么？",
         ["删除来源", "回答中标注引用了哪个文档的哪个片段", "创建文档", "翻译文档"],
         1, "引用溯源让答案可追溯，用户能看到AI回答依据的是哪些文档片段。"))

add(12, "py-ragflow", "文档解析质量",
    "RAGFlow的优势在于文档解析质量。它能正确处理PDF中的表格、图片、公式，保留文档结构信息。",
    "# RAGFlow 文档解析特点:\n# 1. 表格识别 - 保留行列结构\n# 2. 图片OCR - 提取图片中的文字\n# 3. 公式识别 - LaTeX格式输出\n# 4. 版面分析 - 理解文档层次\n\nimport requests\n\n# 获取文档解析状态\ndef get_doc_status(dataset_id, doc_id):\n    url = f'{RAGFLOW_BASE}/api/v1/datasets/{dataset_id}/documents/{doc_id}'\n    resp = requests.get(url, headers=headers)\n    doc = resp.json()['data']\n    return doc['run'], doc['chunk_count']",
    fb("找出代码中的问题",
       ["import requests", "", "def get_doc_status(dataset_id, doc_id):", "    url = f'{RAGFLOW_BASE}/api/v1/datasets/{dataset_id}/documents/{doc_id}'", "    resp = requests.post(url, headers=headers)", "    doc = resp.json()['data']", "    return doc['run'], doc['chunk_count']"],
       4, "第5行用了requests.post()，获取文档状态应该是GET请求，改为requests.get()。"),
    quiz("RAGFlow 处理PDF表格的方式是什么？",
         ["忽略表格", "识别表格结构并保留行列关系", "转为纯文本", "截图保存"],
         1, "RAGFlow能识别PDF中的表格，保留行列结构信息，确保检索时表格数据完整。"))

add(12, "py-ragflow", "RAGFlow 与 Dify 集成",
    "RAGFlow可以作为Dify的外部知识库。在Dify中配置RAGFlow的API地址和密钥，就能在Workflow中使用。",
    "# Dify 中配置 RAGFlow 知识库:\n# 1. 在Dify的Knowledge页面选择'连接外部知识库'\n# 2. 填入RAGFlow的API端点\n# 3. 填入API Key\n# 4. 选择要关联的Dataset\n\n# RAGFlow API端点格式:\nRAGFLOW_ENDPOINT = 'http://localhost:9380/api/v1'\n\n# 在Dify Workflow中使用:\n# Knowledge节点 -> 选择RAGFlow知识库 -> 设置top_k\nprint(f'RAGFlow端点: {RAGFLOW_ENDPOINT}')",
    co("排列集成步骤到正确顺序",
       ["填入API Key", "在Dify的Knowledge页面选择'连接外部知识库'", "选择要关联的Dataset", "填入RAGFlow的API端点", "在Workflow中使用Knowledge节点"],
       [1, 3, 0, 2, 4],
       "正确顺序：进入Knowledge -> 填API端点 -> 填API Key -> 选Dataset -> Workflow中使用。"),
    quiz("RAGFlow 和 Dify 集成的好处是什么？",
         ["没有好处", "Dify提供可视化编排，RAGFlow提供精准文档检索", "更慢", "更贵"],
         1, "集成后在Dify的可视化Workflow中使用RAGFlow的高质量文档检索能力。"))


# ============================================================
# WEEK 12: ts-nextjs (10 points)
# ============================================================

add(12, "ts-nextjs", "Next.js 简介",
    "Next.js是React的全栈框架。支持SSR（服务端渲染）、SSG（静态生成）、API路由等，是生产级React应用的首选。",
    "// app/page.tsx\nexport default function HomePage() {\n    return (\n        <main>\n            <h1>欢迎来到Next.js</h1>\n            <p>这是服务端渲染的页面</p>\n        </main>\n    );\n}",
    po("这段代码中页面是在哪里渲染的？",
       "// app/page.tsx\nexport default function HomePage() {\n    return (\n        <main>\n            <h1>欢迎来到Next.js</h1>\n            <p>这是服务端渲染的页面</p>\n        </main>\n    );\n}",
       ["客户端浏览器", "服务端", "两者都有", "编译时"],
       1, "在App Router中，默认组件是Server Component，在服务端渲染。"),
    quiz("Next.js 相比纯React的主要优势是什么？",
         ["更快的编译", "内置SSR、SSG、路由等全栈能力", "更小的包体积", "更好的CSS支持"],
         1, "Next.js提供SSR、SSG、API路由、文件路由等全栈能力，开箱即用。"))

add(12, "ts-nextjs", "App Router 文件路由",
    "App Router使用文件系统定义路由。app目录下的page.tsx就是页面，layout.tsx是布局，loading.tsx是加载状态。",
    "// app/about/page.tsx -> /about\n// app/blog/[id]/page.tsx -> /blog/123\n\n// app/blog/[id]/page.tsx\nexport default function BlogPost({\n    params\n}: {\n    params: { id: string }\n}) {\n    return <h1>文章 {params.id}</h1>;\n}",
    fl("填写动态路由参数",
       "// app/blog/[id]/page.tsx\nexport default function BlogPost({\n    params\n}: {\n    params: { ___: string }\n}) {\n    return <h1>文章 {params.id}</h1>;\n}",
       [{"position": 0, "answer": "id", "options": ["id", "slug", "key", "index"]}],
       "文件名[id]定义了名为id的动态路由参数。"),
    quiz("app/about/page.tsx 对应的URL路径是什么？",
         ["/page", "/about", "/app/about", "/about/page"],
         1, "app目录下的文件夹名直接映射URL路径，about/page.tsx对应/about。"))

add(12, "ts-nextjs", "Server Components 服务端组件",
    "App Router中默认所有组件都是Server Components。它们在服务端渲染，可以直接访问数据库、文件系统等服务端资源。",
    "// app/users/page.tsx (Server Component)\nasync function UsersPage() {\n    const users = await db.query('SELECT * FROM users');\n    return (\n        <ul>\n            {users.map(u => <li key={u.id}>{u.name}</li>)}\n        </ul>\n    );\n}\nexport default UsersPage;",
    po("这段代码中数据库查询在哪里执行？",
       "async function UsersPage() {\n    const users = await db.query('SELECT * FROM users');\n    return (\n        <ul>\n            {users.map(u => <li key={u.id}>{u.name}</li>)}\n        </ul>\n    );\n}\nexport default UsersPage;",
       ["客户端浏览器", "服务端", "CDN", "数据库本身"],
       1, "Server Component在服务端执行，可以直接查询数据库，SQL不会暴露给客户端。"),
    quiz("Server Components 直接访问数据库的好处是什么？",
         ["更快", "减少客户端JS量，敏感逻辑不暴露给浏览器", "更安全", "所有选项都对"],
         1, "Server Component在服务端执行，减少客户端bundle大小，数据库凭证等不会泄露。"))

add(12, "ts-nextjs", "Client Components 客户端组件",
    "需要交互（事件处理、useState、useEffect）的组件必须标记为Client Component。用 'use client' 指令声明。",
    "'use client';\n\nimport { useState } from 'react';\n\nexport default function Counter() {\n    const [count, setCount] = useState(0);\n    return (\n        <div>\n            <p>计数: {count}</p>\n            <button onClick={() => setCount(c => c + 1)}>+1</button>\n        </div>\n    );\n}",
    fb("找出代码中的问题",
       ["import { useState } from 'react';", "", "export default function Counter() {", "    const [count, setCount] = useState(0);", "    return (", "        <div>", "            <p>计数: {count}</p>", "            <button onClick={() => setCount(c => c + 1)}>+1</button>", "        </div>", "    );", "}"],
       0, "第1行缺少'use client'指令。使用useState和onClick需要标记为Client Component。"),
    quiz("什么时候需要使用 'use client' 指令？",
         ["所有组件", "使用了交互功能（useState、事件处理等）的组件", "只有页面组件", "从不需要"],
         1, "'use client'标记组件为客户端组件，需要使用React hooks或浏览器API时必须添加。"))

add(12, "ts-nextjs", "Server Actions 服务端操作",
    "Server Actions是Next.js 14+的特性，让表单直接调用服务端函数，无需手动创建API路由。",
    "// app/actions.ts\n'use server';\n\nexport async function addUser(formData: FormData) {\n    const name = formData.get('name') as string;\n    await db.insert({ name });\n}\n\n// app/page.tsx\nimport { addUser } from './actions';\n\nexport default function Page() {\n    return (\n        <form action={addUser}>\n            <input name=\"name\" />\n            <button type=\"submit\">添加</button>\n        </form>\n    );\n}",
    fl("填写指令",
       "// app/actions.ts\n'___';\n\nexport async function addUser(formData: FormData) {\n    const name = formData.get('name') as string;\n    await db.insert({ name });\n}",
       [{"position": 0, "answer": "use server", "options": ["use server", "use client", "server only", "server action"]}],
       "'use server'指令标记文件中的函数为Server Actions。"),
    quiz("Server Actions 相比传统API路由的优势是什么？",
         ["更快", "无需手动创建API端点，表单直接调用服务端函数", "更安全", "更小"],
         1, "Server Actions简化了表单处理，不需要手动创建和维护API路由。"))

add(12, "ts-nextjs", "SSG 静态站点生成",
    "SSG在构建时生成HTML页面。用generateStaticParams告诉Next.js哪些动态页面需要预生成。",
    "// app/blog/[id]/page.tsx\nexport async function generateStaticParams() {\n    const posts = await fetch('https://api.example.com/posts');\n    const data = await posts.json();\n    return data.map((post: { id: string }) => ({\n        id: post.id\n    }));\n}\n\nexport default async function Post({ params }: { params: { id: string } }) {\n    const res = await fetch(`https://api.example.com/posts/${params.id}`);\n    const post = await res.json();\n    return <h1>{post.title}</h1>;\n}",
    co("排列代码到正确顺序",
       ["    return data.map((post: { id: string }) => ({ id: post.id }));", "export async function generateStaticParams() {", "    const data = await posts.json();", "    const posts = await fetch('https://api.example.com/posts');", "}"],
       [1, 3, 2, 0, 4],
       "正确顺序：定义generateStaticParams -> 获取数据 -> 解析 -> 返回参数列表 -> 闭合。"),
    quiz("SSG 适合什么场景？",
         ["实时数据", "内容不经常变化的页面（如博客）", "用户仪表盘", "聊天应用"],
         1, "SSG在构建时生成静态HTML，适合内容变化不频繁的页面，加载速度极快。"))

add(12, "ts-nextjs", "middleware 中间件",
    "middleware.ts在请求到达页面之前执行。用于认证、重定向、修改请求头等。放在项目根目录。",
    "// middleware.ts\nimport { NextResponse } from 'next/server';\nimport type { NextRequest } from 'next/server';\n\nexport function middleware(request: NextRequest) {\n    const token = request.cookies.get('token');\n    if (!token && request.nextUrl.pathname.startsWith('/dashboard')) {\n        return NextResponse.redirect(new URL('/login', request.url));\n    }\n    return NextResponse.next();\n}\n\nexport const config = {\n    matcher: ['/dashboard/:path*']\n};",
    po("访问/dashboard但没有token时会怎样？",
       "export function middleware(request: NextRequest) {\n    const token = request.cookies.get('token');\n    if (!token && request.nextUrl.pathname.startsWith('/dashboard')) {\n        return NextResponse.redirect(new URL('/login', request.url));\n    }\n    return NextResponse.next();\n}",
       ["正常显示dashboard", "重定向到/login", "报错404", "显示空白页"],
       1, "没有token且访问/dashboard时，中间件重定向到/login页面。"),
    quiz("middleware.ts 应该放在哪里？",
         ["app目录下", "项目根目录", "src目录下", "public目录下"],
         1, "middleware.ts放在项目根目录（与app目录同级），Next.js自动识别。"))

add(12, "ts-nextjs", "数据获取 fetch",
    "Next.js扩展了fetch API，支持自动缓存和去重。在Server Component中直接await fetch获取数据。",
    "// app/posts/page.tsx\nasync function PostsPage() {\n    const res = await fetch('https://api.example.com/posts', {\n        next: { revalidate: 3600 } // 每小时重新验证\n    });\n    const posts = await res.json();\n    return (\n        <ul>\n            {posts.map((p: { id: string; title: string }) => (\n                <li key={p.id}>{p.title}</li>\n            ))}\n        </ul>\n    );\n}\nexport default PostsPage;",
    fl("填写缓存选项",
       "const res = await fetch('https://api.example.com/posts', {\n    next: { ___: 3600 }\n});",
       [{"position": 0, "answer": "revalidate", "options": ["revalidate", "cache", "ttl", "expire"]}],
       "revalidate设置增量静态再生的时间间隔（秒）。"),
    quiz("next: { revalidate: 3600 } 的作用是什么？",
         ["缓存3600次", "每3600秒（1小时）重新验证数据", "延迟3600ms", "删除缓存"],
         1, "revalidate设置ISR（增量静态再生）间隔，页面在指定秒数后重新生成。"))

add(12, "ts-nextjs", "loading 和 error 边界",
    "loading.tsx定义加载状态UI，error.tsx定义错误处理UI。Next.js自动在合适的时机显示它们。",
    "// app/dashboard/loading.tsx\nexport default function Loading() {\n    return <div className=\"spinner\">加载中...</div>;\n}\n\n// app/dashboard/error.tsx\n'use client';\nexport default function Error({\n    error, reset\n}: {\n    error: Error; reset: () => void;\n}) {\n    return (\n        <div>\n            <h2>出错了！</h2>\n            <button onClick={reset}>重试</button>\n        </div>\n    );\n}",
    fb("找出代码中的问题",
       ["// app/dashboard/error.tsx", "", "export default function Error({", "    error, reset", "}: {", "    error: Error; reset: () => void;", "}) {", "    return (", "        <div>", "            <h2>出错了！</h2>", "            <button onClick={reset}>重试</button>", "        </div>", "    );", "}"],
       0, "error.tsx使用了onClick事件处理，需要'use client'指令。第1行应加上'use client'。"),
    quiz("loading.tsx 的作用是什么？",
         ["删除页面", "定义页面加载时显示的UI", "设置超时", "创建错误"],
         1, "loading.tsx在页面数据加载时自动显示，提供加载状态反馈。"))

add(12, "ts-nextjs", "API Routes 路由处理器",
    "在app/api目录下创建route.ts定义API端点。支持GET、POST、PUT、DELETE等HTTP方法。",
    "// app/api/users/route.ts\nimport { NextResponse } from 'next/server';\n\nexport async function GET() {\n    const users = await db.query('SELECT * FROM users');\n    return NextResponse.json(users);\n}\n\nexport async function POST(request: Request) {\n    const body = await request.json();\n    await db.insert(body);\n    return NextResponse.json({ success: true }, { status: 201 });\n}",
    co("排列代码到正确顺序",
       ["export async function POST(request: Request) {", "import { NextResponse } from 'next/server';", "    return NextResponse.json(users);", "export async function GET() {", "    const users = await db.query('SELECT * FROM users');", "}"],
       [1, 3, 4, 2, 5, 0],
       "正确顺序：导入 -> GET函数 -> 查询数据 -> 返回JSON -> 闭合 -> POST函数。"),
    quiz("app/api/users/route.ts 对应的API路径是什么？",
         ["/route", "/api/users", "/users", "/app/api/users"],
         1, "app/api目录下的文件路由映射为/api前缀的API路径。"))


# ============================================================
# WEEK 12: ts-trpc (8 points)
# ============================================================

add(12, "ts-trpc", "tRPC 简介",
    "tRPC让你用TypeScript构建类型安全的API。前后端共享类型定义，修改后端类型前端自动感知，无需代码生成。",
    "// server/router.ts\nimport { initTRPC } from '@trpc/server';\n\nconst t = initTRPC.create();\nconst appRouter = t.router({\n    hello: t.procedure.query(() => {\n        return { message: 'Hello from tRPC!' };\n    }),\n});\n\nexport type AppRouter = typeof appRouter;",
    po("AppRouter 类型包含了什么信息？",
       "const t = initTRPC.create();\nconst appRouter = t.router({\n    hello: t.procedure.query(() => {\n        return { message: 'Hello from tRPC!' };\n    }),\n});\nexport type AppRouter = typeof appRouter;",
       ["只有函数名", "完整的API路由结构和返回类型", "只有返回值", "空对象"],
       1, "typeof appRouter推断出完整的路由结构、输入输出类型，供前端使用。"),
    quiz("tRPC 的核心优势是什么？",
         ["更快的运行速度", "端到端类型安全，无需代码生成", "更小的包体积", "更好的缓存"],
         1, "tRPC让前后端共享TypeScript类型，修改后端前端自动感知，零代码生成。"))

add(12, "ts-trpc", "Procedure 过程定义",
    "tRPC的procedure是API端点。query用于读取数据，mutation用于修改数据。每个procedure可以有输入验证。",
    "import { z } from 'zod';\n\nconst appRouter = t.router({\n    getUserById: t.procedure\n        .input(z.object({ id: z.string() }))\n        .query(({ input }) => {\n            return db.user.findUnique({ where: { id: input.id } });\n        }),\n\n    createUser: t.procedure\n        .input(z.object({ name: z.string(), email: z.string().email() }))\n        .mutation(({ input }) => {\n            return db.user.create({ data: input });\n        }),\n});",
    fl("填写验证库",
       "import { ___ } from 'zod';\n\nconst schema = z.object({ name: z.string() });",
       [{"position": 0, "answer": "z", "options": ["z", "Zod", "schema", "validate"]}],
       "zod库用 z 作为约定的导入名。"),
    quiz("query 和 mutation 的区别是什么？",
         ["没有区别", "query用于读取（GET），mutation用于修改（POST/PUT/DELETE）", "query更快", "mutation更安全"],
         1, "query对应读操作，mutation对应写操作，语义上区分数据的读和写。"))

add(12, "ts-trpc", "客户端调用 tRPC",
    "前端通过tRPC客户端调用后端API。类型自动推断，调用错误的方法或传错参数TypeScript会报错。",
    "// client/trpc.ts\nimport { createTRPCClient, httpBatchLink } from '@trpc/client';\nimport type { AppRouter } from '../server/router';\n\nconst trpc = createTRPCClient<AppRouter>({\n    links: [\n        httpBatchLink({ url: 'http://localhost:3000/api/trpc' }),\n    ],\n});\n\n// 使用\nconst user = await trpc.getUserById.query({ id: '123' });\nconsole.log(user.name);",
    co("排列代码到正确顺序",
       ["const user = await trpc.getUserById.query({ id: '123' });", "import { createTRPCClient, httpBatchLink } from '@trpc/client';", "import type { AppRouter } from '../server/router';", "const trpc = createTRPCClient<AppRouter>({", "console.log(user.name);"],
       [1, 2, 3, 0, 4],
       "正确顺序：导入客户端 -> 导入路由类型 -> 创建客户端 -> 调用API -> 使用结果。"),
    quiz("为什么 trpc.getUserById.query() 能自动获得类型提示？",
         ["手动定义的", "AppRouter类型包含了完整的API结构和返回类型", "IDE插件", "魔法"],
         1, "AppRouter的类型通过import传递给客户端，TypeScript自动推断出所有API的输入输出类型。"))

add(12, "ts-trpc", "输入验证 Zod",
    "tRPC推荐用Zod做输入验证。Zod定义schema，tRPC自动验证请求参数并提供类型推断。",
    "import { z } from 'zod';\n\nconst createPostSchema = z.object({\n    title: z.string().min(1).max(100),\n    content: z.string().min(10),\n    tags: z.array(z.string()).optional(),\n});\n\nconst createPost = t.procedure\n    .input(createPostSchema)\n    .mutation(({ input }) => {\n        // input的类型已经被Zod推断为:\n        // { title: string; content: string; tags?: string[] }\n        return db.post.create({ data: input });\n    });",
    fb("找出代码中的问题",
       ["import { z } from 'zod';", "", "const createPostSchema = z.object({", "    title: z.string().min(1).max(100),", "    content: z.string().min(10),", "    tags: z.string().optional(),", "});"],
       5, "第6行tags应该是数组类型z.array(z.string()).optional()，不是单个字符串。"),
    quiz("Zod 的 .min(1) 和 .max(100) 的作用是什么？",
         ["设置默认值", "限制字符串长度在1到100之间", "设置类型", "删除数据"],
         1, ".min(1)要求至少1个字符，.max(100)要求最多100个字符，输入不满足则验证失败。"))

add(12, "ts-trpc", "tRPC 中间件",
    "中间件可以在procedure执行前后运行，用于认证、日志、错误处理等。用t.middleware定义。",
    "const isAuthed = t.middleware(({ ctx, next }) => {\n    if (!ctx.session?.user) {\n        throw new TRPCError({ code: 'UNAUTHORIZED' });\n    }\n    return next({\n        ctx: { user: ctx.session.user }\n    });\n});\n\nconst protectedProcedure = t.procedure.use(isAuthed);\n\nconst appRouter = t.router({\n    secret: protectedProcedure.query(({ ctx }) => {\n        return `你好, ${ctx.user.name}`;\n    }),\n});",
    fl("填写错误代码",
       "const isAuthed = t.middleware(({ ctx, next }) => {\n    if (!ctx.session?.user) {\n        throw new TRPCError({ code: '___' });\n    }\n    return next({ ctx: { user: ctx.session.user } });\n});",
       [{"position": 0, "answer": "UNAUTHORIZED", "options": ["UNAUTHORIZED", "FORBIDDEN", "NOT_FOUND", "BAD_REQUEST"]}],
       "未认证时应抛出UNAUTHORIZED（401）错误。"),
    quiz("protectedProcedure.use(isAuthed) 的作用是什么？",
         ["删除过程", "给procedure添加认证中间件", "创建新路由", "设置超时"],
         1, ".use(isAuthed)给procedure添加认证中间件，未认证的请求会被拒绝。"))

add(12, "ts-trpc", "tRPC 错误处理",
    "tRPC用TRPCError抛出标准化的错误。前端可以通过error.code和error.message处理不同类型的错误。",
    "import { TRPCError } from '@trpc/server';\n\nconst appRouter = t.router({\n    getUser: t.procedure\n        .input(z.object({ id: z.string() }))\n        .query(async ({ input }) => {\n            const user = await db.user.findUnique({\n                where: { id: input.id }\n            });\n            if (!user) {\n                throw new TRPCError({\n                    code: 'NOT_FOUND',\n                    message: `用户 ${input.id} 不存在`\n                });\n            }\n            return user;\n        }),\n});",
    co("排列代码到正确顺序",
       ["    if (!user) {", "        throw new TRPCError({", "            code: 'NOT_FOUND',", "            message: `用户 ${input.id} 不存在`", "        });", "import { TRPCError } from '@trpc/server';", "    }"],
       [5, 0, 1, 2, 3, 4, 6],
       "正确顺序：导入TRPCError -> 判断用户不存在 -> 抛出错误 -> 设置code和message。"),
    quiz("tRPC 错误的 NOT_FOUND 对应HTTP状态码多少？",
         ["400", "401", "404", "500"],
         2, "NOT_FOUND对应HTTP 404状态码，表示请求的资源不存在。"))

add(12, "ts-trpc", "tRPC 的 Subscription",
    "Subscription用于实时数据推送。基于WebSocket，客户端可以订阅数据变化并实时接收更新。",
    "import { observable } from '@trpc/server/observable';\n\nconst appRouter = t.router({\n    onMessage: t.procedure.subscription(() => {\n        return observable<string>((emit) => {\n            const handler = (msg: string) => emit.next(msg);\n            messageBus.on('newMessage', handler);\n            return () => {\n                messageBus.off('newMessage', handler);\n            };\n        });\n    }),\n});",
    po("当有新消息时客户端会怎样？",
       "const appRouter = t.router({\n    onMessage: t.procedure.subscription(() => {\n        return observable<string>((emit) => {\n            const handler = (msg: string) => emit.next(msg);\n            messageBus.on('newMessage', handler);\n            return () => { messageBus.off('newMessage', handler); };\n        });\n    }),\n});",
       ["什么都不发生", "实时收到新消息", "报错", "需要手动刷新"],
       1, "Subscription基于WebSocket，新消息通过emit.next推送给所有订阅的客户端。"),
    quiz("tRPC Subscription 基于什么技术？",
         ["HTTP轮询", "WebSocket", "Server-Sent Events", "长轮询"],
         1, "Subscription使用WebSocket实现实时双向通信，客户端能实时接收服务端推送。"))

add(12, "ts-trpc", "tRPC 与 Next.js 集成",
    "tRPC可以无缝集成到Next.js。在app/api/trpc/route.ts中创建处理端，在前端创建tRPC客户端。",
    "// server/trpc.ts\nimport { initTRPC } from '@trpc/server';\n\nexport const createTRPCContext = () => ({});\nconst t = initTRPC.context().create();\nexport const router = t.router;\nexport const publicProcedure = t.procedure;\n\n// app/api/trpc/[trpc]/route.ts\nimport { fetchRequestHandler } from '@trpc/server/adapters/fetch';\nimport { appRouter } from '@/server/router';\n\nexport const GET = (req: Request) =>\n    fetchRequestHandler({\n        endpoint: '/api/trpc',\n        req,\n        router: appRouter,\n        createContext: createTRPCContext,\n    });",
    fl("填写适配器名",
       "import { fetchRequestHandler } from '@trpc/server/adapters/___';",
       [{"position": 0, "answer": "fetch", "options": ["fetch", "next", "express", "node"]}],
       "Next.js App Router使用fetch适配器处理tRPC请求。"),
    quiz("tRPC 与 Next.js 集成时 API 路径怎么配置？",
         ["任意路径", "在fetchRequestHandler的endpoint参数中指定，如'/api/trpc'", "自动配置", "在tsconfig中配置"],
         1, "endpoint参数指定tRPC的API前缀路径，客户端需要匹配这个路径。"))


# ============================================================
# WEEK 12: ts-tauri (8 points)
# ============================================================

add(12, "ts-tauri", "Tauri 简介",
    "Tauri是一个用Web技术构建跨平台桌面应用的框架。前端用React/Vue，后端用Rust。比Electron应用更小、更快、更安全。",
    "// 前端代码 (TypeScript)\nasync function greet(name: string) {\n    // 调用Rust后端命令\n    const greeting = await invoke('greet', { name });\n    console.log(greeting);\n}\ngreet('小明');",
    po("invoke('greet', { name }) 做了什么？",
       "async function greet(name: string) {\n    const greeting = await invoke('greet', { name });\n    console.log(greeting);\n}\ngreet('小明');",
       ["调用前端函数", "调用Rust后端的greet命令", "发送HTTP请求", "创建窗口"],
       1, "invoke是Tauri的IPC方法，从前端调用Rust后端定义的命令。"),
    quiz("Tauri 相比 Electron 的主要优势是什么？",
         ["更多功能", "更小的应用体积、更快的启动、更低的内存占用", "更好的UI", "更简单的API"],
         1, "Tauri使用系统WebView而非捆绑浏览器引擎，应用体积小、启动快、内存占用低。"))

add(12, "ts-tauri", "Rust 后端命令",
    "Tauri的后端用Rust编写。用#[tauri::command]宏定义前端可以调用的命令。",
    "// src-tauri/src/main.rs\n#[tauri::command]\nfn greet(name: &str) -> String {\n    format!(\"你好, {}!\", name)\n}\n\nfn main() {\n    tauri::Builder::default()\n        .invoke_handler(tauri::generate_handler![greet])\n        .run(tauri::generate_context!())\n        .expect(\"运行Tauri应用失败\");\n}",
    fl("填写宏名",
       "// src-tauri/src/main.rs\n#[tauri::___]\nfn greet(name: &str) -> String {\n    format!(\"你好, {}!\", name)\n}",
       [{"position": 0, "answer": "command", "options": ["command", "handler", "function", "api"]}],
       "#[tauri::command]宏将Rust函数标记为前端可调用的命令。"),
    quiz("invoke_handler 的作用是什么？",
         ["删除命令", "注册所有前端可调用的Rust命令", "创建窗口", "设置标题"],
         1, "invoke_handler注册命令列表，让前端通过invoke()能调用这些Rust函数。"))

add(12, "ts-tauri", "Tauri IPC 通信",
    "IPC（进程间通信）是前端和Rust后端通信的机制。invoke()发送请求，emit()发送事件。",
    "// 前端调用后端\nimport { invoke } from '@tauri-apps/api/core';\n\nconst result = await invoke<string>('get_config', {\n    key: 'theme'\n});\nconsole.log(result);\n\n// 后端发送事件到前端\n// Rust: app.emit(\"progress\", 75).unwrap();\n\n// 前端监听事件\nimport { listen } from '@tauri-apps/api/event';\nawait listen<number>('progress', (event) => {\n    console.log(`进度: ${event.payload}%`);\n});",
    co("排列通信流程到正确顺序",
       ["前端invoke调用后端命令", "后端处理请求", "后端emit发送事件", "前端listen监听事件", "前端收到事件更新UI"],
       [0, 1, 2, 3, 4],
       "正确顺序：invoke调用 -> 后端处理 -> emit事件 -> listen监听 -> 更新UI。"),
    quiz("invoke 和 emit 的区别是什么？",
         ["没有区别", "invoke是前端调用后端，emit是后端推送事件到前端", "invoke更快", "emit更安全"],
         1, "invoke是请求-响应模式（前端→后端），emit是事件推送模式（后端→前端）。"))

add(12, "ts-tauri", "Tauri 窗口管理",
    "Tauri可以创建和管理多个窗口。每个窗口加载不同的前端页面，支持自定义标题栏。",
    "// 前端创建新窗口\nimport { WebviewWindow } from '@tauri-apps/api/webviewWindow';\n\nconst settingsWindow = new WebviewWindow('settings', {\n    url: '/settings',\n    title: '设置',\n    width: 600,\n    height: 400,\n    resizable: true,\n});\n\nsettingsWindow.once('tauri://created', () => {\n    console.log('设置窗口已创建');\n});",
    po("这段代码创建了什么？",
       "import { WebviewWindow } from '@tauri-apps/api/webviewWindow';\n\nconst settingsWindow = new WebviewWindow('settings', {\n    url: '/settings',\n    title: '设置',\n    width: 600,\n    height: 400,\n});",
       ["删除窗口", "一个600x400的设置窗口", "主窗口", "报错"],
       1, "new WebviewWindow创建新窗口，名为'settings'，加载/settings路由，尺寸600x400。"),
    quiz("WebviewWindow 的 url 参数是什么？",
         ["外部网址", "前端路由路径", "Rust文件路径", "图片地址"],
         1, "url参数指定窗口加载的前端路由路径，对应你的应用中的页面。"))

add(12, "ts-tauri", "Tauri 文件系统",
    "Tauri提供文件系统API，让Web应用安全地读写本地文件。通过权限系统控制可访问的路径。",
    "import { readTextFile, writeTextFile } from '@tauri-apps/plugin-fs';\nimport { appDataDir } from '@tauri-apps/api/path';\n\n// 写入配置文件\nconst configPath = `${await appDataDir()}/config.json`;\nawait writeTextFile(configPath, JSON.stringify({ theme: 'dark' }));\n\n// 读取配置文件\nconst content = await readTextFile(configPath);\nconst config = JSON.parse(content);\nconsole.log(config.theme);",
    fl("填写读取函数名",
       "import { readTextFile, writeTextFile } from '@tauri-apps/plugin-fs';\n\nconst content = await ___(configPath);\nconst config = JSON.parse(content);",
       [{"position": 0, "answer": "readTextFile", "options": ["readTextFile", "readFile", "getText", "loadFile"]}],
       "readTextFile是Tauri的文件系统API，读取文本文件内容。"),
    quiz("Tauri 的文件系统API为什么要通过权限控制？",
         ["为了更慢", "防止Web应用随意访问用户文件系统", "为了更大的包", "没有原因"],
         1, "权限系统确保应用只能访问授权的路径，保护用户数据安全。"))

add(12, "ts-tauri", "Tauri 插件系统",
    "Tauri通过插件扩展功能。常用插件：文件系统(fs)、对话框(dialog)、通知(notification)、剪贴板(clipboard)等。",
    "// 安装插件\n// cargo tauri add fs\n// npm install @tauri-apps/plugin-fs\n\n// src-tauri/capabilities/default.json\n{\n    \"permissions\": [\n        \"fs:default\",\n        \"fs:allow-read-text-file\",\n        \"fs:allow-write-text-file\"\n    ]\n}\n\n// 前端使用\nimport { readTextFile } from '@tauri-apps/plugin-fs';\nconst data = await readTextFile('config.json');",
    fb("找出代码中的问题",
       ["// 前端使用", "import { readTextFile } from '@tauri-apps/plugin-fs';", "const data = await readTextFile('config.json');", "", "// 但是capabilities中没有配置fs权限"],
       2, "第3行使用了readTextFile，但如果没有在capabilities中配置'fs:allow-read-text-file'权限，调用会失败。"),
    quiz("Tauri 插件的权限配置在哪里？",
         ["package.json", "capabilities/default.json", "tsconfig.json", "Cargo.toml"],
         1, "在src-tauri/capabilities/default.json中配置插件的权限列表。"))

add(12, "ts-tauri", "Tauri 自动更新",
    "Tauri内置自动更新功能。配置更新服务器后，应用启动时自动检查新版本并提示用户更新。",
    "// src-tauri/tauri.conf.json\n{\n    \"plugins\": {\n        \"updater\": {\n            \"endpoints\": [\n                \"https://releases.myapp.com/{{target}}/{{arch}}/{{current_version}}\"\n            ]\n        }\n    }\n}\n\n// 前端检查更新\nimport { check } from '@tauri-apps/plugin-updater';\nconst update = await check();\nif (update) {\n    console.log(`发现新版本: ${update.version}`);\n    await update.downloadAndInstall();\n}",
    co("排列更新流程到正确顺序",
       ["await update.downloadAndInstall()", "const update = await check()", "if (update) {", "    console.log(`发现新版本: ${update.version}`)", "}"],
       [1, 2, 3, 0, 4],
       "正确顺序：检查更新 -> 判断有更新 -> 打印版本 -> 下载安装 -> 结束。"),
    quiz("Tauri 自动更新的配置在哪个文件中？",
         ["package.json", "tauri.conf.json", "Cargo.toml", "tsconfig.json"],
         1, "tauri.conf.json是Tauri的主配置文件，updater插件在此配置更新服务器端点。"))

add(12, "ts-tauri", "Tauri 系统托盘",
    "Tauri支持创建系统托盘图标，用户可以从托盘菜单快速操作应用，即使主窗口关闭应用仍在运行。",
    "// src-tauri/src/main.rs\nuse tauri::tray::TrayIconBuilder;\nuse tauri::menu::{Menu, MenuItem};\n\nfn main() {\n    tauri::Builder::default()\n        .setup(|app| {\n            let menu = Menu::with_items(app, &[\n                &MenuItem::with_id(app, \"show\", \"显示窗口\", true, None::<&str>)?,\n                &MenuItem::with_id(app, \"quit\", \"退出\", true, None::<&str>)?,\n            ])?;\n            TrayIconBuilder::new()\n                .icon(app.default_window_icon().unwrap().clone())\n                .menu(&menu)\n                .build()?;\n            Ok(())\n        })\n        .run(tauri::generate_context!())\n        .expect(\"运行失败\");\n}",
    fl("填写托盘构建器名",
       "use tauri::tray::___;\n\nTrayIconBuilder::new()\n    .icon(app.default_window_icon().unwrap().clone())\n    .menu(&menu)\n    .build()?;",
       [{"position": 0, "answer": "TrayIconBuilder", "options": ["TrayIconBuilder", "TrayBuilder", "SystemTray", "IconTray"]}],
       "TrayIconBuilder是Tauri 2.x中创建系统托盘图标的构建器。"),
    quiz("系统托盘的主要用途是什么？",
         ["显示通知", "让用户从系统托盘快速操作应用，主窗口关闭后应用继续运行", "存储数据", "网络通信"],
         1, "系统托盘让应用在后台运行，用户可以通过托盘菜单快速访问功能。"))


# ============================================================
# WEEK 12: ts-shadcn (8 points)
# ============================================================

add(12, "ts-shadcn", "shadcn/ui 简介",
    "shadcn/ui不是传统的组件库，而是一组可复制粘贴的组件代码。组件直接安装到你的项目中，完全可控可定制。",
    "# 安装shadcn/ui\nnpx shadcn@latest init\n\n# 添加单个组件\nnpx shadcn@latest add button\nnpx shadcn@latest add dialog\nnpx shadcn@latest add input\n\n# 组件代码安装在:\n# components/ui/button.tsx\n# components/ui/dialog.tsx\n# components/ui/input.tsx",
    po("npx shadcn@latest add button 会怎样？",
       "# 安装命令\nnpx shadcn@latest add button",
       ["安装npm包", "将button组件源码复制到你的项目中", "创建新项目", "删除组件"],
       1, "shadcn/ui将组件源码直接复制到你的components/ui目录，不是安装npm包。"),
    quiz("shadcn/ui 和传统组件库（如MUI）的核心区别是什么？",
         ["没有区别", "组件代码在你的项目中，完全可控可定制", "shadcn/ui更大", "MUI更灵活"],
         1, "shadcn/ui把组件源码复制到你的项目，你可以自由修改；传统组件库是外部依赖。"))

add(12, "ts-shadcn", "Button 组件",
    "Button是shadcn/ui最基础的组件。支持多种变体（variant）和尺寸（size），通过className自定义样式。",
    "import { Button } from '@/components/ui/button';\n\nexport default function Page() {\n    return (\n        <div className=\"flex gap-4\">\n            <Button variant=\"default\">默认</Button>\n            <Button variant=\"destructive\">危险</Button>\n            <Button variant=\"outline\">轮廓</Button>\n            <Button variant=\"ghost\">幽灵</Button>\n            <Button size=\"sm\">小按钮</Button>\n            <Button size=\"lg\">大按钮</Button>\n        </div>\n    );\n}",
    fl("填写变体名",
       "import { Button } from '@/components/ui/button';\n\n<Button variant=\"___\">危险</Button>",
       [{"position": 0, "answer": "destructive", "options": ["destructive", "danger", "error", "red"]}],
       "destructive是shadcn/ui中表示危险/删除操作的变体名。"),
    quiz("shadcn/ui Button 的 variant 属性有什么作用？",
         ["设置大小", "设置按钮的视觉样式变体", "设置颜色", "设置文字"],
         1, "variant控制按钮的整体视觉风格，如default、destructive、outline、ghost等。"))

add(12, "ts-shadcn", "Dialog 对话框",
    "Dialog是模态对话框组件。由触发器（Trigger）、内容（Content）、标题（Title）等组合而成。",
    "import {\n    Dialog,\n    DialogTrigger,\n    DialogContent,\n    DialogHeader,\n    DialogTitle,\n    DialogDescription,\n} from '@/components/ui/dialog';\nimport { Button } from '@/components/ui/button';\n\nexport function AlertDialog() {\n    return (\n        <Dialog>\n            <DialogTrigger asChild>\n                <Button>打开对话框</Button>\n            </DialogTrigger>\n            <DialogContent>\n                <DialogHeader>\n                    <DialogTitle>确认操作</DialogTitle>\n                    <DialogDescription>确定要删除这条数据吗？</DialogDescription>\n                </DialogHeader>\n            </DialogContent>\n        </Dialog>\n    );\n}",
    co("排列组件到正确嵌套顺序（由外到内）",
       ["DialogTitle", "Dialog", "DialogContent", "DialogTrigger", "DialogHeader"],
       [1, 3, 4, 2, 0],
       "正确嵌套：Dialog -> DialogTrigger -> DialogContent -> DialogHeader -> DialogTitle。"),
    quiz("DialogTrigger 的 asChild 属性有什么作用？",
         ["删除触发器", "让Trigger不生成额外DOM，直接使用子元素作为触发器", "创建子组件", "设置样式"],
         1, "asChild让Trigger不包裹额外的DOM元素，直接把子元素（如Button）作为触发器。"))

add(12, "ts-shadcn", "Input 和 Form 组件",
    "shadcn/ui的Input配合Form组件使用。Form基于react-hook-form和zod，提供表单验证和错误提示。",
    "import { Input } from '@/components/ui/input';\nimport { Label } from '@/components/ui/label';\n\nexport function EmailForm() {\n    return (\n        <div className=\"grid w-full max-w-sm gap-1.5\">\n            <Label htmlFor=\"email\">邮箱</Label>\n            <Input\n                type=\"email\"\n                id=\"email\"\n                placeholder=\"请输入邮箱\"\n            />\n        </div>\n    );\n}",
    fb("找出代码中的问题",
       ["import { Input } from '@/components/ui/input';", "", "export function EmailForm() {", "    return (", "        <div className=\"grid w-full max-w-sm gap-1.5\">", "            <Input type=\"email\" placeholder=\"请输入邮箱\" />", "        </div>", "    );", "}"],
       5, "第6行缺少Label组件。表单输入应该有对应的Label，提供无障碍访问支持。"),
    quiz("shadcn/ui 的 Form 组件基于什么库？",
         ["formik", "react-hook-form + zod", "redux-form", "antd-form"],
         1, "shadcn/ui的Form基于react-hook-form做表单管理，zod做验证。"))

add(12, "ts-shadcn", "theming 主题系统",
    "shadcn/ui用CSS变量实现主题。在globals.css中定义颜色变量，切换主题只需改变量值。",
    "/* globals.css */\n@layer base {\n    :root {\n        --background: 0 0% 100%;\n        --foreground: 222.2 84% 4.9%;\n        --primary: 222.2 47.4% 11.2%;\n        --primary-foreground: 210 40% 98%;\n        --radius: 0.5rem;\n    }\n    .dark {\n        --background: 222.2 84% 4.9%;\n        --foreground: 210 40% 98%;\n        --primary: 210 40% 98%;\n        --primary-foreground: 222.2 47.4% 11.2%;\n    }\n}",
    fl("填写暗色主题class名",
       "/* globals.css */\n:root {\n    --background: 0 0% 100%;\n}\n.___ {\n    --background: 222.2 84% 4.9%;\n}",
       [{"position": 0, "answer": "dark", "options": ["dark", "night", "theme-dark", "black"]}],
       ".dark是Tailwind CSS和shadcn/ui约定的暗色主题class名。"),
    quiz("shadcn/ui 主题切换的原理是什么？",
         ["更换组件", "通过CSS变量切换不同主题的颜色值", "重新加载页面", "使用不同JS"],
         1, "主题通过CSS变量实现，.dark类切换变量值，所有使用变量的组件自动更新。"))

add(12, "ts-shadcn", "Table 数据表格",
    "shadcn/ui的Table组件提供基础表格结构。配合TanStack Table可以实现排序、筛选、分页等高级功能。",
    "import {\n    Table,\n    TableBody,\n    TableCell,\n    TableHead,\n    TableHeader,\n    TableRow,\n} from '@/components/ui/table';\n\nexport function UserTable({ users }: { users: { name: string; email: string }[] }) {\n    return (\n        <Table>\n            <TableHeader>\n                <TableRow>\n                    <TableHead>姓名</TableHead>\n                    <TableHead>邮箱</TableHead>\n                </TableRow>\n            </TableHeader>\n            <TableBody>\n                {users.map(u => (\n                    <TableRow key={u.email}>\n                        <TableCell>{u.name}</TableCell>\n                        <TableCell>{u.email}</TableCell>\n                    </TableRow>\n                ))}\n            </TableBody>\n        </Table>\n    );\n}",
    po("这段代码渲染了几列？",
       "<Table>\n    <TableHeader>\n        <TableRow>\n            <TableHead>姓名</TableHead>\n            <TableHead>邮箱</TableHead>\n        </TableRow>\n    </TableHeader>\n</Table>",
       ["1列", "2列", "3列", "不确定"],
       1, "TableHeader中有两个TableHead（姓名和邮箱），所以是2列。"),
    quiz("shadcn/ui Table 和 TanStack Table 的关系是什么？",
         ["没有关系", "shadcn/ui提供UI结构，TanStack Table提供排序/筛选/分页逻辑", "完全相同", "TanStack替代shadcn"],
         1, "shadcn/ui的Table负责渲染，TanStack Table负责数据逻辑（排序、筛选、分页等）。"))

add(12, "ts-shadcn", "Select 下拉选择",
    "Select组件提供下拉选择功能。支持分组、禁用选项、搜索等。基于Radix UI的Select原语。",
    "import {\n    Select,\n    SelectContent,\n    SelectItem,\n    SelectTrigger,\n    SelectValue,\n} from '@/components/ui/select';\n\nexport function CitySelect() {\n    return (\n        <Select>\n            <SelectTrigger className=\"w-[180px]\">\n                <SelectValue placeholder=\"选择城市\" />\n            </SelectTrigger>\n            <SelectContent>\n                <SelectItem value=\"beijing\">北京</SelectItem>\n                <SelectItem value=\"shanghai\">上海</SelectItem>\n                <SelectItem value=\"guangzhou\">广州</SelectItem>\n            </SelectContent>\n        </Select>\n    );\n}",
    co("排列组件到正确嵌套顺序（由外到内）",
       ["SelectItem", "Select", "SelectContent", "SelectTrigger", "SelectValue"],
       [1, 3, 4, 2, 0],
       "正确嵌套：Select -> SelectTrigger -> SelectValue -> SelectContent -> SelectItem。"),
    quiz("SelectTrigger 的 placeholder 在什么时候显示？",
         ["总是显示", "没有选择值时显示占位文本", "选择后显示", "从不显示"],
         1, "placeholder在SelectValue没有值时显示提示文本，选择后显示选中的值。"))

add(12, "ts-shadcn", "自定义组件样式",
    "shadcn/ui组件完全可控。通过修改组件源码、覆盖CSS变量、或添加className来自定义。",
    "// components/ui/button.tsx（已安装的源码）\nimport { cva, type VariantProps } from 'class-variance-authority';\n\nconst buttonVariants = cva(\n    'inline-flex items-center justify-center rounded-md text-sm font-medium',\n    {\n        variants: {\n            variant: {\n                default: 'bg-primary text-primary-foreground hover:bg-primary/90',\n                destructive: 'bg-destructive text-destructive-foreground',\n                outline: 'border border-input bg-background',\n            },\n            size: {\n                default: 'h-10 px-4 py-2',\n                sm: 'h-9 rounded-md px-3',\n                lg: 'h-11 rounded-md px-8',\n            },\n        },\n        defaultVariants: {\n            variant: 'default',\n            size: 'default',\n        },\n    }\n);",
    fl("填写样式工具库名",
       "import { cva, type VariantProps } from '___';",
       [{"position": 0, "answer": "class-variance-authority", "options": ["class-variance-authority", "tailwind-merge", "clsx", "classnames"]}],
       "class-variance-authority (cva) 是管理组件变体样式的工具库。"),
    quiz("如何给shadcn/ui Button添加一个新变体？",
         ["安装新包", "直接修改button.tsx源码，在variants中添加新变体", "使用CSS覆盖", "不能添加"],
         1, "组件源码在你的项目中，直接在variants对象中添加新的变体即可。"))


# ============================================================
# WEEK 12: ts-bun (8 points)
# ============================================================

add(12, "ts-bun", "Bun 简介",
    "Bun是一个高性能的JavaScript运行时、打包器和包管理器。它用Zig语言编写，目标是替代Node.js，速度提升数倍。",
    "# 运行TypeScript文件（无需编译）\nbun run index.ts\n\n# 安装依赖（比npm快10倍）\nbun install\n\n# 运行测试\nbun test\n\n# 打包\nbun build ./src/index.ts --outdir ./dist",
    po("bun run index.ts 和 node index.ts 的区别是什么？",
       "# Bun可以直接运行TypeScript\nbun run index.ts\n\n# Node需要先编译\ntsc index.ts && node index.js",
       ["没有区别", "Bun可以直接运行TS，不需要编译步骤", "Bun更慢", "Node更安全"],
       1, "Bun内置TypeScript支持，可以直接运行.ts文件，无需tsc编译。"),
    quiz("Bun 的主要优势是什么？",
         ["更多的API", "极快的速度、内置TS支持、一体化工具链", "更好的文档", "更多的包"],
         1, "Bun用Zig编写，启动快、安装快、打包快，内置TS转译和测试。"))

add(12, "ts-bun", "Bun 运行 TypeScript",
    "Bun内置TypeScript转译器，可以直接运行.ts和.tsx文件。支持JSX、装饰器等特性，无需tsconfig配置。",
    "// index.ts\ninterface User {\n    name: string;\n    age: number;\n}\n\nconst user: User = {\n    name: '小明',\n    age: 20\n};\n\nconsole.log(`姓名: ${user.name}, 年龄: ${user.age}`);\n\n// 运行: bun run index.ts\n// 输出: 姓名: 小明, 年龄: 20",
    fl("填写运行命令",
       "# 直接运行TypeScript文件\n___ run index.ts",
       [{"position": 0, "answer": "bun", "options": ["bun", "node", "ts-node", "tsx"]}],
       "bun run可以直接运行TypeScript文件。"),
    quiz("Bun 运行 TypeScript 之前需要 tsc 编译吗？",
         ["需要", "不需要，Bun内置转译", "看情况", "只在生产环境需要"],
         1, "Bun内置TypeScript转译器，运行时自动转译，无需预先编译。"))

add(12, "ts-bun", "Bun 包管理器",
    "bun install 是Bun的包管理器，兼容npm的package.json。安装速度比npm/yarn/pnpm快很多。",
    "# 初始化项目\nbun init\n\n# 安装依赖\nbun install\nbun add express\nbun add -d typescript\n\n# 移除依赖\nbun remove express\n\n# 运行脚本\nbun run dev",
    co("排列命令到正确顺序（初始化到运行）",
       ["bun run dev", "bun add express", "bun init", "bun install", "bun add -d typescript"],
       [2, 3, 1, 4, 0],
       "正确顺序：init初始化 -> install安装 -> add运行依赖 -> add开发依赖 -> run运行。"),
    quiz("bun add -d typescript 中 -d 表示什么？",
         ["删除", "开发依赖（devDependencies）", "目录", "默认"],
         1, "-d表示开发依赖，安装到devDependencies，只在开发时使用。"))

add(12, "ts-bun", "Bun 打包器",
    "Bun内置打包器，替代webpack/esbuild/vite。支持Tree-shaking、代码分割、多入口打包。",
    "// 打包命令\n// bun build ./src/index.ts --outdir ./dist --minify\n\n// build.ts (Bun的构建脚本)\nconst result = await Bun.build({\n    entrypoints: ['./src/index.ts'],\n    outdir: './dist',\n    minify: true,\n    splitting: true,\n    format: 'esm',\n});\n\nconsole.log(`打包完成: ${result.outputs.length} 个文件`);",
    po("打包后的输出格式是什么？",
       "const result = await Bun.build({\n    entrypoints: ['./src/index.ts'],\n    outdir: './dist',\n    format: 'esm',\n});",
       ["CommonJS", "ESM (ES Modules)", "UMD", "AMD"],
       1, "format: 'esm'指定输出为ESM格式。"),
    quiz("Bun 打包器的 splitting 选项有什么作用？",
         ["删除文件", "自动代码分割，共享模块提取为独立chunk", "合并文件", "压缩代码"],
         1, "splitting启用代码分割，多个入口共享的模块会被提取为独立文件，减少重复。"))

add(12, "ts-bun", "Bun 测试运行器",
    "Bun内置测试运行器，兼容Jest API。describe、test、expect直接可用，无需安装jest。",
    "// sum.test.ts\nimport { describe, test, expect } from 'bun:test';\nimport { sum } from './sum';\n\ndescribe('sum函数', () => {\n    test('1 + 2 = 3', () => {\n        expect(sum(1, 2)).toBe(3);\n    });\n\n    test('负数相加', () => {\n        expect(sum(-1, -2)).toBe(-3);\n    });\n});\n\n// 运行: bun test",
    fb("找出代码中的问题",
       ["// sum.test.ts", "import { describe, test, expect } from 'bun:test';", "import { sum } from './sum';", "", "describe('sum函数', () => {", "    test('1 + 2 = 3', () => {", "        expect(sum(1, 2)).toBe(3);", "    });", "});", "", "// 运行: node test"],
       9, "第10行用了node test运行测试，应该用bun test，因为Bun的测试运行器是bun:test。"),
    quiz("Bun 测试运行器的导入来源是什么？",
         ["jest", "bun:test", "vitest", "mocha"],
         1, "从'bun:test'导入describe、test、expect等测试函数。"))

add(12, "ts-bun", "Bun 内置API",
    "Bun提供许多内置API，替代Node.js的核心模块。如Bun.file()替代fs，Bun.serve()替代http.createServer。",
    "// HTTP服务器\nconst server = Bun.serve({\n    port: 3000,\n    fetch(req) {\n        const url = new URL(req.url);\n        if (url.pathname === '/api/hello') {\n            return Response.json({ message: '你好！' });\n        }\n        return new Response('404 Not Found', { status: 404 });\n    },\n});\nconsole.log(`服务器运行在 http://localhost:${server.port}`);",
    fl("填写服务器方法",
       "const server = Bun.___({\n    port: 3000,\n    fetch(req) {\n        return Response.json({ message: '你好！' });\n    },\n});",
       [{"position": 0, "answer": "serve", "options": ["serve", "createServer", "listen", "http"]}],
       "Bun.serve()创建HTTP服务器。"),
    quiz("Bun.serve() 的 fetch 回调接收什么参数？",
         ["Response", "Request对象", "URL字符串", "Buffer"],
         1, "fetch回调接收Request对象（Web标准API），返回Response对象。"))

add(12, "ts-bun", "Bun 文件操作",
    "Bun.file() 和 Bun.write() 提供高效的文件读写。Bun.file()返回BunFile对象，支持流式读取。",
    "// 读取文件\nconst file = Bun.file('data.json');\nconst text = await file.text();\nconst json = await file.json();\nconsole.log(json);\n\n// 写入文件\nawait Bun.write('output.txt', 'Hello Bun!');\n\n// 复制文件\nawait Bun.write(Bun.file('copy.txt'), Bun.file('output.txt'));",
    po("Bun.file('data.json').json() 返回什么？",
       "const file = Bun.file('data.json');\nconst json = await file.json();\nconsole.log(typeof json);",
       ["string", "解析后的JavaScript对象", "Buffer", "BunFile"],
       1, ".json()读取文件内容并解析为JavaScript对象，等价于JSON.parse(await file.text())。"),
    quiz("Bun.file() 返回的是什么？",
         ["文件内容字符串", "BunFile对象（惰性引用）", "Buffer", "Promise"],
         1, "Bun.file()返回BunFile对象，是文件的惰性引用，调用.text()/.json()才读取内容。"))

add(12, "ts-bun", "Bun 兼容性",
    "Bun兼容大部分Node.js API和npm包。支持node_modules、package.json、CommonJS和ESM模块。",
    "// 兼容Node.js API\nimport { readFile } from 'node:fs/promises';\nimport path from 'node:path';\n\nconst content = await readFile('data.txt', 'utf-8');\nconsole.log(path.resolve('data.txt'));\n\n// 使用npm包\nimport express from 'express';\nconst app = express();\napp.get('/', (req, res) => res.send('Hello!'));\napp.listen(3000);",
    co("排列兼容性说明到正确顺序",
       ["支持node:fs等Node.js内置模块", "支持npm包", "支持CommonJS和ESM", "支持package.json"],
       [3, 1, 0, 2],
       "Bun兼容：package.json -> npm包 -> Node.js内置模块 -> CJS和ESM模块。"),
    quiz("Bun 的 node: 前缀导入是什么意思？",
         ["第三方包", "兼容Node.js内置模块的导入方式", "Bun专用模块", "错误写法"],
         1, "node:前缀是Node.js 16+的模块导入方式，Bun兼容这些内置模块。"))


# ============================================================
# WEEK 12: ai-prompt (8 points)
# ============================================================

add(12, "ai-prompt", "System Prompt 系统提示词",
    "System Prompt定义AI的角色、行为规则和输出格式。它是对话的'背景设定'，影响AI整个对话过程的表现。",
    "# System Prompt 示例\nsystem_prompt = \"\"\"你是一位资深的Python编程教师。\n你的学生是初学者。\n请用简单易懂的语言解释概念。\n每个概念都要给出代码示例。\n如果学生犯错，温和地指出并解释原因。\"\"\"\n\n# 调用API\nresponse = client.chat.completions.create(\n    model='gpt-4',\n    messages=[\n        {'role': 'system', 'content': system_prompt},\n        {'role': 'user', 'content': '什么是列表推导式？'}\n    ]\n)",
    po("这个System Prompt会让AI怎样回答？",
       "system_prompt = \"\"\"你是一位资深的Python编程教师。\n你的学生是初学者。\n请用简单易懂的语言解释概念。\"\"\"\n\nresponse = client.chat.completions.create(\n    model='gpt-4',\n    messages=[\n        {'role': 'system', 'content': system_prompt},\n        {'role': 'user', 'content': '什么是列表推导式？'}\n    ]\n)",
       ["用专业术语解释", "用简单语言解释并给代码示例", "拒绝回答", "用英语回答"],
       1, "System Prompt要求用简单语言、给代码示例，AI会按此风格回答。"),
    quiz("System Prompt 对AI回答的影响是什么？",
         ["没有影响", "定义AI的角色和行为方式，影响整个对话过程", "只影响第一句", "只影响代码"],
         1, "System Prompt设置AI的角色和规则，贯穿整个对话，决定回答的风格和质量。"))

add(12, "ai-prompt", "Few-shot 少样本提示",
    "Few-shot是在提示词中给出几个输入-输出示例，让AI学会你期望的格式和风格。示例越多，AI理解越准确。",
    "prompt = \"\"\"将中文翻译成英文，按照以下示例格式：\n\n输入：今天天气很好\n输出：The weather is nice today\n\n输入：我喜欢吃苹果\n输出：I like eating apples\n\n输入：这本书很有意思\n输出：\"\"\"\n\nresponse = client.chat.completions.create(\n    model='gpt-4',\n    messages=[{'role': 'user', 'content': prompt}]\n)",
    fl("填写提示方式",
       "# 给AI几个示例来引导输出格式\n# 这种方式叫做 ___ 提示\n\nprompt = \"\"\"将中文翻译成英文：\n输入：今天天气很好\n输出：The weather is nice today\n\n输入：我喜欢吃苹果\n输出：I like eating apples\n\n输入：这本书很有意思\n输出：\"\"\"",
       [{"position": 0, "answer": "few-shot", "options": ["few-shot", "zero-shot", "one-shot", "chain-of-thought"]}],
       "给几个示例的方式叫few-shot（少样本）提示。"),
    quiz("Few-shot 提示的作用是什么？",
         ["删除数据", "通过示例让AI学会期望的输出格式和风格", "加速推理", "减少token"],
         1, "Few-shot通过几个输入-输出示例，让AI理解你期望的格式、风格和规则。"))

add(12, "ai-prompt", "Chain-of-Thought 思维链",
    "思维链(CoT)让AI在回答前先展示推理过程。通过在提示中加入'让我们一步一步思考'来触发。",
    "prompt = \"\"\"问题：一个商店有15个苹果，卖掉了8个，又进了12个，现在有多少个？\n\n让我们一步一步思考：\n1. 开始有15个苹果\n2. 卖掉8个：15 - 8 = 7个\n3. 又进了12个：7 + 12 = 19个\n4. 答案：19个苹果\"\"\"\n\n# 或者更简单的方式\nprompt = \"\"\"问题：...\n\n请一步一步思考这个问题。\"\"\"",
    co("排列思维链步骤到正确顺序",
       ["得出最终答案", "分析问题条件", "列出计算步骤", "逐步计算", "验证结果"],
       [1, 2, 3, 0, 4],
       "正确顺序：分析条件 -> 列步骤 -> 逐步计算 -> 得出答案 -> 验证。"),
    quiz("Chain-of-Thought 对复杂问题的好处是什么？",
         ["更快回答", "让AI展示推理过程，减少错误，提高准确率", "更短的回答", "更便宜"],
         1, "CoT让AI逐步推理，避免跳步骤导致的错误，显著提高复杂问题的准确率。"))

add(12, "ai-prompt", "结构化输出提示",
    "通过明确指定输出格式（JSON、Markdown表格等），让AI的回答可以直接被程序解析使用。",
    "prompt = \"\"\"分析以下用户评论的情感，以JSON格式输出：\n\n评论：\"这个产品质量很好，物流也快，非常满意！\"\n\n请严格按以下JSON格式回答：\n{\n    \"sentiment\": \"positive/negative/neutral\",\n    \"confidence\": 0.0到1.0,\n    \"keywords\": [\"关键词1\", \"关键词2\"]\n}\"\"\"\n\n# AI输出:\n# {\"sentiment\": \"positive\", \"confidence\": 0.95, \"keywords\": [\"质量好\", \"物流快\"]}",
    fb("找出提示词中的问题",
       ["分析以下用户评论的情感，以JSON格式输出：", "", "评论：\"这个产品质量很好\"", "", "请按以下格式回答：", "sentiment: positive/negative/neutral", "confidence: 0.0到1.0"],
       5, "第6行sentiment没有用JSON格式包裹，应该给完整的JSON示例，否则AI可能输出非JSON格式。"),
    quiz("为什么要在提示词中指定输出格式？",
         ["为了好看", "让AI输出可被程序直接解析，便于后续处理", "减少token", "让AI更快"],
         1, "结构化输出（如JSON）让程序能直接解析AI的回答，用于自动化流程。"))

add(12, "ai-prompt", "Temperature 温度参数",
    "Temperature控制AI回答的随机性。0表示最确定（总是选最可能的词），1表示更有创意和多样性。",
    "# Temperature = 0: 确定性输出\nresponse = client.chat.completions.create(\n    model='gpt-4',\n    temperature=0,\n    messages=[{'role': 'user', 'content': '1+1=?'}]\n)\n# 总是输出: 2\n\n# Temperature = 1: 创意性输出\nresponse = client.chat.completions.create(\n    model='gpt-4',\n    temperature=1,\n    messages=[{'role': 'user', 'content': '写一首关于春天的诗'}]\n)\n# 每次可能不同",
    fl("填写参数名",
       "response = client.chat.completions.create(\n    model='gpt-4',\n    ___=0,\n    messages=[{'role': 'user', 'content': '1+1=?'}]\n)",
       [{"position": 0, "answer": "temperature", "options": ["temperature", "randomness", "creativity", "top_p"]}],
       "temperature参数控制输出的随机性。"),
    quiz("temperature=0 适合什么场景？",
         ["写诗", "需要确定性输出的场景（如代码生成、数学计算）", "头脑风暴", "创意写作"],
         1, "temperature=0适合需要精确、确定性输出的场景，如代码、数学、数据提取。"))

add(12, "ai-prompt", "角色扮演提示",
    "让AI扮演特定角色可以显著提升回答质量。角色设定越具体，AI的回答越符合预期。",
    "prompt = \"\"\"你是一位有20年经验的前端架构师。\n你曾参与过React、Vue等大型开源项目。\n你说话简洁直接，喜欢用代码说话。\n你最讨厌花哨但没用的代码。\n\n问题：React和Vue该怎么选？\"\"\"\n\n# 另一个例子：多重角色\nprompt = \"\"\"你是代码审查员。请从以下角度审查代码：\n1. 安全专家视角：检查安全漏洞\n2. 性能工程师视角：检查性能问题\n3. 可维护性视角：检查代码质量\"\"\"",
    po("第一个提示会让AI从什么角度回答？",
       "prompt = \"\"\"你是一位有20年经验的前端架构师。\n你曾参与过React、Vue等大型开源项目。\n你说话简洁直接，喜欢用代码说话。\n你最讨厌花哨但没用的代码。\n\n问题：React和Vue该怎么选？\"\"\"",
       ["学术研究角度", "资深架构师的实战经验角度", "初学者角度", "产品经理角度"],
       1, "AI会以20年经验的架构师身份回答，简洁直接，用代码示例说话。"),
    quiz("角色扮演提示的好处是什么？",
         ["让回答更长", "让AI从特定专业视角回答，提升专业性和相关性", "减少token", "让AI更慢"],
         1, "角色设定让AI从特定专业视角思考和回答，输出更专业、更符合预期。"))

add(12, "ai-prompt", "Prompt 模板化",
    "将提示词模板化可以提高复用性。用变量占位符构建模板，运行时填充具体值。",
    "def build_review_prompt(code: str, language: str, focus: str) -> str:\n    return f\"\"\"请审查以下{language}代码。\n重点关注：{focus}\n\n代码：\n```{language}\n{code}\n```\n\n请从以下方面给出审查意见：\n1. 代码质量\n2. 潜在问题\n3. 改进建议\n\n以Markdown格式输出。\"\"\"\n\nprompt = build_review_prompt(\n    code='def add(a,b): return a+b',\n    language='Python',\n    focus='类型安全'\n)",
    co("排列模板化步骤到正确顺序",
       ["运行时填充变量", "定义模板函数", "返回完整提示词", "定义占位符"],
       [1, 3, 0, 2],
       "正确顺序：定义模板函数 -> 定义占位符 -> 填充变量 -> 返回完整提示词。"),
    quiz("提示词模板化的好处是什么？",
         ["更短的代码", "提高复用性，同一模板可用于不同输入", "更慢", "更多token"],
         1, "模板化让提示词可以复用，只需替换变量就能处理不同的输入。"))

add(12, "ai-prompt", "提示词迭代优化",
    "好的提示词需要迭代优化。先写初始版本，测试效果，根据问题逐步改进。记录每次修改和效果。",
    "# 提示词迭代记录\nversion_1 = \"帮我写一封邮件\"  # 太笼统\n\nversion_2 = \"帮我写一封求职邮件，申请前端工程师职位\"  # 加了具体场景\n\nversion_3 = \"\"\"帮我写一封求职邮件。\n职位：前端工程师\n公司：字节跳动\n我的优势：3年React经验，熟悉Next.js\n风格：专业但不生硬，突出技术能力\n长度：200字以内\"\"\"  # 加了详细约束\n\n# version_3 效果最好",
    fb("找出提示词中的问题",
       ["# version_3", "帮我写一封求职邮件。", "职位：前端工程师", "公司：字节跳动", "我的优势：3年React经验", "风格：专业但不生硬", "长度：200字以内"],
       0, "第1行的# version_3是注释，但缺少三引号包裹的多行字符串格式，应该用三引号。"),
    quiz("提示词优化的基本方法是什么？",
         ["随便写", "写初始版本 -> 测试 -> 根据问题逐步改进约束和细节", "一次写好", "让AI自己优化"],
         1, "迭代优化：写初版 -> 测试效果 -> 分析问题 -> 加约束/示例 -> 再测试。"))


# ============================================================
# WEEK 12: ai-architecture (6 points)
# ============================================================

add(12, "ai-architecture", "AI 辅助系统设计",
    "用AI帮助做系统架构设计决策。把需求描述给AI，让它分析技术选型、架构模式、潜在风险。但最终决策权在人。",
    "# AI辅助架构决策的提示词模板\nprompt = \"\"\"我需要设计一个系统，请帮我分析：\n\n需求：\n- 支持10万并发用户\n- 需要实时消息推送\n- 数据需要持久化存储\n- 部署在云服务器\n\n请从以下方面分析：\n1. 推荐的技术栈\n2. 架构模式（单体/微服务/Serverless）\n3. 数据库选型\n4. 潜在瓶颈和解决方案\n5. 预估成本\"\"\"",
    po("AI给出的建议可以直接采用吗？",
       "prompt = \"\"\"我需要设计一个系统，请帮我分析：\n\n需求：\n- 支持10万并发用户\n- 需要实时消息推送\n...\n\n请从以下方面分析：\n1. 推荐的技术栈\n2. 架构模式\n3. 数据库选型\n...\"\"\"",
       ["可以直接采用", "作为参考，需要结合实际验证和团队经验做决策", "完全不能用", "看AI心情"],
       1, "AI的建议是参考，需要结合团队技术栈、预算、时间等实际情况做最终决策。"),
    quiz("AI辅助架构设计的正确态度是什么？",
         ["完全依赖AI", "AI提供分析和建议，人做最终决策", "不用AI", "只用AI写代码"],
         1, "AI帮助分析和提供选项，但最终架构决策需要人根据实际情况判断。"))

add(12, "ai-architecture", "用AI做技术选型对比",
    "让AI对比不同技术方案的优劣。提供具体场景和约束条件，AI会给出有依据的分析。",
    "prompt = \"\"\"请对比以下三种方案，我们的场景是电商后台管理系统：\n\n方案A: React + Next.js + PostgreSQL\n方案B: Vue + Nuxt.js + MySQL\n方案C: React + Vite + MongoDB\n\n对比维度：\n1. 开发效率\n2. 性能表现\n3. 生态和社区支持\n4. 学习成本\n5. 长期维护性\n\n请用表格形式输出对比结果。\"\"\"",
    fl("填写对比维度",
       "请对比三种方案，对比维度包括：\n1. 开发效率\n2. 性能表现\n3. 生态和社区支持\n4. ___\n5. 长期维护性",
       [{"position": 0, "answer": "学习成本", "options": ["学习成本", "代码行数", "运行速度", "包大小"]}],
       "学习成本是技术选型的重要维度，影响团队上手速度。"),
    quiz("技术选型对比时为什么要提供具体场景？",
         ["为了更长的回答", "不同场景适合不同技术，通用建议可能不适用", "AI喜欢场景", "没必要"],
         1, "具体场景让AI给出针对性建议，而不是泛泛而谈的优缺点。"))

add(12, "ai-architecture", "用AI审查架构设计",
    "让AI审查你已有的架构设计，发现潜在问题。提供架构图或描述，让AI从不同角度分析。",
    "prompt = \"\"\"请审查以下系统架构设计：\n\n前端：React SPA\n后端：Node.js Express 单体应用\n数据库：SQLite\n部署：单台云服务器\n缓存：无\n消息队列：无\n\n请从以下角度审查：\n1. 可扩展性：能否支持用户增长？\n2. 可靠性：单点故障风险？\n3. 安全性：是否有明显漏洞？\n4. 性能：瓶颈在哪里？\n\n请指出问题并给出改进建议。\"\"\"",
    co("排列审查步骤到正确顺序",
       ["给出改进建议", "描述当前架构", "指出潜在问题", "从多个角度分析"],
       [1, 3, 2, 0],
       "正确顺序：描述架构 -> 多角度分析 -> 指出问题 -> 给出建议。"),
    quiz("AI审查架构的局限性是什么？",
         ["AI什么都知道", "AI不了解你的团队规模、预算、业务约束等实际情况", "AI总能给出完美方案", "没有局限性"],
         1, "AI不了解你的具体约束（团队、预算、时间），建议需要结合实际情况评估。"))

add(12, "ai-architecture", "用AI生成架构文档",
    "让AI帮你生成架构设计文档的初稿。提供技术选型和设计决策，AI会组织成规范的文档格式。",
    "prompt = \"\"\"请帮我生成一份架构设计文档，包含以下内容：\n\n项目名称：在线教育平台\n技术栈：\n- 前端：Next.js + shadcn/ui\n- 后端：Python FastAPI\n- 数据库：PostgreSQL\n- 缓存：Redis\n- 消息队列：RabbitMQ\n\n请生成包含以下章节的文档：\n1. 系统概述\n2. 架构图（用文字描述）\n3. 技术选型说明\n4. 数据库设计\n5. API设计\n6. 部署方案\n7. 风险评估\"\"\"",
    fb("找出提示词中的问题",
       ["请帮我生成一份架构设计文档，包含以下内容：", "", "项目名称：在线教育平台", "技术栈：", "- 前端：Next.js", "- 后端：Python FastAPI", "", "请生成文档：", "1. 系统概述", "2. 架构图"],
       7, "第8行'请生成文档'太笼统，应该明确要求文档格式（如Markdown）、长度限制、输出语言等。"),
    quiz("AI生成的架构文档需要做什么？",
         ["直接使用", "作为初稿，人工审核、补充细节和修正错误", "删除重写", "不需要"],
         1, "AI生成的文档是初稿，需要人工审核准确性、补充业务细节、修正技术错误。"))

add(12, "ai-architecture", "用AI做代码重构分析",
    "让AI分析现有代码，提出重构建议。提供代码片段和上下文，AI会指出代码异味和改进方案。",
    "prompt = \"\"\"请分析以下代码并提出重构建议：\n\n```python\ndef process_order(order):\n    if order['status'] == 'pending':\n        if order['payment'] == 'paid':\n            if order['stock'] > 0:\n                order['status'] = 'confirmed'\n                send_email(order['email'])\n                update_stock(order['item_id'])\n                log_order(order)\n            else:\n                order['status'] = 'out_of_stock'\n        else:\n            order['status'] = 'payment_failed'\n    return order\n```\n\n请指出：\n1. 代码异味（code smell）\n2. 重构方案\n3. 重构后的代码\"\"\"",
    po("这段代码的主要问题是什么？",
       "def process_order(order):\n    if order['status'] == 'pending':\n        if order['payment'] == 'paid':\n            if order['stock'] > 0:\n                order['status'] = 'confirmed'\n                send_email(order['email'])\n                update_stock(order['item_id'])\n                log_order(order)\n            else:\n                order['status'] = 'out_of_stock'\n        else:\n            order['status'] = 'payment_failed'\n    return order",
       ["语法错误", "嵌套过深（箭头反模式），难以阅读和维护", "性能问题", "安全问题"],
       1, "多层if嵌套形成箭头形状，是典型的代码异味，应该用卫语句（early return）重构。"),
    quiz("AI分析代码重构的局限性是什么？",
         ["AI不懂重构", "AI可能不了解代码的业务上下文和历史原因", "AI总是对的", "没有局限性"],
         1, "AI不了解代码背后的业务逻辑和历史决策，重构建议需要开发者结合上下文判断。"))

add(12, "ai-architecture", "AI辅助架构的局限性",
    "AI辅助架构设计有明确的局限性：不了解你的团队、预算、业务约束、历史债务。最终决策必须由人做出。",
    "# AI辅助架构的正确工作流:\n\n# 1. 明确需求和约束\nconstraints = {\n    'team_size': 3,\n    'budget': '10万/年',\n    'deadline': '3个月',\n    'existing_tech': ['React', 'Python'],\n}\n\n# 2. 让AI分析多种方案\n# 3. 结合约束评估AI建议\n# 4. 团队讨论做最终决策\n# 5. 记录决策理由\n\n# 关键原则:\n# AI是顾问，不是决策者\n# 数据驱动，不要盲信AI\n# 迭代优化，不要一步到位",
    fl("填写关键原则",
       "# AI辅助架构的关键原则:\n# AI是___，不是决策者\n# 数据驱动，不要盲信AI\n# 迭代优化，不要一步到位",
       [{"position": 0, "answer": "顾问", "options": ["顾问", "老板", "执行者", "测试员"]}],
       "AI是提供分析和建议的顾问，最终决策权在人。"),
    quiz("AI辅助架构设计中，人的角色是什么？",
         ["执行者", "最终决策者，结合实际情况判断AI建议", "旁观者", "记录员"],
         1, "人是最终决策者，需要结合团队、预算、时间等实际约束来评估和选择AI的建议。"))


# ============================================================
# Write output
# ============================================================

out_path = Path(__file__).parent / "data" / "kp_week12.json"
out_path.parent.mkdir(parents=True, exist_ok=True)
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(ALL_KP, f, ensure_ascii=False, indent=2)

print(f"Generated {len(ALL_KP)} knowledge points")
print(f"Written to: {out_path}")

# Count by week and module
from collections import Counter
week_counts = Counter(kp["week"] for kp in ALL_KP)
module_counts = Counter(kp["module"] for kp in ALL_KP)
game_counts = Counter(kp["game"]["type"] for kp in ALL_KP)

print(f"\nBy week:")
for w in sorted(week_counts):
    print(f"  Week {w}: {week_counts[w]} points")

print(f"\nBy module:")
for m in sorted(module_counts):
    print(f"  {m}: {module_counts[m]} points")

print(f"\nBy game type:")
for t in sorted(game_counts):
    print(f"  {t}: {game_counts[t]} games")
