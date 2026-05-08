"""
Generate knowledge points for Weeks 1-3.
Week 1: 认知升级 (~40 points)
Week 2: Python变量与数据类型 (~40 points)
Week 3: Python数据结构 (~40 points)

Game types rotate evenly: predict_output, find_bug, fill_blank, code_order
"""

import json
from pathlib import Path

ALL_KP = []
GAME_TYPES = ["predict_output", "find_bug", "fill_blank", "code_order"]
_game_idx = 0


def next_game_type():
    global _game_idx
    t = GAME_TYPES[_game_idx % 4]
    _game_idx += 1
    return t


def kp(week, module, title, explanation, code, game, quiz):
    ALL_KP.append({
        "week": week,
        "module": module,
        "title": title,
        "explanation": explanation,
        "code": code,
        "game": game,
        "quiz": quiz,
    })


def quiz(q, opts, correct, expl):
    return {"question": q, "options": opts, "correct": correct, "explanation": expl}


def game_predict_output(code, options, correct, explanation):
    return {
        "type": "predict_output",
        "title": "预测输出",
        "instructions": "阅读代码，预测输出结果",
        "content": {
            "code": code,
            "options": options,
            "correct": correct,
            "explanation": explanation,
        },
    }


def game_find_bug(code_lines, bug_line, explanation):
    return {
        "type": "find_bug",
        "title": "找出Bug",
        "instructions": "以下代码有错误，请找出出错的那一行",
        "content": {
            "code_lines": code_lines,
            "bug_line": bug_line,
            "explanation": explanation,
        },
    }


def game_fill_blank(code, blanks, explanation):
    return {
        "type": "fill_blank",
        "title": "填空补全",
        "instructions": "请将代码中的空白处填写正确内容",
        "content": {
            "code": code,
            "blanks": blanks,
            "explanation": explanation,
        },
    }


def game_code_order(lines, correct_order, explanation):
    return {
        "type": "code_order",
        "title": "代码排序",
        "instructions": "请将以下代码行按正确顺序排列",
        "content": {
            "lines": lines,
            "correct_order": correct_order,
            "explanation": explanation,
        },
    }


# ============================================================
# WEEK 1: 认知升级 (40 points)
# ============================================================
# module: cognitive-why (15 points)
# module: cognitive-thinking (13 points)
# module: cognitive-languages (12 points)

# --- cognitive-why: 15 points ---

kp(1, "cognitive-why", "什么是程序",
   "程序就是给计算机的一组指令。就像菜谱告诉你怎么做菜一样，程序告诉计算机该做什么。你写的每一行代码，都是在和计算机对话。",
   "print('你好世界！')\n# 输出: 你好世界！",
   game_predict_output("print('你好世界！')", ["你好世界！", "你好世界", "报错", "什么都没有"], 0, "print() 会把括号里的内容输出到屏幕上"),
   quiz("程序是什么？", ["一台电脑", "给计算机的一组指令", "一种语言", "一个网站"], 1, "程序就是给计算机的指令，告诉它该做什么。"))

kp(1, "cognitive-why", "输入和输出",
   "程序的工作流程：接收输入 → 处理数据 → 产出输出。就像自动贩卖机：投币（输入），机器处理，掉出饮料（输出）。",
   "name = input('请输入你的名字：')\nprint(f'你好，{name}！')\n# 如果输入 '小明'，输出: 你好，小明！",
   game_predict_output("name = '小明'\nprint(f'你好，{name}！')", ["你好，小明！", "你好，name！", "报错", "你好，None！"], 0, "f-string 中的 {name} 会被变量的值替换"),
   quiz("input() 函数的作用是什么？", ["输出文字到屏幕", "从用户那里获取输入", "计算数学题", "删除数据"], 1, "input() 用于从用户那里获取输入数据。"))

kp(1, "cognitive-why", "什么是变量",
   "变量就像一个有标签的盒子，你可以在里面放东西。给盒子贴上标签（变量名），以后就能通过标签找到里面的东西。",
   "name = '小红'\nage = 20\nprint(name)   # 输出: 小红\nprint(age)    # 输出: 20",
   game_predict_output("x = 10\ny = x\nx = 20\nprint(y)", ["20", "10", "30", "报错"], 1, "y = x 时，y 得到的是 x 当时的值 10。之后 x 改为 20，不影响 y。"),
   quiz("变量的作用是什么？", ["画图", "存储数据以便后续使用", "连接网络", "打印文字"], 1, "变量用来存储数据，方便后续使用和操作。"))

kp(1, "cognitive-why", "什么是算法",
   "算法就是解决问题的步骤。比如查字典：先翻到中间，看比目标大还是小，再决定往前或往后翻。这就是「二分查找」算法。",
   "# 算法示例：找到列表中最大的数\nnumbers = [3, 7, 1, 9, 4]\nbiggest = numbers[0]  # 假设第一个最大\nfor n in numbers:     # 逐个比较\n    if n > biggest:\n        biggest = n\nprint(biggest)  # 输出: 9",
   game_predict_output("numbers = [3, 7, 1, 9, 4]\nresult = max(numbers)\nprint(result)", ["3", "7", "9", "4"], 2, "max() 返回列表中的最大值，即 9。"),
   quiz("算法是什么？", ["一种编程语言", "解决问题的步骤", "一种电脑", "一个软件"], 1, "算法是解决问题的步骤，就像菜谱是做菜的步骤。"))

kp(1, "cognitive-why", "程序的三大结构：顺序",
   "顺序结构：代码从上到下一行一行执行。这是最基本的程序结构。",
   "print('第一步：起床')\nprint('第二步：刷牙')\nprint('第三步：吃早餐')\n# 按顺序输出三行",
   game_predict_output("print('A')\nprint('B')\nprint('C')", ["C B A", "A B C", "A C B", "报错"], 1, "顺序结构：从上到下依次执行，先A再B再C。"),
   quiz("顺序结构是怎样的？", ["随机执行", "从上到下依次执行", "从下到上执行", "跳着执行"], 1, "顺序结构是最基本的：代码从上到下一行一行执行。"))

kp(1, "cognitive-why", "程序的三大结构：条件判断",
   "条件判断让程序能做选择。就像人生路口：如果下雨，带伞；否则，不带。",
   "weather = '下雨'\nif weather == '下雨':\n    print('带伞')\nelse:\n    print('不带伞')\n# 输出: 带伞",
   game_predict_output("score = 85\nif score >= 60:\n    print('及格')\nelse:\n    print('不及格')", ["及格", "不及格", "85", "报错"], 0, "85 >= 60 为 True，所以执行 if 里的代码，输出'及格'。"),
   quiz("if 语句的作用是什么？", ["重复执行代码", "根据条件做选择", "定义变量", "输出文字"], 1, "if 语句根据条件的真假来决定执行哪段代码。"))

kp(1, "cognitive-why", "程序的三大结构：循环",
   "循环让程序能重复做事情。就像每天闹钟响了就要起床，直到周末关掉闹钟。",
   "# 用 for 循环打印 1 到 5\nfor i in range(1, 6):\n    print(i)\n# 输出: 1 2 3 4 5（每行一个）",
   game_predict_output("for i in range(3):\n    print(i)", ["1 2 3", "0 1 2", "0 1 2 3", "报错"], 1, "range(3) 生成 0、1、2，所以输出 0 1 2（每行一个）。"),
   quiz("循环的作用是什么？", ["做选择", "重复执行代码", "存储数据", "输出文字"], 1, "循环让程序能重复执行某段代码，避免手动写重复的内容。"))

kp(1, "cognitive-why", "什么是调试",
   "调试（Debug）就是找错误、修错误的过程。就像医生看病：先观察症状，再诊断病因，最后开药治疗。",
   "# 调试示例\nage = 20\n# 错误写法：\n# print('年龄是' + age)  # 报错！数字不能直接和文字拼接\n# 正确写法：\nprint('年龄是' + str(age))  # 输出: 年龄是20",
   game_find_bug(
       ["age = 20", "print('年龄是' + age)"],
       2, "age 是数字类型，不能直接和字符串用 + 拼接，需要用 str(age) 转换。"
   ),
   quiz("调试的第一步是什么？", ["直接改代码", "观察错误信息", "删掉代码", "重装系统"], 1, "调试第一步是观察错误信息，了解发生了什么问题。"))

kp(1, "cognitive-why", "错误类型：语法错误",
   "语法错误（SyntaxError）是代码不符合 Python 的语法规则。就像写作文时的错别字和病句。",
   "# 语法错误示例（不要运行）\n# print('hello'   # 缺少右括号\n# if True         # 缺少冒号\n#     print('hi')\n\n# 正确写法：\nif True:\n    print('hi')",
   game_find_bug(
       ["print('hello world'", "# 缺少右括号"],
       1, "print() 的括号没有闭合，需要加上右括号 )。"
   ),
   quiz("SyntaxError 是什么错误？", ["逻辑错误", "语法错误（代码不符合规则）", "网络错误", "文件错误"], 1, "SyntaxError 表示代码不符合 Python 的语法规则。"))

kp(1, "cognitive-why", "错误类型：运行时错误",
   "运行时错误（RuntimeError）在代码运行时才出现。比如除以零。",
   "# 运行时错误示例\nx = 10\ny = 0\n# print(x / y)  # ZeroDivisionError!\n\n# 正确做法：先检查\nif y != 0:\n    print(x / y)\nelse:\n    print('不能除以零')",
   game_find_bug(
       ["x = 10", "y = 0", "result = x / y", "print(result)"],
       3, "y 为 0 时不能做除法，会报 ZeroDivisionError。需要先检查 y != 0。"
   ),
   quiz("ZeroDivisionError 是什么错误？", ["语法错误", "除以零的运行时错误", "网络错误", "拼写错误"], 1, "ZeroDivisionError 是运行时错误，当你尝试除以零时会发生。"))

kp(1, "cognitive-why", "错误类型：逻辑错误",
   "逻辑错误不会报错，但结果不对。程序能运行，但不是你想要的结果。这是最难发现的错误。",
   "# 逻辑错误示例：计算平均分\nscores = [80, 90, 100]\n# 错误：忘了加括号\navg = 80 + 90 + 100 / 3  # 先算了 100/3!\nprint(avg)  # 输出: 203.33...\n\n# 正确：\navg = (80 + 90 + 100) / 3\nprint(avg)  # 输出: 90.0",
   game_predict_output("a = 80\nb = 90\nc = 100\nresult = a + b + c / 3\nprint(result)", ["90.0", "203.33...", "170", "报错"], 1, "运算符优先级：c / 3 先执行 = 33.33...，然后 a + b + 33.33... = 203.33...。"),
   quiz("逻辑错误的特点是什么？", ["会报错", "不报错但结果不对", "程序无法运行", "和语法有关"], 1, "逻辑错误不会报错，程序正常运行，但结果不是你想要的。"))

kp(1, "cognitive-why", "读错误信息",
   "Python 的错误信息包含：错误类型、出错位置（文件名和行号）、具体描述。学会读错误信息是编程的基本功。",
   "# 看这个错误信息：\n# Traceback (most recent call last):\n#   File \"test.py\", line 2, in <module>\n#     print(name)\n# NameError: name 'name' is not defined\n\n# 正确做法：先定义变量\nname = '小明'\nprint(name)  # 输出: 小明",
   game_find_bug(
       ["# 第1行：没有任何变量定义", "print(name)", "# 错误: NameError: name 'name' is not defined"],
       2, "name 变量没有被定义就使用了，会报 NameError。需要先给 name 赋值。"
   ),
   quiz("NameError 通常是什么原因？", ["拼写错误", "使用了未定义的变量", "除以零", "括号不匹配"], 1, "NameError 表示使用了一个还没有定义的变量名。"))

kp(1, "cognitive-why", "注释的作用",
   "注释是写给人看的，Python 会忽略它们。用 # 开头的就是注释。好的注释能帮助你和他人理解代码。",
   "# 这是一条注释\nname = '小明'  # 这也是注释\n\n# 计算年龄\nbirth_year = 2000\nage = 2024 - birth_year  # 今年减去出生年\nprint(age)",
   game_predict_output("x = 5  # 这是注释\nprint(x)", ["5  # 这是注释", "5", "报错", "什么都没有"], 1, "注释不会被执行，print(x) 只输出变量 x 的值 5。"),
   quiz("Python 中 # 的作用是什么？", ["定义变量", "写注释（Python 会忽略）", "输出文字", "循环"], 1, "# 后面的内容是注释，Python 不会执行它，是写给人看的。"))

kp(1, "cognitive-why", "什么是函数",
   "函数就是把一段代码打包起来，取个名字，需要的时候调用它。就像微波炉：把食物放进去（输入），按按钮（调用），拿出热好的食物（输出）。",
   "def greet(name):\n    return f'你好，{name}！'\n\nprint(greet('小明'))  # 输出: 你好，小明！\nprint(greet('小红'))  # 输出: 你好，小红！",
   game_predict_output("def add(a, b):\n    return a + b\n\nresult = add(3, 5)\nprint(result)", ["35", "8", "a + b", "报错"], 1, "add(3, 5) 返回 3 + 5 = 8，所以输出 8。"),
   quiz("函数的主要好处是什么？", ["让代码更长", "代码可以复用，避免重复", "让程序变慢", "只能用一次"], 1, "函数可以把代码打包复用，避免重复写同样的代码。"))

