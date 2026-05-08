"""
Generate knowledge points for Weeks 4-6.
Week 4: Python控制流 (control-flow, loops)
Week 5: Python函数 (functions, closures)
Week 6: Python面向对象 (classes, inheritance)

Output: web/backend/data/kp_weeks_4_6.json
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
# WEEK 4: Python控制流
# ============================================================

# --- py-control-flow (20 points) ---

add(4, "py-control-flow", "if 语句基础",
    "if 语句是最基本的条件判断。如果条件为 True，就执行缩进的代码块。Python用缩进而非花括号表示代码块。",
    "age = 18\nif age >= 18:\n    print('你是成年人')",
    po("这段代码输出什么？",
       "age = 18\nif age >= 18:\n    print('你是成年人')",
       ["什么都不输出", "你是成年人", "报错", "None"],
       1, "age=18满足>=18的条件，所以执行print。"),
    quiz("if 语句中条件为 True 时会怎样？",
         ["跳过代码块", "执行缩进的代码块", "报错", "结束程序"],
         1, "条件为True时执行if后面的缩进代码块。"))

add(4, "py-control-flow", "if-else 双分支",
    "if-else 提供两个分支：条件为True执行if块，否则执行else块。确保所有情况都被处理。",
    "score = 55\nif score >= 60:\n    print('及格')\nelse:\n    print('不及格')",
    fb("找出代码中的错误",
       ["score = 55", "if score >= 60:", "    print('及格')", "else", "    print('不及格')"],
       3, "第4行else后面缺少冒号，应改为 else:。"),
    quiz("if-else 中 else 需要写条件吗？",
         ["需要", "不需要，else处理所有其他情况", "看情况", "必须写条件"],
         1, "else不需要条件，处理所有不满足if条件的情况。"))

add(4, "py-control-flow", "if-elif-else 多分支",
    "elif 是 else if 的缩写，用于多个条件判断。从上到下依次检查，第一个为True的分支被执行。",
    "score = 85\nif score >= 90:\n    print('优秀')\nelif score >= 80:\n    print('良好')\nelif score >= 60:\n    print('及格')\nelse:\n    print('不及格')",
    fl("填写关键字",
       "score = 85\nif score >= 90:\n    print('优秀')\n___ score >= 80:\n    print('良好')\nelif score >= 60:\n    print('及格')\nelse:\n    print('不及格')",
       [{"position": 0, "answer": "elif", "options": ["elif", "else if", "elseif", "or if"]}],
       "Python中多分支用elif，不是else if。"),
    quiz("elif 的含义是什么？",
         ["结束判断", "else if 的缩写", "额外的if", "必须的条件"],
         1, "elif是else if的缩写，用于检查多个条件。"))

add(4, "py-control-flow", "嵌套 if",
    "if 语句可以嵌套使用，在一个if块内部再写if语句。用于需要同时满足多个条件的场景。",
    "age = 25\nhas_id = True\nif age >= 18:\n    if has_id:\n        print('允许进入')\n    else:\n        print('请出示证件')\nelse:\n    print('未成年禁止进入')",
    co("排列代码到正确顺序",
       ["    else:", "        print('未成年禁止进入')", "    if has_id:", "        print('请出示证件')", "        print('允许进入')", "else:", "if age >= 18:"],
       [6, 2, 4, 0, 3, 5, 1],
       "正确顺序：外层if -> 内层if -> 内层else -> 外层else。"),
    quiz("嵌套if的作用是什么？",
         ["加速执行", "同时满足多个条件", "减少代码", "避免错误"],
         1, "嵌套if用于需要同时满足多个条件的场景。"))

add(4, "py-control-flow", "比较运算符",
    "Python的比较运算符：==（等于）、!=（不等于）、>、<、>=、<=。比较结果是布尔值True或False。",
    "a = 10\nb = 20\nprint(a == b)   # False\nprint(a != b)   # True\nprint(a < b)    # True",
    po("这段代码输出什么？",
       "a = 10\nb = 20\nprint(a == b)\nprint(a != b)\nprint(a < b)",
       ["True True True", "False True True", "False False True", "报错"],
       1, "10不等于20所以==为False，!=为True，10<20为True。"),
    quiz("a == b 和 a = b 的区别是什么？",
         ["没有区别", "==是比较，=是赋值", "==是赋值，=是比较", "都是比较"],
         1, "==是比较运算符，检查是否相等；=是赋值运算符。"))

add(4, "py-control-flow", "逻辑运算符 and",
    "and 运算符：两边都为True才返回True。第一个为False就短路返回False，不计算右边。",
    "age = 25\nincome = 8000\nif age >= 18 and income >= 5000:\n    print('符合申请条件')",
    fb("找出代码中的错误",
       ["age = 25", "income = 8000", "if age >= 18 & income >= 5000:", "    print('符合申请条件')"],
       2, "第3行用了&（位运算符），应该用and（逻辑运算符）。改为 if age >= 18 and income >= 5000:。"),
    quiz("True and False 的结果是什么？",
         ["True", "False", "None", "报错"],
         1, "and两边都为True才返回True，有一个False结果就是False。"))

add(4, "py-control-flow", "逻辑运算符 or 和 not",
    "or 运算符：有一个True就返回True。not 运算符：取反，True变False，False变True。",
    "is_weekend = True\nis_holiday = False\nif is_weekend or is_holiday:\n    print('今天休息')\nif not is_holiday:\n    print('今天不是假日')",
    fl("填写逻辑运算符",
       "is_weekend = True\nis_holiday = False\nif is_weekend ___ is_holiday:\n    print('今天休息')",
       [{"position": 0, "answer": "or", "options": ["or", "and", "not", "&"]}],
       "满足一个条件就可以休息，用or。"),
    quiz("not True 的结果是什么？",
         ["True", "False", "None", "0"],
         1, "not取反，True变为False。"))

add(4, "py-control-flow", "三元表达式",
    "Python的三元表达式：value_if_true if condition else value_if_false。一行代码实现条件赋值。",
    "age = 20\nstatus = '成年' if age >= 18 else '未成年'\nprint(status)",
    po("这段代码输出什么？",
       "age = 20\nstatus = '成年' if age >= 18 else '未成年'\nprint(status)",
       ["未成年", "成年", "True", "报错"],
       1, "age=20>=18，条件为True，所以status='成年'。"),
    quiz("Python三元表达式的语法是什么？",
         ["condition ? a : b", "a if condition else b", "if condition then a else b", "condition(a, b)"],
         1, "Python三元表达式：value_if_true if condition else value_if_false。"))

add(4, "py-control-flow", "in 关键字判断成员",
    "in 关键字用于判断某个值是否在序列（字符串、列表、元组等）中。返回布尔值。",
    "fruits = ['苹果', '香蕉', '橙子']\nif '苹果' in fruits:\n    print('有苹果')\nif '葡萄' not in fruits:\n    print('没有葡萄')",
    co("排列代码到正确顺序",
       ["    print('有苹果')", "if '苹果' in fruits:", "if '葡萄' not in fruits:", "    print('没有葡萄')", "fruits = ['苹果', '香蕉', '橙子']"],
       [4, 1, 0, 2, 3],
       "正确顺序：定义列表 -> 判断苹果 -> 输出 -> 判断葡萄 -> 输出。"),
    quiz("'a' in 'abc' 返回什么？",
         ["True", "False", "1", "报错"],
         0, "'a'确实是'abc'的子串，in返回True。"))

add(4, "py-control-flow", "is vs ==",
    "== 比较值是否相等，is 比较是否是同一个对象（内存地址相同）。通常用==比较值，is比较None。",
    "a = [1, 2, 3]\nb = [1, 2, 3]\nprint(a == b)   # True\nprint(a is b)   # False\nprint(a is None) # False",
    fb("找出代码中的错误",
       ["a = [1, 2, 3]", "b = [1, 2, 3]", "if a is b:", "    print('相同')"],
       2, "第3行用is比较列表，虽然值相同但不是同一个对象，应该用==比较值。"),
    quiz("判断变量是否为None应该用什么？",
         ["== None", "is None", "= None", "None in"],
         1, "判断None推荐用is None，因为None是单例对象。"))

add(4, "py-control-flow", "真值和假值",
    "Python中有些值默认为False：0、0.0、空字符串''、空列表[]、None。其他值默认为True。",
    "values = [0, 1, '', 'hello', [], [1], None, True]\nfor v in values:\n    if v:\n        print(f'{v!r} -> True')\n    else:\n        print(f'{v!r} -> False')",
    fl("填写默认为假的值",
       "x = ___\nif x:\n    print('True')\nelse:\n    print('False')  # 会执行",
       [{"position": 0, "answer": "0", "options": ["0", "1", "-1", "'0'"]}],
       "0是Python中的假值之一，if 0 为False。"),
    quiz("以下哪个是假值？",
         ["1", "'0'", "[]", "'hello'"],
         2, "空列表[]是假值。0、''、[]、None、0.0都是假值。"))

add(4, "py-control-flow", "bool() 函数",
    "bool() 函数将任意值转为布尔值。根据真值规则转换：假值转为False，其他转为True。",
    "print(bool(0))        # False\nprint(bool(42))       # True\nprint(bool(''))       # False\nprint(bool('hello'))  # True\nprint(bool([]))       # False",
    po("bool('') 返回什么？",
       "print(bool(0))\nprint(bool(42))\nprint(bool(''))\nprint(bool('hello'))\nprint(bool([]))",
       ["True", "False", "None", "报错"],
       1, "空字符串是假值，bool('')返回False。"),
    quiz("bool(None) 返回什么？",
         ["True", "False", "None", "报错"],
         1, "None是假值，bool(None)返回False。"))

add(4, "py-control-flow", "all() 和 any()",
    "all() 所有元素为True才返回True。any() 有一个为True就返回True。常用于批量条件检查。",
    "numbers = [2, 4, 6, 8]\nprint(all(n % 2 == 0 for n in numbers))  # True\nprint(any(n > 5 for n in numbers))      # True",
    co("排列代码到正确顺序",
       ["print(any(n > 5 for n in numbers))", "numbers = [2, 4, 6, 8]", "print(all(n % 2 == 0 for n in numbers))"],
       [1, 2, 0],
       "正确顺序：定义列表 -> 检查是否全偶数 -> 检查是否有大于5的。"),
    quiz("all([True, True, False]) 返回什么？",
         ["True", "False", "None", "报错"],
         1, "all要求所有元素为True，有一个False就返回False。"))

add(4, "py-control-flow", "条件链",
    "Python支持条件链：a < b < c 等价于 a < b and b < c。代码更简洁。",
    "age = 25\nif 18 <= age < 60:\n    print('劳动年龄')\nif 0 < age <= 100:\n    print('合理年龄')",
    fl("填写条件链",
       "x = 50\nif 0 < x ___ 100:\n    print('有效')",
       [{"position": 0, "answer": "<=", "options": ["<=", "==", "!=", ">"]}],
       "条件链 0 < x <= 100 表示x大于0且小于等于100。"),
    quiz("a < b < c 等价于什么？",
         ["a < (b < c)", "a < b and b < c", "a < b or b < c", "(a < b) < c"],
         1, "条件链 a < b < c 等价于 a < b and b < c。"))

add(4, "py-control-flow", "断言 assert",
    "assert 用于调试：如果条件为False就抛出AssertionError。用于检查程序的前置条件。",
    "def divide(a, b):\n    assert b != 0, '除数不能为零'\n    return a / b\n\nresult = divide(10, 2)\nprint(result)",
    fb("找出代码中的错误",
       ["def divide(a, b):", "    assert b != 0, '除数不能为零'", "    return a / b", "", "result = divide(10, 0)", "print(result)"],
       4, "第5行传入b=0，assert条件b!=0为False，会抛出AssertionError: 除数不能为零。"),
    quiz("assert 的作用是什么？",
         ["处理异常", "调试时检查条件", "定义变量", "导入模块"],
         1, "assert用于调试，条件为False时抛出AssertionError。"))

add(4, "py-control-flow", "match-case 模式匹配",
    "Python 3.10+ 的 match-case 语句，类似其他语言的switch-case，但更强大。",
    "command = 'start'\nmatch command:\n    case 'start':\n        print('启动')\n    case 'stop':\n        print('停止')\n    case _:\n        print('未知命令')",
    fl("填写通配符",
       "command = 'quit'\nmatch command:\n    case 'start':\n        print('启动')\n    case ___:\n        print('未知命令')",
       [{"position": 0, "answer": "_", "options": ["_", "*", "else", "default"]}],
       "match-case中用_作为通配符，匹配所有其他情况。"),
    quiz("match-case 中通配符是什么？",
         ["*", "default", "_", "else"],
         2, "match-case中_作为通配符，匹配所有其他情况。"))

add(4, "py-control-flow", "短路求值",
    "and和or运算符使用短路求值：and遇到False停止，or遇到True停止。右边不会被计算。",
    "def side_effect():\n    print('被调用了')\n    return True\n\nresult = False and side_effect()\nprint(result)",
    po("这段代码输出什么？",
       "def side_effect():\n    print('被调用了')\n    return True\n\nresult = False and side_effect()\nprint(result)",
       ["被调用了\\nFalse", "False", "True", "被调用了\\nTrue"],
       1, "and短路：左边为False，不计算右边，side_effect不会被调用。直接返回False。"),
    quiz("False and side_effect() 中 side_effect 会被调用吗？",
         ["会", "不会，短路求值", "看情况", "报错"],
         1, "and短路：左边为False时右边不会被计算。"))

add(4, "py-control-flow", "条件表达式赋值",
    "可以利用and/or的短路特性实现条件赋值，但推荐用三元表达式更清晰。",
    "name = ''\ngreeting = name and f'你好{name}' or '你好陌生人'\nprint(greeting)",
    co("排列代码到正确顺序",
       ["print(greeting)", "greeting = name and f'你好{name}' or '你好陌生人'", "name = ''"],
       [2, 1, 0],
       "正确顺序：定义变量 -> 条件赋值 -> 打印结果。"),
    quiz("name='' 时 name and 'A' or 'B' 返回什么？",
         ["A", "B", "None", "报错"],
         1, "空字符串是假值，name and 'A'短路返回''（假值），然后or继续，返回'B'。"))

add(4, "py-control-flow", "海象运算符 :=",
    "Python 3.8+ 的海象运算符 := 可以在表达式中赋值。减少重复计算。",
    "data = 'hello world'\nif (n := len(data)) > 5:\n    print(f'长度{n}超过5')",
    fl("填写运算符",
       "data = 'hello world'\nif (n __ len(data)) > 5:\n    print(f'长度{n}超过5')",
       [{"position": 0, "answer": ":=", "options": [":=", "=", "==", "is"]}],
       "海象运算符:=在表达式中同时赋值和使用。"),
    quiz("海象运算符 := 的作用是什么？",
         ["比较", "在表达式中赋值", "定义函数", "导入模块"],
         1, "海象运算符:=在表达式中赋值，减少重复计算。"))

add(4, "py-control-flow", "条件与列表推导",
    "列表推导式中可以使用if条件过滤元素。语法：[x for x in iterable if condition]。",
    "numbers = [1, 2, 3, 4, 5, 6]\nevens = [n for n in numbers if n % 2 == 0]\nprint(evens)",
    po("这段代码输出什么？",
       "numbers = [1, 2, 3, 4, 5, 6]\nevens = [n for n in numbers if n % 2 == 0]\nprint(evens)",
       ["[1, 3, 5]", "[2, 4, 6]", "[1, 2, 3, 4, 5, 6]", "报错"],
       1, "列表推导式过滤出偶数（n%2==0），结果是[2, 4, 6]。"),
    quiz("列表推导式中 if 的作用是什么？",
         ["修改元素", "过滤元素", "排序", "去重"],
         1, "列表推导式中的if用于过滤，只保留满足条件的元素。"))


# --- py-loops (20 points) ---

add(4, "py-loops", "for 循环基础",
    "for 循环用于遍历序列（列表、字符串、元组等）。每次迭代取出一个元素。",
    "fruits = ['苹果', '香蕉', '橙子']\nfor fruit in fruits:\n    print(fruit)",
    po("这段代码输出什么？",
       "fruits = ['苹果', '香蕉', '橙子']\nfor fruit in fruits:\n    print(fruit)",
       ["苹果香蕉橙子", "苹果 香蕉 橙子（三行）", "[苹果, 香蕉, 橙子]", "报错"],
       1, "for循环逐个打印列表元素，每个一行。"),
    quiz("for fruit in fruits 中 fruit 是什么？",
         ["列表名", "当前迭代的元素", "索引", "长度"],
         1, "for循环中变量fruit依次取列表中的每个元素。"))

add(4, "py-loops", "range() 函数",
    "range() 生成整数序列。range(n)从0到n-1，range(start, stop, step)可指定起止和步长。",
    "for i in range(5):\n    print(i, end=' ')\nprint()\nfor i in range(2, 8, 2):\n    print(i, end=' ')",
    fl("填写range参数",
       "for i in range(___, 5):\n    print(i, end=' ')  # 输出: 2 3 4",
       [{"position": 0, "answer": "2", "options": ["2", "0", "1", "3"]}],
       "range(2, 5)生成2, 3, 4，从2开始到4（不包含5）。"),
    quiz("range(3) 生成什么序列？",
         ["1, 2, 3", "0, 1, 2", "0, 1, 2, 3", "1, 2"],
         1, "range(3)从0开始，到2结束（不包含3）。"))

add(4, "py-loops", "while 循环基础",
    "while 循环在条件为True时持续执行。必须确保条件最终变为False，否则会无限循环。",
    "count = 0\nwhile count < 3:\n    print(count)\n    count += 1",
    fb("找出代码中的错误",
       ["count = 0", "while count < 3:", "    print(count)", "    count = count"],
       3, "第4行count没有更新，会无限循环。应该改为 count = count + 1 或 count += 1。"),
    quiz("while 循环什么时候停止？",
         ["执行3次后", "条件为False时", "遇到break时", "永远不停"],
         1, "while循环在条件变为False时停止。"))

add(4, "py-loops", "break 退出循环",
    "break 语句立即终止当前循环。常用于在找到目标后提前退出。",
    "numbers = [1, 3, 5, 7, 8, 9]\nfor n in numbers:\n    if n % 2 == 0:\n        print(f'找到偶数: {n}')\n        break",
    po("这段代码输出什么？",
       "numbers = [1, 3, 5, 7, 8, 9]\nfor n in numbers:\n    if n % 2 == 0:\n        print(f'找到偶数: {n}')\n        break",
       ["找到偶数: 8", "找到偶数: 8 和 找到偶数: 9", "1 3 5 7 8 9", "报错"],
       0, "遍历到8时是偶数，打印后break退出循环，9不会被处理。"),
    quiz("break 的作用是什么？",
         ["跳过当前迭代", "立即终止整个循环", "暂停循环", "重新开始循环"],
         1, "break立即终止整个循环，跳出循环体。"))

add(4, "py-loops", "continue 跳过当前迭代",
    "continue 跳过当前迭代的剩余代码，直接进入下一次迭代。",
    "for i in range(5):\n    if i == 2:\n        continue\n    print(i, end=' ')",
    fl("填写关键字",
       "for i in range(5):\n    if i == 2:\n        ___\n    print(i, end=' ')",
       [{"position": 0, "answer": "continue", "options": ["continue", "break", "pass", "skip"]}],
       "continue跳过当前迭代，不执行后面的print。"),
    quiz("continue 和 break 的区别是什么？",
         ["没有区别", "continue跳过本次，break终止整个循环", "continue更快", "break跳过本次"],
         1, "continue跳过当前迭代进入下一次，break终止整个循环。"))

add(4, "py-loops", "for-else 和 while-else",
    "Python的for/while可以有else子句。循环正常结束（没被break）时执行else。",
    "for n in range(2, 10):\n    if n == 5:\n        break\nelse:\n    print('没有找到5')\nprint(f'找到了: {n}')",
    co("排列代码到正确顺序",
       ["    print('没有找到5')", "    if n == 5:", "for n in range(2, 10):", "        break", "else:", "print(f'找到了: {n}')"],
       [2, 1, 3, 4, 0, 5],
       "正确顺序：for循环 -> 条件判断 -> break -> else -> else体 -> 后续代码。"),
    quiz("for-else 中 else 什么时候执行？",
         ["每次循环后", "循环被break时", "循环正常结束（没break）时", "永远不执行"],
         2, "for-else的else在循环正常结束（没被break）时执行。"))

add(4, "py-loops", "嵌套循环",
    "循环可以嵌套。外层循环每执行一次，内层循环完整执行一遍。",
    "for i in range(3):\n    for j in range(2):\n        print(f'({i},{j})', end=' ')\n    print()",
    po("这段代码输出什么？",
       "for i in range(3):\n    for j in range(2):\n        print(f'({i},{j})', end=' ')\n    print()",
       ["(0,0) (0,1) \\n(1,0) (1,1) \\n(2,0) (2,1)", "(0,0) (1,0) (2,0)", "报错", "(0,0) (0,1) (1,0) (1,1) (2,0) (2,1)"],
       0, "外层3次，内层2次，每次内层循环完换行。"),
    quiz("嵌套循环的总执行次数是多少？",
         ["外层次数", "内层次数", "外层次数 × 内层次数", "不确定"],
         2, "嵌套循环总次数 = 外层次数 × 内层次数。"))

add(4, "py-loops", "enumerate() 带索引遍历",
    "enumerate() 同时获取元素的索引和值。比手动维护计数器更优雅。",
    "fruits = ['苹果', '香蕉', '橙子']\nfor i, fruit in enumerate(fruits):\n    print(f'{i}: {fruit}')",
    fl("填写函数名",
       "fruits = ['苹果', '香蕉', '橙子']\nfor i, fruit in ___(fruits):\n    print(f'{i}: {fruit}')",
       [{"position": 0, "answer": "enumerate", "options": ["enumerate", "range", "zip", "iter"]}],
       "enumerate()同时返回索引和元素。"),
    quiz("enumerate() 返回什么？",
         ["只有索引", "只有值", "索引和值的元组", "列表"],
         2, "enumerate()返回(index, value)元组成的迭代器。"))

add(4, "py-loops", "zip() 并行遍历",
    "zip() 将多个可迭代对象按位置配对。长度以最短的为准。",
    "names = ['小明', '小红', '小刚']\nscores = [90, 85, 92]\nfor name, score in zip(names, scores):\n    print(f'{name}: {score}')",
    co("排列代码到正确顺序",
       ["    print(f'{name}: {score}')", "names = ['小明', '小红', '小刚']", "for name, score in zip(names, scores):", "scores = [90, 85, 92]"],
       [1, 3, 2, 0],
       "正确顺序：定义names -> 定义scores -> zip遍历 -> 打印。"),
    quiz("zip() 配对时长度以什么为准？",
         ["最长的", "最短的", "第一个", "报错"],
         1, "zip()以最短的可迭代对象为准，多余的元素被忽略。"))

add(4, "py-loops", "列表推导式",
    "列表推导式是创建列表的简洁方式。语法：[expression for item in iterable]。",
    "squares = [x**2 for x in range(5)]\nprint(squares)",
    po("这段代码输出什么？",
       "squares = [x**2 for x in range(5)]\nprint(squares)",
       ["[1, 4, 9, 16, 25]", "[0, 1, 4, 9, 16]", "[0, 2, 4, 6, 8]", "报错"],
       1, "range(5)是0-4，平方后得到[0, 1, 4, 9, 16]。"),
    quiz("列表推导式 [x*2 for x in range(3)] 的结果是什么？",
         ["[0, 2, 4]", "[1, 2, 3]", "[2, 4, 6]", "[0, 1, 2]"],
         0, "range(3)是0,1,2，乘以2得[0, 2, 4]。"))

add(4, "py-loops", "字典推导式",
    "字典推导式创建字典。语法：{key: value for item in iterable}。",
    "names = ['alice', 'bob', 'charlie']\nname_lengths = {name: len(name) for name in names}\nprint(name_lengths)",
    fl("填写推导式类型",
       "names = ['alice', 'bob']\nresult = {name: len(name) for name in names}\n# 这是___推导式",
       [{"position": 0, "answer": "字典", "options": ["字典", "列表", "集合", "元组"]}],
       "花括号+冒号是字典推导式的标志。"),
    quiz("{x: x**2 for x in range(3)} 的结果是什么？",
         ["{0:0, 1:1, 2:4}", "[0, 1, 4]", "{0, 1, 4}", "报错"],
         0, "字典推导式：key是x，value是x**2，结果是{0:0, 1:1, 2:4}。"))

add(4, "py-loops", "生成器表达式",
    "生成器表达式用圆括号，不立即计算，而是惰性求值。节省内存，适合大数据。",
    "gen = (x**2 for x in range(5))\nprint(next(gen))  # 0\nprint(next(gen))  # 1\nprint(list(gen))  # [4, 9, 16]",
    fb("找出代码中的问题",
       ["gen = [x**2 for x in range(5)]", "print(next(gen))", "print(next(gen))", "print(list(gen))"],
       0, "第1行用了方括号[]，这是列表推导式不是生成器。应该用圆括号(x**2 for x in range(5))。"),
    quiz("生成器表达式和列表推导式的区别是什么？",
         ["没有区别", "生成器惰性求值，列表立即计算", "生成器更快", "列表更省内存"],
         1, "生成器表达式惰性求值（用到才计算），列表推导式立即计算所有元素。"))

add(4, "py-loops", "循环与字典遍历",
    "遍历字典有三种方式：keys()、values()、items()。items()同时获取键和值。",
    "scores = {'小明': 90, '小红': 85}\nfor name, score in scores.items():\n    print(f'{name}: {score}')",
    fl("填写遍历方法",
       "scores = {'小明': 90, '小红': 85}\nfor name, score in scores.___():\n    print(f'{name}: {score}')",
       [{"position": 0, "answer": "items", "options": ["items", "keys", "values", "pairs"]}],
       "items()返回(key, value)元组组成的迭代器。"),
    quiz("遍历字典时要同时获取键和值，用什么方法？",
         ["keys()", "values()", "items()", "list()"],
         2, "dict.items()返回(key, value)元组，可同时获取键和值。"))

add(4, "py-loops", "反向遍历",
    "reversed() 函数返回反向迭代器。也可以用切片 [::-1] 创建反向副本。",
    "numbers = [1, 2, 3, 4, 5]\nfor n in reversed(numbers):\n    print(n, end=' ')",
    co("排列代码到正确顺序",
       ["    print(n, end=' ')", "for n in reversed(numbers):", "numbers = [1, 2, 3, 4, 5]"],
       [2, 1, 0],
       "正确顺序：定义列表 -> reversed遍历 -> 打印。"),
    quiz("reversed([1,2,3]) 返回什么？",
         ["[3,2,1]", "反向迭代器", "[1,2,3]", "报错"],
         1, "reversed()返回反向迭代器，不是列表。用list()转为列表。"))

add(4, "py-loops", "无限循环",
    "while True 创建无限循环，必须在循环体内用 break 退出。常用于菜单、服务器等场景。",
    "while True:\n    cmd = input('输入命令: ')\n    if cmd == 'quit':\n        break\n    print(f'执行: {cmd}')",
    fb("找出代码中的问题",
       ["while True:", "    cmd = input('输入命令: ')", "    print(f'执行: {cmd}')", "    if cmd == 'quit':", "        break"],
       2, "第3行print在break之前，输入quit时也会打印'执行: quit'。应该把if判断放在print前面。"),
    quiz("while True 循环怎么退出？",
         ["自动停止", "用break退出", "用continue退出", "只能关闭程序"],
         1, "while True是无限循环，必须在循环体内用break退出。"))

add(4, "py-loops", "循环中的 else 子句",
    "for-else中的else在循环完整执行后运行。如果break了就不运行else。常用于搜索场景。",
    "target = 7\nnumbers = [1, 3, 5, 7, 9]\nfor n in numbers:\n    if n == target:\n        print(f'找到{target}')\n        break\nelse:\n    print(f'没找到{target}')",
    fl("填写关键字",
       "for n in numbers:\n    if n == target:\n        break\n___:\n    print('没找到')",
       [{"position": 0, "answer": "else", "options": ["else", "finally", "except", "default"]}],
       "for-else中，循环没被break时执行else块。"),
    quiz("for-else 中 break 了会怎样？",
         ["else也执行", "else不执行", "报错", "不确定"],
         1, "循环被break时else不执行，只有正常结束时才执行else。"))

add(4, "py-loops", "itertools.chain 连接迭代",
    "itertools.chain() 将多个可迭代对象连接成一个。比先拼接列表再遍历更高效。",
    "import itertools\n\nlist_a = [1, 2, 3]\nlist_b = [4, 5, 6]\nfor n in itertools.chain(list_a, list_b):\n    print(n, end=' ')",
    po("这段代码输出什么？",
       "import itertools\nlist_a = [1, 2, 3]\nlist_b = [4, 5, 6]\nfor n in itertools.chain(list_a, list_b):\n    print(n, end=' ')",
       ["[1,2,3] [4,5,6]", "1 2 3 4 5 6", "报错", "(1,4) (2,5) (3,6)"],
       1, "chain按顺序连接两个列表，依次输出1 2 3 4 5 6。"),
    quiz("itertools.chain() 的作用是什么？",
         ["排序", "连接多个可迭代对象", "过滤元素", "创建循环"],
         1, "chain()将多个可迭代对象连接成一个连续的迭代器。"))

add(4, "py-loops", "循环性能优化",
    "避免在循环中重复计算。将不变的计算移到循环外面。列表推导式比等价for循环快。",
    "# 慢：每次循环都调用len()\nfor i in range(len(data)):\n    if i < len(data) - 1:\n        pass\n\n# 快：提前计算\nn = len(data)\nfor i in range(n):\n    if i < n - 1:\n        pass",
    fb("找出代码中的性能问题",
       ["data = [1, 2, 3, 4, 5]", "for i in range(len(data)):", "    for j in range(len(data)):", "        print(i + j)"],
       2, "第3行内层循环也调用len(data)，应该提前 n = len(data) 然后用range(n)。"),
    quiz("循环中如何优化性能？",
         ["增加更多循环", "将不变的计算移到循环外", "使用更多变量", "添加注释"],
         1, "将循环中不变的计算（如len()）移到循环外面，避免重复调用。"))

add(4, "py-loops", "递归简介",
    "递归是函数调用自身。必须有基准条件（停止条件）和递归步骤。常用但要注意栈溢出。",
    "def factorial(n):\n    if n <= 1:\n        return 1\n    return n * factorial(n - 1)\n\nprint(factorial(5))",
    co("排列代码到正确顺序",
       ["    return n * factorial(n - 1)", "    if n <= 1:", "def factorial(n):", "        return 1", "print(factorial(5))"],
       [2, 1, 3, 0, 4],
       "正确顺序：定义函数 -> 基准条件 -> 返回1 -> 递归步骤 -> 调用。"),
    quiz("递归函数必须有什么？",
         ["循环", "基准条件（停止条件）", "全局变量", "import语句"],
         1, "递归必须有基准条件，否则会无限递归导致栈溢出。"))

add(4, "py-loops", "循环与解包",
    "for循环支持解包(unpacking)，可以同时取出多个值。适用于元组列表等可迭代对象。",
    "pairs = [(1, 'a'), (2, 'b'), (3, 'c')]\nfor num, letter in pairs:\n    print(f'{num} -> {letter}')",
    fl("填写解包变量",
       "pairs = [(1, 'a'), (2, 'b'), (3, 'c')]\nfor ___, letter in pairs:\n    print(f'{num} -> {letter}')",
       [{"position": 0, "answer": "num", "options": ["num", "i", "index", "key"]}],
       "for循环解包：第一个值赋给num，第二个赋给letter。"),
    quiz("for a, b in [(1,2), (3,4)] 中 a 和 b 分别是什么？",
         ["a是列表，b是列表", "a=1,b=2 然后 a=3,b=4", "报错", "a=1,b=4"],
         1, "循环解包：第一次a=1,b=2，第二次a=3,b=4。"))


# ============================================================
# WEEK 5: Python函数
# ============================================================

# --- py-functions (20 points) ---

add(5, "py-functions", "函数定义 def",
    "用 def 关键字定义函数。函数名后跟括号和冒号，缩进的代码是函数体。调用时用函数名加括号。",
    "def greet():\n    print('你好，世界！')\n\ngreet()\ngreet()",
    po("这段代码输出什么？",
       "def greet():\n    print('你好，世界！')\n\ngreet()\ngreet()",
       ["你好，世界！", "你好，世界！\\n你好，世界！", "报错", "什么都不输出"],
       1, "调用两次greet()，每次打印一行，共两行。"),
    quiz("def 关键字的作用是什么？",
         ["定义变量", "定义函数", "定义类", "导入模块"],
         1, "def用于定义函数，后跟函数名、参数和函数体。"))

add(5, "py-functions", "参数和返回值",
    "函数可以接受参数，用 return 返回值。没有 return 或 return 后无值则返回 None。",
    "def add(a, b):\n    return a + b\n\nresult = add(3, 5)\nprint(result)",
    fb("找出代码中的错误",
       ["def greet(name):", "    print(f'你好, {name}')", "", "result = greet('小明')", "print(result + '!')"],
       4, "第5行greet没有return，result是None，None + '!'会报TypeError。需要在函数中return字符串。"),
    quiz("函数没有return语句时返回什么？",
         ["0", "空字符串", "None", "报错"],
         2, "没有return或return后无值的函数返回None。"))

add(5, "py-functions", "默认参数",
    "参数可以有默认值。调用时不传该参数就使用默认值。默认参数必须在非默认参数后面。",
    "def greet(name, greeting='你好'):\n    return f'{greeting}, {name}!'\n\nprint(greet('小明'))\nprint(greet('小明', '嗨'))",
    fl("填写默认值",
       "def greet(name, greeting='___'):\n    return f'{greeting}, {name}!'\n\ngreet('小明')  # 你好, 小明!",
       [{"position": 0, "answer": "你好", "options": ["你好", "hello", "嗨", "None"]}],
       "默认参数greeting='你好'，不传时使用'你好'。"),
    quiz("默认参数应该放在哪里？",
         ["非默认参数前面", "非默认参数后面", "任意位置", "不能有默认参数"],
         1, "默认参数必须在非默认参数后面，否则语法错误。"))

add(5, "py-functions", "关键字参数",
    "调用函数时可以用 参数名=值 的形式传参。关键字参数可以不按顺序传递。",
    "def user_info(name, age, city):\n    print(f'{name}, {age}岁, {city}')\n\nuser_info(city='北京', name='小明', age=20)",
    co("排列代码到正确顺序",
       ["user_info(city='北京', name='小明', age=20)", "def user_info(name, age, city):", "    print(f'{name}, {age}岁, {city}')"],
       [1, 2, 0],
       "正确顺序：定义函数 -> 函数体 -> 用关键字参数调用。"),
    quiz("关键字参数的好处是什么？",
         ["更快", "可以不按顺序传参，代码更清晰", "更安全", "减少代码"],
         1, "关键字参数让调用更清晰，且可以不按定义顺序传参。"))

add(5, "py-functions", "可变参数 *args",
    "*args 收集多余的位置参数为一个元组。函数可以接受任意数量的位置参数。",
    "def total(*args):\n    print(f'参数: {args}')\n    return sum(args)\n\nprint(total(1, 2, 3))\nprint(total(10, 20))",
    po("这段代码输出什么？",
       "def total(*args):\n    print(f'参数: {args}')\n    return sum(args)\n\nprint(total(1, 2, 3))",
       ["参数: (1, 2, 3)\\n6", "参数: [1, 2, 3]\\n6", "6", "报错"],
       0, "*args收集为元组(1,2,3)，sum()求和得6。"),
    quiz("*args 在函数内部是什么类型？",
         ["列表", "元组", "字典", "集合"],
         1, "*args收集的位置参数在函数内部是元组(tuple)类型。"))

add(5, "py-functions", "可变关键字参数 **kwargs",
    "**kwargs 收集多余的关键字参数为一个字典。函数可以接受任意数量的关键字参数。",
    "def print_info(**kwargs):\n    for key, value in kwargs.items():\n        print(f'{key}: {value}')\n\nprint_info(name='小明', age=20, city='北京')",
    fl("填写参数语法",
       "def print_info(___):\n    for key, value in kwargs.items():\n        print(f'{key}: {value}')",
       [{"position": 0, "answer": "**kwargs", "options": ["**kwargs", "*kwargs", "*args", "kwargs"]}],
       "**kwargs用双星号，收集关键字参数为字典。"),
    quiz("**kwargs 在函数内部是什么类型？",
         ["列表", "元组", "字典", "集合"],
         2, "**kwargs收集的关键字参数在函数内部是字典(dict)类型。"))

add(5, "py-functions", "返回多个值",
    "Python函数可以返回多个值，实际是返回一个元组。可以用解构接收。",
    "def min_max(numbers):\n    return min(numbers), max(numbers)\n\nlo, hi = min_max([3, 1, 4, 1, 5])\nprint(f'最小: {lo}, 最大: {hi}')",
    co("排列代码到正确顺序",
       ["lo, hi = min_max([3, 1, 4, 1, 5])", "    return min(numbers), max(numbers)", "def min_max(numbers):", "print(f'最小: {lo}, 最大: {hi}')"],
       [2, 1, 0, 3],
       "正确顺序：定义函数 -> 返回多个值 -> 解构接收 -> 打印。"),
    quiz("return a, b 返回的是什么？",
         ["列表", "元组", "两个独立的值", "字典"],
         1, "return a, b 返回一个元组 (a, b)，可以解构接收。"))

add(5, "py-functions", "函数文档字符串",
    "函数体第一个字符串是文档字符串(docstring)。用 help() 或 .__doc__ 可以查看。",
    "def add(a, b):\n    '''计算两个数的和。\n    Args: a, b - 两个数字\n    Returns: 两数之和\n    '''\n    return a + b\n\nprint(add.__doc__)",
    fb("找出代码中的问题",
       ["def add(a, b):", "    '计算两数之和'", "    '参数: a和b'", "    return a + b"],
       2, "第3行是第二个字符串，不是docstring。docstring必须是函数体的第一个语句。应合并为一个多行字符串。"),
    quiz("函数文档字符串写在哪里？",
         ["函数名前面", "函数体第一个语句", "return后面", "函数外面"],
         1, "docstring必须是函数体的第一个语句（字符串字面量）。"))

add(5, "py-functions", "作用域 LEGB",
    "Python查找变量的顺序：Local(局部) -> Enclosing(闭包) -> Global(全局) -> Built-in(内置)。",
    "x = '全局'\ndef outer():\n    x = '闭包'\n    def inner():\n        x = '局部'\n        print(x)\n    inner()\n\nouter()",
    fl("填写作用域查找顺序",
       "# LEGB规则:\n# L: ___  局部作用域\n# E: Enclosing  闭包作用域\n# G: Global  全局作用域\n# B: Built-in  内置作用域",
       [{"position": 0, "answer": "Local", "options": ["Local", "Lambda", "Loop", "List"]}],
       "LEGB: Local -> Enclosing -> Global -> Built-in。"),
    quiz("LEGB 中 E 代表什么？",
         ["Error", "Enclosing（闭包作用域）", "Enum", "Event"],
         1, "E代表Enclosing，指外层函数的作用域（闭包）。"))

add(5, "py-functions", "global 关键字",
    "在函数内修改全局变量需要用 global 声明。否则Python会创建同名的局部变量。",
    "count = 0\n\ndef increment():\n    global count\n    count += 1\n\nincrement()\nincrement()\nprint(count)",
    po("这段代码输出什么？",
       "count = 0\ndef increment():\n    global count\n    count += 1\nincrement()\nincrement()\nprint(count)",
       ["0", "1", "2", "报错"],
       2, "global让函数修改全局变量，调用两次后count变为2。"),
    quiz("不加 global 直接在函数内修改全局变量会怎样？",
         ["正常修改", "创建同名局部变量，全局不变", "报错", "删除变量"],
         1, "不加global时，赋值会创建局部变量，不会修改全局变量。"))

add(5, "py-functions", "nonlocal 关键字",
    "nonlocal 用于在嵌套函数中修改外层函数的变量。不是全局的，是闭包作用域的。",
    "def outer():\n    x = 0\n    def inner():\n        nonlocal x\n        x += 1\n        return x\n    return inner\n\nfn = outer()\nprint(fn())  # 1\nprint(fn())  # 2",
    fl("填写关键字",
       "def outer():\n    x = 0\n    def inner():\n        ___ x\n        x += 1\n        return x\n    return inner",
       [{"position": 0, "answer": "nonlocal", "options": ["nonlocal", "global", "local", "outer"]}],
       "nonlocal声明引用外层函数的变量。"),
    quiz("nonlocal 和 global 的区别是什么？",
         ["没有区别", "nonlocal引用外层函数变量，global引用全局变量", "nonlocal更快", "global更安全"],
         1, "nonlocal修改外层函数的变量，global修改模块级全局变量。"))

add(5, "py-functions", "Lambda 函数",
    "lambda 是匿名函数，只能写一行表达式。语法：lambda 参数: 表达式。适合简单的回调。",
    "square = lambda x: x ** 2\nprint(square(5))  # 25\n\nnumbers = [3, 1, 4, 1, 5]\nsorted_nums = sorted(numbers, key=lambda x: -x)\nprint(sorted_nums)",
    fb("找出代码中的错误",
       ["double = lambda x:", "    return x * 2", "print(double(5))"],
       1, "第2行lambda不能有return语句。lambda只能是单个表达式。应改为 double = lambda x: x * 2。"),
    quiz("lambda 函数的特点是什么？",
         ["可以有多行代码", "只能有一个表达式", "必须有名字", "不能作为参数"],
         1, "lambda是匿名函数，函数体只能是一个表达式，不能有语句。"))

add(5, "py-functions", "函数是一等公民",
    "Python中函数是一等公民：可以赋值给变量、作为参数传递、作为返回值返回。",
    "def add(a, b):\n    return a + b\n\noperation = add\nprint(operation(3, 5))  # 8\n\n# 函数作为参数\ndef apply(fn, a, b):\n    return fn(a, b)\nprint(apply(add, 10, 20))",
    co("排列代码到正确顺序",
       ["print(operation(3, 5))", "def add(a, b):", "operation = add", "    return a + b"],
       [1, 3, 2, 0],
       "正确顺序：定义函数 -> 函数体 -> 赋值给变量 -> 使用。"),
    quiz("函数是一等公民意味着什么？",
         ["函数很特别", "函数可以赋值、传参、返回", "函数必须有名字", "函数不能嵌套"],
         1, "一等公民意味着函数和普通值一样，可以赋值、传参、返回。"))

add(5, "py-functions", "高阶函数 map",
    "map() 将函数应用到可迭代对象的每个元素。返回迭代器，用list()转为列表。",
    "numbers = [1, 2, 3, 4]\nsquares = list(map(lambda x: x**2, numbers))\nprint(squares)",
    po("这段代码输出什么？",
       "numbers = [1, 2, 3, 4]\nsquares = list(map(lambda x: x**2, numbers))\nprint(squares)",
       ["[1, 4, 9, 16]", "[1, 2, 3, 4]", "[2, 4, 6, 8]", "报错"],
       0, "map将lambda应用到每个元素：1**2, 2**2, 3**2, 4**2 = [1, 4, 9, 16]。"),
    quiz("map() 返回什么？",
         ["列表", "迭代器", "字典", "元组"],
         1, "map()返回迭代器，需要用list()转为列表。"))

add(5, "py-functions", "高阶函数 filter",
    "filter() 过滤可迭代对象，只保留函数返回True的元素。",
    "numbers = [1, 2, 3, 4, 5, 6]\nevens = list(filter(lambda x: x % 2 == 0, numbers))\nprint(evens)",
    fl("填写函数名",
       "numbers = [1, 2, 3, 4, 5, 6]\nevens = list(___(lambda x: x % 2 == 0, numbers))\nprint(evens)",
       [{"position": 0, "answer": "filter", "options": ["filter", "map", "select", "find"]}],
       "filter()过滤元素，保留满足条件的。"),
    quiz("filter(fn, iterable) 的作用是什么？",
         ["转换元素", "过滤元素，保留fn返回True的", "排序", "求和"],
         1, "filter保留函数返回True的元素。"))

add(5, "py-functions", "sorted 与 key",
    "sorted() 的 key 参数指定排序依据。接受一个函数，返回用于比较的值。",
    "students = [('小明', 90), ('小红', 85), ('小刚', 92)]\nby_score = sorted(students, key=lambda s: s[1], reverse=True)\nprint(by_score)",
    co("排列代码到正确顺序",
       ["by_score = sorted(students, key=lambda s: s[1], reverse=True)", "students = [('小明', 90), ('小红', 85), ('小刚', 92)]", "print(by_score)"],
       [1, 0, 2],
       "正确顺序：定义数据 -> 按分数降序排序 -> 打印。"),
    quiz("sorted() 中 key 参数的作用是什么？",
         ["排序方向", "指定排序依据函数", "排序算法", "返回类型"],
         1, "key参数指定一个函数，返回值用于比较排序。"))

add(5, "py-functions", "递归函数",
    "递归函数调用自身解决问题。经典例子：斐波那契数列。注意设置基准条件防止无限递归。",
    "def fibonacci(n):\n    if n <= 1:\n        return n\n    return fibonacci(n-1) + fibonacci(n-2)\n\nfor i in range(6):\n    print(fibonacci(i), end=' ')",
    po("这段代码输出什么？",
       "def fibonacci(n):\n    if n <= 1:\n        return n\n    return fibonacci(n-1) + fibonacci(n-2)\nfor i in range(6):\n    print(fibonacci(i), end=' ')",
       ["0 1 1 2 3 5", "1 1 2 3 5 8", "0 1 2 3 4 5", "报错"],
       0, "斐波那契数列：F(0)=0, F(1)=1, F(2)=1, F(3)=2, F(4)=3, F(5)=5。"),
    quiz("递归效率低时可以用什么优化？",
         ["更多参数", "缓存/记忆化", "更多循环", "global变量"],
         1, "用functools.lru_cache等缓存机制可以优化递归，避免重复计算。"))

add(5, "py-functions", "类型提示",
    "Python 3.5+ 支持类型提示(type hints)。用冒号标注参数类型，箭头标注返回类型。不影响运行。",
    "def greet(name: str, times: int = 1) -> str:\n    return f'你好, {name}! ' * times\n\nprint(greet('小明', 2))",
    fl("填写类型提示",
       "def add(a: ___, b: int) -> int:\n    return a + b",
       [{"position": 0, "answer": "int", "options": ["int", "number", "float", "str"]}],
       "类型提示用Python内置类型名，如int、str、float等。"),
    quiz("类型提示会影响程序运行吗？",
         ["会，类型不对就报错", "不会，只是提示", "有时会", "看Python版本"],
         1, "类型提示不影响运行时行为，只是给开发者和IDE看的注解。"))

add(5, "py-functions", "函数装饰器入门",
    "装饰器是一个接受函数并返回新函数的函数。用 @decorator 语法放在函数定义前面。",
    "def log_call(fn):\n    def wrapper(*args, **kwargs):\n        print(f'调用 {fn.__name__}')\n        return fn(*args, **kwargs)\n    return wrapper\n\n@log_call\ndef add(a, b):\n    return a + b\n\nprint(add(3, 5))",
    fb("找出代码中的问题",
       ["def log_call(fn):", "    def wrapper(*args, **kwargs):", "        print(f'调用 {fn.__name__}')", "        return fn(*args, **kwargs)", "", "@log_call", "def add(a, b):", "    return a + b", "", "print(add(3, 5))"],
       -1, "这段代码没有错误。装饰器log_call包装add函数，调用时先打印再执行。"),
    quiz("装饰器的作用是什么？",
         ["删除函数", "在不修改原函数的情况下增加功能", "加速函数", "定义函数"],
         1, "装饰器在不修改原函数代码的情况下，为函数增加额外功能。"))

add(5, "py-functions", "functools.partial",
    "functools.partial() 固定函数的部分参数，创建一个新函数。常用于回调和配置化。",
    "from functools import partial\n\ndef power(base, exponent):\n    return base ** exponent\n\nsquare = partial(power, exponent=2)\ncube = partial(power, exponent=3)\nprint(square(5))  # 25\nprint(cube(3))    # 27",
    fl("填写模块名",
       "from ___ import partial\ndef power(base, exponent):\n    return base ** exponent\nsquare = partial(power, exponent=2)",
       [{"position": 0, "answer": "functools", "options": ["functools", "itertools", "operator", "types"]}],
       "partial在functools模块中。"),
    quiz("functools.partial() 的作用是什么？",
         ["删除参数", "固定部分参数创建新函数", "加速函数", "装饰函数"],
         1, "partial固定函数的部分参数，返回一个新函数。"))


# --- py-closures (20 points) ---

add(5, "py-closures", "什么是闭包",
    "闭包是一个函数加上它引用的外层变量。内部函数引用了外部函数的局部变量，外部函数返回内部函数。",
    "def make_greeting(prefix):\n    def greet(name):\n        return f'{prefix}, {name}!'\n    return greet\n\nhello = make_greeting('你好')\nprint(hello('小明'))",
    po("这段代码输出什么？",
       "def make_greeting(prefix):\n    def greet(name):\n        return f'{prefix}, {name}!'\n    return greet\nhello = make_greeting('你好')\nprint(hello('小明'))",
       ["你好, 小明!", "prefix, 小明!", "报错", "None"],
       0, "闭包捕获了prefix='你好'，调用hello('小明')输出'你好, 小明!'。"),
    quiz("闭包是什么？",
         ["普通函数", "函数加上它引用的外层变量", "全局函数", "匿名函数"],
         1, "闭包是函数和它引用的外层变量的组合。"))

add(5, "py-closures", "闭包的创建",
    "创建闭包的条件：1. 有嵌套函数 2. 内部函数引用外部变量 3. 外部函数返回内部函数。",
    "def counter():\n    count = 0\n    def increment():\n        nonlocal count\n        count += 1\n        return count\n    return increment\n\nc = counter()\nprint(c())  # 1\nprint(c())  # 2",
    co("排列代码到正确顺序",
       ["print(c())  # 1", "c = counter()", "    return increment", "def counter():", "    count = 0", "print(c())  # 2"],
       [3, 4, 2, 1, 0, 5],
       "正确顺序：定义counter -> 定义count -> 返回increment -> 创建闭包 -> 调用。"),
    quiz("创建闭包需要几个条件？",
         ["1个", "2个", "3个", "4个"],
         2, "三个条件：嵌套函数、引用外部变量、返回内部函数。"))

add(5, "py-closures", "闭包捕获变量",
    "闭包捕获的是变量的引用，不是值。如果变量后来被修改，闭包看到的是最新值。",
    "def make_multipliers():\n    multipliers = []\n    for i in range(3):\n        multipliers.append(lambda x: x * i)\n    return multipliers\n\nfns = make_multipliers()\nprint(fns[0](10))  # 期望0，实际？",
    fb("找出代码中的问题",
       ["def make_multipliers():", "    multipliers = []", "    for i in range(3):", "        multipliers.append(lambda x: x * i)", "    return multipliers"],
       3, "第4行lambda捕获的是变量i的引用，不是值。循环结束后i=2，所有lambda都用i=2。应改为 lambda x, i=i: x * i。"),
    quiz("闭包捕获的是变量的什么？",
         ["值的副本", "引用（指向最新值）", "名字", "类型"],
         1, "闭包捕获变量的引用，不是值的副本。"))

add(5, "py-closures", "延迟绑定问题",
    "闭包中的变量在调用时才查找值，不是定义时。这是延迟绑定(late binding)。",
    "def make_funcs():\n    return [lambda: i for i in range(3)]\n\nfuncs = make_funcs()\nprint([f() for f in funcs])",
    fl("填写修复方法",
       "def make_funcs():\n    return [lambda i=i: i for i in range(3)]\n# i=i 将当前值___给参数默认值",
       [{"position": 0, "answer": "绑定", "options": ["绑定", "复制", "删除", "创建"]}],
       "i=i在定义时将当前i值绑定为参数默认值，解决延迟绑定问题。"),
    quiz("延迟绑定问题的修复方法是什么？",
         ["用global", "用默认参数 i=i 捕获当前值", "用nonlocal", "用class"],
         1, "lambda i=i: i 在定义时绑定当前值，避免延迟绑定。"))

add(5, "py-closures", "闭包工厂",
    "闭包工厂是用闭包创建一系列相似的函数。每个闭包有自己的状态。",
    "def make_multiplier(n):\n    def multiply(x):\n        return x * n\n    return multiply\n\ndouble = make_multiplier(2)\ntriple = make_multiplier(3)\nprint(double(5))  # 10\nprint(triple(5))  # 15",
    po("这段代码输出什么？",
       "def make_multiplier(n):\n    def multiply(x):\n        return x * n\n    return multiply\ndouble = make_multiplier(2)\ntriple = make_multiplier(3)\nprint(double(5))\nprint(triple(5))",
       ["10 15", "10 10", "15 15", "报错"],
       0, "double捕获n=2，triple捕获n=3。double(5)=10，triple(5)=15。"),
    quiz("闭包工厂的好处是什么？",
         ["更快", "从一个模板创建多个相似函数", "减少内存", "避免函数"],
         1, "闭包工厂用一个函数生成多个配置不同的函数。"))

add(5, "py-closures", "闭包与回调",
    "闭包常用于回调函数，可以携带创建时的上下文信息。",
    "def on_click(button_name):\n    def handler():\n        print(f'{button_name} 被点击了')\n    return handler\n\nsubmit_handler = on_click('提交按钮')\ncancel_handler = on_click('取消按钮')\nsubmit_handler()",
    fl("填写闭包捕获的变量",
       "def on_click(button_name):\n    def handler():\n        print(f'{___} 被点击了')\n    return handler",
       [{"position": 0, "answer": "button_name", "options": ["button_name", "name", "self", "handler"]}],
       "handler闭包捕获了外层的button_name变量。"),
    quiz("闭包作为回调的好处是什么？",
         ["更快", "可以携带创建时的上下文", "更安全", "更短"],
         1, "闭包可以捕获创建时的变量，在回调时使用这些上下文。"))

add(5, "py-closures", "装饰器基础",
    "装饰器本质是一个接受函数、返回新函数的闭包。@语法是语法糖。",
    "def my_decorator(fn):\n    def wrapper():\n        print('执行前')\n        fn()\n        print('执行后')\n    return wrapper\n\n@my_decorator\ndef say_hello():\n    print('你好')\n\nsay_hello()",
    co("排列代码到正确顺序",
       ["    print('执行后')", "def my_decorator(fn):", "    def wrapper():", "@my_decorator", "    fn()", "        print('你好')", "        print('执行前')", "def say_hello():"],
       [1, 2, 6, 4, 0, 3, 7, 5],
       "正确顺序：装饰器 -> wrapper -> 前 -> fn -> 后 -> @装饰 -> 函数 -> 函数体。"),
    quiz("@my_decorator 语法等价于什么？",
         ["my_decorator()", "say_hello = my_decorator(say_hello)", "my_decorator.say_hello", "say_hello(my_decorator)"],
         1, "@装饰器语法等价于 say_hello = my_decorator(say_hello)。"))

add(5, "py-closures", "带参数的装饰器",
    "带参数的装饰器需要三层嵌套：最外层接受装饰器参数，中间层接受函数，最内层是wrapper。",
    "def repeat(times):\n    def decorator(fn):\n        def wrapper(*args, **kwargs):\n            for _ in range(times):\n                result = fn(*args, **kwargs)\n            return result\n        return wrapper\n    return decorator\n\n@repeat(3)\ndef greet(name):\n    print(f'你好, {name}!')\n\ngreet('小明')",
    fb("找出代码中的错误",
       ["def repeat(fn):", "    def wrapper(*args, **kwargs):", "        for _ in range(3):", "            fn(*args, **kwargs)", "    return wrapper", "", "@repeat", "def greet(name):", "    print(f'你好, {name}!')"],
       0, "第1行repeat应该接受参数times，不是fn。因为@repeat(3)先调用repeat(3)返回decorator，再用decorator装饰函数。"),
    quiz("带参数的装饰器需要几层嵌套？",
         ["1层", "2层", "3层", "4层"],
         2, "三层：外层接受装饰器参数，中层接受函数，内层是wrapper。"))

add(5, "py-closures", "functools.wraps",
    "装饰器会丢失原函数的元信息（名字、文档等）。用 @functools.wraps(fn) 保留这些信息。",
    "from functools import wraps\n\ndef log(fn):\n    @wraps(fn)\n    def wrapper(*args, **kwargs):\n        return fn(*args, **kwargs)\n    return wrapper\n\n@log\ndef add(a, b):\n    '''两数相加'''\n    return a + b\n\nprint(add.__name__)",
    fl("填写装饰器",
       "from functools import wraps\ndef log(fn):\n    ___(fn)\n    def wrapper(*args, **kwargs):\n        return fn(*args, **kwargs)\n    return wrapper",
       [{"position": 0, "answer": "@wraps", "options": ["@wraps", "@decorate", "@copy", "@keep"]}],
       "@wraps(fn)保留原函数的元信息。"),
    quiz("不加 @wraps 会怎样？",
         ["报错", "原函数的__name__、__doc__等信息丢失", "运行更快", "没有影响"],
         1, "不加@wraps，wrapper会替代原函数的元信息（名字变为wrapper）。"))

add(5, "py-closures", "类作为装饰器",
    "任何可调用对象都可以做装饰器。用类实现装饰器时，__init__接受函数，__call__是wrapper。",
    "class CountCalls:\n    def __init__(self, fn):\n        self.fn = fn\n        self.count = 0\n    def __call__(self, *args, **kwargs):\n        self.count += 1\n        print(f'调用次数: {self.count}')\n        return self.fn(*args, **kwargs)\n\n@CountCalls\ndef say_hi():\n    print('嗨')\n\nsay_hi()\nsay_hi()",
    po("这段代码输出什么？",
       "class CountCalls:\n    def __init__(self, fn):\n        self.fn = fn\n        self.count = 0\n    def __call__(self, *args, **kwargs):\n        self.count += 1\n        print(f'调用次数: {self.count}')\n        return self.fn(*args, **kwargs)\n@CountCalls\ndef say_hi():\n    print('嗨')\nsay_hi()\nsay_hi()",
       ["调用次数: 1\\n嗨\\n调用次数: 2\\n嗨", "嗨\\n嗨", "调用次数: 2\\n嗨", "报错"],
       0, "类装饰器每次调用__call__，计数器递增。第一次打印1，第二次打印2。"),
    quiz("用类实现装饰器时，被装饰的函数调用触发哪个方法？",
         ["__init__", "__call__", "__new__", "__repr__"],
         1, "类实例被调用时触发__call__方法。"))

add(5, "py-closures", "装饰器叠加",
    "多个装饰器可以叠加使用。执行顺序从下到上（从最靠近函数的开始）。",
    "def bold(fn):\n    def wrapper():\n        return f'<b>{fn()}</b>'\n    return wrapper\n\ndef italic(fn):\n    def wrapper():\n        return f'<i>{fn()}</i>'\n    return wrapper\n\n@bold\n@italic\ndef hello():\n    return '你好'\n\nprint(hello())",
    fl("填写执行顺序",
       "@bold\n@italic\ndef hello():\n    return '你好'\n# 先应用___，再应用bold",
       [{"position": 0, "answer": "italic", "options": ["italic", "bold", "hello", "wrapper"]}],
       "装饰器从下到上应用：先italic，再bold。"),
    quiz("多个装饰器叠加时执行顺序是什么？",
         ["从上到下", "从下到上", "随机", "只执行第一个"],
         1, "装饰器从下到上（从最靠近函数的开始）依次应用。"))

add(5, "py-closures", "装饰器与状态",
    "装饰器可以在闭包中维护状态，如缓存、计数器等。",
    "def memoize(fn):\n    cache = {}\n    def wrapper(n):\n        if n not in cache:\n            cache[n] = fn(n)\n        return cache[n]\n    return wrapper\n\n@memoize\ndef fib(n):\n    if n <= 1: return n\n    return fib(n-1) + fib(n-2)\n\nprint(fib(30))",
    co("排列代码到正确顺序",
       ["        return cache[n]", "def memoize(fn):", "    cache = {}", "    def wrapper(n):", "        if n not in cache:", "            cache[n] = fn(n)", "    return wrapper"],
       [1, 2, 3, 4, 5, 0, 6],
       "正确顺序：定义memoize -> cache -> wrapper -> 条件 -> 缓存 -> 返回 -> 返回wrapper。"),
    quiz("装饰器中的状态保存在哪里？",
         ["全局变量", "闭包的外层变量", "类属性", "文件"],
         1, "装饰器的状态保存在闭包的外层变量（如cache）中。"))

add(5, "py-closures", "property 装饰器",
    "@property 将方法变成属性访问。可以用点号访问，不需要加括号。",
    "class Circle:\n    def __init__(self, radius):\n        self._radius = radius\n    @property\n    def area(self):\n        return 3.14 * self._radius ** 2\n\nc = Circle(5)\nprint(c.area)",
    fb("找出代码中的错误",
       ["class Circle:", "    def __init__(self, radius):", "        self._radius = radius", "    def area(self):", "        return 3.14 * self._radius ** 2", "c = Circle(5)", "print(c.area())"],
       6, "第7行area是@property，不需要括号。应改为 print(c.area)，不是 c.area()。"),
    quiz("@property 的作用是什么？",
         ["定义类方法", "将方法变成属性访问", "创建私有变量", "继承"],
         1, "@property让方法可以像属性一样用点号访问，不加括号。"))

add(5, "py-closures", "staticmethod 和 classmethod",
    "@staticmethod 不需要self或cls参数。@classmethod 第一个参数是类本身(cls)。",
    "class Math:\n    @staticmethod\n    def add(a, b):\n        return a + b\n    @classmethod\n    def identity(cls, x):\n        return x\n\nprint(Math.add(3, 5))\nprint(Math.identity(42))",
    fl("填写装饰器",
       "class Math:\n    ___\n    def add(a, b):\n        return a + b",
       [{"position": 0, "answer": "@staticmethod", "options": ["@staticmethod", "@classmethod", "@property", "@decorator"]}],
       "不需要self参数的普通方法用@staticmethod装饰。"),
    quiz("@staticmethod 和 @classmethod 的区别是什么？",
         ["没有区别", "staticmethod无参数，classmethod有cls参数", "staticmethod更快", "classmethod更安全"],
         1, "@staticmethod不接收隐式参数，@classmethod第一个参数是类cls。"))

add(5, "py-closures", "闭包实现计数器",
    "闭包可以实现有状态的计数器。每次调用都记住之前的计数值。",
    "def make_counter(start=0):\n    count = start\n    def counter():\n        nonlocal count\n        count += 1\n        return count\n    return counter\n\nc = make_counter(10)\nprint(c())  # 11\nprint(c())  # 12\nprint(c())  # 13",
    po("这段代码输出什么？",
       "def make_counter(start=0):\n    count = start\n    def counter():\n        nonlocal count\n        count += 1\n        return count\n    return counter\nc = make_counter(10)\nprint(c())\nprint(c())\nprint(c())",
       ["10 11 12", "11 12 13", "1 2 3", "报错"],
       1, "start=10，第一次调用count变为11，第二次12，第三次13。"),
    quiz("闭包计数器需要什么关键字修改外层变量？",
         ["global", "nonlocal", "local", "static"],
         1, "nonlocal用于修改外层函数（非全局）的变量。"))

add(5, "py-closures", "闭包实现缓存",
    "闭包可以实现简单的缓存机制，避免重复计算。这就是记忆化(memoization)。",
    "def make_cache(fn):\n    cache = {}\n    def wrapper(*args):\n        if args not in cache:\n            cache[args] = fn(*args)\n        return cache[args]\n    return wrapper\n\n@make_cache\ndef expensive(n):\n    print(f'计算 {n}...')\n    return n ** 2\n\nprint(expensive(5))\nprint(expensive(5))",
    fl("填写缓存数据结构",
       "def make_cache(fn):\n    cache = ___\n    def wrapper(*args):\n        if args not in cache:\n            cache[args] = fn(*args)\n        return cache[args]\n    return wrapper",
       [{"position": 0, "answer": "{}", "options": ["{}", "[]", "()", "set()"]}],
       "缓存用字典{}存储，键是参数，值是计算结果。"),
    quiz("记忆化(memoization)的作用是什么？",
         ["删除缓存", "缓存计算结果避免重复计算", "加速循环", "压缩数据"],
         1, "记忆化缓存函数的计算结果，相同参数直接返回缓存值。"))

add(5, "py-closures", "闭包与事件处理",
    "闭包常用于事件系统，每个事件处理器携带自己的配置。",
    "def make_handler(event_type):\n    def handler(data):\n        print(f'处理{event_type}事件: {data}')\n    return handler\n\nhandlers = {\n    'click': make_handler('点击'),\n    'submit': make_handler('提交'),\n}\n\nevent = 'click'\nhandlers[event]({'x': 10, 'y': 20})",
    co("排列代码到正确顺序",
       ["handlers[event]({'x': 10, 'y': 20})", "handlers = {", "event = 'click'", "def make_handler(event_type):", "    'submit': make_handler('提交'),", "    'click': make_handler('点击'),", "    def handler(data):", "        print(f'处理{event_type}事件: {data}')", "    return handler", "}"],
       [3, 6, 7, 8, 1, 5, 4, 9, 2, 0],
       "正确顺序：定义工厂 -> handler -> 打印 -> 返回 -> 字典 -> click -> submit -> 闭合 -> 事件 -> 调用。"),
    quiz("闭包在事件系统中的优势是什么？",
         ["更快", "每个处理器携带自己的配置", "更安全", "更短"],
         1, "闭包让每个事件处理器携带创建时的事件类型等配置。"))

add(5, "py-closures", "闭包实现配置",
    "闭包可以创建预配置的函数，类似于functools.partial但更灵活。",
    "def make_validator(min_val, max_val):\n    def validate(value):\n        return min_val <= value <= max_val\n    return validate\n\nage_check = make_validator(0, 150)\nscore_check = make_validator(0, 100)\nprint(age_check(25))    # True\nprint(score_check(150)) # False",
    fl("填写闭包名",
       "age_check = make_validator(0, 150)\nscore_check = make_validator(0, 100)\nprint(age_check(25))    # ___",
       [{"position": 0, "answer": "True", "options": ["True", "False", "None", "报错"]}],
       "25在0-150范围内，返回True。"),
    quiz("闭包实现配置比partial更灵活在哪？",
         ["更快", "可以包含任意逻辑，不只是固定参数", "更安全", "更短"],
         1, "闭包可以包含任意验证逻辑，比partial只能固定参数更灵活。"))

add(5, "py-closures", "闭包与柯里化",
    "柯里化是将多参数函数转为一系列单参数函数的技术。闭包天然支持柯里化。",
    "def add(a):\n    def inner(b):\n        return a + b\n    return inner\n\nadd5 = add(5)\nadd10 = add(10)\nprint(add5(3))   # 8\nprint(add10(3))  # 13",
    po("这段代码输出什么？",
       "def add(a):\n    def inner(b):\n        return a + b\n    return inner\nadd5 = add(5)\nadd10 = add(10)\nprint(add5(3))\nprint(add10(3))",
       ["8 13", "5 10", "8 8", "报错"],
       0, "add(5)返回捕获a=5的闭包，add5(3)=5+3=8。add10(3)=10+3=13。"),
    quiz("柯里化(currying)是什么？",
         ["删除参数", "将多参数函数转为一系列单参数函数", "合并函数", "加速函数"],
         1, "柯里化将f(a,b)转为f(a)(b)，每次只接受一个参数。"))

add(5, "py-closures", "闭包陷阱总结",
    "闭包最常见的陷阱是延迟绑定：循环中的lambda共享同一个变量。用默认参数或functools.partial修复。",
    "# 错误：所有函数都返回 2*10=20\nfuncs = [lambda: i * 10 for i in range(3)]\nprint([f() for f in funcs])\n\n# 正确：用默认参数捕获当前值\nfuncs = [lambda i=i: i * 10 for i in range(3)]\nprint([f() for f in funcs])",
    fb("找出代码中的错误",
       ["funcs = [lambda: i * 10 for i in range(3)]", "print([f() for f in funcs])"],
       0, "第1行lambda捕获的是变量i的引用，循环结束后i=2，所有lambda都用i=2。应改为 lambda i=i: i * 10。"),
    quiz("如何避免闭包中的延迟绑定问题？",
         ["用global", "用默认参数 i=i 捕获当前值", "用nonlocal", "用class"],
         1, "lambda i=i: expr 在定义时绑定当前值，是最常用的修复方法。"))


# ============================================================
# WEEK 6: Python面向对象
# ============================================================

# --- py-classes (20 points) ---

add(6, "py-classes", "类的定义",
    "用 class 关键字定义类。类是对象的蓝图，定义了对象有哪些属性和方法。",
    "class Dog:\n    pass\n\nmy_dog = Dog()\nprint(type(my_dog))",
    po("这段代码输出什么？",
       "class Dog:\n    pass\n\nmy_dog = Dog()\nprint(type(my_dog))",
       ["<class 'Dog'>", "<class 'object'>", "Dog", "报错"],
       0, "type()返回对象的类型，my_dog是Dog类的实例。"),
    quiz("class 关键字的作用是什么？",
         ["定义函数", "定义类（对象的蓝图）", "定义变量", "导入模块"],
         1, "class定义类，类是创建对象的蓝图/模板。"))

add(6, "py-classes", "__init__ 构造方法",
    "__init__ 是构造方法，在创建对象时自动调用。self参数代表正在创建的实例。",
    "class Person:\n    def __init__(self, name, age):\n        self.name = name\n        self.age = age\n\np = Person('小明', 20)\nprint(p.name, p.age)",
    fb("找出代码中的错误",
       ["class Person:", "    def __init__(name, age):", "        self.name = name", "        self.age = age", "", "p = Person('小明', 20)"],
       1, "第2行__init__缺少self参数。应改为 def __init__(self, name, age):，所有实例方法第一个参数必须是self。"),
    quiz("__init__ 方法什么时候被调用？",
         ["手动调用", "创建对象时自动调用", "删除对象时", "导入时"],
         1, "__init__在创建对象时自动调用，用于初始化实例属性。"))

add(6, "py-classes", "实例属性",
    "实例属性属于每个对象，通过 self.属性名 定义。每个实例有自己的属性副本。",
    "class Student:\n    def __init__(self, name, score):\n        self.name = name\n        self.score = score\n\ns1 = Student('小明', 90)\ns2 = Student('小红', 85)\nprint(s1.score)",
    fl("填写属性赋值",
       "class Student:\n    def __init__(self, name, score):\n        self.name = name\n        self.___ = score",
       [{"position": 0, "answer": "score", "options": ["score", "self.score", "name", "value"]}],
       "在__init__中用self.score = score定义实例属性。"),
    quiz("实例属性属于什么？",
         ["类", "每个对象（实例）", "全局", "方法"],
         1, "实例属性属于每个对象，不同实例的属性互不影响。"))

add(6, "py-classes", "实例方法",
    "实例方法是定义在类中的函数，第一个参数是self，代表调用该方法的实例。",
    "class Calculator:\n    def __init__(self, value=0):\n        self.value = value\n    def add(self, n):\n        self.value += n\n        return self\n\nc = Calculator(10)\nc.add(5).add(3)\nprint(c.value)",
    co("排列代码到正确顺序",
       ["    def add(self, n):", "    def __init__(self, value=0):", "        self.value = value", "class Calculator:", "        self.value += n", "        return self"],
       [3, 1, 2, 0, 4, 5],
       "正确顺序：class -> __init__ -> 赋值 -> add -> 加法 -> 返回self。"),
    quiz("实例方法的第一个参数是什么？",
         ["this", "self", "cls", "instance"],
         1, "Python约定用self作为实例方法的第一个参数，代表调用者。"))

add(6, "py-classes", "类属性",
    "类属性属于类本身，所有实例共享。在类体内、方法外定义。",
    "class Counter:\n    count = 0\n    def __init__(self):\n        Counter.count += 1\n\nc1 = Counter()\nc2 = Counter()\nprint(Counter.count)",
    po("这段代码输出什么？",
       "class Counter:\n    count = 0\n    def __init__(self):\n        Counter.count += 1\nc1 = Counter()\nc2 = Counter()\nprint(Counter.count)",
       ["0", "1", "2", "报错"],
       2, "创建两个实例，__init__被调用两次，count从0变为2。"),
    quiz("类属性和实例属性的区别是什么？",
         ["没有区别", "类属性所有实例共享，实例属性每个对象独有", "类属性更快", "实例属性更安全"],
         1, "类属性属于类，所有实例共享；实例属性属于每个对象。"))

add(6, "py-classes", "类方法 @classmethod",
    "@classmethod 的第一个参数是类本身(cls)，不是实例。常用于工厂方法。",
    "class Date:\n    def __init__(self, year, month, day):\n        self.year = year\n        self.month = month\n        self.day = day\n    @classmethod\n    def from_string(cls, date_str):\n        y, m, d = date_str.split('-')\n        return cls(int(y), int(m), int(d))\n\nd = Date.from_string('2024-01-15')\nprint(d.year)",
    fl("填写参数名",
       "class Date:\n    @classmethod\n    def from_string(cls, date_str):\n        return cls(2024, 1, 15)\n# 第一个参数___代表类本身",
       [{"position": 0, "answer": "cls", "options": ["cls", "self", "class", "this"]}],
       "@classmethod的第一个参数约定为cls，代表类本身。"),
    quiz("@classmethod 的第一个参数是什么？",
         ["self", "cls（类本身）", "args", "this"],
         1, "@classmethod的第一个参数是cls，代表类本身，不是实例。"))

add(6, "py-classes", "静态方法 @staticmethod",
    "@staticmethod 不接收self或cls参数。与类相关但不需要访问实例或类状态的工具函数。",
    "class MathUtils:\n    @staticmethod\n    def is_even(n):\n        return n % 2 == 0\n\nprint(MathUtils.is_even(4))  # True\nprint(MathUtils.is_even(3))  # False",
    fb("找出代码中的错误",
       ["class MathUtils:", "    @staticmethod", "    def is_even(self, n):", "        return n % 2 == 0", "", "print(MathUtils.is_even(4))"],
       2, "第3行staticmethod不需要self参数。应改为 def is_even(n):。"),
    quiz("staticmethod 需要 self 参数吗？",
         ["需要", "不需要", "有时需要", "用cls代替"],
         1, "@staticmethod不接收self或cls，它是独立于实例和类的方法。"))

add(6, "py-classes", "特殊方法 __str__",
    "__str__ 定义对象的字符串表示。print() 和 str() 会调用它。面向用户友好的输出。",
    "class Book:\n    def __init__(self, title, author):\n        self.title = title\n        self.author = author\n    def __str__(self):\n        return f'《{self.title}》 by {self.author}'\n\nb = Book('三体', '刘慈欣')\nprint(b)",
    po("这段代码输出什么？",
       "class Book:\n    def __init__(self, title, author):\n        self.title = title\n        self.author = author\n    def __str__(self):\n        return f'《{self.title}》 by {self.author}'\nb = Book('三体', '刘慈欣')\nprint(b)",
       ["<Book object>", "《三体》 by 刘慈欣", "报错", "None"],
       1, "print()调用__str__方法，返回格式化的字符串。"),
    quiz("__str__ 方法什么时候被调用？",
         ["创建对象时", "print() 或 str() 调用时", "删除对象时", "比较对象时"],
         1, "print(obj)和str(obj)会调用对象的__str__方法。"))

add(6, "py-classes", "特殊方法 __repr__",
    "__repr__ 定义对象的开发者友好的字符串表示。在交互式环境中直接输入变量名时调用。",
    "class Point:\n    def __init__(self, x, y):\n        self.x = x\n        self.y = y\n    def __repr__(self):\n        return f'Point({self.x}, {self.y})'\n\np = Point(3, 4)\nprint(repr(p))",
    fl("填写方法名",
       "class Point:\n    def __init__(self, x, y):\n        self.x = x\n        self.y = y\n    def ___(self):\n        return f'Point({self.x}, {self.y})'",
       [{"position": 0, "answer": "__repr__", "options": ["__repr__", "__str__", "__init__", "__str__"]}],
       "repr()调用__repr__方法，提供开发者友好的表示。"),
    quiz("__str__ 和 __repr__ 的区别是什么？",
         ["没有区别", "__str__面向用户，__repr__面向开发者", "__str__更快", "__repr__更短"],
         1, "__str__给用户看（友好），__repr__给开发者看（精确，可重建对象）。"))

add(6, "py-classes", "运算符重载 __add__",
    "通过定义 __add__ 等特殊方法，可以自定义运算符的行为。这叫做运算符重载。",
    "class Vector:\n    def __init__(self, x, y):\n        self.x = x\n        self.y = y\n    def __add__(self, other):\n        return Vector(self.x + other.x, self.y + other.y)\n    def __repr__(self):\n        return f'Vector({self.x}, {self.y})'\n\nv1 = Vector(1, 2)\nv2 = Vector(3, 4)\nprint(v1 + v2)",
    co("排列代码到正确顺序",
       ["    def __add__(self, other):", "        return Vector(self.x + other.x, self.y + other.y)", "class Vector:", "    def __init__(self, x, y):", "        self.x = x", "        self.y = y"],
       [2, 3, 4, 5, 0, 1],
       "正确顺序：class -> __init__ -> x赋值 -> y赋值 -> __add__ -> 返回新Vector。"),
    quiz("__add__ 方法重载了什么运算符？",
         ["-", "+", "*", "/"],
         1, "__add__重载+运算符。v1 + v2 等价于 v1.__add__(v2)。"))

add(6, "py-classes", "比较运算符重载",
    "通过 __eq__、__lt__、__gt__ 等方法重载比较运算符。可以用 @functools.total_ordering 自动生成。",
    "from functools import total_ordering\n\n@total_ordering\nclass Student:\n    def __init__(self, name, score):\n        self.name = name\n        self.score = score\n    def __eq__(self, other):\n        return self.score == other.score\n    def __lt__(self, other):\n        return self.score < other.score\n\ns1 = Student('A', 90)\ns2 = Student('B', 85)\nprint(s1 > s2)",
    fl("填写装饰器",
       "from functools import ___\n\n@total_ordering\nclass Student:\n    def __eq__(self, other):\n        return self.score == other.score\n    def __lt__(self, other):\n        return self.score < other.score",
       [{"position": 0, "answer": "total_ordering", "options": ["total_ordering", "lru_cache", "wraps", "partial"]}],
       "@total_ordering只需定义__eq__和__lt__，自动生成其他比较方法。"),
    quiz("@total_ordering 的作用是什么？",
         ["加速比较", "自动生成所有比较方法", "排序", "删除方法"],
         1, "只需定义__eq__和一个比较方法，@total_ordering自动生成其余。"))

add(6, "py-classes", "容器协议 __len__",
    "__len__ 让对象支持 len() 函数。返回容器中元素的数量。",
    "class Playlist:\n    def __init__(self):\n        self.songs = []\n    def add(self, song):\n        self.songs.append(song)\n    def __len__(self):\n        return len(self.songs)\n\np = Playlist()\np.add('歌曲A')\np.add('歌曲B')\nprint(len(p))",
    po("这段代码输出什么？",
       "class Playlist:\n    def __init__(self):\n        self.songs = []\n    def add(self, song):\n        self.songs.append(song)\n    def __len__(self):\n        return len(self.songs)\np = Playlist()\np.add('歌曲A')\np.add('歌曲B')\nprint(len(p))",
       ["2", "0", "报错", "None"],
       0, "添加了两首歌，len(p)调用__len__返回2。"),
    quiz("__len__ 方法让对象支持什么函数？",
         ["str()", "len()", "type()", "int()"],
         1, "__len__让对象支持len()函数调用。"))

add(6, "py-classes", "__getitem__ 和 __setitem__",
    "__getitem__ 让对象支持 obj[key] 读取。__setitem__ 支持 obj[key] = value 赋值。",
    "class Registry:\n    def __init__(self):\n        self._data = {}\n    def __getitem__(self, key):\n        return self._data[key]\n    def __setitem__(self, key, value):\n        self._data[key] = value\n\nr = Registry()\nr['name'] = '小明'\nprint(r['name'])",
    fb("找出代码中的问题",
       ["class Registry:", "    def __init__(self):", "        self._data = {}", "    def __getitem__(self, key):", "        return self._data[key]", "", "r = Registry()", "r['name'] = '小明'"],
       7, "第8行r['name'] = '小明'需要__setitem__方法，但类中没有定义。需要添加def __setitem__(self, key, value)。"),
    quiz("__getitem__ 的作用是什么？",
         ["设置属性", "支持 obj[key] 读取", "删除属性", "创建对象"],
         1, "__getitem__让对象支持下标读取 obj[key]。"))

add(6, "py-classes", "__enter__ 和 __exit__",
    "__enter__ 和 __exit__ 实现上下文管理器协议。支持 with 语句，确保资源正确释放。",
    "class Timer:\n    def __enter__(self):\n        import time\n        self.start = time.time()\n        return self\n    def __exit__(self, *args):\n        import time\n        self.elapsed = time.time() - self.start\n        print(f'耗时: {self.elapsed:.2f}秒')\n\nwith Timer() as t:\n    total = sum(range(1000000))",
    co("排列代码到正确顺序",
       ["    def __exit__(self, *args):", "class Timer:", "    def __enter__(self):", "        return self", "        self.start = time.time()"],
       [1, 2, 4, 3, 0],
       "正确顺序：class -> __enter__ -> 记录时间 -> 返回self -> __exit__。"),
    quiz("with 语句会调用哪两个方法？",
         ["__init__ 和 __del__", "__enter__ 和 __exit__", "__open__ 和 __close__", "__start__ 和 __end__"],
         1, "with语句调用__enter__进入上下文，__exit__退出并清理。"))

add(6, "py-classes", "__call__ 可调用对象",
    "__call__ 让类的实例可以像函数一样被调用。obj() 等价于 obj.__call__()。",
    "class Multiplier:\n    def __init__(self, factor):\n        self.factor = factor\n    def __call__(self, x):\n        return x * self.factor\n\ndouble = Multiplier(2)\ntriple = Multiplier(3)\nprint(double(5))\nprint(triple(5))",
    fl("填写方法名",
       "class Multiplier:\n    def __init__(self, factor):\n        self.factor = factor\n    def ___(self, x):\n        return x * self.factor",
       [{"position": 0, "answer": "__call__", "options": ["__call__", "__apply__", "__run__", "__execute__"]}],
       "__call__让实例可以像函数一样被调用。"),
    quiz("__call__ 方法的作用是什么？",
         ["创建对象", "让实例可以像函数一样被调用", "删除对象", "比较对象"],
         1, "__call__让实例可以像函数一样调用 obj()。"))

add(6, "py-classes", "@property 属性装饰器",
    "@property 将方法变为只读属性。@x.setter 定义setter。实现数据封装。",
    "class Temperature:\n    def __init__(self, celsius):\n        self._celsius = celsius\n    @property\n    def fahrenheit(self):\n        return self._celsius * 9/5 + 32\n    @fahrenheit.setter\n    def fahrenheit(self, value):\n        self._celsius = (value - 32) * 5/9\n\nt = Temperature(100)\nprint(t.fahrenheit)\nt.fahrenheit = 212\nprint(t._celsius)",
    fb("找出代码中的问题",
       ["class Temperature:", "    def __init__(self, celsius):", "        self._celsius = celsius", "    @property", "    def fahrenheit(self):", "        return self._celsius * 9/5 + 32", "    @fahrenheit.setter", "    def fahrenheit(self, value):", "        self._celsius = (value - 32) * 5/9", "", "t = Temperature(100)", "t.fahrenheit = 212", "print(t.fahrenheit())"],
       12, "第13行fahrenheit是@property，不需要括号。应改为 print(t.fahrenheit)。"),
    quiz("@property 的 getter 和 setter 分别用什么装饰器？",
         ["@get 和 @set", "@property 和 @x.setter", "@read 和 @write", "@get_x 和 @set_x"],
         1, "@property装饰getter，@属性名.setter装饰setter。"))

add(6, "py-classes", "描述符基础",
    "描述符是实现了 __get__、__set__ 或 __delete__ 的类。可以自定义属性访问行为。",
    "class Positive:\n    def __set_name__(self, owner, name):\n        self.name = name\n    def __get__(self, obj, objtype=None):\n        return obj.__dict__[self.name]\n    def __set__(self, obj, value):\n        if value < 0:\n            raise ValueError('必须为正数')\n        obj.__dict__[self.name] = value\n\nclass Account:\n    balance = Positive()\n    def __init__(self, balance):\n        self.balance = balance",
    co("排列代码到正确顺序",
       ["        obj.__dict__[self.name] = value", "class Positive:", "    def __set__(self, obj, value):", "    def __get__(self, obj, objtype=None):", "        return obj.__dict__[self.name]", "        if value < 0:"],
       [1, 3, 4, 2, 5, 0],
       "正确顺序：Positive -> __get__ -> 返回 -> __set__ -> 检查 -> 赋值。"),
    quiz("描述符需要实现哪些方法？",
         ["__init__", "__get__、__set__ 或 __delete__", "__str__", "__call__"],
         1, "描述符实现__get__、__set__或__delete__来自定义属性访问。"))

add(6, "py-classes", "__slots__ 限制属性",
    "__slots__ 限制实例可以拥有的属性，节省内存。定义后不能再添加slots外的属性。",
    "class Point:\n    __slots__ = ['x', 'y']\n    def __init__(self, x, y):\n        self.x = x\n        self.y = y\n\np = Point(1, 2)\nprint(p.x)\np.z = 3  # 报错！",
    fl("填写限制属性的变量",
       "class Point:\n    ___ = ['x', 'y']\n    def __init__(self, x, y):\n        self.x = x\n        self.y = y",
       [{"position": 0, "answer": "__slots__", "options": ["__slots__", "__attrs__", "__fields__", "__properties__"]}],
       "__slots__限制实例可以拥有的属性列表。"),
    quiz("__slots__ 的好处是什么？",
         ["更快", "节省内存，限制属性", "更安全", "自动初始化"],
         1, "__slots__通过不用__dict__节省内存，并限制实例属性。"))

add(6, "py-classes", "dataclass 数据类",
    "@dataclass 自动生成 __init__、__repr__、__eq__ 等方法。适合纯数据容器。",
    "from dataclasses import dataclass\n\n@dataclass\nclass Student:\n    name: str\n    score: int\n    grade: str = 'A'\n\ns = Student('小明', 90)\nprint(s)\nprint(s == Student('小明', 90))",
    po("这段代码输出什么？",
       "from dataclasses import dataclass\n@dataclass\nclass Student:\n    name: str\n    score: int\n    grade: str = 'A'\ns = Student('小明', 90)\nprint(s)\nprint(s == Student('小明', 90))",
       ["Student(name='小明', score=90, grade='A')\\nTrue", "小明\\nTrue", "报错", "None\\nFalse"],
       0, "@dataclass自动生成__repr__和__eq__，打印格式化的表示，比较基于所有字段。"),
    quiz("@dataclass 自动生成哪些方法？",
         ["只有__init__", "__init__、__repr__、__eq__等", "只有__str__", "只有__repr__"],
         1, "@dataclass自动生成__init__、__repr__、__eq__等常用方法。"))

add(6, "py-classes", "枚举类",
    "enum.Enum 定义一组命名常量。比普通变量更安全，防止无效值。",
    "from enum import Enum\n\nclass Color(Enum):\n    RED = 1\n    GREEN = 2\n    BLUE = 3\n\nc = Color.RED\nprint(c.name)\nprint(c.value)\nprint(c == Color.RED)",
    fl("填写基类",
       "from enum import Enum\nclass Color(___):\n    RED = 1\n    GREEN = 2",
       [{"position": 0, "answer": "Enum", "options": ["Enum", "Class", "Object", "Base"]}],
       "枚举类继承Enum基类。"),
    quiz("枚举类的好处是什么？",
         ["更快", "防止无效值，代码更清晰", "更短", "更灵活"],
         1, "枚举限制值只能是预定义的常量，防止无效值。"))


# --- py-inheritance (20 points) ---

add(6, "py-inheritance", "继承基础",
    "子类继承父类的所有属性和方法。用 class Child(Parent) 语法。子类可以添加新功能。",
    "class Animal:\n    def __init__(self, name):\n        self.name = name\n    def speak(self):\n        return f'{self.name}发出声音'\n\nclass Dog(Animal):\n    def fetch(self):\n        return f'{self.name}捡球'\n\nd = Dog('旺财')\nprint(d.speak())\nprint(d.fetch())",
    co("排列代码到正确顺序",
       ["    def fetch(self):", "class Dog(Animal):", "class Animal:", "    def __init__(self, name):", "        self.name = name", "    def speak(self):", "        return f'{self.name}发出声音'", "        return f'{self.name}捡球'"],
       [2, 3, 4, 5, 6, 1, 0, 7],
       "正确顺序：Animal -> __init__ -> name -> speak -> 返回 -> Dog -> fetch -> 返回。"),
    quiz("class Dog(Animal) 中 Dog 和 Animal 的关系是什么？",
         ["Dog创建Animal", "Dog继承Animal", "Animal继承Dog", "没有关系"],
         1, "Dog(Animal)表示Dog继承Animal，Dog是子类，Animal是父类。"))

add(6, "py-inheritance", "方法重写",
    "子类可以重写(override)父类的方法。同名方法会覆盖父类的实现。",
    "class Shape:\n    def area(self):\n        return 0\n\nclass Circle(Shape):\n    def __init__(self, radius):\n        self.radius = radius\n    def area(self):\n        return 3.14 * self.radius ** 2\n\nc = Circle(5)\nprint(c.area())",
    fb("找出代码中的问题",
       ["class Shape:", "    def area(self):", "        return 0", "", "class Circle(Shape):", "    def __init__(self, radius):", "        self.radius = radius", "    def area(self):", "        return 3.14 * self.radius ** 2", "", "c = Circle(5)", "print(Shape.area(c))"],
       11, "第12行Shape.area(c)绕过了Circle的重写，直接调用父类的area返回0。应改为 c.area() 调用子类重写的方法。"),
    quiz("方法重写(override)是什么？",
         ["删除父类方法", "子类重新定义父类的方法", "调用父类方法", "创建新方法"],
         1, "重写是子类定义与父类同名的方法，覆盖父类的实现。"))

add(6, "py-inheritance", "super() 调用父类",
    "super() 调用父类的方法。常用于在子类中扩展父类的功能而不是完全替换。",
    "class Base:\n    def __init__(self, name):\n        self.name = name\n\nclass Child(Base):\n    def __init__(self, name, age):\n        super().__init__(name)\n        self.age = age\n\nc = Child('小明', 20)\nprint(c.name, c.age)",
    fl("填写调用父类的函数",
       "class Child(Base):\n    def __init__(self, name, age):\n        ___().__init__(name)\n        self.age = age",
       [{"position": 0, "answer": "super", "options": ["super", "parent", "base", "cls"]}],
       "super()返回代理对象，调用父类的方法。"),
    quiz("super() 的作用是什么？",
         ["创建父类", "调用父类的方法", "删除父类", "比较父类"],
         1, "super()调用父类的方法，常用于在子类__init__中调用父类__init__。"))

add(6, "py-inheritance", "多态",
    "多态：不同类的对象对同一方法有不同的实现。调用时不需要知道具体类型。",
    "class Cat:\n    def speak(self):\n        return '喵~'\n\nclass Dog:\n    def speak(self):\n        return '汪!'\n\ndef animal_sound(animal):\n    print(animal.speak())\n\nanimal_sound(Cat())\nanimal_sound(Dog())",
    po("这段代码输出什么？",
       "class Cat:\n    def speak(self):\n        return '喵~'\nclass Dog:\n    def speak(self):\n        return '汪!'\ndef animal_sound(animal):\n    print(animal.speak())\nanimal_sound(Cat())\nanimal_sound(Dog())",
       ["喵~\\n汪!", "汪!\\n喵~", "报错", "None\\nNone"],
       0, "多态：同一个speak方法，Cat返回'喵~'，Dog返回'汪!'。"),
    quiz("多态的含义是什么？",
         ["一个类有多个方法", "不同对象对同一方法有不同实现", "一个方法有多个参数", "一个对象有多个类型"],
         1, "多态让不同类型的对象对同一调用有不同的响应。"))

add(6, "py-inheritance", "isinstance 和 issubclass",
    "isinstance(obj, Class) 检查对象是否是某类的实例。issubclass(Child, Parent) 检查继承关系。",
    "class Animal: pass\nclass Dog(Animal): pass\nclass Cat(Animal): pass\n\nd = Dog()\nprint(isinstance(d, Dog))     # True\nprint(isinstance(d, Animal))  # True\nprint(issubclass(Dog, Animal))",
    fl("填写检查函数",
       "class Animal: pass\nclass Dog(Animal): pass\nd = Dog()\nprint(___(d, Animal))  # True",
       [{"position": 0, "answer": "isinstance", "options": ["isinstance", "issubclass", "type", "hasattr"]}],
       "isinstance检查对象是否是某类（或其子类）的实例。"),
    quiz("isinstance(Dog(), Animal) 返回什么？",
         ["False", "True", "None", "报错"],
         1, "Dog继承Animal，Dog的实例也是Animal的实例，返回True。"))

add(6, "py-inheritance", "抽象类 ABC",
    "ABC（抽象基类）不能被实例化，只能被继承。用 @abstractmethod 定义抽象方法，子类必须实现。",
    "from abc import ABC, abstractmethod\n\nclass Shape(ABC):\n    @abstractmethod\n    def area(self):\n        pass\n\nclass Circle(Shape):\n    def __init__(self, r):\n        self.r = r\n    def area(self):\n        return 3.14 * self.r ** 2\n\nc = Circle(5)\nprint(c.area())",
    fb("找出代码中的错误",
       ["from abc import ABC, abstractmethod", "", "class Shape(ABC):", "    @abstractmethod", "    def area(self):", "        pass", "", "s = Shape()"],
       7, "第8行尝试实例化抽象类Shape，会报TypeError。抽象类不能直接创建实例。"),
    quiz("抽象类(ABC)能被实例化吗？",
         ["能", "不能，只能被继承", "有时能", "看Python版本"],
         1, "抽象类不能实例化，只能被继承。子类必须实现所有抽象方法。"))

add(6, "py-inheritance", "多重继承",
    "Python支持多重继承：class Child(Parent1, Parent2)。子类继承所有父类的方法。",
    "class Flyable:\n    def fly(self):\n        return '飞行'\n\nclass Swimmable:\n    def swim(self):\n        return '游泳'\n\nclass Duck(Flyable, Swimmable):\n    pass\n\nd = Duck()\nprint(d.fly())\nprint(d.swim())",
    fl("填写继承语法",
       "class Duck(Flyable, Swimmable):\n    pass\n# Duck同时继承了___和Swimmable",
       [{"position": 0, "answer": "Flyable", "options": ["Flyable", "Animal", "Object", "Duck"]}],
       "多重继承用逗号分隔多个父类：class Duck(Flyable, Swimmable)。"),
    quiz("多重继承中如果两个父类有同名方法会怎样？",
         ["报错", "按MRO顺序调用第一个", "随机调用", "两个都调用"],
         1, "多重继承按MRO（方法解析顺序）查找方法，调用第一个找到的。"))

add(6, "py-inheritance", "MRO 方法解析顺序",
    "MRO(Method Resolution Order)决定方法查找顺序。用 类名.__mro__ 或 mro() 查看。",
    "class A:\n    def greet(self): return 'A'\nclass B(A):\n    def greet(self): return 'B'\nclass C(A):\n    pass\nclass D(B, C):\n    pass\n\nprint(D.__mro__)\nprint(D().greet())",
    co("排列代码到正确顺序",
       ["class D(B, C):", "class B(A):", "    def greet(self): return 'A'", "class A:", "    def greet(self): return 'B'", "class C(A):", "    pass"],
       [3, 2, 1, 4, 5, 6, 0],
       "正确顺序：A -> greetA -> B -> greetB -> C -> pass -> D。"),
    quiz("MRO 的查找顺序是什么？",
         ["从右到左", "深度优先", "C3线性化算法", "随机"],
         2, "Python使用C3线性化算法确定MRO，保证单调性和一致性。"))

add(6, "py-inheritance", "Mixin 模式",
    "Mixin是提供额外功能的类，通常不单独使用。通过多重继承组合功能。",
    "class JSONMixin:\n    def to_json(self):\n        import json\n        return json.dumps(self.__dict__)\n\nclass User(JSONMixin):\n    def __init__(self, name, age):\n        self.name = name\n        self.age = age\n\nu = User('小明', 20)\nprint(u.to_json())",
    po("这段代码输出什么？",
       "class JSONMixin:\n    def to_json(self):\n        import json\n        return json.dumps(self.__dict__)\nclass User(JSONMixin):\n    def __init__(self, name, age):\n        self.name = name\n        self.age = age\nu = User('小明', 20)\nprint(u.to_json())",
       ["{\"name\": \"小明\", \"age\": 20}", "小明", "报错", "None"],
       0, "JSONMixin提供to_json方法，User继承后可以直接使用。__dict__包含实例属性。"),
    quiz("Mixin 模式的特点是什么？",
         ["单独使用", "提供额外功能，通过多重继承组合", "替代继承", "必须有__init__"],
         1, "Mixin提供可复用的功能片段，通过多重继承组合到类中。"))

add(6, "py-inheritance", "组合 vs 继承",
    "组合(has-a)：对象包含其他对象。继承(is-a)：子类是父类的一种。优先用组合，少用继承。",
    "# 继承：Dog is an Animal\nclass Dog(Animal):\n    pass\n\n# 组合：Car has an Engine\nclass Engine:\n    def start(self): return '引擎启动'\n\nclass Car:\n    def __init__(self):\n        self.engine = Engine()\n    def start(self):\n        return self.engine.start()",
    fb("找出代码中的设计问题",
       ["class Engine:", "    def start(self): return '引擎启动'", "", "class Car:", "    def __init__(self):", "        self.engine = Engine()", "    def start(self):", "        return self.engine.start()", "", "# 如果要创建ElectricCar，应该？", "class ElectricCar(Car):  # 继承"],
       10, "第11行用继承不合适，ElectricCar的引擎不同。应改为组合：在ElectricCar中包含ElectricEngine。"),
    quiz("什么时候优先用组合而非继承？",
         ["总是用继承", "当是'has-a'关系时用组合", "当是'is-a'关系时用组合", "任何时候"],
         1, "'has-a'关系用组合（包含），'is-a'关系用继承（是一种）。"))

add(6, "py-inheritance", "鸭子类型",
    "鸭子类型：不关心对象是什么类，只关心它有没有需要的方法。'如果它像鸭子叫，那它就是鸭子。'",
    "class Duck:\n    def quack(self): return '嘎嘎'\n\nclass Person:\n    def quack(self): return '我学鸭子叫：嘎嘎'\n\ndef make_it_quack(thing):\n    print(thing.quack())\n\nmake_it_quack(Duck())\nmake_it_quack(Person())",
    fl("填写类型检查方式",
       "# 鸭子类型不检查class，只检查___\n# 如果对象有quack方法，就当它是鸭子",
       [{"position": 0, "answer": "方法", "options": ["方法", "属性", "类型", "名字"]}],
       "鸭子类型只关心对象有没有需要的方法，不关心类型。"),
    quiz("鸭子类型的核心思想是什么？",
         ["检查类型", "不检查类型，只检查行为（方法）", "必须继承", "必须用ABC"],
         1, "鸭子类型不关心对象是什么类，只关心它有没有需要的方法。"))

add(6, "py-inheritance", "继承与 __init__",
    "子类不定义__init__时自动继承父类的__init__。定义了就必须手动调用super().__init__()。",
    "class Base:\n    def __init__(self, x):\n        self.x = x\n\nclass Child(Base):\n    def __init__(self, x, y):\n        super().__init__(x)\n        self.y = y\n\nc = Child(1, 2)\nprint(c.x, c.y)",
    fb("找出代码中的错误",
       ["class Base:", "    def __init__(self, x):", "        self.x = x", "", "class Child(Base):", "    def __init__(self, x, y):", "        self.y = y", "", "c = Child(1, 2)", "print(c.x)"],
       6, "第7行Child的__init__没有调用super().__init__(x)，c.x未被初始化，访问会报AttributeError。"),
    quiz("子类定义了__init__后需要做什么？",
         ["什么都不做", "手动调用 super().__init__() 初始化父类", "删除父类", "重写所有方法"],
         1, "子类定义__init__后必须手动调用super().__init__()来初始化父类属性。"))

add(6, "py-inheritance", "菱形继承",
    "菱形继承：多个子类继承同一个父类，孙类继承多个子类。MRO确保父类只被初始化一次。",
    "class A:\n    def __init__(self):\n        print('A')\nclass B(A):\n    def __init__(self):\n        super().__init__()\n        print('B')\nclass C(A):\n    def __init__(self):\n        super().__init__()\n        print('C')\nclass D(B, C):\n    def __init__(self):\n        super().__init__()\n        print('D')",
    po("D() 输出什么？",
       "class A:\n    def __init__(self): print('A')\nclass B(A):\n    def __init__(self): super().__init__(); print('B')\nclass C(A):\n    def __init__(self): super().__init__(); print('C')\nclass D(B, C):\n    def __init__(self): super().__init__(); print('D')\nD()",
       ["A B C D", "A B D", "A C B D", "A C B D"],
       2, "MRO: D -> B -> C -> A。super()沿MRO调用，输出A C B D。"),
    quiz("菱形继承中Python如何避免重复初始化？",
         ["忽略重复", "MRO确保每个类只被初始化一次", "报错", "随机初始化"],
         1, "C3线性化的MRO确保在菱形继承中每个类只被初始化一次。"))

add(6, "py-inheritance", "协议 Protocol",
    "typing.Protocol 定义结构化子类型(鸭子类型的正式版)。类不需要显式继承Protocol。",
    "from typing import Protocol\n\nclass Drawable(Protocol):\n    def draw(self) -> str: ...\n\nclass Circle:\n    def draw(self) -> str:\n        return '画圆'\n\ndef render(obj: Drawable) -> None:\n    print(obj.draw())\n\nrender(Circle())",
    fl("填写基类",
       "from typing import Protocol\nclass Drawable(___):\n    def draw(self) -> str: ...",
       [{"position": 0, "answer": "Protocol", "options": ["Protocol", "ABC", "Interface", "Base"]}],
       "Protocol定义结构化子类型，类不需要显式继承。"),
    quiz("Protocol 和 ABC 的区别是什么？",
         ["没有区别", "Protocol不需要显式继承，ABC必须继承", "Protocol更快", "ABC更灵活"],
         1, "Protocol是结构化子类型，不需要显式继承；ABC需要显式继承。"))

add(6, "py-inheritance", "继承链",
    "继承可以有多层：GrandParent -> Parent -> Child。每层都可以添加或重写方法。",
    "class Animal:\n    def __init__(self, name):\n        self.name = name\n    def speak(self): return '...'\nclass Mammal(Animal):\n    def walk(self): return f'{self.name}走路'\nclass Dog(Mammal):\n    def speak(self): return '汪!'\n\nd = Dog('旺财')\nprint(d.speak())\nprint(d.walk())",
    co("排列代码到正确顺序",
       ["class Dog(Mammal):", "class Mammal(Animal):", "    def walk(self): return f'{self.name}走路'", "    def speak(self): return '汪!'", "class Animal:", "    def __init__(self, name):", "        self.name = name", "    def speak(self): return '...'"],
       [4, 5, 6, 7, 1, 2, 0, 3],
       "正确顺序：Animal -> __init__ -> name -> speak -> Mammal -> walk -> Dog -> speak。"),
    quiz("三层继承中，子类能访问哪些方法？",
         ["只能自己的", "自己的和所有父类的", "只能父类的", "只能祖父类的"],
         1, "子类可以访问自己定义的方法以及所有祖先类的方法。"))

add(6, "py-inheritance", "猴子补丁",
    "猴子补丁是在运行时修改类或模块。可以给已有类添加方法，但应谨慎使用。",
    "class Dog:\n    def __init__(self, name):\n        self.name = name\n\n# 猴子补丁：运行时添加方法\ndef bark(self):\n    return f'{self.name}: 汪!'\n\nDog.bark = bark\n\nd = Dog('旺财')\nprint(d.bark())",
    fl("填写猴子补丁的代码",
       "class Dog:\n    def __init__(self, name):\n        self.name = name\ndef bark(self):\n    return f'{self.name}: 汪!'\n# 猴子补丁\nDog.___ = bark",
       [{"position": 0, "answer": "bark", "options": ["bark", "add", "method", "new"]}],
       "Dog.bark = bark 直接给类添加方法，这就是猴子补丁。"),
    quiz("猴子补丁是什么？",
         ["删除方法", "运行时修改类或模块", "创建新类", "导入模块"],
         1, "猴子补丁是在运行时动态修改类或模块的行为。"))

add(6, "py-inheritance", "密封类",
    "密封类(Sealed Class)不能被继承。Python没有内置支持，可以用元类实现。",
    "class SealedMeta(type):\n    _sealed = set()\n    def __init_subclass__(cls, **kwargs):\n        raise TypeError('不能继承密封类')\n\nclass Sealed(metaclass=SealedMeta):\n    pass\n\nclass TryExtend(Sealed):  # 报错！\n    pass",
    fb("找出代码中的问题",
       ["class SealedMeta(type):", "    _sealed = set()", "    def __init_subclass__(cls, **kwargs):", "        raise TypeError('不能继承密封类')", "", "class Sealed(metaclass=SealedMeta):", "    pass", "", "class TryExtend(Sealed):", "    pass"],
       8, "第9行尝试继承密封类Sealed，会触发__init_subclass__中的TypeError。"),
    quiz("密封类的作用是什么？",
         ["加速实例化", "防止被继承", "自动初始化", "创建单例"],
         1, "密封类禁止其他类继承它，确保类的行为不被修改。"))

add(6, "py-inheritance", "类工厂",
    "类工厂是动态创建类的函数。type() 可以在运行时创建新类。",
    "# type() 创建类等价于 class 语句\nDog = type('Dog', (object,), {\n    'species': '犬科',\n    'bark': lambda self: '汪!'\n})\n\nd = Dog()\nprint(d.species)\nprint(d.bark())",
    co("排列代码到正确顺序",
       ["print(d.species)", "    'bark': lambda self: '汪!'", "d = Dog()", "Dog = type('Dog', (object,), {", "})", "    'species': '犬科',", "print(d.bark())"],
       [3, 5, 1, 4, 2, 0, 6],
       "正确顺序：type创建类 -> species -> bark -> 闭合 -> 实例化 -> 打印species -> 打印bark。"),
    quiz("type('Dog', (object,), {}) 中三个参数分别是什么？",
         ["名字、父类元组、属性字典", "名字、属性、方法", "父类、名字、属性", "属性、名字、父类"],
         0, "type(类名, 父类元组, 属性字典) 动态创建类。"))

add(6, "py-inheritance", "单例模式",
    "单例模式确保一个类只有一个实例。用__new__方法控制实例的创建。",
    "class Singleton:\n    _instance = None\n    def __new__(cls):\n        if cls._instance is None:\n            cls._instance = super().__new__(cls)\n        return cls._instance\n\na = Singleton()\nb = Singleton()\nprint(a is b)",
    fl("填写实例检查",
       "class Singleton:\n    _instance = None\n    def __new__(cls):\n        if cls._instance is ___:\n            cls._instance = super().__new__(cls)\n        return cls._instance",
       [{"position": 0, "answer": "None", "options": ["None", "True", "False", "0"]}],
       "检查_instance是否为None，如果是则创建新实例。"),
    quiz("单例模式的作用是什么？",
         ["创建多个实例", "确保一个类只有一个实例", "加速实例化", "删除实例"],
         1, "单例模式确保全局只有一个实例，常用于配置、数据库连接等。"))

add(6, "py-inheritance", "继承最佳实践",
    "继承最佳实践：1.优先组合 2.浅继承层次 3.里氏替换原则 4.用ABC定义接口 5.避免菱形继承。",
    "# 好的设计：接口用ABC\nfrom abc import ABC, abstractmethod\n\nclass Repository(ABC):\n    @abstractmethod\n    def save(self, item): pass\n    @abstractmethod\n    def find(self, id): pass\n\nclass UserRepository(Repository):\n    def save(self, item): ...\n    def find(self, id): ...",
    fl("填写最佳实践",
       "# 继承层次不要太___\n# 推荐最多3层：Base -> Middle -> Leaf",
       [{"position": 0, "answer": "深", "options": ["深", "宽", "多", "少"]}],
       "继承层次不要太深，推荐最多3层，过深会导致理解和维护困难。"),
    quiz("里氏替换原则(LSP)的含义是什么？",
         ["子类必须调用父类方法", "子类对象必须能替换父类对象使用", "父类必须调用子类方法", "子类不能重写父类"],
         1, "LSP：子类对象必须能在任何使用父类的地方正确工作，不改变程序的正确性。"))


# ============================================================
# Write output
# ============================================================

out_path = Path(__file__).parent / "data" / "kp_weeks_4_6.json"
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
