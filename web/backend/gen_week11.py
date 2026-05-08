"""
Generate knowledge points for Week 11.
Week 11: 设计模式与AI框架
- pat-strategy: 策略模式
- pat-observer: 观察者模式
- pat-factory: 工厂模式
- pat-repository: 仓库模式
- pat-pipeline: 管道模式
- py-fastapi: FastAPI框架
- py-langchain: LangChain框架

Output: web/backend/data/kp_week11.json
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
# WEEK 11: 设计模式与AI框架
# ============================================================

# --- pat-strategy (10 points) ---

add(11, "pat-strategy", "什么是策略模式",
    "策略模式把不同的算法封装成独立的策略类，让它们可以互相替换。客户端不需要知道具体算法，只通过上下文对象使用。就像导航App可以选择最快路线、最短路线、不走高速等不同策略。",
    "// 策略接口\ntype SortStrategy = (arr: number[]) => number[];\n\n// 具体策略\nconst bubbleSort: SortStrategy = (arr) => {\n    const a = [...arr];\n    // 冒泡排序逻辑\n    return a;\n};\n\nconst quickSort: SortStrategy = (arr) => {\n    // 快速排序逻辑\n    return [...arr];\n};",
    po("策略模式的核心思想是什么？",
       "// 策略接口\ntype SortStrategy = (arr: number[]) => number[];\n\nconst bubbleSort: SortStrategy = (arr) => {\n    const a = [...arr];\n    return a;\n};",
       ["把所有算法写在一个函数里", "把算法封装成可替换的策略", "用if-else选择算法", "删除算法"],
       1, "策略模式的核心是把算法封装成独立的策略对象，可以互相替换。"),
    quiz("策略模式的主要优点是什么？",
         ["代码更短", "算法可以互相替换，避免大量if-else", "运行更快", "减少内存"],
         1, "策略模式让算法独立于客户端变化，可以互相替换，避免大量if-else判断。"))

add(11, "pat-strategy", "上下文类 Context",
    "上下文类持有策略对象的引用，通过策略接口调用具体算法。客户端通过设置不同的策略来改变行为。",
    "class Context {\n    private strategy: SortStrategy;\n\n    constructor(strategy: SortStrategy) {\n        this.strategy = strategy;\n    }\n\n    setStrategy(strategy: SortStrategy) {\n        this.strategy = strategy;\n    }\n\n    execute(arr: number[]): number[] {\n        return this.strategy(arr);\n    }\n}",
    fl("填写方法名",
       "class Context {\n    private strategy: SortStrategy;\n\n    constructor(strategy: SortStrategy) {\n        this.strategy = strategy;\n    }\n\n    ___(strategy: SortStrategy) {\n        this.strategy = strategy;\n    }\n\n    execute(arr: number[]): number[] {\n        return this.strategy(arr);\n    }\n}",
       [{"position": 0, "answer": "setStrategy", "options": ["setStrategy", "changeStrategy", "updateStrategy", "swapStrategy"]}],
       "setStrategy是策略模式中切换策略的标准方法名。"),
    quiz("上下文类的作用是什么？",
         ["实现具体算法", "持有策略对象，通过接口调用算法", "创建策略", "删除策略"],
         1, "上下文类持有策略引用，客户端通过它间接调用具体算法。"))

add(11, "pat-strategy", "运行时切换策略",
    "策略模式最大的优势是可以在运行时动态切换算法。不需要修改代码，只需要换一个策略对象。",
    "const context = new Context(bubbleSort);\nconsole.log(context.execute([3, 1, 2]));\n\n// 运行时切换为快速排序\ncontext.setStrategy(quickSort);\nconsole.log(context.execute([3, 1, 2]));",
    co("排列代码到正确顺序",
       ["context.setStrategy(quickSort);", "const context = new Context(bubbleSort);", "console.log(context.execute([3, 1, 2]));", "console.log(context.execute([3, 1, 2]));"],
       [1, 2, 0, 3],
       "正确顺序：创建上下文 -> 执行排序 -> 切换策略 -> 再次执行。"),
    quiz("策略模式可以在什么时候切换算法？",
         ["只能在编译时", "可以在运行时动态切换", "不能切换", "只能切换一次"],
         1, "策略模式支持运行时动态切换算法，这是它的核心优势。"))

add(11, "pat-strategy", "策略模式与if-else",
    "没有策略模式时，选择算法通常用if-else。当算法增多时，代码会变得很长且难以维护。策略模式消除了这些条件判断。",
    "// 不好的做法\nfunction sort(arr, type) {\n    if (type === 'bubble') {\n        // 冒泡排序\n    } else if (type === 'quick') {\n        // 快速排序\n    } else if (type === 'merge') {\n        // 归并排序\n    }\n}\n\n// 策略模式的做法\ncontext.setStrategy(bubbleSort);",
    fb("找出代码中的问题",
       ["// 不好的做法", "function sort(arr, type) {", "    if (type === 'bubble') {", "        // 冒泡排序", "    } else if (type === 'quick') {", "        // 快速排序", "    } else if (type === 'merge') {", "        // 归并排序", "    }", "}"],
       -1, "这段代码没有语法错误，但展示了if-else的问题：每增加一种算法都要修改函数，违反开闭原则。策略模式可以解决这个问题。"),
    quiz("策略模式如何替代if-else？",
         ["用switch替代", "把每个分支封装成独立策略对象", "用三元运算符", "不能替代"],
         1, "策略模式把每个算法分支封装成独立的策略类，通过替换策略对象来选择算法。"))

add(11, "pat-strategy", "策略接口的定义",
    "策略接口定义了所有具体策略必须实现的方法。这是策略模式的契约，确保所有策略可以互相替换。",
    "interface PaymentStrategy {\n    pay(amount: number): boolean;\n}\n\nclass CreditCard implements PaymentStrategy {\n    pay(amount: number): boolean {\n        console.log(`信用卡支付 ${amount}元`);\n        return true;\n    }\n}\n\nclass WeChatPay implements PaymentStrategy {\n    pay(amount: number): boolean {\n        console.log(`微信支付 ${amount}元`);\n        return true;\n    }\n}",
    fl("填写接口名",
       "interface ___ {\n    pay(amount: number): boolean;\n}\n\nclass CreditCard implements PaymentStrategy {\n    pay(amount: number): boolean {\n        console.log(`信用卡支付 ${amount}元`);\n        return true;\n    }\n}",
       [{"position": 0, "answer": "PaymentStrategy", "options": ["PaymentStrategy", "Payment", "Strategy", "PayMethod"]}],
       "PaymentStrategy明确表达了这是支付策略的接口。"),
    quiz("策略接口的作用是什么？",
         ["实现具体算法", "定义所有策略必须实现的契约", "创建对象", "删除数据"],
         1, "策略接口确保所有具体策略有统一的方法签名，可以互相替换。"))

add(11, "pat-strategy", "Python中的策略模式",
    "Python中可以用函数作为策略（函数是一等公民），不需要定义类。这比面向对象的方式更简洁。",
    "def bubble_sort(arr):\n    return sorted(arr)  # 简化示例\n\ndef quick_sort(arr):\n    return sorted(arr)  # 简化示例\n\ndef sort_with_strategy(arr, strategy):\n    return strategy(arr)\n\nresult = sort_with_strategy([3, 1, 2], bubble_sort)\nprint(result)",
    po("这段代码输出什么？",
       "def bubble_sort(arr):\n    return sorted(arr)\n\ndef sort_with_strategy(arr, strategy):\n    return strategy(arr)\n\nresult = sort_with_strategy([3, 1, 2], bubble_sort)\nprint(result)",
       ["[3, 1, 2]", "[1, 2, 3]", "报错", "None"],
       1, "sorted()返回排序后的列表，[3,1,2]排序后是[1,2,3]。"),
    quiz("Python中实现策略模式最简洁的方式是什么？",
         ["必须用类", "直接用函数作为策略", "用if-else", "用全局变量"],
         1, "Python函数是一等公民，可以直接传递函数作为策略，比定义类更简洁。"))

add(11, "pat-strategy", "策略模式的实际应用",
    "策略模式在实际项目中广泛使用：排序算法选择、支付方式选择、验证规则选择、压缩算法选择等场景。",
    "class Validator {\n    constructor(private strategy: (value: string) => boolean) {}\n\n    validate(value: string): boolean {\n        return this.strategy(value);\n    }\n}\n\nconst emailValidator = new Validator(\n    (v) => v.includes('@')\n);\nconst phoneValidator = new Validator(\n    (v) => /^1\\d{10}$/.test(v)\n);",
    co("排列代码到正确顺序",
       ["const phoneValidator = new Validator(", "    (v) => /^1\\d{10}$/.test(v)", ");", "class Validator {", "    constructor(private strategy: (value: string) => boolean) {}", "const emailValidator = new Validator(", "    (v) => v.includes('@')", ");", "    validate(value: string): boolean {", "        return this.strategy(value);", "    }", "}"],
       [3, 4, 8, 9, 10, 11, 5, 6, 7, 0, 1, 2],
       "正确顺序：定义Validator类 -> 构造函数 -> validate方法 -> 创建email验证器 -> 创建phone验证器。"),
    quiz("以下哪个场景适合使用策略模式？",
         ["只有一种算法", "需要在多种算法间切换", "算法永远不会变", "只有两行代码"],
         1, "策略模式适合需要在多种算法间动态切换的场景。"))

add(11, "pat-strategy", "策略与工厂结合",
    "策略模式常与工厂模式结合。工厂根据条件创建合适的策略对象，上下文使用策略执行算法。",
    "function createSortStrategy(type: string): SortStrategy {\n    switch (type) {\n        case 'bubble': return bubbleSort;\n        case 'quick': return quickSort;\n        default: throw new Error('未知策略');\n    }\n}\n\nconst strategy = createSortStrategy('quick');\nconst context = new Context(strategy);",
    fb("找出代码中的问题",
       ["function createSortStrategy(type: string): SortStrategy {", "    switch (type) {", "        case 'bubble': return bubbleSort;", "        case 'quick': return quickSort;", "        default: throw new Error('未知策略');", "    }", "}", "", "const strategy = createSortStrategy('merge');", "const context = new Context(strategy);"],
       8, "第9行传入'merge'，但switch中没有'case merge'，会走到default抛出错误。"),
    quiz("策略模式与工厂模式结合的好处是什么？",
         ["代码更长", "工厂负责创建策略，上下文负责使用策略", "更慢", "没有好处"],
         1, "工厂负责创建合适的策略对象，上下文负责使用策略，职责分离更清晰。"))

add(11, "pat-strategy", "开闭原则与策略模式",
    "策略模式遵循开闭原则：对扩展开放（可以添加新策略），对修改封闭（不需要修改已有代码）。",
    "// 添加新策略：只需新增一个类\nclass Alipay implements PaymentStrategy {\n    pay(amount: number): boolean {\n        console.log(`支付宝支付 ${amount}元`);\n        return true;\n    }\n}\n// 不需要修改任何已有代码！\ncontext.setStrategy(new Alipay());",
    fl("填写新策略类名",
       "// 添加新策略：只需新增一个类\nclass ___ implements PaymentStrategy {\n    pay(amount: number): boolean {\n        console.log(`支付宝支付 ${amount}元`);\n        return true;\n    }\n}",
       [{"position": 0, "answer": "Alipay", "options": ["Alipay", "Payment", "NewPay", "Strategy"]}],
       "Alipay是支付宝的类名，实现了PaymentStrategy接口。"),
    quiz("开闭原则的含义是什么？",
         ["对扩展开放，对修改封闭", "对扩展封闭，对修改开放", "都开放", "都封闭"],
         0, "开闭原则：软件实体对扩展开放（可以加新功能），对修改封闭（不改已有代码）。"))

add(11, "pat-strategy", "策略模式的优缺点",
    "优点：算法可替换、符合开闭原则、消除if-else。缺点：客户端必须知道所有策略、增加类的数量。",
    "// 优点：切换算法只需一行\ncontext.setStrategy(new QuickSort());\n\n// 缺点：客户端需要了解所有策略\nconst strategies = {\n    bubble: new BubbleSort(),\n    quick: new QuickSort(),\n    merge: new MergeSort(),\n    heap: new HeapSort(),\n};",
    co("排列优缺点到正确顺序",
       ["符合开闭原则", "算法可替换", "增加类的数量", "消除if-else", "客户端必须知道所有策略"],
       [1, 3, 0, 4, 2],
       "优点：算法可替换、消除if-else、符合开闭原则。缺点：客户端必须知道所有策略、增加类的数量。"),
    quiz("策略模式的主要缺点是什么？",
         ["运行慢", "客户端必须知道所有策略，增加类数量", "不能切换算法", "代码太短"],
         1, "策略模式的缺点是客户端需要了解所有策略类，且每种策略一个类，增加了类的数量。"))


# --- pat-observer (10 points) ---

add(11, "pat-observer", "什么是观察者模式",
    "观察者模式定义了对象间的一对多依赖关系。当一个对象（主题）状态变化时，所有依赖它的对象（观察者）都会收到通知。就像你订阅了一个YouTube频道，有新视频时会收到通知。",
    "interface Observer {\n    update(data: string): void;\n}\n\nclass Subject {\n    private observers: Observer[] = [];\n\n    subscribe(observer: Observer) {\n        this.observers.push(observer);\n    }\n\n    notify(data: string) {\n        this.observers.forEach(o => o.update(data));\n    }\n}",
    po("观察者模式的核心思想是什么？",
       "interface Observer {\n    update(data: string): void;\n}\n\nclass Subject {\n    private observers: Observer[] = [];\n\n    subscribe(observer: Observer) {\n        this.observers.push(observer);\n    }\n\n    notify(data: string) {\n        this.observers.forEach(o => o.update(data));\n    }\n}",
       ["一对多的依赖关系，状态变化时自动通知", "一对一的调用关系", "循环调用", "随机通知"],
       0, "观察者模式的核心是一对多依赖，主题状态变化时自动通知所有观察者。"),
    quiz("观察者模式解决什么问题？",
         ["排序问题", "对象间的松耦合通信", "内存管理", "文件读写"],
         1, "观察者模式让对象间松耦合通信，主题不需要知道观察者的具体实现。"))

add(11, "pat-observer", "发布-订阅模式",
    "发布-订阅是观察者模式的变体。发布者和订阅者通过消息中心（事件总线）通信，彼此完全解耦。",
    "class EventBus {\n    private handlers: Map<string, Function[]> = new Map();\n\n    on(event: string, handler: Function) {\n        if (!this.handlers.has(event)) {\n            this.handlers.set(event, []);\n        }\n        this.handlers.get(event)!.push(handler);\n    }\n\n    emit(event: string, data: any) {\n        this.handlers.get(event)?.forEach(h => h(data));\n    }\n}",
    fl("填写注册事件的方法名",
       "class EventBus {\n    private handlers: Map<string, Function[]> = new Map();\n\n    ___(event: string, handler: Function) {\n        if (!this.handlers.has(event)) {\n            this.handlers.set(event, []);\n        }\n        this.handlers.get(event)!.push(handler);\n    }\n\n    emit(event: string, data: any) {\n        this.handlers.get(event)?.forEach(h => h(data));\n    }\n}",
       [{"position": 0, "answer": "on", "options": ["on", "subscribe", "listen", "register"]}],
       "on是注册事件处理函数的标准方法名，对应emit触发事件。"),
    quiz("发布-订阅与直接观察者的区别是什么？",
         ["没有区别", "发布-订阅通过消息中心解耦，观察者直接通知", "发布-订阅更快", "观察者更安全"],
         1, "发布-订阅通过事件总线解耦，发布者不知道订阅者是谁。"))

add(11, "pat-observer", "事件监听与触发",
    "事件监听是观察者模式最常见的应用。addEventListener/addListener注册回调，事件发生时触发所有回调。",
    "const button = {\n    listeners: {} as Record<string, Function[]>,\n    on(event: string, fn: Function) {\n        (this.listeners[event] ??= []).push(fn);\n    },\n    click() {\n        this.listeners['click']?.forEach(fn => fn());\n    }\n};\n\nbutton.on('click', () => console.log('点击了！'));\nbutton.click();",
    po("这段代码输出什么？",
       "const button = {\n    listeners: {} as Record<string, Function[]>,\n    on(event: string, fn: Function) {\n        (this.listeners[event] ??= []).push(fn);\n    },\n    click() {\n        this.listeners['click']?.forEach(fn => fn());\n    }\n};\n\nbutton.on('click', () => console.log('点击了！'));\nbutton.click();",
       ["什么都不输出", "点击了！", "报错", "undefined"],
       1, "button.click()触发click事件，执行注册的回调函数，输出'点击了！'。"),
    quiz("addEventListener 是什么模式的应用？",
         ["工厂模式", "观察者模式", "策略模式", "单例模式"],
         1, "addEventListener是观察者模式的经典应用，注册回调在事件发生时被调用。"))

add(11, "pat-observer", "观察者的订阅与取消",
    "观察者需要能够订阅和取消订阅。取消订阅防止内存泄漏，特别是在组件销毁时。",
    "class EventEmitter {\n    private listeners = new Map<string, Set<Function>>();\n\n    on(event: string, fn: Function): () => void {\n        if (!this.listeners.has(event)) {\n            this.listeners.set(event, new Set());\n        }\n        this.listeners.get(event)!.add(fn);\n        // 返回取消订阅函数\n        return () => this.listeners.get(event)?.delete(fn);\n    }\n}",
    fb("找出代码中的问题",
       ["class EventEmitter {", "    private listeners = new Map<string, Set<Function>>();", "", "    on(event: string, fn: Function): () => void {", "        if (!this.listeners.has(event)) {", "            this.listeners.set(event, new Set());", "        }", "        this.listeners.get(event)!.add(fn);", "        return () => this.listeners.get(event)?.delete(fn);", "    }", "}"],
       -1, "这段代码没有错误。使用Set自动去重，返回取消订阅函数是良好的设计模式。"),
    quiz("为什么需要取消订阅？",
         ["代码更短", "防止内存泄漏", "加快运行", "没有原因"],
         1, "不取消订阅会导致观察者持续被引用，无法被垃圾回收，造成内存泄漏。"))

add(11, "pat-observer", "Python中的观察者模式",
    "Python中可以用函数列表实现简单的观察者模式。函数作为一等公民可以直接存储和调用。",
    "class EventEmitter:\n    def __init__(self):\n        self._handlers = {}\n\n    def on(self, event, handler):\n        self._handlers.setdefault(event, []).append(handler)\n\n    def emit(self, event, data=None):\n        for handler in self._handlers.get(event, []):\n            handler(data)\n\nemitter = EventEmitter()\nemitter.on('message', lambda d: print(f'收到: {d}'))\nemitter.emit('message', '你好')",
    po("这段代码输出什么？",
       "class EventEmitter:\n    def __init__(self):\n        self._handlers = {}\n\n    def on(self, event, handler):\n        self._handlers.setdefault(event, []).append(handler)\n\n    def emit(self, event, data=None):\n        for handler in self._handlers.get(event, []):\n            handler(data)\n\nemitter = EventEmitter()\nemitter.on('message', lambda d: print(f'收到: {d}'))\nemitter.emit('message', '你好')",
       ["收到: 你好", "你好", "报错", "什么都不输出"],
       0, "emit触发message事件，调用注册的lambda函数，输出'收到: 你好'。"),
    quiz("Python中实现观察者模式最简洁的方式是什么？",
         ["必须用抽象类", "用函数列表存储回调", "用全局变量", "用if-else"],
         1, "Python中用列表存储函数引用，调用时遍历执行即可。"))

add(11, "pat-observer", "观察者模式的应用场景",
    "观察者模式广泛用于：GUI事件处理、消息队列、数据绑定、状态管理（如Redux）、实时通知系统。",
    "// React中的状态管理示例\nclass Store {\n    private state = { count: 0 };\n    private subscribers: Function[] = [];\n\n    subscribe(fn: Function) {\n        this.subscribers.push(fn);\n        return () => {\n            this.subscribers = this.subscribers.filter(s => s !== fn);\n        };\n    }\n\n    increment() {\n        this.state.count++;\n        this.subscribers.forEach(fn => fn(this.state));\n    }\n}",
    co("排列代码到正确顺序",
       ["        this.subscribers.forEach(fn => fn(this.state));", "    increment() {", "    subscribe(fn: Function) {", "        this.subscribers.push(fn);", "        this.state.count++;", "    }", "class Store {", "    private state = { count: 0 };", "    private subscribers: Function[] = [];"],
       [6, 7, 8, 2, 3, 1, 4, 0, 5],
       "正确顺序：定义Store类 -> state属性 -> subscribers数组 -> subscribe方法 -> increment方法。"),
    quiz("以下哪个不是观察者模式的典型应用？",
         ["GUI事件处理", "消息队列", "排序算法", "状态管理"],
         2, "排序算法使用策略模式，不是观察者模式。"))

add(11, "pat-observer", "观察者与主题的解耦",
    "观察者模式的核心优势是松耦合。主题只知道观察者实现了某个接口，不需要知道具体是谁。",
    "// 主题不需要知道观察者的具体类型\ninterface Subscriber {\n    onNews(news: string): void;\n}\n\nclass NewsAgency {\n    private subs: Subscriber[] = [];\n\n    addSubscriber(sub: Subscriber) {\n        this.subs.push(sub);\n    }\n\n    publishNews(news: string) {\n        this.subs.forEach(s => s.onNews(news));\n    }\n}",
    fl("填写接口名",
       "interface ___ {\n    onNews(news: string): void;\n}\n\nclass NewsAgency {\n    private subs: Subscriber[] = [];\n\n    addSubscriber(sub: Subscriber) {\n        this.subs.push(sub);\n    }\n\n    publishNews(news: string) {\n        this.subs.forEach(s => s.onNews(news));\n    }\n}",
       [{"position": 0, "answer": "Subscriber", "options": ["Subscriber", "Observer", "Listener", "Watcher"]}],
       "Subscriber是订阅者的接口名，定义了onNews方法。"),
    quiz("观察者模式如何实现松耦合？",
         ["用全局变量", "主题只依赖观察者接口，不依赖具体实现", "用硬编码", "直接调用具体类"],
         1, "主题通过接口与观察者交互，不知道也不关心观察者的具体类型。"))

add(11, "pat-observer", "同步与异步通知",
    "观察者通知可以是同步的（立即执行所有回调）或异步的（用setTimeout或Promise延迟执行）。",
    "// 同步通知\nnotify(data) {\n    this.observers.forEach(o => o.update(data));\n}\n\n// 异步通知\nasync notifyAsync(data) {\n    const promises = this.observers.map(\n        o => Promise.resolve(o.update(data))\n    );\n    await Promise.all(promises);\n}",
    fb("找出代码中的问题",
       ["// 同步通知", "notify(data) {", "    this.observers.forEach(o => o.update(data));", "}", "", "// 异步通知", "async notifyAsync(data) {", "    const promises = this.observers.map(", "        o => Promise.resolve(o.update(data))", "    );", "    await Promise.all(promises);", "}"],
       -1, "这段代码没有错误。同步通知立即执行，异步通知用Promise.all等待所有观察者完成。"),
    quiz("异步通知的优势是什么？",
         ["更快", "不阻塞主线程，可以并行处理", "更安全", "更简单"],
         1, "异步通知不阻塞调用者，观察者可以并行处理，提高响应性。"))

add(11, "pat-observer", "观察者模式的错误处理",
    "通知观察者时，一个观察者的错误不应该影响其他观察者。需要用try/catch隔离每个通知。",
    "notify(data) {\n    this.observers.forEach(o => {\n        try {\n            o.update(data);\n        } catch (error) {\n            console.error('观察者错误:', error);\n        }\n    });\n}",
    fl("填写错误处理关键字",
       "notify(data) {\n    this.observers.forEach(o => {\n        ___ {\n            o.update(data);\n        } catch (error) {\n            console.error('观察者错误:', error);\n        }\n    });\n}",
       [{"position": 0, "answer": "try", "options": ["try", "if", "catch", "throw"]}],
       "try/catch用于捕获观察者执行中的错误，防止一个观察者失败影响其他观察者。"),
    quiz("为什么通知观察者时需要try/catch？",
         ["代码更长", "一个观察者的错误不应影响其他观察者", "更快", "不需要"],
         1, "try/catch隔离每个观察者的错误，确保一个失败不会阻止其他观察者收到通知。"))

add(11, "pat-observer", "观察者模式的优缺点",
    "优点：松耦合、支持广播通信、符合开闭原则。缺点：通知顺序不可控、可能导致循环依赖、调试困难。",
    "// 优点：添加新观察者无需修改主题\nclass NewWidget implements Subscriber {\n    onNews(news: string) {\n        console.log('新组件收到:', news);\n    }\n}\nagency.addSubscriber(new NewWidget());",
    co("排列优缺点到正确顺序",
       ["通知顺序不可控", "松耦合", "可能导致循环依赖", "支持广播通信", "调试困难", "符合开闭原则"],
       [1, 3, 5, 0, 2, 4],
       "优点：松耦合、支持广播通信、符合开闭原则。缺点：通知顺序不可控、可能导致循环依赖、调试困难。"),
    quiz("观察者模式的主要缺点是什么？",
         ["运行慢", "通知顺序不可控，可能导致循环依赖", "不能添加观察者", "代码太短"],
         1, "观察者模式的缺点包括通知顺序不可控、可能出现循环依赖、调试困难。"))


# --- pat-factory (10 points) ---

add(11, "pat-factory", "什么是工厂模式",
    "工厂模式把对象的创建过程封装起来，客户端不需要知道具体的创建细节。就像你去餐厅点菜，不需要知道厨房怎么做。",
    "// 简单工厂\nclass ButtonFactory {\n    static create(type: string) {\n        switch (type) {\n            case 'primary': return new PrimaryButton();\n            case 'danger': return new DangerButton();\n            default: throw new Error('未知按钮类型');\n        }\n    }\n}",
    po("工厂模式的核心思想是什么？",
       "class ButtonFactory {\n    static create(type: string) {\n        switch (type) {\n            case 'primary': return new PrimaryButton();\n            case 'danger': return new DangerButton();\n            default: throw new Error('未知按钮类型');\n        }\n    }\n}",
       ["直接new对象", "封装对象创建过程", "删除对象", "修改对象"],
       1, "工厂模式封装了对象的创建过程，客户端不需要知道具体创建细节。"),
    quiz("工厂模式解决什么问题？",
         ["排序问题", "对象创建的耦合问题", "内存问题", "网络问题"],
         1, "工厂模式把对象创建从业务逻辑中分离，降低耦合度。"))

add(11, "pat-factory", "简单工厂 Simple Factory",
    "简单工厂用一个工厂类的静态方法，根据参数创建不同的产品。这是最简单的工厂形式。",
    "class Logger {\n    static create(type: string) {\n        if (type === 'console') {\n            return { log: (msg: string) => console.log(msg) };\n        } else if (type === 'file') {\n            return { log: (msg: string) => /* 写入文件 */ {} };\n        }\n        throw new Error('未知日志类型');\n    }\n}\n\nconst logger = Logger.create('console');\nlogger.log('测试');",
    fl("填写工厂方法名",
       "class Logger {\n    static ___(type: string) {\n        if (type === 'console') {\n            return { log: (msg: string) => console.log(msg) };\n        } else if (type === 'file') {\n            return { log: (msg: string) => /* 写入文件 */ {} };\n        }\n        throw new Error('未知日志类型');\n    }\n}",
       [{"position": 0, "answer": "create", "options": ["create", "make", "build", "new"]}],
       "create是工厂方法的标准命名，表示创建对象。"),
    quiz("简单工厂的缺点是什么？",
         ["代码太短", "每新增产品都要修改工厂方法", "运行慢", "不能创建对象"],
         1, "简单工厂违反开闭原则，新增产品需要修改工厂方法的if-else或switch。"))

add(11, "pat-factory", "工厂方法 Factory Method",
    "工厂方法模式定义一个创建对象的接口，让子类决定实例化哪个类。每个产品有自己的工厂。",
    "interface ShapeFactory {\n    createShape(): Shape;\n}\n\nclass CircleFactory implements ShapeFactory {\n    createShape(): Shape {\n        return new Circle();\n    }\n}\n\nclass RectangleFactory implements ShapeFactory {\n    createShape(): Shape {\n        return new Rectangle();\n    }\n}",
    co("排列代码到正确顺序",
       ["    createShape(): Shape {", "interface ShapeFactory {", "        return new Circle();", "class CircleFactory implements ShapeFactory {", "    }", "    createShape(): Shape;", "}"],
       [1, 5, 6, 3, 0, 2, 4, 6],
       "正确顺序：定义工厂接口 -> 方法签名 -> 实现工厂类 -> 方法实现。"),
    quiz("工厂方法与简单工厂的区别是什么？",
         ["没有区别", "工厂方法通过子类决定创建哪个产品", "简单工厂更灵活", "工厂方法更简单"],
         1, "工厂方法让子类决定创建哪个产品，符合开闭原则。"))

add(11, "pat-factory", "抽象工厂 Abstract Factory",
    "抽象工厂创建一系列相关产品的家族。比如UI工厂创建按钮、输入框、对话框等一整套组件。",
    "interface UIFactory {\n    createButton(): Button;\n    createInput(): Input;\n}\n\nclass DarkThemeFactory implements UIFactory {\n    createButton() { return new DarkButton(); }\n    createInput() { return new DarkInput(); }\n}\n\nclass LightThemeFactory implements UIFactory {\n    createButton() { return new LightButton(); }\n    createInput() { return new LightInput(); }\n}",
    fl("填写工厂接口名",
       "interface ___ {\n    createButton(): Button;\n    createInput(): Input;\n}\n\nclass DarkThemeFactory implements UIFactory {\n    createButton() { return new DarkButton(); }\n    createInput() { return new DarkInput(); }\n}",
       [{"position": 0, "answer": "UIFactory", "options": ["UIFactory", "ThemeFactory", "ComponentFactory", "WidgetFactory"]}],
       "UIFactory创建一整套UI组件的工厂接口。"),
    quiz("抽象工厂与工厂方法的区别是什么？",
         ["没有区别", "抽象工厂创建产品家族，工厂方法创建单个产品", "抽象工厂更简单", "工厂方法更灵活"],
         1, "抽象工厂创建一系列相关产品（产品家族），工厂方法只创建单个产品。"))

add(11, "pat-factory", "Python中的工厂模式",
    "Python中工厂模式可以用函数或类实现。函数式工厂更简洁，类工厂更灵活。",
    "def create_logger(log_type):\n    loggers = {\n        'console': lambda msg: print(msg),\n        'file': lambda msg: open('log.txt', 'a').write(msg + '\\n'),\n    }\n    if log_type not in loggers:\n        raise ValueError(f'未知日志类型: {log_type}')\n    return loggers[log_type]\n\nlogger = create_logger('console')\nlogger('测试消息')",
    po("这段代码输出什么？",
       "def create_logger(log_type):\n    loggers = {\n        'console': lambda msg: print(msg),\n        'file': lambda msg: open('log.txt', 'a').write(msg + '\\n'),\n    }\n    if log_type not in loggers:\n        raise ValueError(f'未知日志类型: {log_type}')\n    return loggers[log_type]\n\nlogger = create_logger('console')\nlogger('测试消息')",
       ["测试消息", "console", "报错", "什么都不输出"],
       0, "create_logger('console')返回lambda函数，调用logger('测试消息')打印消息。"),
    quiz("Python中实现工厂模式最简洁的方式是什么？",
         ["必须用类", "用字典映射类型到创建函数", "用if-else", "用全局变量"],
         1, "Python用字典映射类型到创建函数，比switch/if-else更简洁。"))

add(11, "pat-factory", "工厂模式与依赖注入",
    "工厂模式常与依赖注入结合。工厂负责创建对象，注入器负责把对象注入到需要的地方。",
    "class ServiceContainer {\n    private factories = new Map<string, () => any>();\n\n    register(name: string, factory: () => any) {\n        this.factories.set(name, factory);\n    }\n\n    resolve<T>(name: string): T {\n        const factory = this.factories.get(name);\n        if (!factory) throw new Error(`未注册: ${name}`);\n        return factory();\n    }\n}\n\nconst container = new ServiceContainer();\ncontainer.register('logger', () => new ConsoleLogger());",
    fb("找出代码中的问题",
       ["class ServiceContainer {", "    private factories = new Map<string, () => any>();", "", "    register(name: string, factory: () => any) {", "        this.factories.set(name, factory);", "    }", "", "    resolve<T>(name: string): T {", "        const factory = this.factories.get(name);", "        if (!factory) throw new Error(`未注册: ${name}`);", "        return factory();", "    }", "}", "", "const container = new ServiceContainer();", "container.register('logger', () => new ConsoleLogger());", "const logger = container.resolve('database');  // 未注册！"],
       16, "第17行resolve('database')，但只注册了'logger'，会抛出'未注册: database'错误。"),
    quiz("依赖注入容器的作用是什么？",
         ["排序数据", "集中管理对象的创建和生命周期", "删除对象", "压缩代码"],
         1, "依赖注入容器集中管理对象的创建、配置和注入，降低组件间的耦合。"))

add(11, "pat-factory", "工厂模式的实际应用",
    "工厂模式广泛用于：数据库连接创建、日志系统、UI组件库、插件系统、配置驱动的对象创建。",
    "function createDatabase(config) {\n    const drivers = {\n        mysql: () => new MySQLConnection(config),\n        postgres: () => new PostgresConnection(config),\n        sqlite: () => new SQLiteConnection(config),\n    };\n    const creator = drivers[config.type];\n    if (!creator) throw new Error('不支持的数据库');\n    return creator();\n}",
    co("排列代码到正确顺序",
       ["    const creator = drivers[config.type];", "function createDatabase(config) {", "        sqlite: () => new SQLiteConnection(config),", "    const drivers = {", "        postgres: () => new PostgresConnection(config),", "    };", "        mysql: () => new MySQLConnection(config),", "    if (!creator) throw new Error('不支持的数据库');", "    return creator();", "}"],
       [1, 3, 6, 4, 2, 5, 0, 7, 8, 9],
       "正确顺序：定义函数 -> 创建驱动映射 -> 返回实例 -> 获取创建器 -> 检查。"),
    quiz("以下哪个场景不适合使用工厂模式？",
         ["数据库连接创建", "简单的数值计算", "UI组件创建", "插件系统"],
         1, "简单的数值计算不需要工厂模式，直接计算即可。"))

add(11, "pat-factory", "注册式工厂",
    "注册式工厂允许在运行时动态注册新的产品类型。比硬编码的工厂更灵活。",
    "class PluginFactory {\n    private static registry = new Map<string, () => Plugin>();\n\n    static register(name: string, creator: () => Plugin) {\n        this.registry.set(name, creator);\n    }\n\n    static create(name: string): Plugin {\n        const creator = this.registry.get(name);\n        if (!creator) throw new Error(`未注册插件: ${name}`);\n        return creator();\n    }\n}\n\n// 运行时注册新插件\nPluginFactory.register('auth', () => new AuthPlugin());",
    fl("填写注册方法名",
       "class PluginFactory {\n    private static registry = new Map<string, () => Plugin>();\n\n    static ___(name: string, creator: () => Plugin) {\n        this.registry.set(name, creator);\n    }\n\n    static create(name: string): Plugin {\n        const creator = this.registry.get(name);\n        if (!creator) throw new Error(`未注册插件: ${name}`);\n        return creator();\n    }\n}",
       [{"position": 0, "answer": "register", "options": ["register", "add", "set", "push"]}],
       "register是注册工厂方法的标准命名。"),
    quiz("注册式工厂的优势是什么？",
         ["代码更短", "运行时动态注册新产品，无需修改已有代码", "更快", "更安全"],
         1, "注册式工厂支持运行时动态注册，符合开闭原则。"))

add(11, "pat-factory", "工厂模式的优缺点",
    "优点：解耦创建与使用、符合开闭原则（工厂方法）、便于测试。缺点：增加类的数量、代码复杂度提高。",
    "// 优点：便于测试，可以mock工厂\nclass MockDatabaseFactory implements DatabaseFactory {\n    createConnection() {\n        return new MockConnection();\n    }\n}",
    fb("找出代码中的问题",
       ["// 优点：便于测试，可以mock工厂", "class MockDatabaseFactory implements DatabaseFactory {", "    createConnection() {", "        return new MockConnection();", "    }", "}"],
       -1, "这段代码没有错误。用mock工厂替代真实工厂，便于单元测试。"),
    quiz("工厂模式便于测试的原因是什么？",
         ["代码更短", "可以用mock工厂替代真实工厂进行测试", "不需要测试", "运行更快"],
         1, "通过接口和工厂模式，可以轻松替换为mock实现进行单元测试。"))

add(11, "pat-factory", "三种工厂模式对比",
    "简单工厂：一个工厂类，静态方法创建。工厂方法：多个工厂子类，各自创建。抽象工厂：创建产品家族。",
    "// 简单工厂：一个工厂\nSimpleFactory.create('type');\n\n// 工厂方法：多个工厂\nnew CircleFactory().create();\n\n// 抽象工厂：产品家族\nnew DarkThemeFactory().createButton();\nnew DarkThemeFactory().createInput();",
    co("排列三种工厂到正确顺序",
       ["抽象工厂：创建产品家族", "简单工厂：一个工厂类，静态方法创建", "工厂方法：多个工厂子类，各自创建"],
       [1, 2, 0],
       "从简单到复杂：简单工厂 -> 工厂方法 -> 抽象工厂。"),
    quiz("哪种工厂模式创建产品家族？",
         ["简单工厂", "工厂方法", "抽象工厂", "都不是"],
         2, "抽象工厂创建一系列相关产品（产品家族），如整套UI组件。"))


# --- pat-repository (10 points) ---

add(11, "pat-repository", "什么是仓库模式",
    "仓库模式把数据访问逻辑封装在仓库类中，业务代码不直接操作数据库。就像图书馆的管理员帮你找书，你不需要自己去书架上翻。",
    "interface Repository<T> {\n    findById(id: number): T | null;\n    findAll(): T[];\n    save(item: T): void;\n    delete(id: number): void;\n}\n\nclass UserRepository implements Repository<User> {\n    private users: User[] = [];\n\n    findById(id: number) {\n        return this.users.find(u => u.id === id) || null;\n    }\n}",
    po("仓库模式的核心思想是什么？",
       "interface Repository<T> {\n    findById(id: number): T | null;\n    findAll(): T[];\n    save(item: T): void;\n    delete(id: number): void;\n}",
       ["直接操作数据库", "封装数据访问逻辑，业务代码不依赖数据源", "删除数据", "压缩数据"],
       1, "仓库模式封装数据访问，业务代码通过仓库接口操作数据，不关心数据来源。"),
    quiz("仓库模式解决什么问题？",
         ["排序问题", "数据访问与业务逻辑的耦合", "内存问题", "网络问题"],
         1, "仓库模式把数据访问从业务逻辑中分离，降低耦合度，便于切换数据源。"))

add(11, "pat-repository", "仓库接口定义",
    "仓库接口定义了标准的CRUD操作。泛型<T>让接口适用于任何实体类型。",
    "interface ProductRepository {\n    getById(id: number): Product;\n    getAll(): Product[];\n    getByCategory(category: string): Product[];\n    save(product: Product): void;\n    delete(id: number): void;\n    count(): number;\n}",
    fl("填写方法名",
       "interface ProductRepository {\n    getById(id: number): Product;\n    getAll(): Product[];\n    getByCategory(category: string): Product[];\n    save(product: Product): void;\n    delete(id: number): void;\n    ___(): number;\n}",
       [{"position": 0, "answer": "count", "options": ["count", "size", "length", "total"]}],
       "count()返回仓库中的记录总数。"),
    quiz("仓库接口通常包含哪些操作？",
         ["只有读取", "CRUD（增删改查）", "只有写入", "只有删除"],
         1, "仓库接口通常包含CRUD操作：Create创建、Read读取、Update更新、Delete删除。"))

add(11, "pat-repository", "内存仓库实现",
    "内存仓库用数组或Map存储数据，用于测试和原型开发。不持久化数据，程序重启后数据丢失。",
    "class InMemoryUserRepository implements Repository<User> {\n    private users: Map<number, User> = new Map();\n    private nextId = 1;\n\n    findById(id: number) {\n        return this.users.get(id) || null;\n    }\n\n    save(user: User) {\n        if (!user.id) user.id = this.nextId++;\n        this.users.set(user.id, user);\n    }\n\n    findAll() {\n        return Array.from(this.users.values());\n    }\n\n    delete(id: number) {\n        this.users.delete(id);\n    }\n}",
    fb("找出代码中的问题",
       ["class InMemoryUserRepository implements Repository<User> {", "    private users: Map<number, User> = new Map();", "    private nextId = 1;", "", "    findById(id: number) {", "        return this.users.get(id) || null;", "    }", "", "    save(user: User) {", "        if (!user.id) user.id = this.nextId++;", "        this.users.set(user.id, user);", "    }", "", "    findAll() {", "        return Array.from(this.users.values());", "    }", "", "    delete(id: number) {", "        this.users.delete(id);", "    }", "}"],
       -1, "这段代码没有错误。用Map存储实体，支持按ID快速查找，是内存仓库的标准实现。"),
    quiz("内存仓库适合什么场景？",
         ["生产环境", "测试和原型开发", "大数据处理", "实时系统"],
         1, "内存仓库不持久化数据，适合单元测试和快速原型开发。"))

add(11, "pat-repository", "Python中的仓库模式",
    "Python中仓库模式可以用抽象基类定义接口，字典或列表实现内存仓库。",
    "from abc import ABC, abstractmethod\n\nclass UserRepository(ABC):\n    @abstractmethod\n    def find_by_id(self, user_id: int):\n        pass\n\n    @abstractmethod\n    def save(self, user):\n        pass\n\nclass InMemoryUserRepository(UserRepository):\n    def __init__(self):\n        self._users = {}\n\n    def find_by_id(self, user_id):\n        return self._users.get(user_id)\n\n    def save(self, user):\n        self._users[user['id']] = user",
    po("这段代码中 InMemoryUserRepository 的 _users 是什么类型？",
       "class InMemoryUserRepository(UserRepository):\n    def __init__(self):\n        self._users = {}\n\n    def find_by_id(self, user_id):\n        return self._users.get(user_id)",
       ["列表", "字典", "集合", "元组"],
       1, "self._users = {} 创建了一个空字典，用键值对存储用户数据。"),
    quiz("Python中定义仓库接口用什么？",
         ["普通类", "抽象基类ABC", "函数", "模块"],
         1, "Python用抽象基类ABC定义仓库接口，@abstractmethod标记必须实现的方法。"))

add(11, "pat-repository", "仓库模式与ORM",
    "仓库模式常与ORM（如SQLAlchemy、TypeORM）配合。仓库封装ORM查询，业务代码不需要写SQL。",
    "class TypeORMUserRepository implements Repository<User> {\n    constructor(private orm: EntityManager) {}\n\n    async findById(id: number): Promise<User | null> {\n        return this.orm.findOne(User, { where: { id } });\n    }\n\n    async save(user: User): Promise<void> {\n        await this.orm.save(User, user);\n    }\n\n    async findAll(): Promise<User[]> {\n        return this.orm.find(User);\n    }\n}",
    fl("填写ORM方法名",
       "class TypeORMUserRepository implements Repository<User> {\n    constructor(private orm: EntityManager) {}\n\n    async findById(id: number): Promise<User | null> {\n        return this.orm.___(User, { where: { id } });\n    }\n\n    async save(user: User): Promise<void> {\n        await this.orm.save(User, user);\n    }\n\n    async findAll(): Promise<User[]> {\n        return this.orm.find(User);\n    }\n}",
       [{"position": 0, "answer": "findOne", "options": ["findOne", "get", "fetch", "query"]}],
       "findOne是TypeORM中查找单个实体的方法。"),
    quiz("仓库模式与ORM配合的好处是什么？",
         ["代码更长", "业务代码不直接写SQL，便于切换数据库", "更慢", "没有好处"],
         1, "仓库封装ORM查询，业务代码不依赖具体数据库，便于测试和切换数据源。"))

add(11, "pat-repository", "仓库模式的依赖注入",
    "业务类通过构造函数接收仓库接口，不关心具体实现。这是依赖倒置原则的体现。",
    "class UserService {\n    constructor(private userRepo: Repository<User>) {}\n\n    getUser(id: number) {\n        const user = this.userRepo.findById(id);\n        if (!user) throw new Error('用户不存在');\n        return user;\n    }\n}\n\n// 注入内存仓库（测试用）\nconst service = new UserService(new InMemoryUserRepository());",
    co("排列代码到正确顺序",
       ["    constructor(private userRepo: Repository<User>) {}", "class UserService {", "const service = new UserService(new InMemoryUserRepository());", "    getUser(id: number) {", "        return user;", "        const user = this.userRepo.findById(id);", "        if (!user) throw new Error('用户不存在');", "    }", "}"],
       [1, 0, 3, 5, 6, 4, 7, 8, 2],
       "正确顺序：定义UserService -> 构造函数 -> getUser方法 -> 查找用户 -> 检查 -> 返回。"),
    quiz("依赖倒置原则在仓库模式中如何体现？",
         ["业务类直接依赖数据库", "业务类依赖仓库接口，不依赖具体实现", "没有体现", "用全局变量"],
         1, "业务类依赖抽象的仓库接口，具体实现通过依赖注入提供。"))

add(11, "pat-repository", "查询规格模式",
    "复杂查询可以用规格模式（Specification）封装。把查询条件组合成对象，仓库接受规格对象执行查询。",
    "interface Specification<T> {\n    isSatisfied(item: T): boolean;\n}\n\nclass ActiveUserSpec implements Specification<User> {\n    isSatisfied(user: User): boolean {\n        return user.active === true;\n    }\n}\n\nclass AdminSpec implements Specification<User> {\n    isSatisfied(user: User): boolean {\n        return user.role === 'admin';\n    }\n}\n\nfind(spec: Specification<User>): User[] {\n    return this.users.filter(u => spec.isSatisfied(u));\n}",
    fl("填写规格接口方法名",
       "interface Specification<T> {\n    ___(item: T): boolean;\n}\n\nclass ActiveUserSpec implements Specification<User> {\n    isSatisfied(user: User): boolean {\n        return user.active === true;\n    }\n}",
       [{"position": 0, "answer": "isSatisfied", "options": ["isSatisfied", "match", "check", "test"]}],
       "isSatisfied是规格模式的标准方法名，表示是否满足条件。"),
    quiz("规格模式的作用是什么？",
         ["排序数据", "封装查询条件，可以组合使用", "删除数据", "压缩数据"],
         1, "规格模式把查询条件封装成对象，可以用AND/OR组合，便于复用和测试。"))

add(11, "pat-repository", "仓库模式与单元测试",
    "仓库模式最大的好处之一是便于单元测试。用内存仓库替代真实数据库，测试快速且可靠。",
    "// 测试用例\ndescribe('UserService', () => {\n    it('应该返回用户', () => {\n        const repo = new InMemoryUserRepository();\n        repo.save({ id: 1, name: '小明' });\n        const service = new UserService(repo);\n        const user = service.getUser(1);\n        expect(user.name).toBe('小明');\n    });\n});",
    fb("找出代码中的问题",
       ["describe('UserService', () => {", "    it('应该返回用户', () => {", "        const repo = new InMemoryUserRepository();", "        repo.save({ id: 1, name: '小明' });", "        const service = new UserService(repo);", "        const user = service.getUser(1);", "        expect(user.name).toBe('小明');", "    });", "});"],
       -1, "这段代码没有错误。使用内存仓库进行单元测试，不依赖真实数据库，测试快速可靠。"),
    quiz("为什么仓库模式便于单元测试？",
         ["代码更短", "可以用内存仓库替代真实数据库", "不需要测试", "运行更快"],
         1, "内存仓库作为测试替身，避免依赖真实数据库，测试快速且可控。"))

add(11, "pat-repository", "多数据源仓库",
    "一个仓库可以支持多种数据源：内存、数据库、API、文件。通过切换实现来切换数据源。",
    "// 同一个接口，不同实现\nconst memoryRepo = new InMemoryUserRepository();\nconst dbRepo = new DatabaseUserRepository(dataSource);\nconst apiRepo = new ApiUserRepository(apiClient);\n\n// 业务代码不变\nfunction getUser(repo: Repository<User>, id: number) {\n    return repo.findById(id);\n}\n\ngetUser(memoryRepo, 1);  // 从内存取\ngetUser(dbRepo, 1);      // 从数据库取",
    co("排列代码到正确顺序",
       ["getUser(apiRepo, 1);", "const memoryRepo = new InMemoryUserRepository();", "function getUser(repo: Repository<User>, id: number) {", "const apiRepo = new ApiUserRepository(apiClient);", "    return repo.findById(id);", "getUser(memoryRepo, 1);", "}", "const dbRepo = new DatabaseUserRepository(dataSource);"],
       [1, 7, 3, 2, 4, 6, 5, 0],
       "正确顺序：创建内存仓库 -> 创建数据库仓库 -> 创建API仓库 -> 定义函数 -> 使用。"),
    quiz("多数据源仓库的好处是什么？",
         ["代码更长", "业务代码不依赖具体数据源，便于切换", "更慢", "没有好处"],
         1, "多数据源仓库让业务代码与数据源解耦，可以轻松切换内存、数据库、API等。"))

add(11, "pat-repository", "仓库模式的优缺点",
    "优点：解耦数据访问、便于测试、可切换数据源。缺点：简单项目过度设计、增加代码量、可能有性能开销。",
    "// 优点：一行代码切换数据源\nconst repo = process.env.NODE_ENV === 'test'\n    ? new InMemoryUserRepository()\n    : new DatabaseUserRepository();",
    fl("填写环境判断",
       "const repo = process.env.NODE_ENV === '___'\n    ? new InMemoryUserRepository()\n    : new DatabaseUserRepository();",
       [{"position": 0, "answer": "test", "options": ["test", "dev", "prod", "local"]}],
       "NODE_ENV === 'test'判断是否为测试环境，测试时使用内存仓库。"),
    quiz("仓库模式的主要缺点是什么？",
         ["运行慢", "简单项目过度设计，增加代码量", "不能切换数据源", "不能测试"],
         1, "对于简单的CRUD项目，仓库模式可能过度设计，增加不必要的代码量。"))


# --- pat-pipeline (10 points) ---

add(11, "pat-pipeline", "什么是管道模式",
    "管道模式把处理过程分成多个阶段，数据按顺序流过每个阶段。每个阶段只做一件事，像工厂的流水线。就像你在网上购物：下单 -> 支付 -> 发货 -> 收货。",
    "type Middleware = (ctx: Context, next: () => void) => void;\n\nconst logMiddleware: Middleware = (ctx, next) => {\n    console.log('请求开始:', ctx.url);\n    next();\n    console.log('请求结束');\n};\n\nconst authMiddleware: Middleware = (ctx, next) => {\n    if (!ctx.user) throw new Error('未登录');\n    next();\n};",
    po("管道模式的核心思想是什么？",
       "type Middleware = (ctx: Context, next: () => void) => void;\n\nconst logMiddleware: Middleware = (ctx, next) => {\n    console.log('请求开始:', ctx.url);\n    next();\n    console.log('请求结束');\n};",
       ["把所有逻辑写在一起", "处理过程分成多个阶段顺序执行", "随机执行", "并行执行"],
       1, "管道模式把处理分成多个阶段，数据顺序流过每个阶段，每个阶段只做一件事。"),
    quiz("管道模式类似什么？",
         ["数据库", "工厂流水线", "排序算法", "搜索算法"],
         1, "管道模式像工厂流水线，每个工位（阶段）完成特定任务，产品依次通过。"))

add(11, "pat-pipeline", "中间件链 Middleware Chain",
    "中间件链是管道模式的经典应用。每个中间件处理请求后调用next()传递给下一个，形成链条。",
    "class Pipeline {\n    private middlewares: Middleware[] = [];\n\n    use(middleware: Middleware) {\n        this.middlewares.push(middleware);\n    }\n\n    execute(ctx: Context) {\n        let index = 0;\n        const next = () => {\n            if (index < this.middlewares.length) {\n                this.middlewares[index++](ctx, next);\n            }\n        };\n        next();\n    }\n}",
    fl("填写添加中间件的方法名",
       "class Pipeline {\n    private middlewares: Middleware[] = [];\n\n    ___(middleware: Middleware) {\n        this.middlewares.push(middleware);\n    }\n\n    execute(ctx: Context) {\n        let index = 0;\n        const next = () => {\n            if (index < this.middlewares.length) {\n                this.middlewares[index++](ctx, next);\n            }\n        };\n        next();\n    }\n}",
       [{"position": 0, "answer": "use", "options": ["use", "add", "register", "push"]}],
       "use是Express/Koa中添加中间件的标准方法名。"),
    quiz("中间件链中next()的作用是什么？",
         ["结束处理", "传递给下一个中间件", "报错", "返回数据"],
         1, "next()调用下一个中间件，不调用则链条中断，后续中间件不会执行。"))

add(11, "pat-pipeline", "顺序执行与洋葱模型",
    "洋葱模型是中间件链的特殊形式：请求从外到内穿过中间件，响应从内到外返回。Koa框架使用这种模型。",
    "async function onionMiddleware(ctx, next) {\n    console.log('1. 请求进入');\n    await next();\n    console.log('4. 响应返回');\n}\n\nasync function coreMiddleware(ctx, next) {\n    console.log('2. 核心处理');\n    ctx.body = 'Hello';\n    console.log('3. 核心完成');\n}",
    co("排列输出到正确顺序",
       ["4. 响应返回", "1. 请求进入", "2. 核心处理", "3. 核心完成"],
       [1, 2, 3, 0],
       "洋葱模型：请求进入 -> 核心处理 -> 核心完成 -> 响应返回。"),
    quiz("洋葱模型的执行顺序是什么？",
         ["从内到外", "从外到内再到外", "随机", "并行"],
         1, "洋葱模型：请求从外到内穿过中间件，响应从内到外返回。"))

add(11, "pat-pipeline", "Python中的管道模式",
    "Python中管道可以用函数列表实现。每个函数接收数据，处理后返回，传递给下一个函数。",
    "def pipeline(*steps):\n    def execute(data):\n        result = data\n        for step in steps:\n            result = step(result)\n        return result\n    return execute\n\nprocess = pipeline(\n    lambda x: x.strip(),\n    lambda x: x.lower(),\n    lambda x: x.replace(' ', '_')\n)\nprint(process('  Hello World  '))",
    po("这段代码输出什么？",
       "def pipeline(*steps):\n    def execute(data):\n        result = data\n        for step in steps:\n            result = step(result)\n        return result\n    return execute\n\nprocess = pipeline(\n    lambda x: x.strip(),\n    lambda x: x.lower(),\n    lambda x: x.replace(' ', '_')\n)\nprint(process('  Hello World  '))",
       ["Hello World", "hello_world", "  hello world  ", "报错"],
       1, "strip去空格 -> lower转小写 -> replace空格为下划线，结果是'hello_world'。"),
    quiz("Python中实现管道模式最简洁的方式是什么？",
         ["必须用类", "用函数列表顺序执行", "用if-else", "用全局变量"],
         1, "Python用函数列表顺序执行，每个函数处理后返回结果给下一个。"))

add(11, "pat-pipeline", "错误处理与短路",
    "管道中的中间件可以短路（不调用next），也可以用try/catch捕获错误。错误处理中间件通常放在最后。",
    "const errorMiddleware: Middleware = async (ctx, next) => {\n    try {\n        await next();\n    } catch (error) {\n        ctx.status = 500;\n        ctx.body = { error: error.message };\n        console.error('错误:', error);\n    }\n};\n\nconst authMiddleware: Middleware = (ctx, next) => {\n    if (!ctx.user) {\n        ctx.status = 401;\n        ctx.body = '未登录';\n        return; // 短路，不调用next\n    }\n    next();\n};",
    fb("找出代码中的问题",
       ["const errorMiddleware: Middleware = async (ctx, next) => {", "    try {", "        await next();", "    } catch (error) {", "        ctx.status = 500;", "        ctx.body = { error: error.message };", "        console.error('错误:', error);", "    }", "};", "", "const authMiddleware: Middleware = (ctx, next) => {", "    if (!ctx.user) {", "        ctx.status = 401;", "        ctx.body = '未登录';", "        return; // 短路，不调用next", "    }", "    next();", "};"],
       -1, "这段代码没有错误。错误处理中间件用try/catch捕获，认证中间件在未登录时短路返回。"),
    quiz("短路是什么意思？",
         ["报错", "中间件不调用next()，后续中间件不执行", "程序崩溃", "重新执行"],
         1, "短路指中间件决定不调用next()，中断管道执行，后续中间件不会运行。"))

add(11, "pat-pipeline", "数据转换管道",
    "管道模式常用于数据转换：原始数据经过一系列转换步骤，最终得到需要的格式。类似Unix管道 | 。",
    "function transformPipeline(data) {\n    return [\n        (d) => d.filter(item => item.active),  // 过滤\n        (d) => d.map(item => ({                  // 转换\n            id: item.id,\n            name: item.name.toUpperCase()\n        })),\n        (d) => d.sort((a, b) => a.name.localeCompare(b.name)), // 排序\n    ].reduce((acc, fn) => fn(acc), data);\n}",
    fl("填写reduce的初始值",
       "function transformPipeline(data) {\n    return [\n        (d) => d.filter(item => item.active),\n        (d) => d.map(item => ({ id: item.id, name: item.name.toUpperCase() })),\n        (d) => d.sort((a, b) => a.name.localeCompare(b.name)),\n    ].reduce((acc, fn) => fn(acc), ___);\n}",
       [{"position": 0, "answer": "data", "options": ["data", "[]", "{}", "null"]}],
       "reduce的初始值是原始数据data，依次经过过滤、转换、排序。"),
    quiz("Unix管道 | 类似什么设计模式？",
         ["工厂模式", "管道模式", "观察者模式", "策略模式"],
         1, "Unix管道把前一个命令的输出作为下一个命令的输入，类似管道模式。"))

add(11, "pat-pipeline", "请求处理管道",
    "Web框架中的请求处理就是管道模式：认证 -> 验证 -> 处理 -> 响应。每个步骤是一个中间件。",
    "const pipeline = new Pipeline();\n\npipeline.use(corsMiddleware);      // CORS处理\npipeline.use(authMiddleware);      // 身份认证\npipeline.use(validateMiddleware);  // 参数验证\npipeline.use(rateLimitMiddleware); // 限流\npipeline.use(handlerMiddleware);   // 业务处理\n\npipeline.execute(requestContext);",
    co("排列中间件到正确顺序",
       ["pipeline.use(handlerMiddleware);", "pipeline.use(corsMiddleware);", "pipeline.use(rateLimitMiddleware);", "pipeline.use(authMiddleware);", "pipeline.use(validateMiddleware);"],
       [1, 3, 4, 2, 0],
       "正确顺序：CORS -> 认证 -> 验证 -> 限流 -> 业务处理。"),
    quiz("请求处理管道中认证应该在什么位置？",
         ["最后", "在业务处理之前", "在CORS之前", "任意位置"],
         1, "认证应该在业务处理之前，确保只有已认证的用户能访问后续处理。"))

add(11, "pat-pipeline", "可组合的管道",
    "管道应该是可组合的：小管道可以组合成大管道。就像乐高积木，小块拼成大结构。",
    "const authPipeline = new Pipeline();\nauthPipeline.use(authMiddleware);\nauthPipeline.use(roleMiddleware);\n\nconst apiPipeline = new Pipeline();\napiPipeline.use(corsMiddleware);\napiPipeline.use(rateLimitMiddleware);\napiPipeline.use(authPipeline);  // 组合！\napiPipeline.use(handlerMiddleware);",
    fb("找出代码中的问题",
       ["const authPipeline = new Pipeline();", "authPipeline.use(authMiddleware);", "authPipeline.use(roleMiddleware);", "", "const apiPipeline = new Pipeline();", "apiPipeline.use(corsMiddleware);", "apiPipeline.use(rateLimitMiddleware);", "apiPipeline.use(authPipeline);  // 组合！", "apiPipeline.use(handlerMiddleware);"],
       -1, "这段代码没有错误。小管道authPipeline被组合到apiPipeline中，实现管道的复用和组合。"),
    quiz("管道组合的好处是什么？",
         ["代码更长", "小管道可复用，组合成复杂处理流程", "更慢", "没有好处"],
         1, "可组合的管道让小的功能单元可以复用，像积木一样组合成复杂处理流程。"))

add(11, "pat-pipeline", "管道模式的应用场景",
    "管道模式适用于：Web请求处理、数据ETL、构建流水线（CI/CD）、图像处理、文本处理。",
    "// 数据ETL管道\nconst etlPipeline = pipeline(\n    extract,    // 从数据源提取\n    transform,  // 转换格式\n    validate,   // 验证数据\n    load,       // 加载到目标\n);\n\nconst result = etlPipeline(rawData);",
    fl("填写ETL的三个步骤",
       "// 数据ETL管道\nconst etlPipeline = pipeline(\n    ___,    // 从数据源提取\n    ___,    // 转换格式\n    ___,    // 验证数据\n    load,   // 加载到目标\n);",
       [{"position": 0, "answer": "extract", "options": ["extract", "export", "fetch", "read"]},
        {"position": 1, "answer": "transform", "options": ["transform", "convert", "change", "modify"]},
        {"position": 2, "answer": "validate", "options": ["validate", "verify", "check", "test"]}],
       "ETL：Extract提取 -> Transform转换 -> Validate验证 -> Load加载。"),
    quiz("ETL代表什么？",
         ["Edit Transfer Load", "Extract Transform Load", "Encode Transfer Link", "Extract Test Load"],
         1, "ETL是Extract Transform Load的缩写，是数据处理的标准流程。"))

add(11, "pat-pipeline", "管道模式的优缺点",
    "优点：单一职责、可复用、可组合、易于测试。缺点：调试困难（需要跟踪整个链）、性能开销（每层都有调用）。",
    "// 优点：每个中间件可独立测试\ntest('auth中间件应该拒绝未登录用户', () => {\n    const ctx = { user: null };\n    const next = jest.fn();\n    authMiddleware(ctx, next);\n    expect(next).not.toHaveBeenCalled();\n});",
    co("排列优缺点到正确顺序",
       ["调试困难", "单一职责", "性能开销", "可复用", "可组合", "易于测试"],
       [1, 3, 4, 5, 0, 2],
       "优点：单一职责、可复用、可组合、易于测试。缺点：调试困难、性能开销。"),
    quiz("管道模式的主要缺点是什么？",
         ["运行慢", "调试困难，需要跟踪整个链", "不能组合", "代码太短"],
         1, "管道模式的缺点是调试困难，需要跟踪数据在整个链中的流转。"))


# --- py-fastapi (10 points) ---

add(11, "py-fastapi", "FastAPI 简介",
    "FastAPI是Python的现代Web框架，特点是高性能、自动文档、类型检查。基于Python类型注解和Pydantic。",
    "from fastapi import FastAPI\n\napp = FastAPI()\n\n@app.get('/')\nasync def root():\n    return {'message': 'Hello World'}\n\n# 运行: uvicorn main:app --reload",
    po("访问 / 会返回什么？",
       "from fastapi import FastAPI\n\napp = FastAPI()\n\n@app.get('/')\nasync def root():\n    return {'message': 'Hello World'}",
       ["Hello World", "{'message': 'Hello World'}", "报错", "空页面"],
       1, "FastAPI自动将字典转为JSON响应，返回{'message': 'Hello World'}。"),
    quiz("FastAPI的主要特点是什么？",
         ["只能写同步代码", "高性能、自动文档、类型检查", "没有路由功能", "不支持异步"],
         1, "FastAPI基于Starlette和Pydantic，高性能、自动生成OpenAPI文档、类型安全。"))

add(11, "py-fastapi", "路由与请求方法",
    "FastAPI用装饰器定义路由。@app.get()处理GET请求，@app.post()处理POST，@app.put()处理PUT，@app.delete()处理DELETE。",
    "from fastapi import FastAPI\n\napp = FastAPI()\n\n@app.get('/users')\nasync def get_users():\n    return [{'id': 1, 'name': '小明'}]\n\n@app.post('/users')\nasync def create_user(name: str, age: int):\n    return {'id': 2, 'name': name, 'age': age}",
    fl("填写处理POST请求的装饰器",
       "from fastapi import FastAPI\n\napp = FastAPI()\n\n@app.___('/users')\nasync def create_user(name: str, age: int):\n    return {'id': 2, 'name': name, 'age': age}",
       [{"position": 0, "answer": "post", "options": ["post", "get", "put", "create"]}],
       "@app.post()装饰器处理HTTP POST请求。"),
    quiz("FastAPI中如何定义路由？",
         ["用配置文件", "用装饰器如@app.get('/path')", "用类", "用全局变量"],
         1, "FastAPI用装饰器定义路由，如@app.get()、@app.post()等。"))

add(11, "py-fastapi", "Pydantic 数据模型",
    "Pydantic用类定义数据模型，自动验证请求数据。类型错误会返回422错误和详细的错误信息。",
    "from pydantic import BaseModel\n\nclass UserCreate(BaseModel):\n    name: str\n    age: int\n    email: str\n\n@app.post('/users')\nasync def create_user(user: UserCreate):\n    return {'id': 1, **user.model_dump()}",
    po("如果传入 age: 'abc' 会怎样？",
       "from pydantic import BaseModel\n\nclass UserCreate(BaseModel):\n    name: str\n    age: int\n    email: str\n\n@app.post('/users')\nasync def create_user(user: UserCreate):\n    return {'id': 1, **user.model_dump()}",
       ["正常返回", "返回422错误，提示age必须是整数", "报500错误", "age变为NaN"],
       1, "Pydantic自动验证类型，'abc'不是int，返回422错误和详细错误信息。"),
    quiz("Pydantic的作用是什么？",
         ["渲染页面", "数据验证和序列化", "数据库操作", "文件处理"],
         1, "Pydantic用类型注解自动验证数据，序列化/反序列化JSON。"))

add(11, "py-fastapi", "路径参数 Path Parameters",
    "路径参数是URL中的一部分，用花括号{}定义。FastAPI自动提取并转换类型。",
    "from fastapi import FastAPI\n\napp = FastAPI()\n\n@app.get('/users/{user_id}')\nasync def get_user(user_id: int):\n    return {'user_id': user_id}\n\n# 访问 /users/42 -> {'user_id': 42}",
    fl("填写路径参数名",
       "from fastapi import FastAPI\n\napp = FastAPI()\n\n@app.get('/users/{___}')\nasync def get_user(user_id: int):\n    return {'user_id': user_id}",
       [{"position": 0, "answer": "user_id", "options": ["user_id", "id", "userId", "user"]}],
       "路径参数名必须与函数参数名一致，FastAPI自动匹配。"),
    quiz("路径参数的类型转换由谁完成？",
         ["手动转换", "FastAPI自动转换", "浏览器", "不需要转换"],
         1, "FastAPI根据函数参数的类型注解自动转换路径参数。"))

add(11, "py-fastapi", "查询参数 Query Parameters",
    "查询参数是URL中?后面的键值对。函数参数中不是路径参数的都会被当作查询参数。",
    "from fastapi import FastAPI\n\napp = FastAPI()\n\n@app.get('/users')\nasync def get_users(\n    skip: int = 0,\n    limit: int = 10,\n    search: str = ''\n):\n    return {'skip': skip, 'limit': limit, 'search': search}\n\n# /users?skip=20&limit=5&search=小明",
    po("访问 /users?skip=5&limit=3 返回什么？",
       "from fastapi import FastAPI\n\napp = FastAPI()\n\n@app.get('/users')\nasync def get_users(skip: int = 0, limit: int = 10, search: str = ''):\n    return {'skip': skip, 'limit': limit, 'search': search}",
       ["{'skip': 0, 'limit': 10, 'search': ''}", "{'skip': 5, 'limit': 3, 'search': ''}", "报错", "{'skip': 5, 'limit': 3}"],
       1, "skip=5和limit=3覆盖默认值，search使用默认空字符串。"),
    quiz("查询参数与路径参数的区别是什么？",
         ["没有区别", "查询参数在?后面，路径参数在URL路径中", "查询参数更快", "路径参数更安全"],
         1, "路径参数是URL的一部分(/users/{id})，查询参数在?后面(?skip=10)。"))

add(11, "py-fastapi", "请求体 Request Body",
    "用Pydantic模型定义请求体。FastAPI自动解析JSON请求体并验证数据。",
    "from pydantic import BaseModel\nfrom typing import Optional\n\nclass Item(BaseModel):\n    name: str\n    description: Optional[str] = None\n    price: float\n    in_stock: bool = True\n\n@app.post('/items')\nasync def create_item(item: Item):\n    return item.model_dump()",
    fb("找出代码中的问题",
       ["from pydantic import BaseModel", "from typing import Optional", "", "class Item(BaseModel):", "    name: str", "    description: Optional[str] = None", "    price: float", "    in_stock: bool = True", "", "@app.post('/items')", "async def create_item(item: Item):", "    return item.model_dump()"],
       -1, "这段代码没有错误。Optional[str] = None表示description可选，in_stock有默认值True。"),
    quiz("FastAPI如何处理请求体？",
         ["手动解析JSON", "用Pydantic模型自动解析和验证", "不支持请求体", "用字符串接收"],
         1, "FastAPI用Pydantic模型自动解析JSON请求体，验证类型和必填字段。"))

add(11, "py-fastapi", "依赖注入 Dependency Injection",
    "FastAPI的依赖注入让函数声明需要什么依赖，框架自动提供。常用于数据库连接、认证、配置等。",
    "from fastapi import Depends\n\nasync def get_db():\n    db = DatabaseSession()\n    try:\n        yield db\n    finally:\n        db.close()\n\n@app.get('/users')\nasync def get_users(db = Depends(get_db)):\n    return db.query(User).all()",
    fl("填写依赖注入函数名",
       "from fastapi import Depends\n\nasync def get_db():\n    db = DatabaseSession()\n    try:\n        yield db\n    finally:\n        db.close()\n\n@app.get('/users')\nasync def get_users(db = ___(get_db)):\n    return db.query(User).all()",
       [{"position": 0, "answer": "Depends", "options": ["Depends", "Inject", "Require", "Use"]}],
       "Depends是FastAPI依赖注入的核心函数。"),
    quiz("FastAPI依赖注入的作用是什么？",
         ["删除数据", "自动提供函数所需的依赖（如数据库连接）", "加速程序", "压缩代码"],
         1, "依赖注入让函数声明需要什么，框架自动创建和提供，解耦业务逻辑和基础设施。"))

add(11, "py-fastapi", "响应模型 Response Model",
    "response_model参数定义响应的数据结构。FastAPI自动过滤多余字段，确保响应格式一致。",
    "from pydantic import BaseModel\n\nclass UserOut(BaseModel):\n    id: int\n    name: str\n    email: str\n\nclass UserIn(BaseModel):\n    name: str\n    email: str\n    password: str\n\n@app.post('/users', response_model=UserOut)\nasync def create_user(user: UserIn):\n    return {'id': 1, 'name': user.name, 'email': user.email, 'password': '***'}",
    po("响应中会包含password字段吗？",
       "class UserOut(BaseModel):\n    id: int\n    name: str\n    email: str\n\n@app.post('/users', response_model=UserOut)\nasync def create_user(user: UserIn):\n    return {'id': 1, 'name': user.name, 'email': user.email, 'password': '***'}",
       ["会包含", "不会，response_model过滤了password", "报错", "看情况"],
       1, "response_model=UserOut确保响应只包含id、name、email，password被过滤掉。"),
    quiz("response_model的作用是什么？",
         ["验证请求", "定义响应结构，过滤多余字段", "加速响应", "压缩数据"],
         1, "response_model定义响应格式，自动过滤不在模型中的字段，保证API安全性。"))

add(11, "py-fastapi", "中间件 Middleware",
    "中间件在每个请求前后执行。常用于CORS、日志、认证、错误处理等全局功能。",
    "from fastapi import FastAPI\nfrom fastapi.middleware.cors import CORSMiddleware\n\napp = FastAPI()\n\napp.add_middleware(\n    CORSMiddleware,\n    allow_origins=['*'],\n    allow_methods=['*'],\n    allow_headers=['*'],\n)\n\n@app.middleware('http')\nasync def log_requests(request, call_next):\n    print(f'请求: {request.url}')\n    response = await call_next(request)\n    return response",
    co("排列代码到正确顺序",
       ["    allow_headers=['*'],", "app.add_middleware(", "    allow_methods=['*'],", "    CORSMiddleware,", "    allow_origins=['*'],", ")"],
       [1, 3, 4, 2, 0, 5],
       "正确顺序：add_middleware -> CORSMiddleware -> origins -> methods -> headers。"),
    quiz("FastAPI中间件在什么时候执行？",
         ["只在GET请求时", "每个请求前后都执行", "只在错误时", "只在启动时"],
         1, "中间件拦截每个请求，在处理前后执行，适合全局功能如CORS、日志。"))

add(11, "py-fastapi", "异常处理",
    "FastAPI用HTTPException返回HTTP错误。可以自定义异常处理器返回统一的错误格式。",
    "from fastapi import HTTPException\n\n@app.get('/users/{user_id}')\nasync def get_user(user_id: int):\n    user = find_user(user_id)\n    if not user:\n        raise HTTPException(\n            status_code=404,\n            detail='用户不存在'\n        )\n    return user",
    fl("填写异常类名",
       "from fastapi import ___\n\n@app.get('/users/{user_id}')\nasync def get_user(user_id: int):\n    user = find_user(user_id)\n    if not user:\n        raise HTTPException(\n            status_code=404,\n            detail='用户不存在'\n        )\n    return user",
       [{"position": 0, "answer": "HTTPException", "options": ["HTTPException", "Exception", "Error", "ApiError"]}],
       "HTTPException是FastAPI中返回HTTP错误的标准方式。"),
    quiz("FastAPI中如何返回404错误？",
         ["return 404", "raise HTTPException(status_code=404)", "print('404')", "sys.exit(404)"],
         1, "raise HTTPException(status_code=404, detail='...') 返回HTTP 404错误。"))



# --- py-langchain (10 points) ---

add(11, "py-langchain", "什么是LangChain",
    "LangChain是Python的LLM应用开发框架。它提供了构建AI应用的组件：模型调用、提示词管理、链式调用、代理、RAG等。",
    "from langchain_openai import ChatOpenAI\nfrom langchain_core.messages import HumanMessage\n\nllm = ChatOpenAI(model='gpt-4')\nresponse = llm.invoke([HumanMessage(content='你好')])\nprint(response.content)",
    po("这段代码做什么？",
       "from langchain_openai import ChatOpenAI\nfrom langchain_core.messages import HumanMessage\n\nllm = ChatOpenAI(model='gpt-4')\nresponse = llm.invoke([HumanMessage(content='你好')])\nprint(response.content)",
       ["报错", "调用GPT-4模型并打印回复", "创建数据库", "删除文件"],
       1, "创建ChatOpenAI实例，发送'你好'消息，打印模型的回复内容。"),
    quiz("LangChain的主要作用是什么？",
         ["数据可视化", "LLM应用开发框架", "Web服务器", "数据库管理"],
         1, "LangChain是构建LLM应用的框架，提供模型调用、链、代理、RAG等组件。"))

add(11, "py-langchain", "提示词模板 Prompt Template",
    "PromptTemplate把用户输入填入模板，生成完整的提示词。避免每次手动拼接字符串。",
    "from langchain_core.prompts import ChatPromptTemplate\n\nprompt = ChatPromptTemplate.from_messages([\n    ('system', '你是一个{role}助手'),\n    ('user', '{question}')\n])\n\nmessages = prompt.invoke({'role': '编程', 'question': '什么是Python'})\nprint(messages)",
    fl("填写模板变量",
       "from langchain_core.prompts import ChatPromptTemplate\n\nprompt = ChatPromptTemplate.from_messages([\n    ('system', '你是一个{___}助手'),\n    ('user', '{question}')\n])",
       [{"position": 0, "answer": "role", "options": ["role", "type", "name", "job"]}],
       "{role}是模板变量，在invoke时传入具体值。"),
    quiz("PromptTemplate的作用是什么？",
         ["删除提示词", "管理和复用提示词模板", "训练模型", "压缩文本"],
         1, "PromptTemplate管理提示词模板，用变量填充，避免硬编码提示词。"))

add(11, "py-langchain", "链 Chain",
    "链把多个组件串联起来：提示词 -> 模型 -> 输出解析器。用 | 运算符连接，类似Unix管道。",
    "from langchain_openai import ChatOpenAI\nfrom langchain_core.prompts import ChatPromptTemplate\nfrom langchain_core.output_parsers import StrOutputParser\n\nprompt = ChatPromptTemplate.from_messages([\n    ('system', '用一句话解释'),\n    ('user', '{topic}')\n])\n\nllm = ChatOpenAI(model='gpt-4')\nchain = prompt | llm | StrOutputParser()\n\nresult = chain.invoke({'topic': '量子计算'})\nprint(result)",
    co("排列链的组件到正确顺序",
       ["StrOutputParser()", "ChatOpenAI(model='gpt-4')", "ChatPromptTemplate.from_messages(...)"],
       [2, 1, 0],
       "链的顺序：PromptTemplate -> LLM -> OutputParser。"),
    quiz("LangChain中链的连接符是什么？",
         ["+", "|", "->", "&"],
         1, "LangChain用 | 运算符连接组件，类似Unix管道，数据从左到右流过。"))

add(11, "py-langchain", "输出解析器 Output Parser",
    "输出解析器把模型的原始输出转为结构化数据。StrOutputParser返回纯字符串，JsonOutputParser返回JSON。",
    "from langchain_core.output_parsers import JsonOutputParser\nfrom langchain_core.prompts import ChatPromptTemplate\nfrom pydantic import BaseModel\n\nclass MovieReview(BaseModel):\n    title: str\n    rating: int\n    summary: str\n\nparser = JsonOutputParser(pydantic_object=MovieReview)\n\nprompt = ChatPromptTemplate.from_messages([\n    ('system', '{format_instructions}'),\n    ('user', '评价电影{movie}')\n])",
    fl("填写输出解析器类名",
       "from langchain_core.output_parsers import ___\n\nparser = JsonOutputParser(pydantic_object=MovieReview)",
       [{"position": 0, "answer": "JsonOutputParser", "options": ["JsonOutputParser", "StrOutputParser", "CsvOutputParser", "XmlOutputParser"]}],
       "JsonOutputParser将模型输出解析为JSON格式。"),
    quiz("输出解析器的作用是什么？",
         ["删除输出", "把模型原始输出转为结构化数据", "加速模型", "压缩数据"],
         1, "输出解析器把LLM的文本输出转为程序可用的结构化数据。"))

add(11, "py-langchain", "RAG 检索增强生成",
    "RAG（Retrieval Augmented Generation）让模型基于检索到的文档回答问题。解决模型知识过时和幻觉问题。",
    "from langchain_community.vectorstores import FAISS\nfrom langchain_openai import OpenAIEmbeddings\nfrom langchain_core.runnables import RunnablePassthrough\n\n# 创建向量数据库\nvectorstore = FAISS.from_texts(\n    ['Python是一种编程语言', 'JavaScript用于前端开发'],\n    embedding=OpenAIEmbeddings()\n)\nretriever = vectorstore.as_retriever()\n\n# RAG链\nrag_chain = (\n    {'context': retriever, 'question': RunnablePassthrough()}\n    | prompt | llm | StrOutputParser()\n)",
    po("RAG的核心思想是什么？",
       "vectorstore = FAISS.from_texts(\n    ['Python是一种编程语言', 'JavaScript用于前端开发'],\n    embedding=OpenAIEmbeddings()\n)\nretriever = vectorstore.as_retriever()",
       ["直接问模型", "先检索相关文档，再让模型基于文档回答", "删除文档", "压缩文档"],
       1, "RAG先从知识库检索相关文档，把文档作为上下文传给模型，减少幻觉。"),
    quiz("RAG解决什么问题？",
         ["代码太长", "模型知识过时和幻觉问题", "网络问题", "内存问题"],
         1, "RAG通过检索外部知识库，让模型基于真实数据回答，减少幻觉和知识过时。"))

add(11, "py-langchain", "向量数据库",
    "向量数据库存储文本的向量表示（embedding），支持语义搜索。找到意思最相近的文本，而不是关键词匹配。",
    "from langchain_openai import OpenAIEmbeddings\nfrom langchain_community.vectorstores import FAISS\n\n# 文本转向量并存储\nvectorstore = FAISS.from_texts(\n    texts=['猫是宠物', '狗是宠物', 'Python是编程语言'],\n    embedding=OpenAIEmbeddings()\n)\n\n# 语义搜索\nresults = vectorstore.similarity_search('编程', k=2)\nprint(results[0].page_content)",
    po("搜索'编程'会返回什么？",
       "vectorstore = FAISS.from_texts(\n    texts=['猫是宠物', '狗是宠物', 'Python是编程语言'],\n    embedding=OpenAIEmbeddings()\n)\nresults = vectorstore.similarity_search('编程', k=2)\nprint(results[0].page_content)",
       ["猫是宠物", "Python是编程语言", "狗是宠物", "报错"],
       1, "语义搜索找到与'编程'意思最相近的文本，'Python是编程语言'最匹配。"),
    quiz("向量数据库与传统数据库搜索的区别是什么？",
         ["没有区别", "向量数据库支持语义搜索（意思匹配），传统数据库是关键词匹配", "向量数据库更慢", "传统数据库更准"],
         1, "向量数据库用embedding进行语义搜索，理解文本含义，不只是关键词匹配。"))

add(11, "py-langchain", "Agent 代理",
    "Agent让LLM自主决定使用哪些工具来完成任务。模型根据问题选择调用搜索、计算、数据库查询等工具。",
    "from langchain.agents import tool, AgentExecutor\nfrom langchain_openai import ChatOpenAI\n\n@tool\ndef calculator(expression: str) -> str:\n    \"\"\"计算数学表达式\"\"\"\n    return str(eval(expression))\n\n@tool\ndef search(query: str) -> str:\n    \"\"\"搜索网络信息\"\"\"\n    return f'搜索结果: {query}'\n\nllm = ChatOpenAI(model='gpt-4')\nagent = create_react_agent(llm, [calculator, search])\nexecutor = AgentExecutor(agent=agent, tools=[calculator, search])",
    fl("填写工具装饰器",
       "from langchain.agents import tool\n\n@___\ndef calculator(expression: str) -> str:\n    \"\"\"计算数学表达式\"\"\"\n    return str(eval(expression))",
       [{"position": 0, "answer": "tool", "options": ["tool", "func", "agent", "helper"]}],
       "@tool装饰器把函数标记为Agent可使用的工具。"),
    quiz("Agent与Chain的区别是什么？",
         ["没有区别", "Chain固定流程，Agent根据问题自主选择工具", "Agent更简单", "Chain更灵活"],
         1, "Chain是固定的组件链，Agent由LLM根据问题动态决定使用哪些工具。"))

add(11, "py-langchain", "Memory 记忆",
    "Memory让对话Agent记住之前的对话内容。ConversationBufferMemory存储完整对话历史。",
    "from langchain.memory import ConversationBufferMemory\nfrom langchain.chains import ConversationChain\n\nmemory = ConversationBufferMemory(return_messages=True)\n\nchain = ConversationChain(\n    llm=ChatOpenAI(model='gpt-4'),\n    memory=memory\n)\n\nchain.invoke({'input': '我叫小明'})\nresult = chain.invoke({'input': '我叫什么？'})\nprint(result['response'])",
    po("第二次调用会返回什么？",
       "memory = ConversationBufferMemory(return_messages=True)\n\nchain = ConversationChain(\n    llm=ChatOpenAI(model='gpt-4'),\n    memory=memory\n)\n\nchain.invoke({'input': '我叫小明'})\nresult = chain.invoke({'input': '我叫什么？'})",
       ["不知道", "你叫小明", "报错", "空"],
       1, "Memory记住了第一次对话'我叫小明'，第二次问'我叫什么'时能正确回答。"),
    quiz("Memory的作用是什么？",
         ["删除对话", "让Agent记住之前的对话历史", "加速模型", "压缩数据"],
         1, "Memory存储对话历史，让Agent能记住上下文，实现多轮对话。"))

add(11, "py-langchain", "文档加载器 Document Loader",
    "文档加载器从各种来源加载文档：PDF、网页、文本文件、数据库等。加载后转为统一的Document对象。",
    "from langchain_community.document_loaders import (\n    PyPDFLoader,\n    WebBaseLoader,\n    TextLoader\n)\n\n# 加载PDF\npdf_loader = PyPDFLoader('document.pdf')\npages = pdf_loader.load()\n\n# 加载网页\nweb_loader = WebBaseLoader('https://example.com')\ndocs = web_loader.load()\n\nprint(f'PDF页数: {len(pages)}')",
    co("排列加载器到正确顺序（按数据源类型）",
       ["TextLoader('data.txt')", "PyPDFLoader('doc.pdf')", "WebBaseLoader('https://example.com')"],
       [1, 0, 2],
       "按数据源类型：文件(PDF) -> 文件(TXT) -> 网页。"),
    quiz("Document Loader的作用是什么？",
         ["删除文档", "从各种来源加载文档为统一格式", "压缩文档", "编辑文档"],
         1, "Document Loader从PDF、网页、文件等加载文档，转为统一的Document对象供后续处理。"))

add(11, "py-langchain", "文本分割器 Text Splitter",
    "大文档需要分割成小块（chunk）才能放入向量数据库。分割时保持语义完整性，避免切断句子。",
    "from langchain.text_splitter import RecursiveCharacterTextSplitter\n\nsplitter = RecursiveCharacterTextSplitter(\n    chunk_size=500,\n    chunk_overlap=50,\n    separators=['\\n\\n', '\\n', '。', '，']\n)\n\nlong_text = '这是一篇很长的文章...' * 100\nchunks = splitter.split_text(long_text)\nprint(f'分割成 {len(chunks)} 块')",
    fl("填写分割器参数",
       "splitter = RecursiveCharacterTextSplitter(\n    ___=500,\n    chunk_overlap=50,\n    separators=['\\n\\n', '\\n', '。', '，']\n)",
       [{"position": 0, "answer": "chunk_size", "options": ["chunk_size", "max_length", "block_size", "text_size"]}],
       "chunk_size定义每个文本块的最大字符数。"),
    quiz("为什么需要文本分割？",
         ["代码更短", "大文档需要分成小块才能放入向量数据库", "加速模型", "删除文本"],
         1, "LLM有上下文长度限制，大文档需要分割成小块存储到向量数据库中。"))



# ============================================================
# Write output
# ============================================================

out_path = Path(__file__).parent / "data" / "kp_week11.json"
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