kp(1, "cognitive-why", "什么是库和模块",
   "库（Library）是别人写好的代码集合，你直接拿来用就行。就像工具箱：不用自己造锤子，直接用现成的。",
   "import random  # 导入随机数库\n\nnumber = random.randint(1, 6)  # 掷骰子\nprint(f'你掷出了 {number} 点')",
   game_predict_output("import math\nprint(math.sqrt(16))", ["4.0", "16", "256", "报错"], 0, "math.sqrt(16) 计算 16 的平方根，结果是 4.0。"),
   quiz("import 语句的作用是什么？", ["定义函数", "导入别人写好的代码库", "输出文字", "删除文件"], 1, "import 用来导入库，让你使用别人已经写好的功能。"))

kp(1, "cognitive-why", "编程的本质",
   "编程的本质不是写代码，而是解决问题。代码只是工具，思路才是关键。先想清楚怎么解决，再写代码。",
   "# 问题：判断一个数是奇数还是偶数\n# 思路：能被2整除就是偶数\nnumber = 7\nif number % 2 == 0:\n    print('偶数')\nelse:\n    print('奇数')  # 输出: 奇数",
   game_predict_output("number = 10\nif number % 2 == 0:\n    print('偶数')\nelse:\n    print('奇数')", ["奇数", "偶数", "10", "报错"], 1, "10 % 2 == 0 为 True，所以输出'偶数'。"),
   quiz("编程的本质是什么？", ["写很多代码", "解决问题", "背语法", "用最新技术"], 1, "编程的本质是解决问题，代码只是实现思路的工具。"))


# --- cognitive-thinking: 13 points ---

kp(1, "cognitive-thinking", "AI时代的编程思维",
   "在AI时代，编程思维比写代码更重要。你需要学会：定义问题、分解任务、设计方案、验证结果。AI帮你写代码，但思路要你来想。",
   "# AI时代的工作流程\n# 1. 定义问题：我要做什么？\n# 2. 分解任务：拆成小步骤\n# 3. 设计方案：每步怎么做\n# 4. 用AI生成代码\n# 5. 验证结果\nprint('AI是工具，思维是核心')",
   game_predict_output("task = '写一个计算器'\nsteps = ['获取输入', '解析运算符', '计算结果', '显示结果']\nprint(len(steps))", ["4", "3", "5", "报错"], 0, "列表 steps 有 4 个元素，len() 返回 4。"),
   quiz("AI时代，什么比写代码更重要？", ["背语法", "编程思维（定义问题、分解任务）", "打字速度", "英语水平"], 1, "AI可以帮你写代码，但解决问题的思路需要你自己来。"))

kp(1, "cognitive-thinking", "分解思维",
   "分解就是把大问题拆成小问题。就像吃大象：一口一口来。每个小问题都更容易解决。",
   "# 分解示例：计算班级平均分\n# 大问题：计算平均分\n# 分解：\n# 步骤1：获取所有分数\nscores = [85, 90, 78, 92, 88]\n# 步骤2：计算总分\ntotal = sum(scores)\n# 步骤3：计算平均分\navg = total / len(scores)\nprint(f'平均分: {avg}')",
   game_predict_output("scores = [80, 90, 100]\ntotal = sum(scores)\navg = total / len(scores)\nprint(avg)", ["90.0", "80.0", "270", "3"], 0, "sum = 270, len = 3, 270 / 3 = 90.0。"),
   quiz("分解思维是什么？", ["合并多个问题", "把大问题拆成小问题", "跳过难题", "只做简单的事"], 1, "分解思维是把复杂的大问题拆分成多个简单的小问题，逐个解决。"))

kp(1, "cognitive-thinking", "抽象思维",
   "抽象就是忽略细节，抓住重点。你用手机打电话时，不需要知道信号是怎么传输的——那些细节被抽象掉了。",
   "# 抽象示例\ndef calculate_area(length, width):\n    '''计算矩形面积（抽象：隐藏了乘法细节）'''\n    return length * width\n\n# 使用时只需要知道：传入长和宽\nresult = calculate_area(5, 3)\nprint(f'面积: {result}')  # 面积: 15",
   game_predict_output("def double(x):\n    return x * 2\n\nprint(double(7))", ["7", "14", "72", "报错"], 1, "double(7) 返回 7 * 2 = 14。"),
   quiz("抽象思维的作用是什么？", ["展示所有细节", "忽略细节，抓住重点", "让代码更复杂", "删除信息"], 1, "抽象帮助我们忽略不必要的细节，专注于核心问题。"))

kp(1, "cognitive-thinking", "模式识别",
   "模式识别就是发现事物之间的相似之处。如果你发现两个问题的解法类似，就可以复用之前的方案。",
   "# 模式识别示例\ndef find_max(numbers):\n    result = numbers[0]\n    for n in numbers:\n        if n > result:\n            result = n\n    return result\n\ndef find_min(numbers):\n    result = numbers[0]\n    for n in numbers:\n        if n < result:\n            result = n\n    return result\n# 两个函数结构一样，只是比较符号不同",
   game_fill_blank(
       "def find_max(numbers):\n    result = numbers[0]\n    for n in numbers:\n        if n ____ result:\n            result = n\n    return result",
       [{"position": 1, "answer": ">", "options": [">", "<", "==", ">="]}],
       "找最大值时，如果当前数比已知最大值更大（>），就更新最大值。"
   ),
   quiz("模式识别的好处是什么？", ["让代码更长", "复用已有的解决方案", "增加复杂度", "没有好处"], 1, "识别模式可以让你复用之前的解决方案，提高效率。"))

kp(1, "cognitive-thinking", "逐步细化",
   "逐步细化就是先写大纲，再补充细节。就像画画：先画轮廓，再填颜色，最后加细节。",
   "# 逐步细化示例\n# 第一步：大纲\ndef greet_user(name, time):\n    if time < 12:\n        return f'早上好，{name}！'\n    elif time < 18:\n        return f'下午好，{name}！'\n    else:\n        return f'晚上好，{name}！'\n\nprint(greet_user('小明', 9))",
   game_predict_output("def greet_user(name, time):\n    if time < 12:\n        return f'早上好，{name}！'\n    elif time < 18:\n        return f'下午好，{name}！'\n    else:\n        return f'晚上好，{name}！'\n\nprint(greet_user('小明', 15))", ["早上好，小明！", "下午好，小明！", "晚上好，小明！", "报错"], 1, "15 < 18 为 True 且 >= 12，所以返回'下午好，小明！'。"),
   quiz("逐步细化的正确顺序是什么？", ["先细节再大纲", "先大纲再补充细节", "随便写", "只写大纲"], 1, "先写整体框架（大纲），再逐步补充每个部分的细节。"))

kp(1, "cognitive-thinking", "假设与验证",
   "编程时经常需要假设代码的执行结果，然后运行验证。假设错了？修改，再验证。这就是编程的日常。",
   "# 假设：这段代码会输出什么？\nx = 5\ny = 3\nresult = x ** y\n# 假设：5的3次方 = 125\nprint(result)  # 验证：确实输出 125",
   game_predict_output("x = 2\ny = 10\nresult = x ** y\nprint(result)", ["20", "1024", "12", "报错"], 1, "2 ** 10 = 1024，即 2 的 10 次方。"),
   quiz("假设与验证的循环是什么？", ["写代码 → 不测试", "假设结果 → 运行验证 → 修改", "只假设不验证", "只验证不假设"], 1, "编程的核心循环：假设 → 验证 → 修正 → 再验证。"))

kp(1, "cognitive-thinking", "从具体到一般",
   "先解决一个具体问题，再推广到一般情况。比如：先算 3+5，再写一个函数算任意两个数的和。",
   "# 从具体到一般\n# 具体：算 3 + 5\nprint(3 + 5)  # 8\n\n# 一般：写一个函数\ndef add(a, b):\n    return a + b\n\nprint(add(3, 5))   # 8\nprint(add(10, 20))  # 30\nprint(add(100, 200))  # 300",
   game_predict_output("def multiply(a, b):\n    return a * b\n\nprint(multiply(4, 5))\nprint(multiply(3, 3))", ["20 和 9", "45 和 33", "20 和 3", "报错"], 0, "4 * 5 = 20, 3 * 3 = 9，输出两行：20 和 9。"),
   quiz("从具体到一般的思路是什么？", ["先一般再具体", "先解决具体问题，再推广", "只做具体的", "只做一般的"], 1, "先解决具体问题，找到规律，再推广成通用方案。"))

kp(1, "cognitive-thinking", "逆向思维",
   "有时候从结果倒推更简单。知道想要什么输出，倒推需要什么输入和步骤。",
   "# 逆向思维：想让用户看到 'Hello, Alice!'\n# 倒推：需要一个 f-string\n# 再倒推：需要变量 name = 'Alice'\nname = 'Alice'\nprint(f'Hello, {name}!')  # 正是我们想要的",
   game_fill_blank(
       "# 目标：输出 '分数: 90'\nscore = 90\nprint(f'分数: ____')",
       [{"position": 1, "answer": "{score}", "options": ["{score}", "score", "[score]", "(score)"]}],
       "f-string 中用 {score} 嵌入变量的值。"
   ),
   quiz("逆向思维怎么用在编程中？", ["从代码开始写", "从想要的结果倒推步骤", "随机尝试", "不写代码"], 1, "逆向思维：先明确想要什么结果，再倒推需要什么步骤来实现。"))

kp(1, "cognitive-thinking", "测试思维",
   "写完代码要测试。测试边界情况：0、负数、空值、最大值。好的程序员一半时间在写测试。",
   "# 测试思维\nimport math\ndef is_positive(n):\n    return n > 0\n\n# 测试正常情况\nprint(is_positive(5))    # True\n# 测试边界\nprint(is_positive(0))    # False（边界！）\nprint(is_positive(-3))   # False",
   game_predict_output("def is_positive(n):\n    return n > 0\n\nprint(is_positive(0))", ["True", "False", "0", "报错"], 1, "0 > 0 为 False，所以 is_positive(0) 返回 False。"),
   quiz("测试时应该注意什么？", ["只测正常情况", "测试边界情况（0、负数、空值等）", "不测试", "只测一次"], 1, "好的测试要覆盖边界情况，比如 0、负数、空值等特殊输入。"))

kp(1, "cognitive-thinking", "简单优先原则",
   "能用简单方法解决的，就不要用复杂的。简单代码更好理解、更好维护、更少错误。",
   "# 简单 vs 复杂\n# 复杂：用循环判断奇偶\nn = 7\nresult = '偶数'\nfor i in range(1):\n    if n % 2 != 0:\n        result = '奇数'\n\n# 简单：直接判断\nif n % 2 == 0:\n    print('偶数')\nelse:\n    print('奇数')  # 更清晰！",
   game_predict_output("x = 10\n# 简单方法\nresult = x > 0\nprint(result)", ["True", "False", "10", "报错"], 0, "10 > 0 为 True，简单直接。"),
   quiz("为什么简单代码更好？", ["因为简单代码运行更快", "因为简单代码更易理解和维护", "因为复杂代码不能运行", "没有区别"], 1, "简单代码更容易理解、维护，也更少出错。"))

kp(1, "cognitive-thinking", "数据驱动思维",
   "让数据说话。不要凭感觉做决定，用数据来验证。程序的输入输出就是数据。",
   "# 数据驱动：统计成绩\nscores = [85, 90, 78, 92, 88, 65, 95]\n\n# 用数据说话\nprint(f'最高分: {max(scores)}')\nprint(f'最低分: {min(scores)}')\nprint(f'平均分: {sum(scores)/len(scores):.1f}')",
   game_predict_output("data = [10, 20, 30, 40, 50]\nprint(max(data) - min(data))", ["40", "50", "10", "150"], 0, "max = 50, min = 10, 50 - 10 = 40。"),
   quiz("数据驱动思维的核心是什么？", ["凭感觉做决定", "用数据来验证和做决定", "忽略数据", "只看最大的数"], 1, "数据驱动：用实际数据来验证假设和做决定，而不是凭感觉。"))

kp(1, "cognitive-thinking", "迭代改进",
   "好的程序不是一次写成的。先写一个能用的版本，再不断改进。这就是迭代。",
   "# 迭代改进示例\n# 版本1：简单版\ndef is_even_v1(n):\n    if n % 2 == 0:\n        return True\n    else:\n        return False\n\n# 版本2：简化版\ndef is_even_v2(n):\n    return n % 2 == 0\n\nprint(is_even_v2(4))  # True",
   game_predict_output("def is_even(n):\n    return n % 2 == 0\n\nprint(is_even(7))\nprint(is_even(8))", ["True True", "False True", "True False", "报错"], 1, "7 % 2 = 1 != 0 → False, 8 % 2 = 0 → True。"),
   quiz("迭代改进是什么意思？", ["一次写完美", "先写能用的版本，再不断改进", "不改进代码", "删掉重写"], 1, "迭代改进：先写一个基本能用的版本，然后不断优化和完善。"))

kp(1, "cognitive-thinking", "分解复杂问题的实例",
   "面对复杂问题时，先把它分解成小任务。每个小任务写一个函数，最后组合起来。",
   "# 分解：写一个简单的计算器\n# 小任务1：获取数字\ndef get_number(prompt):\n    return float(input(prompt))\n\n# 小任务2：计算\ndef calculate(a, b, op):\n    if op == '+': return a + b\n    if op == '-': return a - b\n    if op == '*': return a * b\n    if op == '/': return a / b if b != 0 else '不能除以零'\n\nprint(calculate(10, 3, '+'))  # 13.0",
   game_predict_output("def calculate(a, b, op):\n    if op == '+': return a + b\n    if op == '-': return a - b\n\nprint(calculate(10, 3, '-'))", ["13.0", "7.0", "30", "报错"], 1, "op 是 '-'，所以返回 10 - 3 = 7.0。"),
   quiz("分解复杂问题时，每个小任务应该怎么实现？", ["写在一个大函数里", "每个小任务写一个独立函数", "不写函数", "用全局变量"], 1, "每个小任务写一个独立的函数，职责单一，最后组合调用。"))


# --- cognitive-languages: 12 points ---

kp(1, "cognitive-languages", "为什么学Python",
   "Python 是 AI 和数据科学的第一语言。语法简洁，像读英语一样。拥有庞大的库生态：NumPy、PyTorch、Pandas 等。",
   "# Python 的简洁之美\nname = 'Python'\nprint(f'{name} 是 AI 时代最重要的语言')\n\n# 同样的功能，其他语言可能需要更多代码",
   game_predict_output("language = 'Python'\nprint(f'{language}很简洁')", ["Python很简洁", "language很简洁", "报错", "很简洁"], 0, "f-string 中 {language} 被替换为变量值 'Python'。"),
   quiz("Python 在哪个领域排名第一？", ["游戏开发", "AI 和数据科学", "手机开发", "操作系统"], 1, "Python 是 AI、机器学习和数据科学领域的第一语言。"))

kp(1, "cognitive-languages", "为什么学TypeScript",
   "TypeScript 是 JavaScript 的超集，添加了类型系统。是前端开发的主流语言，也用于后端（Node.js）。类型安全能在运行前发现错误。",
   "// TypeScript 示例\nfunction add(a: number, b: number): number {\n    return a + b;\n}\nconsole.log(add(3, 5)); // 8\n// add('3', 5)  // 编译时报错！",
   game_fill_blank(
       "// TypeScript 函数签名\nfunction greet(name: ____): string {\n    return 'Hello, ' + name;\n}",
       [{"position": 1, "answer": "string", "options": ["string", "number", "boolean", "any"]}],
       "参数 name 应该是字符串类型，用 string 声明。"
   ),
   quiz("TypeScript 相比 JavaScript 的主要优势是什么？", ["运行更快", "添加了类型系统，提前发现错误", "语法更简单", "不需要学 JavaScript"], 1, "TypeScript 的类型系统能在编译时就发现错误，比运行时才发现更安全。"))

kp(1, "cognitive-languages", "Python和TypeScript的分工",
   "Python 负责 AI/数据/后端，TypeScript 负责前端/全栈。两者配合覆盖 90%+ 的现代开发需求。",
   "# Python: AI 后端\nfrom flask import Flask\napp = Flask(__name__)\n\n@app.route('/api/data')\ndef get_data():\n    return {'result': 42}",
   game_predict_output("python_tasks = ['AI', '数据分析', '后端']\nts_tasks = ['前端', '全栈', '类型安全']\nprint(len(python_tasks) + len(ts_tasks))", ["3", "6", "5", "报错"], 1, "两个列表各有 3 个元素，3 + 3 = 6。"),
   quiz("Python 和 TypeScript 的分工是？", ["Python 做前端，TS 做后端", "Python 做 AI/数据/后端，TS 做前端/全栈", "完全重叠", "互不相关"], 1, "Python 擅长 AI、数据分析和后端，TypeScript 擅长前端和全栈开发。"))

kp(1, "cognitive-languages", "静态类型 vs 动态类型",
   "Python 是动态类型：变量类型在运行时确定。TypeScript 是静态类型：类型在编写代码时就确定。两种方式各有优缺点。",
   "# Python 动态类型\nx = 5       # x 是 int\nx = 'hello' # x 变成了 str，没问题！\nprint(x)    # hello",
   game_predict_output("x = 42\nx = 'hello'\nprint(x)", ["42", "hello", "报错", "42 hello"], 1, "Python 是动态类型，x 可以从 int 变成 str。"),
   quiz("动态类型语言的特点是什么？", ["变量类型固定不变", "变量类型在运行时确定", "不能用变量", "只有数字类型"], 1, "动态类型语言中，变量的类型在运行时才确定，可以随时改变。"))

kp(1, "cognitive-languages", "强类型 vs 弱类型",
   "Python 是强类型：不同类型不能随意混合运算。'1' + 1 会报错。弱类型语言（如 JS）会自动转换。",
   "# Python 强类型\nnum = 1\ntext = '2'\n# print(num + text)  # TypeError!\n\n# 正确做法：显式转换\nprint(num + int(text))   # 3\nprint(str(num) + text)   # '12'",
   game_find_bug(
       ["age = 25", "print('年龄: ' + age)"],
       2, "Python 是强类型，字符串和数字不能直接用 + 拼接。需要 str(age) 转换。"
   ),
   quiz("Python 的强类型意味着什么？", ["所有类型都一样", "不同类型不能随意混合运算", "没有类型", "自动转换类型"], 1, "强类型意味着 Python 不会自动转换类型，不同类型混合操作会报错。"))

kp(1, "cognitive-languages", "Python的简洁语法",
   "Python 用缩进表示代码块，不用大括号。这让代码看起来更干净、更像自然语言。",
   "# Python 语法简洁\nif 5 > 3:\n    print('5 大于 3')\n    print('这是对的')\n\n# 对比其他语言：\n# if (5 > 3) {\n#     console.log('5 大于 3');\n# }",
   game_predict_output("x = 10\nif x > 5:\n    print('大')\n    print('很大')", ["大", "很大", "大 很大", "报错"], 0, "x > 5 为 True，执行缩进的两行，输出'大'和'很大'（两行）。"),
   quiz("Python 用什么表示代码块？", ["大括号 {}", "缩进（空格或Tab）", "圆括号 ()", "方括号 []"], 1, "Python 用缩进来表示代码块，这是它语法简洁的原因之一。"))

kp(1, "cognitive-languages", "Python的交互模式",
   "Python 有交互模式（REPL），可以一行一行输入代码并立即看到结果。非常适合学习和测试。",
   "# 在终端中输入 python 就进入交互模式\n# >>> 是提示符\n# >>> 2 + 3\n# 5\n# >>> print('hello')\n# hello\n\n# 在代码中模拟：\nresult = 2 + 3\nprint(result)  # 5",
   game_predict_output("# 交互模式\n>>> 10 * 2\n>>> 5 + 3", ["20", "8", "20 和 8", "报错"], 1, "在交互模式中，每行表达式都会输出结果。但这里模拟的是两行独立代码。"),
   quiz("Python 交互模式适合做什么？", ["写大型项目", "快速测试和学习", "部署上线", "连接数据库"], 1, "交互模式（REPL）可以快速测试代码片段，非常适合学习和调试。"))

kp(1, "cognitive-languages", "选择语言的依据",
   "选择语言看三点：1. 要解决什么问题？2. 生态系统（库和工具）？3. 团队和社区支持？",
   "# 选语言示例\n# 做网站前端 → TypeScript/JavaScript\n# 做数据分析 → Python\n# 做手机App → Swift(苹果) / Kotlin(安卓)\n# 做游戏 → C# (Unity) / C++ (Unreal)",
   game_fill_blank(
       "# 做 AI 模型训练 → ____\n# 做网站前端 → TypeScript",
       [{"position": 1, "answer": "Python", "options": ["Python", "Java", "C++", "HTML"]}],
       "Python 是 AI 和机器学习的首选语言。"
   ),
   quiz("选择编程语言时，最重要的是看什么？", ["谁最新", "要解决的问题和生态系统", "语法是否好看", "朋友推荐"], 1, "选择语言要看要解决的问题类型、生态系统和社区支持。"))

kp(1, "cognitive-languages", "代码可读性",
   "代码是写给人看的，顺便让机器执行。好的代码应该像读文章一样清晰。",
   "# 不好的写法\ndef f(x,y):\n    return x+y if x>y else y-x\n\n# 好的写法\ndef calculate(a, b):\n    '''比较两个数并返回结果'''\n    if a > b:\n        return a + b\n    else:\n        return b - a",
   game_find_bug(
       ["def f(x):", "    return x*2+1", "# 这个函数做什么？看不懂！"],
       2, "函数名 'f' 和代码没有注释，别人看不懂。应该用有意义的名字和添加说明。"
   ),
   quiz("为什么代码可读性很重要？", ["让程序更快", "方便自己和他人理解和维护", "让代码更短", "不重要"], 1, "代码是写给人看的，可读性好才能方便维护和协作。"))

kp(1, "cognitive-languages", "Python的用途范围",
   "Python 的用途非常广泛：AI/机器学习、数据分析、Web后端、自动化脚本、科学计算等。但不适合做前端和手机App。",
   "# Python 的主要用途\n# 1. AI 和机器学习\n# import torch\n# 2. 数据分析\n# import pandas\n# 3. Web 后端\n# from flask import Flask\n# 4. 自动化脚本\n# import os\nprint('Python 用途广泛！')",
   game_predict_output("uses = ['AI', '数据分析', 'Web后端', '自动化', '科学计算']\nprint(len(uses))", ["5", "4", "3", "报错"], 0, "列表 uses 有 5 个元素。"),
   quiz("Python 不擅长哪个领域？", ["AI/机器学习", "前端网页开发", "数据分析", "自动化脚本"], 1, "Python 不擅长前端开发，前端主要用 TypeScript/JavaScript。"))

kp(1, "cognitive-languages", "TypeScript的类型注解",
   "TypeScript 用冒号 : 来声明类型。这让代码更安全，IDE 也能提供更好的自动补全。",
   "// TypeScript 类型注解\nlet age: number = 25;\nlet name: string = 'Alice';\nlet isStudent: boolean = true;\n\nfunction add(a: number, b: number): number {\n    return a + b;\n}",
   game_fill_blank(
       "let score: ____ = 95;",
       [{"position": 1, "answer": "number", "options": ["number", "string", "boolean", "any"]}],
       "95 是数字，所以类型应该是 number。"
   ),
   quiz("TypeScript 中 let age: number = 25 的 : number 是什么？", ["注释", "类型注解，声明 age 是数字类型", "赋值运算", "函数调用"], 1, ": number 是类型注解，告诉 TypeScript 这个变量是数字类型。"))

kp(1, "cognitive-languages", "编译型 vs 解释型语言",
   "Python 是解释型：代码逐行运行。TypeScript 需要编译：先转成 JS，再运行。各有优缺点。",
   "# Python: 解释型，直接运行\nprint('hello')  # 直接执行\n\n# TypeScript: 先编译成 JavaScript\n# let x: number = 5;  → 编译 → let x = 5;\n# 然后运行编译后的 JavaScript",
   game_predict_output("language = 'Python'\ntype_ = '解释型'\nprint(f'{language}是{type_}语言')", ["Python是解释型语言", "Python是编译型语言", "language是type_语言", "报错"], 0, "f-string 中变量被替换为各自的值。"),
   quiz("Python 是什么类型的语言？", ["编译型", "解释型（逐行运行）", "机器语言", "汇编语言"], 1, "Python 是解释型语言，代码逐行解释执行，不需要预先编译。"))


# ============================================================
# WEEK 2: Python变量与数据类型 (40 points)
# ============================================================
# module: py-variables (20 points)
# module: py-types (20 points)

# --- py-variables: 20 points ---

kp(2, "py-variables", "变量的创建",
   "在 Python 中，用等号 = 创建变量并赋值。等号左边是变量名，右边是要存的值。",
   "# 创建变量\nname = '小明'      # 创建一个字符串变量\nage = 18           # 创建一个数字变量\nis_student = True  # 创建一个布尔变量\n\nprint(name)  # 输出: 小明",
   game_predict_output("city = '北京'\nprint(city)", ["北京", "city", "'北京'", "报错"], 0, "print(city) 输出变量 city 的值，即'北京'。"),
   quiz("如何在 Python 中创建变量？", ["用 var 关键字", "直接用 = 赋值", "用 let 关键字", "用 define"], 1, "Python 中直接用 = 就能创建变量并赋值，不需要特殊关键字。"))

kp(2, "py-variables", "变量赋值的原理",
   "赋值不是把值放进盒子，而是让变量名指向一个值。就像给一个东西贴标签。",
   "# 变量是标签，不是盒子\na = [1, 2, 3]  # a 指向这个列表\nb = a          # b 也指向同一个列表\nb.append(4)    # 通过 b 修改列表\nprint(a)       # [1, 2, 3, 4]  a 也变了！",
   game_predict_output("a = [1, 2, 3]\nb = a\nb.append(4)\nprint(a)", ["[1, 2, 3]", "[1, 2, 3, 4]", "[4, 2, 3]", "报错"], 1, "a 和 b 指向同一个列表，通过 b 修改后，a 看到的也变了。"),
   quiz("Python 变量赋值的实质是什么？", ["复制值到新盒子", "让变量名指向一个值", "删除旧值", "创建新类型"], 1, "赋值是让变量名指向一个对象，不是把值复制到盒子里。"))

kp(2, "py-variables", "变量命名规则",
   "变量名只能包含字母、数字和下划线，不能以数字开头，不能使用 Python 关键字。",
   "# 合法的变量名\nuser_name = '小明'   # 好：下划线分隔\nage2 = 20           # 可以有数字（不在开头）\n_private = True     # 下划线开头\n\n# 不合法的变量名（会报错）\n# 2name = '错'       # 不能以数字开头\n# my-name = '错'     # 不能有横杠\n# class = '错'       # 不能用关键字",
   game_find_bug(
       ["my-name = '小明'", "print(my-name)"],
       1, "变量名不能包含横杠 -，Python 会认为是减法运算。应该用下划线：my_name。"
   ),
   quiz("以下哪个变量名是合法的？", ["2name", "my-name", "my_name", "class"], 2, "my_name 是合法的。2name 以数字开头，my-name 有横杠，class 是关键字。"))

kp(2, "py-variables", "变量重新赋值",
   "变量可以随时重新赋新值。新值会替换旧值。变量的类型也可以改变（因为 Python 是动态类型）。",
   "# 重新赋值\nx = 10\nprint(x)  # 10\n\nx = 'hello'  # 从数字变成字符串\nprint(x)  # hello\n\nx = [1, 2, 3]  # 变成列表\nprint(x)  # [1, 2, 3]",
   game_predict_output("x = 5\nx = 10\nx = 15\nprint(x)", ["5", "10", "15", "30"], 2, "变量最终保存的是最后一次赋值的值，即 15。"),
   quiz("变量重新赋值后，旧值会怎样？", ["还在", "被新值替换", "报错", "保存在别处"], 1, "重新赋值后，变量指向新值，旧值如果没有其他引用会被回收。"))

kp(2, "py-variables", "多重赋值",
   "可以在一行给多个变量同时赋值。可以是相同值，也可以是不同值。",
   "# 同时给多个变量赋不同值\na, b, c = 1, 2, 3\nprint(a, b, c)  # 1 2 3\n\n# 同时给多个变量赋相同值\nx = y = z = 0\nprint(x, y, z)  # 0 0 0",
   game_predict_output("a, b, c = 10, 20, 30\nprint(b)", ["10", "20", "30", "报错"], 1, "a=10, b=20, c=30，print(b) 输出 20。"),
   quiz("a, b = 1, 2 之后，b 的值是多少？", ["1", "2", "报错", "None"], 1, "多重赋值按位置对应：a=1, b=2。"))

kp(2, "py-variables", "交换变量值",
   "Python 可以优雅地交换两个变量的值，不需要临时变量。这是 Python 的特殊语法。",
   "# 交换变量\na = 10\nb = 20\nprint(f'交换前: a={a}, b={b}')\n\na, b = b, a  # 优雅地交换！\nprint(f'交换后: a={a}, b={b}')\n# 交换后: a=20, b=10",
   game_predict_output("x = 1\ny = 2\nx, y = y, x\nprint(x, y)", ["1 2", "2 1", "报错", "1 1"], 1, "x, y = y, x 交换了两个变量的值，x 变成 2，y 变成 1。"),
   quiz("Python 中交换变量 a, b 的值，最简洁的方式是？", ["用临时变量", "a, b = b, a", "a = b; b = a", "不能交换"], 1, "Python 可以直接用 a, b = b, a 来交换，不需要临时变量。"))

kp(2, "py-variables", "变量作用域初步",
   "变量有自己的“活动范围”。函数里定义的变量是局部变量，外面不能用。",
   "# 局部变量\n\ndef my_func():\n    x = 10  # 局部变量，只在函数内有效\n    print(f'函数内: {x}')\n\nmy_func()\n# print(x)  # 报错！x 在外面不存在",
   game_find_bug(
       ["def my_func():", "    secret = 42", "", "my_func()", "print(secret)"],
       5, "secret 是函数内的局部变量，函数外不能访问。会报 NameError。"
   ),
   quiz("函数内定义的变量，函数外能用吗？", ["能", "不能（局部变量）", "看情况", "不确定"], 1, "函数内定义的变量是局部变量，只在函数内有效，外面访问会报错。"))

kp(2, "py-variables", "全局变量",
   "在函数外定义的变量是全局变量，函数内可以读取。但要在函数内修改全局变量，需要用 global 关键字。",
   "# 全局变量\ncount = 0  # 全局变量\n\ndef increment():\n    global count  # 声明使用全局变量\n    count += 1\n\nincrement()\nincrement()\nprint(count)  # 2",
   game_predict_output("x = 5\n\ndef change():\n    global x\n    x = 10\n\nchange()\nprint(x)", ["5", "10", "报错", "None"], 1, "global 声明后，函数内修改的是全局变量 x，所以输出 10。"),
   quiz("在函数内修改全局变量需要什么关键字？", ["local", "global", "public", "var"], 1, "需要用 global 关键字声明，才能在函数内修改全局变量。"))

kp(2, "py-variables", "常量的约定",
   "Python 没有真正的常量。约定用全大写字母命名的变量为常量，表示不应该被修改。",
   "# 常量（约定，不是强制）\nPI = 3.14159\nMAX_RETRIES = 3\nAPI_URL = 'https://api.example.com'\n\n# 这些值不应该被修改\nprint(PI)  # 3.14159\n# PI = 3  # 虽然不报错，但违反约定",
   game_predict_output("MAX_SIZE = 100\nprint(MAX_SIZE)", ["100", "MAX_SIZE", "报错", "None"], 0, "MAX_SIZE 是一个变量（虽然按约定是常量），值为 100。"),
   quiz("Python 中常量用什么命名风格？", ["camelCase", "snake_case", "全大写（UPPER_CASE）", "PascalCase"], 2, "Python 约定常量用全大写字母和下划线命名，如 MAX_SIZE。"))

kp(2, "py-variables", "删除变量",
   "用 del 关键字可以删除变量。删除后就不能再使用了。",
   "# 删除变量\nx = 10\nprint(x)  # 10\n\ndel x  # 删除变量 x\n# print(x)  # NameError: x 未定义",
   game_find_bug(
       ["name = '小明'", "del name", "print(name)"],
       3, "del name 删除了变量 name，之后再 print(name) 会报 NameError。"
   ),
   quiz("del x 之后再 print(x) 会怎样？", ["输出 None", "输出 0", "报 NameError", "输出 x"], 2, "del 删除了变量，再使用会报 NameError（变量未定义）。"))

kp(2, "py-variables", "链式赋值",
   "可以让多个变量指向同一个值。对于不可变类型（如数字），修改一个不影响其他。",
   "# 链式赋值\na = b = c = 100\nprint(a, b, c)  # 100 100 100\n\na = 200  # 只改 a\nprint(a, b, c)  # 200 100 100（b, c 不变）",
   game_predict_output("a = b = 5\na = 10\nprint(b)", ["10", "5", "报错", "None"], 1, "a = b = 5 让 a 和 b 都指向 5。a = 10 只改变 a，b 不受影响。"),
   quiz("a = b = 5 后，把 a 改为 10，b 的值是多少？", ["10", "5", "报错", "None"], 1, "对于数字这种不可变类型，a = 10 只是让 a 指向新值，b 仍然指向 5。"))

kp(2, "py-variables", "变量的 id 和 is",
   "每个对象都有一个唯一的 id（内存地址）。is 比较的是 id（是否同一个对象），== 比较的是值。",
   "# id 和 is\na = [1, 2, 3]\nb = [1, 2, 3]\nc = a\n\nprint(a == b)   # True（值相同）\nprint(a is b)   # False（不同对象）\nprint(a is c)   # True（同一对象）\nprint(id(a) == id(c))  # True",
   game_predict_output("a = [1, 2]\nb = [1, 2]\nprint(a == b)\nprint(a is b)", ["True True", "True False", "False True", "False False"], 1, "== 比较值（True），is 比较是否同一对象（False）。"),
   quiz("a is b 和 a == b 的区别是什么？", ["完全一样", "is 比较对象身份，== 比较值", "is 比较值，== 比较类型", "都不对"], 1, "is 比较两个变量是否指向同一个对象，== 比较值是否相等。"))

kp(2, "py-variables", "可变与不可变变量",
   "数字、字符串、元组是不可变的：创建后不能修改。列表、字典是可变的：可以修改内容。",
   "# 不可变：字符串\ns = 'hello'\ns[0] = 'H'  # 报错！字符串不能修改\n# 要改只能创建新的：\ns = 'Hello'  # 新对象\n\n# 可变：列表\nlst = [1, 2, 3]\nlst[0] = 10  # 可以修改\nprint(lst)   # [10, 2, 3]",
   game_find_bug(
       ["text = 'hello'", "text[0] = 'H'", "print(text)"],
       2, "字符串是不可变的，不能用索引修改单个字符。需要创建新字符串：text = 'Hello'。"
   ),
   quiz("以下哪种类型是不可变的？", ["列表 list", "字典 dict", "字符串 str", "集合 set"], 2, "字符串是不可变的，创建后不能修改内容。列表、字典、集合都是可变的。"))

kp(2, "py-variables", "变量命名最佳实践",
   "好名字要：有意义、简洁、用 snake_case。避免单个字母（循环变量除外）和缩写。",
   "# 好的命名\nuser_name = '小明'      # 清晰\nmax_retry_count = 3     # 有意义\nis_valid = True         # 布尔用 is_/has_\n\n# 不好的命名\nx = '小明'              # 太短\nmrc = 3                 # 意义不明\nflag = True             # 不具体",
   game_fill_blank(
       "# 判断用户是否成年\nis_adult = age >= ____",
       [{"position": 1, "answer": "18", "options": ["18", "20", "16", "21"]}],
       "成年人的标准年龄一般是 18 岁。"
   ),
   quiz("布尔类型的变量推荐用什么前缀？", ["get_", "set_", "is_ 或 has_", "do_"], 2, "布尔变量推荐用 is_ 或 has_ 前缀，如 is_valid、has_permission。"))

kp(2, "py-variables", "type() 查看变量类型",
   "用 type() 函数可以查看变量的类型。这是调试时非常有用的工具。",
   "# 查看变量类型\nx = 42\nprint(type(x))         # <class 'int'>\nprint(type(3.14))      # <class 'float'>\nprint(type('hello'))   # <class 'str'>\nprint(type(True))      # <class 'bool'>\nprint(type(None))      # <class 'NoneType'>",
   game_predict_output("x = 'hello'\nprint(type(x))", ["<class 'str'>", "<class 'int'>", "str", "hello"], 0, "type('hello') 返回 <class 'str'>，表示这是字符串类型。"),
   quiz("type('hello') 返回什么？", ["hello", "<class 'str'>", "string", "str"], 1, "type() 返回类型的完整表示：<class 'str'>。"))

kp(2, "py-variables", "变量的内存管理",
   "Python 自动管理内存。当一个对象没有变量引用它时，会被自动回收（垃圾回收）。",
   "# 内存管理\na = [1, 2, 3]  # 创建列表，a 引用它\nb = a          # b 也引用它\na = None       # a 不再引用列表\nprint(b)       # [1, 2, 3] 列表还在（b 还引用着）\nb = None       # b 也不引用了，列表会被回收",
   game_predict_output("a = [1, 2, 3]\nb = a\na = None\nprint(b)", ["None", "[1, 2, 3]", "报错", "[None, 2, 3]"], 1, "a = None 只是让 a 不再引用列表，b 还引用着，所以 b 还能看到列表。"),
   quiz("Python 什么时候回收内存中的对象？", ["立刻回收", "当没有变量引用该对象时自动回收", "从不回收", "手动回收"], 1, "Python 使用垃圾回收机制，当对象没有被任何变量引用时，自动回收内存。"))

kp(2, "py-variables", "变量命名：避免关键字",
   "Python 有一些保留关键字（如 if、for、while、class 等），不能用作变量名。",
   "# Python 关键字（不能用作变量名）\n# if, else, elif, for, while, return,\n# class, def, import, from, True, False,\n# None, and, or, not, in, is, try, except...\n\n# 错误示例：\n# class = '数学'  # 报错！\n\n# 正确：\nclass_name = '数学'\nprint(class_name)",
   game_find_bug(
       ["for = 10", "print(for)"],
       1, "'for' 是 Python 关键字，不能用作变量名。应该用其他名字如 count。"
   ),
   quiz("以下哪个不能用作变量名？", ["my_var", "count", "for", "data"], 2, "'for' 是 Python 的关键字，不能用作变量名。"))

kp(2, "py-variables", "f-string 格式化输出",
   "f-string 是 Python 3.6+ 的字符串格式化方式。在字符串前加 f，用 {} 嵌入变量。",
   "# f-string 格式化\nname = '小明'\nage = 20\nscore = 95.5\n\n# 基本用法\nprint(f'{name} 今年 {age} 岁')\n# 表达式\nprint(f'明年 {age + 1} 岁')\n# 格式化小数\nprint(f'分数: {score:.1f}')",
   game_predict_output("name = 'Python'\nversion = 3\nprint(f'{name} {version}')", ["Python 3", "name version", "{Python} {3}", "报错"], 0, "f-string 中 {name} 和 {version} 被替换为变量的值。"),
   quiz("f-string 中怎么嵌入变量？", ["用 $", "用 {}（字符串前加 f）", "用 %", "用 @"], 1, "f-string 在字符串前加 f，用花括号 {} 嵌入变量或表达式。"))

kp(2, "py-variables", "输入与类型转换",
   "input() 总是返回字符串。如果需要数字，必须用 int() 或 float() 转换。",
   "# 输入并转换类型\n# age_str = input('请输入年龄：')  # 返回字符串\nage_str = '20'  # 模拟输入\nage = int(age_str)  # 转为整数\n\nprint(f'年龄: {age}')\nprint(f'十年后: {age + 10}')",
   game_predict_output("x = input('输入: ')  # 假设输入 5\ny = int(x)\nprint(y + 10)", ["15", "510", "报错", "5 10"], 0, "input 返回字符串 '5'，int('5') = 5，5 + 10 = 15。"),
   quiz("input('年龄: ') 返回的类型是什么？", ["int", "str", "float", "bool"], 1, "input() 总是返回字符串类型，即使输入的是数字。"))

kp(2, "py-variables", "连续赋值和覆盖",
   "变量被覆盖后，旧值就丢失了。要小心不要意外覆盖重要数据。",
   "# 覆盖变量\nname = '小明'\nold_name = name  # 先备份\nname = '小红'    # 覆盖\nprint(f'新名字: {name}')      # 小红\nprint(f'旧名字: {old_name}')  # 小明",
   game_predict_output("x = 1\nx = 2\nx = 3\nprint(x)", ["1", "2", "3", "6"], 2, "变量被覆盖，最终值是最后一次赋的值 3。"),
   quiz("变量被覆盖后，旧值会怎样？", ["还在内存中", "丢失（除非有备份）", "自动保存", "报错"], 1, "变量覆盖后旧值丢失。如果还需要旧值，应该先备份到另一个变量。"))


# --- py-types: 20 points ---

kp(2, "py-types", "整数类型 int",
   "整数（int）是没有小数点的数字。Python 的整数没有大小限制，可以存任意大的数。",
   "# 整数\na = 42\nb = -10\nc = 0\nbig = 99999999999999999999999999\n\nprint(type(a))  # <class 'int'>\nprint(big)      # 没有溢出！",
   game_predict_output("x = 1000000000 * 1000000000\nprint(type(x))", ["<class 'int'>", "<class 'float'>", "报错", "溢出"], 0, "Python 的整数没有大小限制，大数乘法仍然是 int。"),
   quiz("Python 中整数有大小限制吗？", ["有，最大 2^31", "没有，可以任意大", "有，最大 1000000", "有，最大 2^64"], 1, "Python 的整数没有大小限制，可以存储任意大的整数。"))

kp(2, "py-types", "浮点数类型 float",
   "浮点数（float）是带小数点的数字。注意浮点数可能有精度问题。",
   "# 浮点数\npi = 3.14159\nprice = 9.99\n\n# 精度问题\nresult = 0.1 + 0.2\nprint(result)           # 0.30000000000000004\nprint(round(result, 1)) # 0.3（四舍五入）",
   game_predict_output("print(0.1 + 0.2)", ["0.3", "0.30000000000000004", "报错", "0"], 1, "浮点数精度问题：0.1 + 0.2 实际结果是 0.30000000000000004。"),
   quiz("为什么 0.1 + 0.2 不等于 0.3？", ["Python 有 bug", "浮点数精度问题（计算机用二进制存储小数）", "语法错误", "类型错误"], 1, "计算机用二进制存储小数，有些十进制小数无法精确表示，导致精度误差。"))

kp(2, "py-types", "字符串类型 str",
   "字符串（str）是文本数据，用引号括起来。单引号、双引号都可以，三引号可以写多行。",
   "# 字符串的不同写法\ns1 = 'hello'\ns2 = \"hello\"\ns3 = '''多行\n字符串'''\n\nprint(s1)  # hello\nprint(s3)  # 多行\n          # 字符串",
   game_predict_output("s = \"It's a test\"\nprint(s)", ["It's a test", "Its a test", "报错", "It\\'s a test"], 0, "双引号可以包含单引号，直接输出。"),
   quiz("以下哪种不是合法的字符串写法？", ["'hello'", "\"hello\"", "hello", "'''hello'''"], 2, "没有引号的 hello 不是字符串，会被当成变量名。"))

kp(2, "py-types", "布尔类型 bool",
   "布尔类型（bool）只有两个值：True 和 False。用于条件判断和逻辑运算。",
   "# 布尔值\nis_sunny = True\nis_raining = False\n\n# 比较运算产生布尔值\nprint(5 > 3)    # True\nprint(5 == 3)   # False\nprint(5 != 3)   # True",
   game_predict_output("x = 10\nresult = x > 5\nprint(result)", ["True", "False", "10", "5"], 0, "10 > 5 为 True，所以 result 是 True。"),
   quiz("bool 类型有几个值？", ["无数个", "2 个（True 和 False）", "3 个", "0 个"], 1, "布尔类型只有 True 和 False 两个值。"))

kp(2, "py-types", "None 类型",
   "None 表示“没有值”。函数没有 return 语句时，默认返回 None。",
   "# None 的含义\nresult = None\nprint(result)        # None\nprint(type(result))  # <class 'NoneType'>\n\ndef say_hi():\n    print('hi')\n    # 没有 return\n\nx = say_hi()  # 返回 None\nprint(x)      # None",
   game_predict_output("def func():\n    pass\n\nresult = func()\nprint(result)", ["None", "pass", "报错", "func"], 0, "函数没有 return 语句，默认返回 None。"),
   quiz("函数没有 return 语句时，返回什么？", ["0", "空字符串", "None", "报错"], 1, "没有 return 的函数默认返回 None。"))

kp(2, "py-types", "type() 函数详解",
   "type() 返回对象的类型。可以用 == 比较类型，也可以用 isinstance()。",
   "# type() 用法\nprint(type(42))          # <class 'int'>\nprint(type('hello'))     # <class 'str'>\nprint(type([1, 2]))      # <class 'list'>\n\n# 比较类型\nprint(type(42) == int)   # True\nprint(isinstance(42, int))  # True（推荐）",
   game_predict_output("print(type(3.14) == float)", ["True", "False", "float", "报错"], 0, "type(3.14) 返回 <class 'float'>，与 float 相等，所以是 True。"),
   quiz("推荐用什么方式检查类型？", ["type() == 类型", "isinstance(变量, 类型)", "直接猜测", "看变量名"], 1, "推荐使用 isinstance()，它支持继承关系检查，更灵活。"))

kp(2, "py-types", "int() 类型转换",
   "int() 可以把字符串和浮点数转为整数。浮数会截断小数部分（不是四舍五入）。",
   "# int() 转换\nprint(int('42'))      # 42（字符串转整数）\nprint(int(3.99))      # 3（截断，不是四舍五入！）\nprint(int(3.14))      # 3\nprint(int('100'))     # 100\n# int('hello')       # 报错！",
   game_predict_output("print(int(3.9))", ["4", "3", "3.9", "报错"], 1, "int() 截断小数部分，int(3.9) = 3，不是四舍五入。"),
   quiz("int(3.9) 的结果是什么？", ["4", "3", "3.9", "报错"], 1, "int() 截断小数部分（不是四舍五入），所以 int(3.9) = 3。"))

kp(2, "py-types", "float() 类型转换",
   "float() 可以把字符串和整数转为浮点数。整数会加上 .0。",
   "# float() 转换\nprint(float(42))       # 42.0\nprint(float('3.14'))   # 3.14\nprint(float('7'))      # 7.0\n# float('hello')      # 报错！",
   game_predict_output("print(float(42))", ["42", "42.0", "42.00", "报错"], 1, "float(42) 将整数 42 转为浮点数 42.0。"),
   quiz("float(42) 的结果是什么？", ["42", "42.0", "42.00", "报错"], 1, "float(42) 将整数转为浮点数，加上小数点：42.0。"))

kp(2, "py-types", "str() 类型转换",
   "str() 可以把任何类型转为字符串。这在拼接字符串时很有用。",
   "# str() 转换\nprint(str(42))         # '42'\nprint(str(3.14))       # '3.14'\nprint(str(True))       # 'True'\nprint(str(None))       # 'None'\n\n# 实际应用：数字和字符串拼接\nage = 25\nprint('年龄: ' + str(age))  # 年龄: 25",
   game_predict_output("x = 100\nprint('分数: ' + str(x))", ["分数: 100", "分数: x", "报错", "分数:100"], 0, "str(100) = '100'，然后和 '分数: ' 拼接。"),
   quiz("为什么需要 str() 转换？", ["为了计算", "为了把数字等类型变成字符串来拼接", "为了排序", "不需要"], 1, "str() 把其他类型转为字符串，方便和别的字符串拼接。"))

kp(2, "py-types", "bool() 类型转换",
   "bool() 转换规则：0、0.0、''、None、空容器 转为 False，其他都是 True。",
   "# bool() 转换\nprint(bool(0))        # False\nprint(bool(1))        # True\nprint(bool(''))       # False（空字符串）\nprint(bool('hello'))  # True\nprint(bool(None))     # False\nprint(bool([]))       # False（空列表）\nprint(bool([1, 2]))   # True",
   game_predict_output("print(bool(0))\nprint(bool(1))\nprint(bool(''))", ["True True True", "False True False", "True False True", "False False False"], 1, "bool(0)=False, bool(1)=True, bool('')=False。"),
   quiz("以下哪个 bool() 转换结果是 False？", ["bool(1)", "bool('hello')", "bool(0)", "bool([1])"], 2, "bool(0) 是 False。0、空字符串、None、空容器都是 False。"))

kp(2, "py-types", "数值运算符",
   "Python 支持 +（加）、-（减）、*（乘）、/（除）、//（整除）、%（取余）、**（幂）。",
   "# 数值运算\nprint(10 + 3)   # 13\nprint(10 - 3)   # 7\nprint(10 * 3)   # 30\nprint(10 / 3)   # 3.3333...\nprint(10 // 3)  # 3（整除）\nprint(10 % 3)   # 1（取余）\nprint(2 ** 3)   # 8（2的3次方）",
   game_predict_output("print(17 % 5)", ["2", "3", "3.4", "17"], 0, "17 % 5 = 2（17除以5余2）。"),
   quiz("10 // 3 的结果是什么？", ["3.33", "3", "4", "1"], 1, "// 是整除运算符，10 // 3 = 3（丢弃小数部分）。"))

kp(2, "py-types", "运算符优先级",
   "运算符优先级：** > * / // % > + -。不确定时用括号明确优先级。",
   "# 优先级示例\nprint(2 + 3 * 4)    # 14（先乘后加）\nprint((2 + 3) * 4)  # 20（括号优先）\nprint(2 ** 3 ** 2)  # 512（**从右往左）\nprint((2 ** 3) ** 2)  # 64",
   game_predict_output("print(2 + 3 * 4)", ["20", "14", "24", "报错"], 1, "先算 3 * 4 = 12，再算 2 + 12 = 14。乘法优先级高于加法。"),
   quiz("2 + 3 * 4 的结果是？", ["20", "14", "24", "报错"], 1, "乘法优先级高于加法：先算 3*4=12，再算 2+12=14。"))

kp(2, "py-types", "比较运算符",
   "比较运算符：==（等于）、!=（不等于）、>、<、>=、<=。结果都是布尔值。",
   "# 比较运算\nprint(5 == 5)    # True\nprint(5 != 3)    # True\nprint(10 > 7)    # True\nprint(3 >= 3)    # True\nprint(2 < 1)     # False\nprint(5 == 5.0)  # True（值相等）",
   game_predict_output("print(3 == 3.0)", ["True", "False", "报错", "3"], 0, "== 比较值，3 和 3.0 的值相等，所以是 True。"),
   quiz("5 == 5.0 的结果是什么？", ["True", "False", "报错", "5.0"], 0, "== 比较的是值是否相等，5 和 5.0 值相等，所以是 True。"))

kp(2, "py-types", "字符串拼接和重复",
   "字符串可以用 + 拼接，用 * 重复。但字符串不能和数字直接用 +。",
   "# 字符串操作\nprint('hello' + ' ' + 'world')  # hello world\nprint('ha' * 3)                  # hahaha\nprint('=' * 20)                  # ====================\n\n# 注意：字符串不能和数字直接 +\n# print('age: ' + 25)  # 报错！",
   game_predict_output("print('ab' * 3)", ["ababab", "ab 3", "报错", "abab"], 0, "'ab' * 3 重复字符串 3 次，结果是 'ababab'。"),
   quiz("'hello' * 3 的结果是什么？", ["hellohellohello", "hello 3", "报错", "hello3"], 0, "* 操作符重复字符串，'hello' * 3 = 'hellohellohello'。"))

kp(2, "py-types", "字符串索引",
   "字符串中的每个字符都有索引，从 0 开始。负索引从末尾开始，-1 是最后一个。",
   "# 字符串索引\ns = 'Python'\nprint(s[0])    # P（第一个）\nprint(s[1])    # y\nprint(s[-1])   # n（最后一个）\nprint(s[-2])   # o\nprint(len(s))  # 6（长度）",
   game_predict_output("s = 'Hello'\nprint(s[-1])", ["H", "o", "报错", "Hello"], 1, "负索引 -1 是最后一个字符，'Hello' 的最后一个是 'o'。"),
   quiz("'Python'[-1] 的结果是什么？", ["P", "n", "o", "报错"], 1, "负索引 -1 表示最后一个字符，'Python' 的最后一个是 'n'。"))

kp(2, "py-types", "字符串切片",
   "切片 [start:end] 截取子字符串。start 是起始位置（包含），end 是结束位置（不包含）。",
   "# 字符串切片\ns = 'Hello World'\nprint(s[0:5])   # Hello\nprint(s[6:])    # World（从6到末尾）\nprint(s[:5])    # Hello（从开头到5）\nprint(s[::2])   # HloWrd（步长2）",
   game_predict_output("s = 'Python'\nprint(s[1:4])", ["Pyt", "yth", "Pyth", "ytho"], 1, "s[1:4] 取索引 1、2、3 的字符，即 'yth'。"),
   quiz("'Python'[1:4] 的结果是什么？", ["Pyt", "yth", "Pyth", "ytho"], 1, "切片 [1:4] 取索引 1、2、3（不含4），结果是 'yth'。"))

kp(2, "py-types", "常用字符串方法",
   "字符串有很多内置方法：upper()、lower()、strip()、replace()、split()、find()。",
   "# 常用字符串方法\ns = '  Hello World  '\nprint(s.strip())         # 'Hello World'（去空格）\nprint(s.strip().upper()) # 'HELLO WORLD'\nprint(s.strip().lower()) # 'hello world'\nprint(s.strip().replace('World', 'Python'))  # 'Hello Python'",
   game_predict_output("s = '  hello  '\nprint(s.strip().upper())", ["  HELLO  ", "HELLO", "hello", "报错"], 1, "先 strip() 去空格，再 upper() 转大写，结果是 'HELLO'。"),
   quiz(".strip() 方法的作用是什么？", ["转大写", "去除首尾空白字符", "替换字符", "分割字符串"], 1, ".strip() 去除字符串首尾的空格、换行等空白字符。"))

kp(2, "py-types", "字符串查找和替换",
   "find() 查找子字符串的位置，replace() 替换子字符串。找不到返回 -1。",
   "# 查找和替换\ns = 'Hello World'\nprint(s.find('World'))     # 6（位置）\nprint(s.find('Python'))   # -1（找不到）\nprint(s.replace('World', 'Python'))  # 'Hello Python'\n\n# in 关键字\nprint('World' in s)  # True",
   game_predict_output("s = 'Hello World'\nprint(s.find('World'))", ["True", "6", "-1", "报错"], 1, "find() 返回子字符串的起始索引，'World' 从位置 6 开始。"),
   quiz("find() 找不到子字符串时返回什么？", ["0", "None", "-1", "报错"], 2, "find() 找不到时返回 -1，不会报错。"))

kp(2, "py-types", "字符串分割和连接",
   "split() 把字符串按分隔符拆分成列表。join() 把列表中的字符串连接起来。",
   "# 分割和连接\ns = 'apple,banana,cherry'\nfruits = s.split(',')\nprint(fruits)  # ['apple', 'banana', 'cherry']\n\n# 连接\nresult = ' - '.join(fruits)\nprint(result)  # 'apple - banana - cherry'",
   game_predict_output("s = 'a-b-c'\nparts = s.split('-')\nprint(len(parts))", ["1", "2", "3", "报错"], 2, "'a-b-c' 按 '-' 分割成 ['a', 'b', 'c']，共 3 个元素。"),
   quiz("split(',') 的作用是什么？", ["连接字符串", "按逗号分割字符串为列表", "删除逗号", "计算逗号数量"], 1, "split(',') 按逗号把字符串分割成一个列表。"))

kp(2, "py-types", "类型转换的安全性",
   "不是所有类型转换都能成功。int('hello') 会报错。要先检查或用 try/except 处理。",
   "# 安全的类型转换\ndef safe_int(value):\n    try:\n        return int(value)\n    except ValueError:\n        return None\n\nprint(safe_int('42'))     # 42\nprint(safe_int('hello'))  # None（不报错）",
   game_predict_output("try:\n    x = int('abc')\nexcept ValueError:\n    x = 0\nprint(x)", ["abc", "0", "报错", "None"], 1, "int('abc') 会报 ValueError，被 except 捕获，x = 0。"),
   quiz("int('hello') 会怎样？", ["返回 0", "返回 None", "报 ValueError", "返回 'hello'"], 2, "int('hello') 无法转换，会报 ValueError 错误。"))

kp(2, "py-types", "字符串格式化数字",
   "f-string 可以格式化数字：控制小数位数、千分位、百分比等。",
   "# 数字格式化\npi = 3.14159\nprint(f'{pi:.2f}')       # 3.14（2位小数）\nprint(f'{pi:.4f}')       # 3.1416（4位小数）\n\nmoney = 1234567\nprint(f'{money:,}')      # 1,234,567（千分位）\n\nrate = 0.856\nprint(f'{rate:.1%}')     # 85.6%（百分比）",
   game_predict_output("pi = 3.14159\nprint(f'{pi:.2f}')", ["3.14", "3.14159", "3.1416", "3.1"], 0, ":.2f 保留2位小数，四舍五入到 3.14。"),
   quiz("f'{3.14159:.2f}' 的结果是什么？", ["3.14159", "3.14", "3.1", "3.1416"], 1, ":.2f 保留2位小数，四舍五入得到 3.14。"))


# ============================================================
# WEEK 3: Python数据结构 (40 points)
# ============================================================
# module: py-lists (20 points)
# module: py-dicts (20 points)

# --- py-lists: 20 points ---

kp(3, "py-lists", "创建列表",
   "列表用方括号 [] 创建，元素用逗号分隔。列表可以包含任何类型的元素，也可以混合类型。",
   "# 创建列表\nfruits = ['苹果', '香蕉', '橙子']\nnumbers = [1, 2, 3, 4, 5]\nmixed = [1, 'hello', True, 3.14]\nempty = []\n\nprint(fruits)    # ['苹果', '香蕉', '橙子']\nprint(len(fruits))  # 3",
   game_predict_output("lst = [1, 'two', 3.0]\nprint(len(lst))", ["1", "2", "3", "报错"], 2, "列表有3个元素，len() 返回 3。"),
   quiz("如何创建一个空列表？", ["{}", "[]", "()", "''"], 1, "[] 创建空列表。{} 是空字典，() 是空元组，'' 是空字符串。"))

kp(3, "py-lists", "列表索引",
   "列表和字符串一样，用索引访问元素。索引从 0 开始，负索引从末尾开始。",
   "# 列表索引\nfruits = ['苹果', '香蕉', '橙子', '葡萄']\nprint(fruits[0])    # 苹果（第一个）\nprint(fruits[1])    # 香蕉\nprint(fruits[-1])   # 葡萄（最后一个）\nprint(fruits[-2])   # 橙子",
   game_predict_output("lst = [10, 20, 30, 40]\nprint(lst[2])", ["10", "20", "30", "40"], 2, "索引 2 是第三个元素，即 30。"),
   quiz("[10, 20, 30][1] 的结果是什么？", ["10", "20", "30", "报错"], 1, "索引 1 是第二个元素，即 20。"))

kp(3, "py-lists", "列表切片",
   "切片 [start:end] 获取子列表。start 包含，end 不包含。可以省略 start 或 end。",
   "# 列表切片\nnums = [0, 1, 2, 3, 4, 5]\nprint(nums[1:4])   # [1, 2, 3]\nprint(nums[:3])    # [0, 1, 2]\nprint(nums[3:])    # [3, 4, 5]\nprint(nums[::2])   # [0, 2, 4]（步长2）\nprint(nums[::-1])  # [5, 4, 3, 2, 1, 0]（反转）",
   game_predict_output("lst = [1, 2, 3, 4, 5]\nprint(lst[1:3])", ["[1, 2]", "[2, 3]", "[1, 2, 3]", "[2, 3, 4]"], 1, "lst[1:3] 取索引 1 和 2（不含3），结果是 [2, 3]。"),
   quiz("[1, 2, 3, 4, 5][1:3] 的结果是什么？", ["[1, 2]", "[2, 3]", "[1, 2, 3]", "[2, 3, 4]"], 1, "切片 [1:3] 取索引 1 和 2（不含 3），结果是 [2, 3]。"))

kp(3, "py-lists", "修改列表元素",
   "列表是可变的，可以通过索引直接修改元素。字符串不能这样修改。",
   "# 修改列表元素\nfruits = ['苹果', '香蕉', '橙子']\nfruits[1] = '芒果'  # 把香蕉改成芒果\nprint(fruits)  # ['苹果', '芒果', '橙子']\n\n# 也可以修改切片\nfruits[0:2] = ['西瓜', '草莓']\nprint(fruits)  # ['西瓜', '草莓', '橙子']",
   game_predict_output("lst = [1, 2, 3]\nlst[0] = 10\nprint(lst)", ["[1, 2, 3]", "[10, 2, 3]", "[1, 10, 3]", "报错"], 1, "lst[0] = 10 把第一个元素从 1 改为 10，结果是 [10, 2, 3]。"),
   quiz("列表能通过索引修改元素吗？", ["能", "不能", "只有第一个能", "看情况"], 0, "列表是可变类型，可以通过索引直接修改元素的值。"))

kp(3, "py-lists", "append() 添加元素",
   "append() 在列表末尾添加一个元素。这是最常用的列表操作之一。",
   "# append 添加元素\nfruits = ['苹果', '香蕉']\nfruits.append('橙子')\nprint(fruits)  # ['苹果', '香蕉', '橙子']\n\nfruits.append('葡萄')\nprint(fruits)  # ['苹果', '香蕉', '橙子', '葡萄']",
   game_predict_output("lst = [1, 2]\nlst.append(3)\nlst.append(4)\nprint(lst)", ["[1, 2]", "[1, 2, 3]", "[1, 2, 3, 4]", "[4, 3, 2, 1]"], 2, "两次 append 分别添加 3 和 4，结果是 [1, 2, 3, 4]。"),
   quiz("append() 的作用是什么？", ["在开头添加元素", "在末尾添加元素", "删除元素", "排序"], 1, "append() 在列表末尾添加一个新元素。"))

kp(3, "py-lists", "insert() 插入元素",
   "insert(index, element) 在指定位置插入元素。原来位置及后面的元素往后移。",
   "# insert 插入元素\nfruits = ['苹果', '橙子']\nfruits.insert(1, '香蕉')  # 在索引1处插入\nprint(fruits)  # ['苹果', '香蕉', '橙子']\n\nfruits.insert(0, '西瓜')  # 在开头插入\nprint(fruits)  # ['西瓜', '苹果', '香蕉', '橙子']",
   game_predict_output("lst = [1, 3, 4]\nlst.insert(1, 2)\nprint(lst)", ["[2, 1, 3, 4]", "[1, 2, 3, 4]", "[1, 3, 2, 4]", "报错"], 1, "insert(1, 2) 在索引1处插入2，原元素后移，结果是 [1, 2, 3, 4]。"),
   quiz("insert(1, 'x') 在哪里插入？", ["开头", "索引1的位置", "末尾", "报错"], 1, "insert(index, element) 在指定索引位置插入元素。"))

kp(3, "py-lists", "remove() 和 pop()",
   "remove(value) 按值删除第一个匹配项。pop(index) 按索引删除并返回该元素。",
   "# remove 和 pop\nfruits = ['苹果', '香蕉', '橙子', '香蕉']\nfruits.remove('香蕉')  # 删除第一个'香蕉'\nprint(fruits)  # ['苹果', '橙子', '香蕉']\n\nlast = fruits.pop()  # 删除并返回最后一个\nprint(last)    # 香蕉\nprint(fruits)  # ['苹果', '橙子']",
   game_predict_output("lst = [1, 2, 3, 4]\nlst.pop()\nprint(lst)", ["[1, 2, 3, 4]", "[1, 2, 3]", "[2, 3, 4]", "[1, 2, 4]"], 1, "pop() 不带参数时删除并返回最后一个元素，结果是 [1, 2, 3]。"),
   quiz("pop() 不指定索引时删除哪个元素？", ["第一个", "最后一个", "随机", "报错"], 1, "pop() 不指定索引时删除并返回最后一个元素。"))

kp(3, "py-lists", "列表排序",
   "sort() 原地排序（修改原列表）。sorted() 返回新列表，不修改原列表。reverse=True 降序。",
   "# 列表排序\nnums = [3, 1, 4, 1, 5, 9]\nnums.sort()\nprint(nums)  # [1, 1, 3, 4, 5, 9]\n\n# 降序\nnums.sort(reverse=True)\nprint(nums)  # [9, 5, 4, 3, 1, 1]\n\n# sorted() 不修改原列表\noriginal = [3, 1, 2]\nnew_list = sorted(original)\nprint(original)  # [3, 1, 2]\nprint(new_list)  # [1, 2, 3]",
   game_predict_output("lst = [3, 1, 2]\nlst.sort()\nprint(lst)", ["[3, 1, 2]", "[1, 2, 3]", "[3, 2, 1]", "报错"], 1, "sort() 原地排序，从小到大：[1, 2, 3]。"),
   quiz("sort() 和 sorted() 的区别是什么？", ["完全一样", "sort() 修改原列表，sorted() 返回新列表", "sort() 返回新列表", "sorted() 修改原列表"], 1, "sort() 原地排序修改原列表，sorted() 返回新列表不修改原列表。"))

kp(3, "py-lists", "列表反转",
   "reverse() 原地反转列表。也可以用切片 [::-1] 创建反转的新列表。",
   "# 列表反转\nnums = [1, 2, 3, 4, 5]\nnums.reverse()\nprint(nums)  # [5, 4, 3, 2, 1]\n\n# 用切片反转（不修改原列表）\noriginal = [1, 2, 3]\nreversed_list = original[::-1]\nprint(original)      # [1, 2, 3]\nprint(reversed_list)  # [3, 2, 1]",
   game_predict_output("lst = [1, 2, 3]\nlst.reverse()\nprint(lst)", ["[1, 2, 3]", "[3, 2, 1]", "[2, 1, 3]", "报错"], 1, "reverse() 原地反转，[1, 2, 3] 变成 [3, 2, 1]。"),
   quiz("reverse() 的作用是什么？", ["排序", "原地反转列表", "删除元素", "复制列表"], 1, "reverse() 原地反转列表中元素的顺序。"))

kp(3, "py-lists", "列表长度和统计",
   "len() 获取长度，count() 统计某个元素出现的次数，index() 查找元素的位置。",
   "# 长度和统计\nnums = [1, 2, 3, 2, 4, 2]\nprint(len(nums))       # 6\nprint(nums.count(2))   # 3（2出现了3次）\nprint(nums.index(3))   # 2（3在索引2）",
   game_predict_output("lst = [1, 2, 2, 3, 2]\nprint(lst.count(2))", ["1", "2", "3", "报错"], 2, "count(2) 统计 2 出现的次数，共 3 次。"),
   quiz("[1, 2, 2, 3].count(2) 的结果是什么？", ["1", "2", "3", "报错"], 1, "count(2) 统计 2 出现的次数，[1, 2, 2, 3] 中 2 出现了 2 次。"))

kp(3, "py-lists", "列表遍历",
   "用 for 循环遍历列表中的每个元素。这是处理列表最常用的方式。",
   "# 遍历列表\nfruits = ['苹果', '香蕉', '橙子']\nfor fruit in fruits:\n    print(f'我喜欢{fruit}')\n\n# 带索引遍历\nfor i, fruit in enumerate(fruits):\n    print(f'{i}: {fruit}')",
   game_predict_output("lst = [10, 20, 30]\nfor x in lst:\n    print(x * 2)", ["20 40 60", "10 20 30", "报错", "20 40 60（一行）"], 0, "遍历列表，每个元素乘以2：20、40、60（每行一个）。"),
   quiz("遍历列表用什么语句？", ["while", "for...in", "if", "def"], 1, "for...in 是遍历列表的标准方式，依次取出每个元素。"))

kp(3, "py-lists", "列表推导式基础",
   "列表推导式是创建列表的简洁方式。格式：[表达式 for 变量 in 可迭代对象]。",
   "# 列表推导式\n# 传统方式\nsquares = []\nfor i in range(5):\n    squares.append(i ** 2)\nprint(squares)  # [0, 1, 4, 9, 16]\n\n# 推导式（更简洁）\nsquares2 = [i ** 2 for i in range(5)]\nprint(squares2)  # [0, 1, 4, 9, 16]",
   game_predict_output("result = [x * 2 for x in [1, 2, 3]]\nprint(result)", ["[1, 2, 3]", "[2, 4, 6]", "[2, 3, 4]", "报错"], 1, "列表推导式对每个元素乘以2：[2, 4, 6]。"),
   quiz("[x + 1 for x in [1, 2, 3]] 的结果是什么？", ["[1, 2, 3]", "[2, 3, 4]", "[1, 1, 1]", "报错"], 1, "每个元素加1：1+1=2, 2+1=3, 3+1=4，结果是 [2, 3, 4]。"))

kp(3, "py-lists", "带条件的列表推导式",
   "推导式可以加 if 条件过滤元素。格式：[表达式 for 变量 in 可迭代对象 if 条件]。",
   "# 带条件的推导式\n# 筛选偶数\nevens = [x for x in range(10) if x % 2 == 0]\nprint(evens)  # [0, 2, 4, 6, 8]\n\n# 筛选长度大于3的名字\nnames = ['Bob', 'Alice', 'Tom', 'David']\nlong_names = [n for n in names if len(n) > 3]\nprint(long_names)  # ['Alice', 'David']",
   game_predict_output("result = [x for x in [1, 2, 3, 4, 5] if x > 3]\nprint(result)", ["[4, 5]", "[1, 2, 3]", "[3, 4, 5]", "报错"], 0, "过滤出大于3的元素：4 和 5。"),
   quiz("[x for x in [1,2,3,4] if x % 2 == 0] 的结果是什么？", ["[1, 3]", "[2, 4]", "[1, 2, 3, 4]", "报错"], 1, "筛选偶数：2 和 4，结果是 [2, 4]。"))

kp(3, "py-lists", "嵌套列表",
   "列表可以包含其他列表，形成嵌套结构。常用于表示矩阵（二维数据）。",
   "# 嵌套列表（矩阵）\nmatrix = [\n    [1, 2, 3],\n    [4, 5, 6],\n    [7, 8, 9]\n]\nprint(matrix[0])      # [1, 2, 3]（第一行）\nprint(matrix[0][1])   # 2（第一行第二列）\nprint(matrix[1][2])   # 6（第二行第三列）",
   game_predict_output("m = [[1, 2], [3, 4]]\nprint(m[1][0])", ["1", "2", "3", "4"], 2, "m[1] 是 [3, 4]，m[1][0] 是 3。"),
   quiz("[[1,2],[3,4]][1][1] 的结果是什么？", ["1", "2", "3", "4"], 3, "[1] 是 [3,4]，[1][1] 是 4。"))

kp(3, "py-lists", "列表合并",
   "用 + 合并两个列表，用 extend() 把一个列表的元素添加到另一个列表。",
   "# 合并列表\nlist1 = [1, 2, 3]\nlist2 = [4, 5, 6]\n\n# 用 +\ncombined = list1 + list2\nprint(combined)  # [1, 2, 3, 4, 5, 6]\n\n# 用 extend()\nlist1.extend(list2)\nprint(list1)  # [1, 2, 3, 4, 5, 6]",
   game_predict_output("a = [1, 2]\nb = [3, 4]\nprint(a + b)", ["[1, 2]", "[3, 4]", "[1, 2, 3, 4]", "报错"], 2, "+ 合并两个列表，结果是 [1, 2, 3, 4]。"),
   quiz("[1,2] + [3,4] 的结果是什么？", ["[1, 2, 3, 4]", "[4, 6]", "[[1,2], [3,4]]", "报错"], 0, "+ 合并列表，结果是 [1, 2, 3, 4]。"))

kp(3, "py-lists", "列表成员检测",
   "用 in 关键字检查元素是否在列表中。返回 True 或 False。",
   "# 成员检测\nfruits = ['苹果', '香蕉', '橙子']\nprint('苹果' in fruits)    # True\nprint('葡萄' in fruits)    # False\nprint('葡萄' not in fruits)  # True\n\n# 在 if 中使用\nif '苹果' in fruits:\n    print('有苹果！')",
   game_predict_output("lst = [1, 2, 3]\nprint(2 in lst)\nprint(5 in lst)", ["True True", "False False", "True False", "False True"], 2, "2 在列表中 → True，5 不在 → False。"),
   quiz("2 in [1, 2, 3] 的结果是什么？", ["True", "False", "2", "报错"], 0, "in 检查元素是否在列表中，2 在 [1, 2, 3] 中，所以是 True。"))

kp(3, "py-lists", "列表复制",
   "直接赋值不会复制列表（只是引用）。要用 copy() 或切片 [:] 来真正复制。",
   "# 列表复制\noriginal = [1, 2, 3]\n\n# 错误方式（引用）\nref = original\nref.append(4)\nprint(original)  # [1, 2, 3, 4]  原列表也变了！\n\n# 正确方式（复制）\noriginal = [1, 2, 3]\ncopy = original.copy()  # 或 original[:]\ncopy.append(4)\nprint(original)  # [1, 2, 3]  原列表不变",
   game_find_bug(
       ["original = [1, 2, 3]", "copy = original", "copy.append(4)", "print(original)"],
       2, "copy = original 只是引用，不是复制。应该用 copy = original.copy()。"
   ),
   quiz("如何真正复制一个列表？", ["new = old", "new = old.copy()", "new = old[0]", "new = list(old[0])"], 1, "用 .copy() 或 [:] 切片来创建列表的真正副本。"))

kp(3, "py-lists", "列表解包",
   "列表解包可以把列表中的元素赋给多个变量。变量数量要匹配。",
   "# 列表解包\npoint = [3, 5]\nx, y = point\nprint(f'x={x}, y={y}')  # x=3, y=5\n\n# 用 * 收集剩余元素\nfirst, *rest = [1, 2, 3, 4, 5]\nprint(first)  # 1\nprint(rest)   # [2, 3, 4, 5]",
   game_predict_output("a, b, c = [10, 20, 30]\nprint(b)", ["10", "20", "30", "报错"], 1, "解包：a=10, b=20, c=30，print(b) 输出 20。"),
   quiz("a, b = [1, 2, 3] 会怎样？", ["a=1, b=2", "a=1, b=[2,3]", "报错", "a=[1,2,3]"], 2, "变量数量和元素数量不匹配会报 ValueError。需要 a, b, c = [1, 2, 3]。"))

kp(3, "py-lists", "列表常用内置函数",
   "sum() 求和，max() 最大值，min() 最小值，len() 长度，sorted() 排序。",
   "# 列表常用函数\nnums = [3, 1, 4, 1, 5, 9]\nprint(sum(nums))      # 23\nprint(max(nums))      # 9\nprint(min(nums))      # 1\nprint(len(nums))      # 6\nprint(sorted(nums))   # [1, 1, 3, 4, 5, 9]",
   game_predict_output("lst = [10, 20, 30]\nprint(sum(lst) / len(lst))", ["20.0", "60", "30", "报错"], 0, "sum = 60, len = 3, 60 / 3 = 20.0。"),
   quiz("sum([1, 2, 3, 4]) 的结果是什么？", ["10", "4", "24", "报错"], 0, "sum() 求所有元素的和：1+2+3+4 = 10。"))


# --- py-dicts: 20 points ---

kp(3, "py-dicts", "创建字典",
   "字典用花括号 {} 创建，包含键值对。格式：{key: value, key: value}。键必须是不可变类型。",
   "# 创建字典\nstudent = {\n    'name': '小明',\n    'age': 20,\n    'score': 95\n}\nprint(student)  # {'name': '小明', 'age': 20, 'score': 95}\n\n# 空字典\nempty = {}",
   game_predict_output("d = {'a': 1, 'b': 2}\nprint(len(d))", ["1", "2", "3", "报错"], 1, "字典有2个键值对，len() 返回 2。"),
   quiz("字典用什么符号创建？", ["[]", "{}", "()", "<>"], 1, "字典用花括号 {} 创建，包含键值对。"))

kp(3, "py-dicts", "字典访问值",
   "用键来访问字典的值。用 d[key] 或 d.get(key)。get() 在键不存在时返回 None 而不是报错。",
   "# 访问字典值\nperson = {'name': '小明', 'age': 20}\nprint(person['name'])     # 小明\nprint(person['age'])      # 20\n\n# get() 更安全\nprint(person.get('name'))  # 小明\nprint(person.get('phone'))  # None（不报错）\nprint(person.get('phone', '无'))  # 无（默认值）",
   game_predict_output("d = {'x': 10, 'y': 20}\nprint(d['x'])", ["10", "20", "x", "报错"], 0, "用键 'x' 访问字典，得到对应的值 10。"),
   quiz("字典中用什么来获取值？", ["索引", "键（key）", "位置", "类型"], 1, "字典用键（key）来访问对应的值（value）。"))

kp(3, "py-dicts", "添加和修改键值对",
   "用 d[key] = value 添加新键值对或修改已有键的值。",
   "# 添加和修改\nstudent = {'name': '小明'}\n\n# 添加\nstudent['age'] = 20\nprint(student)  # {'name': '小明', 'age': 20}\n\n# 修改\nstudent['age'] = 21\nprint(student)  # {'name': '小明', 'age': 21}",
   game_predict_output("d = {'a': 1}\nd['b'] = 2\nd['a'] = 10\nprint(d)", ["{'a': 1, 'b': 2}", "{'a': 10, 'b': 2}", "{'a': 10}", "报错"], 1, "添加 b=2，修改 a=10，结果是 {'a': 10, 'b': 2}。"),
   quiz("d['new_key'] = value 在键不存在时会怎样？", ["报错", "创建新的键值对", "忽略", "返回 None"], 1, "键不存在时会创建新的键值对。"))

kp(3, "py-dicts", "删除键值对",
   "用 del 删除指定键值对，用 pop() 删除并返回值，用 clear() 清空字典。",
   "# 删除键值对\nstudent = {'name': '小明', 'age': 20, 'score': 95}\n\n# del 删除\ndel student['score']\nprint(student)  # {'name': '小明', 'age': 20}\n\n# pop 删除并返回\nage = student.pop('age')\nprint(age)      # 20\nprint(student)  # {'name': '小明'}",
   game_predict_output("d = {'a': 1, 'b': 2, 'c': 3}\ndel d['b']\nprint(d)", ["{'a': 1, 'c': 3}", "{'a': 1, 'b': 2}", "{'a': 1, 'b': 2, 'c': 3}", "报错"], 0, "del d['b'] 删除键 'b' 及其值，剩下 {'a': 1, 'c': 3}。"),
   quiz("del d['key'] 的作用是什么？", ["删除整个字典", "删除指定键值对", "清空字典", "报错"], 1, "del d['key'] 删除字典中指定键及其对应的值。"))

kp(3, "py-dicts", "字典遍历",
   "遍历字典可以用 keys()、values()、items()。items() 同时获取键和值。",
   "# 遍历字典\nstudent = {'name': '小明', 'age': 20, 'score': 95}\n\n# 遍历键\nfor key in student.keys():\n    print(key)\n\n# 遍历值\nfor value in student.values():\n    print(value)\n\n# 遍历键值对\nfor key, value in student.items():\n    print(f'{key}: {value}')",
   game_predict_output("d = {'a': 1, 'b': 2}\nfor k, v in d.items():\n    print(v)", ["1 2", "a b", "报错", "1"], 0, "items() 返回键值对，v 是值，输出 1 和 2（每行一个）。"),
   quiz("items() 返回什么？", ["只返回键", "只返回值", "返回键值对的元组", "返回列表"], 2, "items() 返回字典的键值对，每个元素是一个 (key, value) 元组。"))

kp(3, "py-dicts", "字典推导式",
   "字典推导式类似列表推导式，用 {key: value for ...} 创建字典。",
   "# 字典推导式\n# 数字和它的平方\nsquares = {x: x**2 for x in range(5)}\nprint(squares)  # {0: 0, 1: 1, 2: 4, 3: 9, 4: 16}\n\n# 带条件\neven_squares = {x: x**2 for x in range(10) if x % 2 == 0}\nprint(even_squares)  # {0: 0, 2: 4, 4: 16, 6: 36, 8: 64}",
   game_predict_output("d = {k: k*2 for k in [1, 2, 3]}\nprint(d)", ["{1: 2, 2: 4, 3: 6}", "{1: 1, 2: 2, 3: 3}", "[2, 4, 6]", "报错"], 0, "字典推导式：1→2, 2→4, 3→6。"),
   quiz("{x: x+1 for x in [1, 2]} 的结果是什么？", ["{1: 2, 2: 3}", "{2: 3}", "[2, 3]", "报错"], 0, "1→1+1=2, 2→2+1=3，结果是 {1: 2, 2: 3}。"))

kp(3, "py-dicts", "字典的 in 操作",
   "in 检查的是键（不是值）。如果要检查值，用 value in d.values()。",
   "# 检查键是否存在\nstudent = {'name': '小明', 'age': 20}\nprint('name' in student)     # True\nprint('小明' in student)     # False（检查的是键）\nprint('小明' in student.values())  # True（检查值）",
   game_predict_output("d = {'a': 1, 'b': 2}\nprint('a' in d)\nprint(1 in d)", ["True True", "True False", "False True", "False False"], 1, "'a' 是键 → True。1 是值不是键 → False。"),
   quiz("1 in {'a': 1, 'b': 2} 的结果是什么？", ["True", "False", "报错", "1"], 1, "in 检查的是键。1 不是键（'a' 和 'b' 才是），所以是 False。"))

kp(3, "py-dicts", "字典合并",
   "用 update() 合并两个字典。如果有相同的键，后面的值会覆盖前面的。",
   "# 合并字典\nd1 = {'a': 1, 'b': 2}\nd2 = {'b': 3, 'c': 4}\nd1.update(d2)\nprint(d1)  # {'a': 1, 'b': 3, 'c': 4}\n# 'b' 的值被 d2 覆盖了",
   game_predict_output("d1 = {'x': 1}\nd2 = {'y': 2}\nd1.update(d2)\nprint(d1)", ["{'x': 1}", "{'y': 2}", "{'x': 1, 'y': 2}", "报错"], 2, "update() 把 d2 的键值对添加到 d1 中，结果是 {'x': 1, 'y': 2}。"),
   quiz("两个字典有相同键时，update() 会怎样？", ["报错", "后面的值覆盖前面的", "保留前面的", "创建两个键"], 1, "有相同键时，update() 用后面的值覆盖前面的值。"))

kp(3, "py-dicts", "嵌套字典",
   "字典的值可以是任何类型，包括另一个字典。这叫嵌套字典。",
   "# 嵌套字典\nstudents = {\n    '小明': {'age': 20, 'score': 95},\n    '小红': {'age': 19, 'score': 88}\n}\n\n# 访问嵌套值\nprint(students['小明']['age'])    # 20\nprint(students['小红']['score'])  # 88",
   game_predict_output("d = {'a': {'x': 1}, 'b': {'x': 2}}\nprint(d['b']['x'])", ["1", "2", "报错", "{'x': 2}"], 1, "d['b'] 是 {'x': 2}，d['b']['x'] 是 2。"),
   quiz("访问嵌套字典 students['小明']['age'] 的顺序是？", ["先值后键", "先外层键，再内层键", "同时访问", "随机"], 1, "先用外层键 ['小明'] 获取内层字典，再用内层键 ['age'] 获取值。"))

kp(3, "py-dicts", "字典的 setdefault",
   "setdefault(key, default)：如果键存在，返回对应的值；如果不存在，设置默认值并返回。",
   "# setdefault\nconfig = {'theme': 'dark'}\n\n# 键存在，返回已有值\ntheme = config.setdefault('theme', 'light')\nprint(theme)   # dark（不改变）\n\n# 键不存在，设置默认值\nlang = config.setdefault('language', 'zh')\nprint(lang)    # zh（新增）\nprint(config)  # {'theme': 'dark', 'language': 'zh'}",
   game_predict_output("d = {'a': 1}\nd.setdefault('a', 10)\nd.setdefault('b', 20)\nprint(d)", ["{'a': 1}", "{'a': 10, 'b': 20}", "{'a': 1, 'b': 20}", "报错"], 2, "'a' 已存在不改变，'b' 不存在则设置为 20。"),
   quiz("setdefault 和直接赋值的区别是什么？", ["完全一样", "setdefault 不覆盖已有值", "setdefault 更快", "没有区别"], 1, "setdefault 只在键不存在时才设置默认值，不会覆盖已有的值。"))

kp(3, "py-dicts", "字典的 get 方法",
   "get(key, default) 安全地获取值。键存在返回值，不存在返回 default（默认 None）。",
   "# get 方法\nstudent = {'name': '小明', 'age': 20}\n\nprint(student.get('name'))          # 小明\nprint(student.get('phone'))         # None\nprint(student.get('phone', '未知'))  # 未知\n\n# 对比直接访问\n# print(student['phone'])  # KeyError!",
   game_predict_output("d = {'x': 10}\nprint(d.get('x'))\nprint(d.get('y', 0))", ["10 和 0", "10 和 None", "None 和 None", "报错"], 0, "get('x') 返回 10，get('y', 0) 键不存在返回默认值 0。"),
   quiz("get('key', 'default') 在键不存在时返回什么？", ["None", "'default'", "报错", "0"], 1, "get 方法在键不存在时返回指定的默认值。"))

kp(3, "py-dicts", "字典的键的限制",
   "字典的键必须是不可变类型：数字、字符串、元组。列表和字典不能作为键。",
   "# 键的限制\n# 合法的键\nd = {\n    1: '数字键',\n    'name': '字符串键',\n    (1, 2): '元组键'\n}\nprint(d['name'])     # 字符串键\nprint(d[(1, 2)])     # 元组键\n\n# 不合法的键\n# {[1,2]: 'test'}  # TypeError: 列表不能做键",
   game_find_bug(
       ["key = [1, 2]", "d = {key: 'value'}", "print(d)"],
       2, "列表是可变类型，不能作为字典的键。应该用元组：key = (1, 2)。"
   ),
   quiz("以下哪个不能作为字典的键？", ["数字", "字符串", "列表", "元组"], 2, "列表是可变类型，不能作为字典的键。数字、字符串、元组都可以。"))

kp(3, "py-dicts", "字典的 copy",
   "和列表一样，字典也需要用 copy() 来真正复制。直接赋值只是引用。",
   "# 字典复制\nd1 = {'a': 1, 'b': 2}\nd2 = d1           # 引用（不是复制）\nd2['c'] = 3\nprint(d1)          # {'a': 1, 'b': 2, 'c': 3} d1 也变了！\n\n# 正确复制\nd1 = {'a': 1, 'b': 2}\nd3 = d1.copy()\nd3['c'] = 3\nprint(d1)          # {'a': 1, 'b': 2}  d1 不变",
   game_find_bug(
       ["original = {'a': 1}", "copy = original", "copy['b'] = 2", "print(original)"],
       2, "copy = original 只是引用。应该用 copy = original.copy() 来真正复制。"
   ),
   quiz("d2 = d1 之后修改 d2，d1 会怎样？", ["不变", "也会变（是同一个对象）", "报错", "变成 None"], 1, "d2 = d1 只是引用同一个字典对象，修改 d2 也会影响 d1。"))

kp(3, "py-dicts", "字典的 popitem",
   "popitem() 删除并返回字典中最后一个键值对。字典为空时会报错。",
   "# popitem\nconfig = {'host': 'localhost', 'port': 8080, 'debug': True}\n\nlast = config.popitem()\nprint(last)     # ('debug', True)\nprint(config)   # {'host': 'localhost', 'port': 8080}",
   game_predict_output("d = {'a': 1, 'b': 2}\nitem = d.popitem()\nprint(item)", ["('a', 1)", "('b', 2)", "b", "报错"], 1, "popitem() 返回最后插入的键值对 ('b', 2)。"),
   quiz("popitem() 返回什么？", ["只返回键", "只返回值", "返回键值对元组", "返回 None"], 2, "popitem() 返回一个 (key, value) 元组。"))

kp(3, "py-dicts", "用字典计数",
   "字典非常适合用来计数。遍历数据，用字典记录每个元素出现的次数。",
   "# 用字典统计字符频率\ntext = 'hello'\nfreq = {}\nfor char in text:\n    freq[char] = freq.get(char, 0) + 1\nprint(freq)  # {'h': 1, 'e': 1, 'l': 2, 'o': 1}",
   game_predict_output("text = 'abc'\nresult = {}\nfor c in text:\n    result[c] = result.get(c, 0) + 1\nprint(result)", ["{'a': 1, 'b': 1, 'c': 1}", "{'a': 3}", "报错", "3"], 0, "每个字符各出现1次，结果是 {'a': 1, 'b': 1, 'c': 1}。"),
   quiz("用字典计数时，get(c, 0) + 1 的作用是什么？", ["删除元素", "如果键不存在返回0，存在则加1", "总是返回1", "报错"], 1, "get(c, 0) 在键不存在时返回 0，存在时返回当前值，然后 +1 更新计数。"))

kp(3, "py-dicts", "字典 vs 列表的选择",
   "列表适合有序数据、需要索引。字典适合键值映射、需要快速查找。根据需求选择。",
   "# 列表 vs 字典\n# 列表：有序，用索引访问\nscores_list = [85, 90, 78, 92]\nprint(scores_list[0])  # 85\n\n# 字典：键值映射，用键访问\nscores_dict = {'小明': 85, '小红': 90, '小华': 78}\nprint(scores_dict['小明'])  # 85",
   game_predict_output("students = {'小明': 90, '小红': 85}\nprint(students['小红'])", ["90", "85", "小红", "报错"], 1, "用键 '小红' 访问字典，得到值 85。"),
   quiz("什么时候用字典比列表更好？", ["数据有序时", "需要按名字/键快速查找时", "数据量小时", "都不好"], 1, "需要按键（如名字）快速查找值时，字典比列表更合适。"))


# ============================================================
# GENERATE OUTPUT
# ============================================================

def main():
    output_dir = Path(__file__).parent / "data"
    output_dir.mkdir(exist_ok=True)
    output_path = output_dir / "kp_weeks_1_3.json"

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(ALL_KP, f, ensure_ascii=False, indent=2)

    # Summary
    print(f"Total knowledge points: {len(ALL_KP)}")
    for w in range(1, 4):
        week_pts = [p for p in ALL_KP if p["week"] == w]
        print(f"  Week {w}: {len(week_pts)} points")
        modules = {}
        for p in week_pts:
            modules.setdefault(p["module"], []).append(p)
        for mod, pts in modules.items():
            print(f"    {mod}: {len(pts)} points")

    games = [p["game"] for p in ALL_KP if isinstance(p.get("game"), dict)]
    print(f"\nStructured games: {len(games)}")
    game_types = {}
    for g in games:
        t = g["type"]
        game_types[t] = game_types.get(t, 0) + 1
    for t, c in sorted(game_types.items()):
        print(f"  {t}: {c}")

    print(f"\nSaved to: {output_path}")


if __name__ == "__main__":
    main()
