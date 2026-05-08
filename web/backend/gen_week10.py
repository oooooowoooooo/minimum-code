"""
Generate knowledge points for Week 10.
Week 10: 装饰器与设计模式 (Decorators & Design Patterns)
  - ts-decorators (15 points): TypeScript装饰器
  - pat-di (12 points): 依赖注入模式
  - pat-middleware (12 points): 中间件模式
  - pat-builder (11 points): 建造者模式

Output: web/backend/data/kp_week10.json
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
# WEEK 10: 装饰器与设计模式
# ============================================================

# --- ts-decorators (15 points) ---

add(10, "ts-decorators", "什么是装饰器",
    "装饰器是一种特殊的声明，可以附加到类、方法、属性或参数上，用来修改或扩展它们的行为。用 @expression 的形式使用。",
    "function sealed(target: Function) {\n    Object.seal(target);\n    Object.seal(target.prototype);\n}\n\n@sealed\nclass Greeter {\n    greeting: string;\n    constructor(message: string) {\n        this.greeting = message;\n    }\n}",
    po("装饰器 @sealed 会怎样影响 Greeter 类？",
       "function sealed(target: Function) {\n    Object.seal(target);\n    Object.seal(target.prototype);\n}\n\n@sealed\nclass Greeter {\n    greeting: string;\n    constructor(message: string) {\n        this.greeting = message;\n    }\n}",
       ["删除Greeter类", "阻止给Greeter添加新属性", "让Greeter变成接口", "什么都不做"],
       1, "Object.seal阻止添加新属性，装饰器在类定义时执行。"),
    quiz("装饰器使用什么符号？",
         ["#expression", "@expression", "$expression", "%expression"],
         1, "装饰器使用 @ 符号，如 @sealed、@log 等。"))

add(10, "ts-decorators", "类装饰器",
    "类装饰器接收类的构造函数作为参数，可以返回一个新的构造函数来替代原来的。用来修改或替换类的行为。",
    "function Logger<T extends { new (...args: any[]): {} }>(constructor: T) {\n    return class extends constructor {\n        creationTime = new Date();\n    };\n}\n\n@Logger\nclass MyService {}\nconst s = new MyService();\nconsole.log((s as any).creationTime);",
    fl("填写装饰器的参数类型",
       "function Logger<T extends { new (...args: any[]): {} }>(___: T) {\n    return class extends constructor {\n        creationTime = new Date();\n    };\n}",
       [{"position": 0, "answer": "constructor", "options": ["constructor", "target", "class", "this"]}],
       "类装饰器接收类的构造函数作为参数。"),
    quiz("类装饰器的参数是什么？",
         ["类的实例", "类的构造函数", "类的属性名", "类的方法"],
         1, "类装饰器接收构造函数作为参数，可返回新构造函数替换原类。"))

add(10, "ts-decorators", "装饰器工厂",
    "装饰器工厂是一个返回装饰器的函数。这样可以给装饰器传参数，更灵活。",
    "function log(prefix: string) {\n    return function (target: any, key: string, descriptor: PropertyDescriptor) {\n        const original = descriptor.value;\n        descriptor.value = function (...args: any[]) {\n            console.log(`${prefix}: ${key} called`);\n            return original.apply(this, args);\n        };\n    };\n}\n\nclass Calculator {\n    @log('DEBUG')\n    add(a: number, b: number) { return a + b; }\n}",
    fb("找出代码中的问题",
       ["function log(prefix: string) {", "    return function (target: any, key: string, descriptor: PropertyDescriptor) {", "        const original = descriptor.value;", "        descriptor.value = function (...args: any[]) {", "            console.log(`${prefix}: ${key} called`);", "            return original.apply(this, args);", "        };", "    };", "}", "", "class Calculator {", "    @log", "    add(a: number, b: number) { return a + b; }", "}"],
       11, "第12行 @log 应该是 @log('DEBUG')，因为log是装饰器工厂，需要调用并传入参数。"),
    quiz("装饰器工厂和普通装饰器的区别是什么？",
         ["没有区别", "装饰器工厂返回装饰器，可以传参数", "装饰器工厂更快", "普通装饰器更灵活"],
         1, "装饰器工厂是一个函数，返回实际的装饰器，允许传入配置参数。"))

add(10, "ts-decorators", "方法装饰器",
    "方法装饰器在方法声明前使用，接收三个参数：target（原型）、key（方法名）、descriptor（属性描述符）。",
    "function Log(target: any, key: string, descriptor: PropertyDescriptor) {\n    const original = descriptor.value;\n    descriptor.value = function (...args: any[]) {\n        console.log(`调用 ${key}，参数: ${args}`);\n        return original.apply(this, args);\n    };\n}\n\nclass MathTool {\n    @Log\n    multiply(a: number, b: number) { return a * b; }\n}\nnew MathTool().multiply(3, 4);",
    po("运行这段代码会输出什么？",
       "function Log(target: any, key: string, descriptor: PropertyDescriptor) {\n    const original = descriptor.value;\n    descriptor.value = function (...args: any[]) {\n        console.log(`调用 ${key}，参数: ${args}`);\n        return original.apply(this, args);\n    };\n}\n\nclass MathTool {\n    @Log\n    multiply(a: number, b: number) { return a * b; }\n}\nnew MathTool().multiply(3, 4);",
       ["12", "调用 multiply，参数: 3,4", "报错", "什么都不输出"],
       1, "方法装饰器包装了multiply方法，调用时先打印日志，再执行原方法。"),
    quiz("方法装饰器的 descriptor.value 是什么？",
         ["类的构造函数", "被装饰的方法", "方法的返回值", "类的属性"],
         1, "descriptor.value 是被装饰的方法本身，可以被替换或包装。"))

add(10, "ts-decorators", "属性装饰器",
    "属性装饰器在属性声明前使用。接收 target 和 key 两个参数，不能直接修改属性值，通常用于元数据注册。",
    "function format(target: any, key: string) {\n    let value: string;\n    const getter = () => value;\n    const setter = (newVal: string) => {\n        value = newVal.trim();\n    };\n    Object.defineProperty(target, key, {\n        get: getter,\n        set: setter,\n    });\n}\n\nclass User {\n    @format\n    name: string = '';\n}",
    fl("填写属性装饰器的参数个数",
       "function format(target: any, key: ___) {\n    let value: string;\n    const getter = () => value;\n    const setter = (newVal: string) => {\n        value = newVal.trim();\n    };\n}",
       [{"position": 0, "answer": "string", "options": ["string", "number", "PropertyDescriptor", "any"]}],
       "属性装饰器接收target（原型）和key（属性名字符串）两个参数。"),
    quiz("属性装饰器能直接修改属性值吗？",
         ["能", "不能，通常用于元数据注册", "看情况", "只能读取"],
         1, "属性装饰器不能通过descriptor修改，通常配合Object.defineProperty或元数据API使用。"))

add(10, "ts-decorators", "参数装饰器",
    "参数装饰器用在方法参数上，接收 target、key（方法名）和 parameterIndex（参数索引）三个参数。",
    "function LogParam(target: any, key: string, index: number) {\n    console.log(`方法 ${key} 的第 ${index} 个参数被装饰`);\n}\n\nclass UserService {\n    createUser(@LogParam name: string, @LogParam age: number) {\n        return { name, age };\n    }\n}",
    co("排列代码到正确顺序",
       ["function LogParam(target: any, key: string, index: number) {", "    console.log(`方法 ${key} 的第 ${index} 个参数被装饰`);", "}", "", "class UserService {", "    createUser(@LogParam name: string, @LogParam age: number) {", "        return { name, age };", "    }", "}"],
       [0, 1, 2, 4, 5, 6, 7, 8],
       "正确顺序：定义装饰器 -> 函数体 -> 类 -> 带装饰器参数的方法。"),
    quiz("参数装饰器的第三个参数是什么？",
         ["参数类型", "参数索引", "参数名", "参数值"],
         1, "parameterIndex是参数在参数列表中的位置索引（从0开始）。"))

add(10, "ts-decorators", "Reflect.metadata 元数据",
    "Reflect.metadata 是一个元数据API，可以给装饰的目标附加额外的信息。需要 reflect-metadata 库。",
    "import 'reflect-metadata';\n\nfunction role(name: string) {\n    return Reflect.metadata('role', name);\n}\n\n@role('admin')\nclass AdminPanel {}\n\nconst r = Reflect.getMetadata('role', AdminPanel);\nconsole.log(r);",
    po("这段代码输出什么？",
       "import 'reflect-metadata';\n\nfunction role(name: string) {\n    return Reflect.metadata('role', name);\n}\n\n@role('admin')\nclass AdminPanel {}\n\nconst r = Reflect.getMetadata('role', AdminPanel);\nconsole.log(r);",
       ["undefined", "admin", "role", "报错"],
       1, "Reflect.metadata('role', 'admin') 给类附加了元数据，getMetadata取回'admin'。"),
    quiz("Reflect.metadata 的作用是什么？",
         ["删除元数据", "给装饰目标附加元数据信息", "创建类", "导入模块"],
         1, "Reflect.metadata用于在装饰目标上存储和读取元数据。"))

add(10, "ts-decorators", "多个装饰器组合",
    "多个装饰器可以叠加使用。执行顺序是：从上到下求值，从下到上执行（类似函数组合）。",
    "function First() {\n    console.log('First 求值');\n    return (target: any) => console.log('First 执行');\n}\nfunction Second() {\n    console.log('Second 求值');\n    return (target: any) => console.log('Second 执行');\n}\n\n@First()\n@Second()\nclass MyClass {}",
    po("控制台输出顺序是什么？",
       "function First() {\n    console.log('First 求值');\n    return (target: any) => console.log('First 执行');\n}\nfunction Second() {\n    console.log('Second 求值');\n    return (target: any) => console.log('Second 执行');\n}\n\n@First()\n@Second()\nclass MyClass {}",
       ["First执行、Second执行", "First求值、Second求值、Second执行、First执行", "Second求值、First求值", "报错"],
       1, "先从上到下求值（First求值、Second求值），再从下到上执行（Second执行、First执行）。"),
    quiz("多个装饰器的执行顺序是怎样的？",
         ["从上到下", "从下到上", "随机", "同时执行"],
         1, "装饰器从上到下求值，但从下到上执行（类似函数组合 f(g(x))）。"))

add(10, "ts-decorators", "装饰器与 TypeScript 配置",
    "使用装饰器需要在 tsconfig.json 中开启 experimentalDecorators 选项。",
    "{\n    \"compilerOptions\": {\n        \"target\": \"ES2021\",\n        \"experimentalDecorators\": true,\n        \"emitDecoratorMetadata\": true\n    }\n}",
    fl("填写配置项名",
       "{\n    \"compilerOptions\": {\n        \"target\": \"ES2021\",\n        \"___\": true,\n        \"emitDecoratorMetadata\": true\n    }\n}",
       [{"position": 0, "answer": "experimentalDecorators", "options": ["experimentalDecorators", "decorators", "enableDecorators", "useDecorators"]}],
       "experimentalDecorators是启用装饰器的编译器选项。"),
    quiz("使用装饰器需要开启哪个配置项？",
         ["strict", "experimentalDecorators", "jsx", "target"],
         1, "experimentalDecorators: true 启用装饰器支持。"))

add(10, "ts-decorators", "自动绑定 this 的装饰器",
    "方法装饰器可以用来自动绑定 this，解决回调中 this 丢失的问题。",
    "function AutoBind(target: any, key: string, descriptor: PropertyDescriptor) {\n    const original = descriptor.value;\n    return {\n        configurable: true,\n        get() {\n            return original.bind(this);\n        }\n    };\n}\n\nclass Button {\n    label = '点击我';\n    @AutoBind\n    onClick() {\n        console.log(this.label);\n    }\n}\nconst btn = new Button();\nconst handler = btn.onClick;\nhandler();",
    po("handler() 输出什么？",
       "class Button {\n    label = '点击我';\n    @AutoBind\n    onClick() {\n        console.log(this.label);\n    }\n}\nconst btn = new Button();\nconst handler = btn.onClick;\nhandler();",
       ["undefined", "点击我", "报错", "Button"],
       1, "AutoBind装饰器自动绑定了this，所以handler()中this仍然指向btn实例。"),
    quiz("AutoBind装饰器解决了什么问题？",
         ["类型错误", "回调中this丢失的问题", "性能问题", "导入问题"],
         1, "AutoBind用bind固定this，解决把方法作为回调传递时this指向错误的问题。"))

add(10, "ts-decorators", "类装饰器实现单例模式",
    "用类装饰器可以轻松实现单例模式，确保一个类只有一个实例。",
    "function Singleton<T extends { new (...args: any[]): {} }>(constructor: T) {\n    let instance: T;\n    return class extends constructor {\n        constructor(...args: any[]) {\n            if (instance) return instance;\n            super(...args);\n            instance = this as any;\n        }\n    };\n}\n\n@Singleton\nclass Database {}\nconst db1 = new Database();\nconst db2 = new Database();\nconsole.log(db1 === db2);",
    fb("找出代码中的问题",
       ["function Singleton<T extends { new (...args: any[]): {} }>(constructor: T) {", "    let instance: T;", "    return class extends constructor {", "        constructor(...args: any[]) {", "            if (instance) return instance;", "            super(...args);", "            instance = this as any;", "        }", "    };", "}", "", "@Singleton", "class Database {}", "const db1 = new Database();", "const db2 = new Database();", "console.log(db1 === db2);"],
       -1, "这段代码没有错误。Singleton装饰器确保db1和db2是同一个实例，输出true。"),
    quiz("用装饰器实现单例模式的好处是什么？",
         ["更快", "类本身不需要知道单例逻辑，解耦", "更安全", "更简单"],
         1, "装饰器让单例逻辑与业务逻辑分离，类本身不需要关心是否是单例。"))

add(10, "ts-decorators", "装饰器执行时机",
    "装饰器在类定义时执行（不是实例化时）。这意味着装饰器代码只运行一次。",
    "function LogClass(constructor: Function) {\n    console.log(`类 ${constructor.name} 被定义了`);\n}\n\n@LogClass\nclass Animal { name: string; constructor(n: string) { this.name = n; } }\nconsole.log('---创建实例---');\nnew Animal('猫');\nnew Animal('狗');",
    po("控制台输出顺序是什么？",
       "function LogClass(constructor: Function) {\n    console.log(`类 ${constructor.name} 被定义了`);\n}\n\n@LogClass\nclass Animal { name: string; constructor(n: string) { this.name = n; } }\nconsole.log('---创建实例---');\nnew Animal('猫');\nnew Animal('狗');",
       ["Animal被定义了、---创建实例---、Animal被定义了、Animal被定义了", "Animal被定义了、---创建实例---", "---创建实例---、Animal被定义了", "---创建实例---"],
       1, "装饰器在类定义时执行一次，之后new不会再次触发装饰器。"),
    quiz("装饰器在什么时候执行？",
         ["每次实例化时", "类定义时（只执行一次）", "程序结束时", "编译时"],
         1, "装饰器在类定义时执行，只运行一次，不是每次new都执行。"))

add(10, "ts-decorators", "用装饰器实现缓存",
    "方法装饰器可以实现计算结果缓存（memoize），避免重复计算。",
    "function Memoize(target: any, key: string, descriptor: PropertyDescriptor) {\n    const original = descriptor.value;\n    const cache = new Map<string, any>();\n    descriptor.value = function (...args: any[]) {\n        const k = JSON.stringify(args);\n        if (cache.has(k)) return cache.get(k);\n        const result = original.apply(this, args);\n        cache.set(k, result);\n        return result;\n    };\n}\n\nclass MathUtil {\n    @Memoize\n    fibonacci(n: number): number {\n        if (n <= 1) return n;\n        return this.fibonacci(n - 1) + this.fibonacci(n - 2);\n    }\n}",
    fl("填写缓存数据结构",
       "function Memoize(target: any, key: string, descriptor: PropertyDescriptor) {\n    const original = descriptor.value;\n    const cache = new ___<string, any>();\n    descriptor.value = function (...args: any[]) {",
       [{"position": 0, "answer": "Map", "options": ["Map", "Set", "Array", "Object"]}],
       "Map适合做键值对缓存，支持has/get/set方法。"),
    quiz("Memoize装饰器的核心思想是什么？",
         ["删除结果", "缓存计算结果避免重复计算", "加速网络请求", "减少内存"],
         1, "Memoize用Map缓存已计算的结果，相同输入直接返回缓存值。"))

add(10, "ts-decorators", "装饰器的限制与 TC39 提案",
    "TypeScript的装饰器有两种标准：旧版（experimentalDecorators）和TC39 Stage 3新版标准。新版语法略有不同。",
    "// 旧版 TypeScript 装饰器\nfunction log(target: any, key: string) { /* ... */ }\n\nclass User {\n    @log\n    name: string = '';\n}\n\n// TC39 Stage 3 新标准装饰器\n// 语法略有不同，不再使用 experimentalDecorators",
    co("排列知识点到正确顺序",
       ["TC39 Stage 3是新的装饰器标准", "TypeScript旧版需要experimentalDecorators", "新版和旧版装饰器语法略有不同", "装饰器目前仍处于演进中"],
       [1, 0, 2, 3],
       "正确顺序：了解旧版配置 -> 新标准存在 -> 语法差异 -> 持续演进。"),
    quiz("TypeScript装饰器的现状是什么？",
         ["已完全稳定", "旧版可用，TC39新标准在演进中", "已被废弃", "只有JavaScript支持"],
         1, "旧版通过experimentalDecorators可用，TC39 Stage 3新标准正在演进。"))

add(10, "ts-decorators", "方法装饰器替换原方法",
    "方法装饰器可以通过 descriptor.value 替换原方法。新方法可以调用原方法，也可以完全替换它。",
    "function Uppercase(target: any, key: string, descriptor: PropertyDescriptor) {\n    const original = descriptor.value;\n    descriptor.value = function (...args: any[]) {\n        const result = original.apply(this, args);\n        return typeof result === 'string' ? result.toUpperCase() : result;\n    };\n}\n\nclass Formatter {\n    @Uppercase\n    greet(name: string) {\n        return `hello, ${name}`;\n    }\n}\nconsole.log(new Formatter().greet('world'));",
    po("这段代码输出什么？",
       "class Formatter {\n    @Uppercase\n    greet(name: string) {\n        return `hello, ${name}`;\n    }\n}\nconsole.log(new Formatter().greet('world'));",
       ["hello, world", "HELLO, WORLD", "报错", "undefined"],
       1, "Uppercase装饰器把返回值转为大写，所以输出HELLO, WORLD。"),
    quiz("方法装饰器中 descriptor.value 指的是什么？",
         ["类的构造函数", "被装饰的原始方法", "方法的返回值", "方法的参数"],
         1, "descriptor.value是被装饰的方法本身，替换它可以改变方法行为。"))


# --- pat-di (12 points) ---

add(10, "pat-di", "什么是依赖注入",
    "依赖注入(DI)是一种设计模式：对象不自己创建依赖，而是从外部接收。就像你不自己造工具，而是别人给你准备好。",
    "// 没有依赖注入\nclass UserService {\n    private db = new MySQLDatabase(); // 紧耦合\n    getUser() { return this.db.query('SELECT * FROM users'); }\n}\n\n// 使用依赖注入\nclass UserService {\n    constructor(private db: Database) {} // 松耦合\n    getUser() { return this.db.query('SELECT * FROM users'); }\n}",
    po("依赖注入版本的UserService有什么优势？",
       "// 没有依赖注入\nclass UserService {\n    private db = new MySQLDatabase(); // 紧耦合\n    getUser() { return this.db.query('SELECT * FROM users'); }\n}\n\n// 使用依赖注入\nclass UserService {\n    constructor(private db: Database) {} // 松耦合\n    getUser() { return this.db.query('SELECT * FROM users'); }\n}",
       ["代码更短", "可以轻松替换不同的数据库实现", "运行更快", "不需要接口"],
       1, "依赖注入让UserService不依赖具体数据库，可以注入MySQL、PostgreSQL等任何实现。"),
    quiz("依赖注入的核心思想是什么？",
         ["自己创建依赖", "从外部接收依赖，不自己创建", "删除依赖", "导入依赖"],
         1, "DI的核心是对象不自己创建依赖，而是由外部提供，实现松耦合。"))

add(10, "pat-di", "构造函数注入",
    "构造函数注入是最常见的DI方式。依赖通过构造函数参数传入，对象创建时就确定了所有依赖。",
    "interface Logger {\n    log(msg: string): void;\n}\n\nclass ConsoleLogger implements Logger {\n    log(msg: string) { console.log(msg); }\n}\n\nclass App {\n    constructor(private logger: Logger) {}\n    run() {\n        this.logger.log('应用启动');\n    }\n}\n\nconst app = new App(new ConsoleLogger());\napp.run();",
    fl("填写注入方式",
       "class App {\n    constructor(private logger: ___) {}\n    run() {\n        this.logger.log('应用启动');\n    }\n}",
       [{"position": 0, "answer": "Logger", "options": ["Logger", "ConsoleLogger", "string", "any"]}],
       "构造函数注入使用接口类型，不依赖具体实现。"),
    quiz("构造函数注入的优点是什么？",
         ["代码更短", "依赖在创建时就确定，不可变", "更快", "不需要接口"],
         1, "构造函数注入确保依赖在对象创建时就确定，对象始终处于有效状态。"))

add(10, "pat-di", "Setter 注入",
    "Setter注入通过setter方法设置依赖。依赖可以在对象创建后随时更改，更灵活但也更不安全。",
    "class NotificationService {\n    private sender!: MessageSender;\n    \n    setSender(sender: MessageSender) {\n        this.sender = sender;\n    }\n    \n    send(msg: string) {\n        this.sender.send(msg);\n    }\n}\n\nconst service = new NotificationService();\nservice.setSender(new EmailSender());\nservice.send('你好');",
    fb("找出代码中的问题",
       ["class NotificationService {", "    private sender!: MessageSender;", "    ", "    setSender(sender: MessageSender) {", "        this.sender = sender;", "    }", "    ", "    send(msg: string) {", "        this.sender.send(msg);", "    }", "}", "", "const service = new NotificationService();", "service.send('你好');  // sender还未设置！", "service.setSender(new EmailSender());"],
       13, "第14行在setSender之前就调用了send()，此时sender是undefined会报错。Setter注入的缺点就是依赖可能未设置。"),
    quiz("Setter注入相比构造函数注入的缺点是什么？",
         ["更慢", "依赖可能未设置就被使用", "更复杂", "不灵活"],
         1, "Setter注入允许对象在依赖未设置时就被使用，可能导致运行时错误。"))

add(10, "pat-di", "接口注入",
    "接口注入要求接收者实现一个特定的注入接口。注入方调用接口方法来传递依赖。",
    "interface InjectLogger {\n    setLogger(logger: Logger): void;\n}\n\nclass OrderService implements InjectLogger {\n    private logger!: Logger;\n    \n    setLogger(logger: Logger) {\n        this.logger = logger;\n    }\n    \n    createOrder() {\n        this.logger.log('订单已创建');\n    }\n}",
    co("排列代码到正确顺序",
       ["    setLogger(logger: Logger) {", "interface InjectLogger {", "    setLogger(logger: Logger): void;", "}", "class OrderService implements InjectLogger {", "        this.logger = logger;", "    }", "    private logger!: Logger;"],
       [1, 2, 3, 4, 7, 0, 5, 6],
       "正确顺序：定义注入接口 -> 接口方法 -> 类实现接口 -> 属性 -> setter -> 赋值。"),
    quiz("接口注入的特点是什么？",
         ["不需要接口", "接收者必须实现注入接口", "更快", "更简单"],
         1, "接口注入通过接口约束注入行为，接收者必须实现特定的注入接口方法。"))

add(10, "pat-di", "DI 容器概念",
    "DI容器是一个注册和解析依赖的中心。把所有依赖关系注册到容器中，需要时从容器获取。",
    "class Container {\n    private services = new Map<string, any>();\n    \n    register<T>(name: string, instance: T) {\n        this.services.set(name, instance);\n    }\n    \n    resolve<T>(name: string): T {\n        return this.services.get(name);\n    }\n}\n\nconst container = new Container();\ncontainer.register('logger', new ConsoleLogger());\nconst logger = container.resolve<Logger>('logger');",
    fl("填写容器的存储类型",
       "class Container {\n    private services = new ___<string, any>();\n    \n    register<T>(name: string, instance: T) {\n        this.services.set(name, instance);\n    }",
       [{"position": 0, "answer": "Map", "options": ["Map", "Array", "Set", "Object"]}],
       "Map适合存储命名的服务实例，键是服务名，值是实例。"),
    quiz("DI容器的主要作用是什么？",
         ["创建UI", "集中管理和解析依赖关系", "网络请求", "数据存储"],
         1, "DI容器是依赖的注册中心，集中管理所有依赖关系，需要时自动解析。"))

add(10, "pat-di", "生命周期管理：单例 vs 瞬时",
    "DI容器管理对象的生命周期。单例(Singleton)每次获取同一实例，瞬时(Transient)每次获取新实例。",
    "class Container {\n    private singletons = new Map<string, any>();\n    private factories = new Map<string, () => any>();\n    \n    registerSingleton<T>(name: string, factory: () => T) {\n        this.factories.set(name, factory);\n    }\n    \n    resolve<T>(name: string): T {\n        if (!this.singletons.has(name)) {\n            const factory = this.factories.get(name)!;\n            this.singletons.set(name, factory());\n        }\n        return this.singletons.get(name);\n    }\n}",
    po("两次resolve同一个name会怎样？",
       "class Container {\n    private singletons = new Map<string, any>();\n    private factories = new Map<string, () => any>();\n    registerSingleton<T>(name: string, factory: () => T) {\n        this.factories.set(name, factory);\n    }\n    resolve<T>(name: string): T {\n        if (!this.singletons.has(name)) {\n            this.singletons.set(name, this.factories.get(name)!());\n        }\n        return this.singletons.get(name);\n    }\n}\nconst c = new Container();\nc.registerSingleton('db', () => new Database());\nconst a = c.resolve('db');\nconst b = c.resolve('db');\nconsole.log(a === b);",
       ["false", "true", "报错", "undefined"],
       1, "单例模式下，第二次resolve会返回缓存的实例，所以a === b为true。"),
    quiz("单例和瞬时的区别是什么？",
         ["没有区别", "单例每次同一实例，瞬时每次新实例", "单例更快", "瞬时更安全"],
         1, "Singleton每次返回同一实例，Transient每次创建新实例。"))

add(10, "pat-di", "自动注入与反射",
    "利用TypeScript的emitDecoratorMetadata和反射，DI容器可以自动解析构造函数参数的类型并注入。",
    "import 'reflect-metadata';\n\nfunction Injectable() {\n    return (target: Function) => {};\n}\n\n@Injectable()\nclass Logger {\n    log(msg: string) { console.log(msg); }\n}\n\n@Injectable()\nclass App {\n    constructor(private logger: Logger) {}\n}\n\n// 容器通过反射获取App的参数类型[Logger]并自动注入",
    fb("找出代码中的问题",
       ["import 'reflect-metadata';", "", "function Injectable() {", "    return (target: Function) => {};", "}", "", "@Injectable()", "class Logger {", "    log(msg: string) { console.log(msg); }", "}", "", "@Injectable()", "class App {", "    constructor(private logger: Logger) {}", "}", "", "// 容器自动注入"],
       -1, "这段代码没有语法错误。但实际使用需要tsconfig开启emitDecoratorMetadata才能让反射获取参数类型。"),
    quiz("自动注入依赖什么TypeScript特性？",
         ["泛型", "emitDecoratorMetadata和反射", "枚举", "类型推断"],
         1, "自动注入需要emitDecoratorMetadata编译器选项配合reflect-metadata库。"))

add(10, "pat-di", "依赖注入的好处",
    "依赖注入带来松耦合、易测试、易扩展三大好处。是大型项目架构的基础。",
    "// 易测试：可以注入Mock对象\nclass UserService {\n    constructor(private db: Database) {}\n    getUser(id: number) { return this.db.find(id); }\n}\n\n// 测试时注入Mock\nclass MockDB implements Database {\n    find(id: number) { return { id, name: '测试用户' }; }\n}\nconst service = new UserService(new MockDB());",
    co("排列DI的好处",
       ["易扩展：新增实现无需修改使用者", "易测试：可以注入Mock对象替代真实依赖", "松耦合：不依赖具体实现，依赖接口"],
       [2, 1, 0],
       "正确顺序：松耦合是基础 -> 易测试是直接收益 -> 易扩展是长期价值。"),
    quiz("依赖注入最直接的测试好处是什么？",
         ["代码更短", "可以注入Mock对象替代真实依赖", "运行更快", "不需要写测试"],
         1, "DI允许注入Mock对象，测试时不需要真实数据库、网络等外部依赖。"))

add(10, "pat-di", "控制反转 IoC",
    "控制反转(IoC)是DI的理论基础。传统方式对象自己控制依赖的创建，IoC把这个控制权交给外部容器。",
    "// 传统方式：对象自己控制\n// class UserRepo {\n//     private db = new RealDB(); // 自己创建\n// }\n\n// IoC：控制权交给外部\n// class UserRepo {\n//     constructor(private db: DB) {} // 外部提供\n// }\n// const repo = new UserRepo(new RealDB());",
    fl("填写概念名称",
       "___(IoC)是DI的理论基础。传统方式对象自己控制依赖的创建，IoC把这个控制权交给外部容器。",
       [{"position": 0, "answer": "控制反转", "options": ["控制反转", "依赖注入", "工厂模式", "单例模式"]}],
       "控制反转(IoC)是更广泛的概念，依赖注入是IoC的一种实现方式。"),
    quiz("IoC和DI的关系是什么？",
         ["完全相同", "IoC是原则，DI是IoC的一种实现", "DI是原则，IoC是DI的一种实现", "没有关系"],
         1, "IoC是更广泛的编程原则，DI是实现IoC的具体方式之一。"))

add(10, "pat-di", "循环依赖问题",
    "当A依赖B、B又依赖A时，就产生了循环依赖。DI容器需要特殊处理（如延迟加载）来解决。",
    "// 循环依赖示例\nclass ServiceA {\n    constructor(private b: ServiceB) {}\n}\nclass ServiceB {\n    constructor(private a: ServiceA) {}\n}\n// new ServiceA(new ServiceB(new ServiceA(...))) 无限循环！\n\n// 解决方案：延迟加载\nclass ServiceB {\n    private a!: ServiceA;\n    setA(a: ServiceA) { this.a = a; }\n}",
    fb("找出代码中的问题",
       ["class ServiceA {", "    constructor(private b: ServiceB) {}", "}", "class ServiceB {", "    constructor(private a: ServiceA) {}", "}", "// 创建时：", "const a = new ServiceA(new ServiceB(a));  // a还未定义！"],
       7, "第8行在a还未赋值时就引用了它，同时ServiceA和ServiceB互相依赖形成循环。"),
    quiz("如何解决循环依赖？",
         ["删除一个类", "使用延迟加载或setter注入", "添加更多依赖", "忽略错误"],
         1, "循环依赖可通过延迟加载、setter注入或将共同依赖提取到第三个类来解决。"))

add(10, "pat-di", "TypeScript 中的 DI 实践",
    "在实际TypeScript项目中，常用 inversify、tsyringe 等库来实现DI。它们提供了装饰器和容器的完整方案。",
    "import { injectable, inject, container } from 'tsyringe';\n\n@injectable()\nclass Logger {\n    log(msg: string) { console.log(msg); }\n}\n\n@injectable()\nclass App {\n    constructor(@inject(Logger) private logger: Logger) {}\n    start() { this.logger.log('App started'); }\n}\n\nconst app = container.resolve(App);\napp.start();",
    co("排列代码到正确顺序",
       ["@injectable()", "import { injectable, inject, container } from 'tsyringe';", "class Logger {", "    log(msg: string) { console.log(msg); }", "}", "const app = container.resolve(App);", "@injectable()", "class App {", "    constructor(@inject(Logger) private logger: Logger) {}", "    start() { this.logger.log('App started'); }", "}", "app.start();"],
       [1, 0, 2, 3, 4, 6, 7, 8, 9, 10, 5, 11],
       "正确顺序：导入 -> Logger装饰器 -> Logger类 -> App装饰器 -> App类 -> 从容器解析 -> 运行。"),
    quiz("tsyringe中 @injectable() 装饰器的作用是什么？",
         ["删除类", "标记类可以被容器管理和注入", "创建实例", "导入模块"],
         1, "@injectable()标记类可以被DI容器自动解析和注入依赖。"))

add(10, "pat-di", "Token 与标识符",
    "DI容器用Token（标识符）来注册和查找服务。Token可以是字符串、Symbol或类型本身。",
    "const container = new Map<string | symbol, any>();\n\n// 字符串Token\ncontainer.set('Logger', new ConsoleLogger());\n\n// Symbol Token（避免命名冲突）\nconst TOKENS = {\n    Logger: Symbol('Logger'),\n    Database: Symbol('Database'),\n};\ncontainer.set(TOKENS.Logger, new ConsoleLogger());\n\nconst logger = container.get(TOKENS.Logger);",
    fl("填写Token类型",
       "const TOKENS = {\n    Logger: ___('Logger'),\n    Database: Symbol('Database'),\n};",
       [{"position": 0, "answer": "Symbol", "options": ["Symbol", "String", "Number", "Object"]}],
       "Symbol作为Token可以避免命名冲突，每个Symbol都是唯一的。"),
    quiz("DI容器中使用Symbol作为Token的好处是什么？",
         ["更快", "避免命名冲突，每个Symbol唯一", "更简单", "更安全"],
         1, "Symbol是唯一的，用作Token可以避免不同模块间的命名冲突。"))


# --- pat-middleware (12 points) ---

add(10, "pat-middleware", "什么是中间件模式",
    "中间件模式把请求处理分成多个环节，每个环节（中间件）做一件事。像流水线一样，请求依次经过每个中间件。",
    "type Middleware = (req: Request, next: () => void) => void;\n\nconst logging: Middleware = (req, next) => {\n    console.log(`请求: ${req.url}`);\n    next();\n};\n\nconst auth: Middleware = (req, next) => {\n    if (req.headers.auth) next();\n    else console.log('未授权');\n};",
    fl("填写中间件类型",
       "type ___ = (req: Request, next: () => void) => void;",
       [{"position": 0, "answer": "Middleware", "options": ["Middleware", "Handler", "Controller", "Service"]}],
       "Middleware是中间件的类型别名，接收请求和next函数。"),
    quiz("中间件模式的核心思想是什么？",
         ["一个函数处理所有事", "把处理分成多个环节依次执行", "并行处理", "删除请求"],
         1, "中间件模式将请求处理拆分为独立的环节，每个中间件负责一件事，依次执行。"))

add(10, "pat-middleware", "中间件链（责任链）",
    "多个中间件组成一条链，请求沿着链条传递。每个中间件决定是否继续传递（调用next）或中断链条。",
    "class MiddlewareChain {\n    private middlewares: Function[] = [];\n    \n    use(fn: Function) {\n        this.middlewares.push(fn);\n    }\n    \n    execute(req: any) {\n        let index = 0;\n        const next = () => {\n            if (index < this.middlewares.length) {\n                this.middlewares[index++](req, next);\n            }\n        };\n        next();\n    }\n}",
    po("如果注册3个中间件，execute会怎样？",
       "class MiddlewareChain {\n    private middlewares: Function[] = [];\n    use(fn: Function) { this.middlewares.push(fn); }\n    execute(req: any) {\n        let index = 0;\n        const next = () => {\n            if (index < this.middlewares.length) {\n                this.middlewares[index++](req, next);\n            }\n        };\n        next();\n    }\n}\nconst chain = new MiddlewareChain();\nchain.use((req: any, next: Function) => { console.log('1'); next(); });\nchain.use((req: any, next: Function) => { console.log('2'); next(); });\nchain.use((req: any, next: Function) => { console.log('3'); next(); });\nchain.execute({});",
       ["1 2 3", "3 2 1", "只执行第一个", "报错"],
       0, "每个中间件调用next()后执行下一个，按注册顺序依次输出1、2、3。"),
    quiz("中间件链中不调用next()会怎样？",
         ["报错", "链条中断，后续中间件不执行", "自动继续", "跳过下一个"],
         1, "不调用next()就中断了链条，后续的中间件不会被执行。"))

add(10, "pat-middleware", "请求-响应管道",
    "中间件形成一个管道：请求从外到内穿过中间件，响应从内到外返回。每个中间件可以修改请求和响应。",
    "type Middleware = (req: any, res: any, next: () => void) => void;\n\nconst addTimestamp: Middleware = (req, res, next) => {\n    req.timestamp = Date.now();\n    next();\n    console.log(`耗时: ${Date.now() - req.timestamp}ms`);\n};\n\nconst handler: Middleware = (req, res, next) => {\n    res.body = 'Hello';\n};",
    co("排列请求-响应的处理顺序",
       ["handler处理请求并设置响应", "addTimestamp记录开始时间", "addTimestamp计算耗时", "请求到达"],
       [3, 1, 0, 2],
       "正确顺序：请求到达 -> 记录时间 -> handler处理 -> 计算耗时（next()之后的代码在响应时执行）。"),
    quiz("请求-响应管道中，next()之后的代码在什么时候执行？",
         ["请求阶段", "响应阶段（返回时）", "不执行", "编译时"],
         1, "next()之后的代码在响应返回时执行，可以用来记录日志、计算耗时等。"))

add(10, "pat-middleware", "错误处理中间件",
    "错误处理中间件专门捕获前面中间件抛出的错误。通常有4个参数（err, req, res, next）来区分普通中间件。",
    "type ErrorMiddleware = (err: Error, req: any, res: any, next: Function) => void;\n\nconst errorHandler: ErrorMiddleware = (err, req, res, next) => {\n    console.error('错误:', err.message);\n    res.status = 500;\n    res.body = { error: '服务器内部错误' };\n};\n\n// 普通中间件抛出错误\nconst validate: Middleware = (req, res, next) => {\n    if (!req.body) throw new Error('请求体为空');\n    next();\n};",
    fb("找出代码中的问题",
       ["type ErrorMiddleware = (err: Error, req: any, res: any, next: Function) => void;", "", "const errorHandler: ErrorMiddleware = (err, req, res, next) => {", "    console.error('错误:', err.message);", "    res.status = 500;", "    res.body = { error: '服务器内部错误' };", "};", "", "const validate: Middleware = (req, res, next) => {", "    if (!req.body) throw new Error('请求体为空');", "    next();  // 如果抛错了这里不会执行", "};"],
       10, "第11行throw之后的next()不会执行。错误会被错误处理中间件捕获。代码本身没有语法错误。"),
    quiz("错误处理中间件有什么特别之处？",
         ["没有特别", "有4个参数（err, req, res, next）来区分", "执行更快", "不需要next"],
         1, "错误处理中间件通过4个参数（第一个是err）来区分于普通中间件。"))

add(10, "pat-middleware", "Koa 风格洋葱模型",
    "Koa的中间件是洋葱模型：请求从外到内，响应从内到外。await next()前是请求阶段，之后是响应阶段。",
    "type KoaMiddleware = (ctx: any, next: () => Promise<void>) => Promise<void>;\n\nconst m1: KoaMiddleware = async (ctx, next) => {\n    console.log('m1 请求');\n    await next();\n    console.log('m1 响应');\n};\n\nconst m2: KoaMiddleware = async (ctx, next) => {\n    console.log('m2 请求');\n    await next();\n    console.log('m2 响应');\n};",
    po("执行顺序是什么？",
       "type KoaMiddleware = (ctx: any, next: () => Promise<void>) => Promise<void>;\nconst m1: KoaMiddleware = async (ctx, next) => {\n    console.log('m1 请求');\n    await next();\n    console.log('m1 响应');\n};\nconst m2: KoaMiddleware = async (ctx, next) => {\n    console.log('m2 请求');\n    await next();\n    console.log('m2 响应');\n};",
       ["m1请求、m1响应、m2请求、m2响应", "m1请求、m2请求、m2响应、m1响应", "m2请求、m1请求", "报错"],
       1, "洋葱模型：m1请求 -> m2请求 -> m2响应 -> m1响应。像洋葱一样一层一层。"),
    quiz("洋葱模型中 await next() 之后的代码在什么时候执行？",
         ["请求阶段", "响应阶段（返回时）", "不执行", "同时执行"],
         1, "await next()等待内层中间件完成后，才继续执行后面的代码（响应阶段）。"))

add(10, "pat-middleware", "中间件的组合 compose",
    "compose函数把多个中间件组合成一个。实现洋葱模型的核心是递归调用next。",
    "function compose(middlewares: Function[]) {\n    return function (ctx: any) {\n        let index = -1;\n        function dispatch(i: number): Promise<void> {\n            if (i <= index) return Promise.reject(new Error('next() called multiple times'));\n            index = i;\n            const fn = middlewares[i];\n            if (!fn) return Promise.resolve();\n            return Promise.resolve(fn(ctx, () => dispatch(i + 1)));\n        }\n        return dispatch(0);\n    };\n}",
    fl("填写初始索引值",
       "function compose(middlewares: Function[]) {\n    return function (ctx: any) {\n        let index = ___;\n        function dispatch(i: number): Promise<void> {",
       [{"position": 0, "answer": "-1", "options": ["-1", "0", "1", "null"]}],
       "index初始为-1，第一次dispatch(0)时index变为0，防止next()被多次调用。"),
    quiz("compose函数中index的作用是什么？",
         ["计数", "防止next()被多次调用", "排序", "缓存"],
         1, "index记录当前执行到哪个中间件，如果i<=index说明next()被重复调用了。"))

add(10, "pat-middleware", "Express 风格中间件",
    "Express中间件是简单的(req, res, next)函数。不需要await，通过调用next()传递控制权。",
    "import express from 'express';\nconst app = express();\n\n// 日志中间件\napp.use((req, res, next) => {\n    console.log(`${req.method} ${req.url}`);\n    next();\n});\n\n// 路由处理\napp.get('/', (req, res) => {\n    res.send('Hello');\n});",
    co("排列代码到正确顺序",
       ["app.get('/', (req, res) => {", "const app = express();", "    console.log(`${req.method} ${req.url}`);", "import express from 'express';", "    next();", "app.use((req, res, next) => {", "});", "    res.send('Hello');", "});"],
       [3, 1, 5, 2, 4, 6, 0, 7, 8],
       "正确顺序：导入 -> 创建app -> 注册中间件 -> 日志 -> next -> 闭合 -> 路由处理。"),
    quiz("Express中间件需要await吗？",
         ["必须", "不需要，直接调用next()", "看情况", "用callback"],
         1, "Express中间件是回调风格，直接调用next()传递控制权，不需要await。"))

add(10, "pat-middleware", "中间件的实用场景",
    "中间件常用于：日志记录、身份认证、请求验证、错误处理、CORS、压缩、限流等横切关注点。",
    "// 认证中间件\nconst auth = (req: any, res: any, next: Function) => {\n    const token = req.headers.authorization;\n    if (!token) {\n        res.status = 401;\n        res.body = { error: '未登录' };\n        return; // 不调用next，中断链条\n    }\n    req.user = verifyToken(token);\n    next();\n};",
    po("没有token时会怎样？",
       "const auth = (req: any, res: any, next: Function) => {\n    const token = req.headers.authorization;\n    if (!token) {\n        res.status = 401;\n        res.body = { error: '未登录' };\n        return;\n    }\n    req.user = verifyToken(token);\n    next();\n};\n// req.headers.authorization 为 undefined",
       ["继续执行后续中间件", "返回401未登录错误", "报错", "跳过认证"],
       1, "没有token时设置401状态码并返回错误，不调用next()中断链条。"),
    quiz("中间件不调用next()会怎样？",
         ["报错", "中断链条，后续中间件不执行", "自动继续", "重试"],
         1, "不调用next()意味着中断请求处理链条，后续中间件不会执行。"))

add(10, "pat-middleware", "中间件的执行顺序",
    "中间件按注册顺序执行。app.use() 的调用顺序决定了中间件的执行顺序，这很重要。",
    "app.use(cors());           // 1. 处理跨域\napp.use(bodyParser());      // 2. 解析请求体\napp.use(auth());            // 3. 身份认证\napp.use(rateLimiter());     // 4. 限流\napp.use(router);            // 5. 路由处理",
    fb("找出中间件顺序的问题",
       ["app.use(router);            // 路由处理", "app.use(cors());           // 处理跨域", "app.use(auth());            // 身份认证", "app.use(bodyParser());      // 解析请求体"],
       0, "第1行router应该在最后。正确的顺序：cors -> bodyParser -> auth -> router。路由处理应该在认证之后。"),
    quiz("为什么cors中间件通常放在最前面？",
         ["更快", "预检请求(OPTIONS)需要在认证之前处理", "更安全", "看情况"],
         1, "浏览器的CORS预检请求不带认证信息，如果cors在auth后面，预检会被拒绝。"))

add(10, "pat-middleware", "中间件与装饰器的区别",
    "中间件和装饰器都能增强功能，但方式不同。中间件是运行时动态组合，装饰器是定义时静态附加。",
    "// 中间件：运行时组合\napp.use(logging);\napp.use(auth);\napp.get('/users', handler);\n\n// 装饰器：定义时附加\n@Log\nclass UserController {\n    @Auth\n    getUsers() { /* ... */ }\n}",
    fl("填写模式特点",
       "___是运行时动态组合，___是定义时静态附加。",
       [{"position": 0, "answer": "中间件", "options": ["中间件", "装饰器", "工厂", "单例"]},
        {"position": 1, "answer": "装饰器", "options": ["中间件", "装饰器", "工厂", "单例"]}],
       "中间件在运行时动态组合，装饰器在类/方法定义时静态附加。"),
    quiz("中间件和装饰器的主要区别是什么？",
         ["没有区别", "中间件是运行时动态组合，装饰器是定义时静态附加", "中间件更快", "装饰器更灵活"],
         1, "中间件在运行时可以动态增减，装饰器在代码定义时就确定了。"))

add(10, "pat-middleware", "实现一个简单的中间件框架",
    "实现中间件框架的核心：注册(use)、组合(compose)、执行(run)。理解这些就能理解Express和Koa的原理。",
    "class App {\n    private middlewares: Function[] = [];\n    \n    use(fn: Function) {\n        this.middlewares.push(fn);\n    }\n    \n    run(ctx: any) {\n        let index = 0;\n        const next = (): Promise<void> => {\n            if (index >= this.middlewares.length) return Promise.resolve();\n            return Promise.resolve(this.middlewares[index++](ctx, next));\n        };\n        return next();\n    }\n}",
    co("排列实现步骤",
       ["实现run执行方法", "定义中间件数组", "注册中间件push到数组", "实现use方法", "递归调用next执行链条"],
       [1, 3, 2, 0, 4],
       "正确顺序：定义数组 -> 实现use方法 -> push注册 -> 实现run -> 递归next。"),
    quiz("实现中间件框架最核心的部分是什么？",
         ["use方法", "next的递归调用机制", "错误处理", "类型定义"],
         1, "next的递归调用机制是核心，它让中间件可以按顺序依次执行。"))

add(10, "pat-middleware", "中间件的 context 对象",
    "Koa风格的中间件使用共享的context对象传递数据。每个中间件都可以读写context，实现数据传递。",
    "type Ctx = { req: any; res: any; state: Record<string, any> };\n\nclass App {\n    private middlewares: ((ctx: Ctx, next: () => Promise<void>) => Promise<void>)[] = [];\n    \n    use(fn: (ctx: Ctx, next: () => Promise<void>) => Promise<void>) {\n        this.middlewares.push(fn);\n    }\n    \n    async handle(req: any) {\n        const ctx: Ctx = { req, res: {}, state: {} };\n        let index = 0;\n        const next = async (): Promise<void> => {\n            if (index < this.middlewares.length) {\n                await this.middlewares[index++](ctx, next);\n            }\n        };\n        await next();\n        return ctx.res;\n    }\n}",
    fb("找出代码中的问题",
       ["type Ctx = { req: any; res: any; state: Record<string, any> };", "", "class App {", "    private middlewares: ((ctx: Ctx, next: () => Promise<void>) => Promise<void>)[] = [];", "    use(fn: (ctx: Ctx, next: () => Promise<void>) => Promise<void>) {", "        this.middlewares.push(fn);", "    }", "    async handle(req: any) {", "        const ctx: Ctx = { req, res: {}, state: {} };", "        let index = 0;", "        const next = async (): Promise<void> => {", "            if (index < this.middlewares.length) {", "                await this.middlewares[index++](ctx, next);", "            }", "        };", "        await next();", "        return ctx.res;", "    }", "}"],
       -1, "这段代码没有错误。context对象在中间件之间共享，每个中间件都可以读写ctx.state来传递数据。"),
    quiz("context对象中state的作用是什么？",
         ["存储请求头", "在中间件之间传递数据", "存储数据库连接", "删除数据"],
         1, "ctx.state是中间件之间共享的数据空间，一个中间件写入，后续中间件可以读取。"))


# --- pat-builder (11 points) ---

add(10, "pat-builder", "什么是建造者模式",
    "建造者模式把复杂对象的构建过程分步骤进行。就像盖房子：先打地基、再砌墙、再封顶，一步步来。",
    "class QueryBuilder {\n    private table = '';\n    private conditions: string[] = [];\n    private limitValue = 0;\n    \n    from(table: string) {\n        this.table = table;\n        return this;\n    }\n    where(condition: string) {\n        this.conditions.push(condition);\n        return this;\n    }\n    limit(n: number) {\n        this.limitValue = n;\n        return this;\n    }\n    build() {\n        return `SELECT * FROM ${this.table} WHERE ${this.conditions.join(' AND ')} LIMIT ${this.limitValue}`;\n    }\n}",
    fl("填写返回值使方法可链式调用",
       "from(table: string) {\n    this.table = table;\n    return ___;\n}",
       [{"position": 0, "answer": "this", "options": ["this", "null", "void", "QueryBuilder"]}],
       "return this 返回当前实例，支持链式调用。"),
    quiz("建造者模式解决什么问题？",
         ["性能问题", "复杂对象的构建过程太复杂", "类型错误", "导入问题"],
         1, "建造者模式将复杂对象的构建过程分步骤，使代码更清晰、可读。"))

add(10, "pat-builder", "流式接口 Fluent Interface",
    "流式接口让方法调用可以链式连接。每个方法返回this，像说话一样自然。",
    "const query = new QueryBuilder()\n    .from('users')\n    .where('age > 18')\n    .where('active = true')\n    .limit(10)\n    .build();\n\nconsole.log(query);",
    po("query的值是什么？",
       "class QueryBuilder {\n    private table = '';\n    private conditions: string[] = [];\n    private limitValue = 0;\n    from(t: string) { this.table = t; return this; }\n    where(c: string) { this.conditions.push(c); return this; }\n    limit(n: number) { this.limitValue = n; return this; }\n    build() { return `SELECT * FROM ${this.table} WHERE ${this.conditions.join(' AND ')} LIMIT ${this.limitValue}`; }\n}\nconst query = new QueryBuilder()\n    .from('users')\n    .where('age > 18')\n    .where('active = true')\n    .limit(10)\n    .build();\nconsole.log(query);",
       ["SELECT * FROM users WHERE age > 18 AND active = true LIMIT 10", "报错", "undefined", "SELECT * FROM users LIMIT 10"],
       0, "链式调用依次设置table、conditions和limit，build()组装成SQL。"),
    quiz("流式接口的核心是什么？",
         ["返回新对象", "每个方法返回this实现链式调用", "返回Promise", "返回数组"],
         1, "流式接口的关键是每个方法返回this，使调用可以链式连接。"))

add(10, "pat-builder", "分步构建过程",
    "建造者模式把构建过程分成明确的步骤。每个步骤只做一件事，最后组合成完整对象。",
    "class HttpRequestBuilder {\n    private method = 'GET';\n    private url = '';\n    private headers: Record<string, string> = {};\n    private body: string | null = null;\n    \n    setMethod(m: string) { this.method = m; return this; }\n    setUrl(u: string) { this.url = u; return this; }\n    addHeader(k: string, v: string) { this.headers[k] = v; return this; }\n    setBody(b: string) { this.body = b; return this; }\n    \n    build() {\n        return { method: this.method, url: this.url, headers: this.headers, body: this.body };\n    }\n}",
    co("排列构建步骤",
       ["设置URL", "设置请求方法", "构建最终对象", "添加请求头", "设置请求体"],
       [1, 0, 3, 4, 2],
       "正确顺序：设置方法 -> 设置URL -> 添加头 -> 设置body -> 构建对象。"),
    quiz("每个构建步骤应该做什么？",
         ["做多件事", "只做一件事", "删除数据", "返回Promise"],
         1, "每个步骤职责单一，只做一件事，符合单一职责原则。"))

add(10, "pat-builder", "Director 指挥者",
    "Director封装了构建的流程，知道按什么顺序调用Builder的步骤。Builder只负责构建，Director负责编排。",
    "class Director {\n    constructor(private builder: HttpRequestBuilder) {}\n    \n    buildGetRequest(url: string) {\n        return this.builder\n            .setMethod('GET')\n            .setUrl(url)\n            .addHeader('Accept', 'application/json')\n            .build();\n    }\n    \n    buildPostRequest(url: string, body: string) {\n        return this.builder\n            .setMethod('POST')\n            .setUrl(url)\n            .addHeader('Content-Type', 'application/json')\n            .setBody(body)\n            .build();\n    }\n}",
    fb("找出代码中的问题",
       ["class Director {", "    constructor(private builder: HttpRequestBuilder) {}", "    ", "    buildGetRequest(url: string) {", "        return this.builder", "            .setMethod('GET')", "            .setUrl(url)", "            .addHeader('Accept', 'application/json')", "            .build();  // 每次build后builder状态被重置了吗？", "    }", "    ", "    buildPostRequest(url: string, body: string) {", "        return this.builder", "            .setMethod('POST')", "            .setUrl(url)", "            .addHeader('Content-Type', 'application/json')", "            .setBody(body)", "            .build();", "    }", "}"],
       -1, "代码本身没有语法错误。但要注意：同一个builder实例多次调用可能有状态残留问题，实际使用中通常每次创建新builder。"),
    quiz("Director的作用是什么？",
         ["构建对象", "封装构建流程，编排构建步骤", "删除对象", "类型检查"],
         1, "Director知道构建的顺序和规则，Builder只负责具体的构建工作。"))

add(10, "pat-builder", "TypeScript 链式调用的类型",
    "TypeScript中，让每个方法返回this的正确类型是用this类型或泛型，确保链式调用时类型正确。",
    "class Builder<T> {\n    protected data: Partial<T> = {};\n    \n    set<K extends keyof T>(key: K, value: T[K]): this {\n        this.data[key] = value;\n        return this;\n    }\n    \n    build(): T {\n        return this.data as T;\n    }\n}\n\nclass UserBuilder extends Builder<{ name: string; age: number }> {}\n\nconst user = new UserBuilder()\n    .set('name', '小明')\n    .set('age', 20)\n    .build();",
    fl("填写返回类型",
       "set<K extends keyof T>(key: K, value: T[K]): ___ {\n    this.data[key] = value;\n    return this;\n}",
       [{"position": 0, "answer": "this", "options": ["this", "Builder<T>", "T", "void"]}],
       "返回this类型确保子类链式调用时类型不会丢失为父类。"),
    quiz("为什么用 this 类型而不是 Builder<T>？",
         ["没有区别", "this类型在子类链式调用时保持正确类型", "更快", "更简单"],
         1, "this是多态类型，子类方法返回的this会自动推断为子类类型。"))

add(10, "pat-builder", "不可变对象的建造者",
    "建造者模式可以用来构建不可变对象。Builder构建完成后，产出的对象不可修改。",
    "interface ImmutableUser {\n    readonly name: string;\n    readonly age: number;\n    readonly email: string;\n}\n\nclass UserBuilder {\n    private _name = '';\n    private _age = 0;\n    private _email = '';\n    \n    setName(n: string) { this._name = n; return this; }\n    setAge(a: number) { this._age = a; return this; }\n    setEmail(e: string) { this._email = e; return this; }\n    \n    build(): ImmutableUser {\n        return Object.freeze({\n            name: this._name,\n            age: this._age,\n            email: this._email,\n        });\n    }\n}",
    po("build之后能修改user.name吗？",
       "const user = new UserBuilder()\n    .setName('小明')\n    .setAge(20)\n    .setEmail('test@test.com')\n    .build();\n\ntry {\n    (user as any).name = '新名字';\n    console.log('修改成功');\n} catch (e) {\n    console.log('修改失败');\n}",
       ["修改成功", "修改失败", "报错", "undefined"],
       0, "Object.freeze在非严格模式下静默失败（不报错），但值不会被修改。严格模式下会抛错。"),
    quiz("Object.freeze的作用是什么？",
         ["删除对象", "冻结对象使其不可修改", "复制对象", "序列化对象"],
         1, "Object.freeze冻结对象，阻止添加、删除、修改属性。"))

add(10, "pat-builder", "参数对象模式 Parameter Object",
    "当构造函数参数太多时，可以用参数对象模式。这是建造者模式的简化版。",
    "interface UserOptions {\n    name: string;\n    age: number;\n    email?: string;\n    phone?: string;\n    address?: string;\n}\n\nclass User {\n    name: string;\n    age: number;\n    email: string;\n    \n    constructor(options: UserOptions) {\n        this.name = options.name;\n        this.age = options.age;\n        this.email = options.email || '';\n    }\n}\n\nconst user = new User({ name: '小明', age: 20 });",
    fb("找出代码中的问题",
       ["interface UserOptions {", "    name: string;", "    age: number;", "    email?: string;", "    phone?: string;", "    address?: string;", "}", "", "class User {", "    name: string;", "    age: number;", "    email: string;", "    ", "    constructor(options: UserOptions) {", "        this.name = options.name;", "        this.age = options.age;", "        this.email = options.email;  // email可能是undefined！", "    }", "}"],
       16, "第17行options.email可能是undefined（可选属性），但this.email是string类型。应改为 options.email || ''。"),
    quiz("参数对象模式和建造者模式的关系是什么？",
         ["完全相同", "参数对象是建造者的简化版", "没有关系", "参数对象更复杂"],
         1, "参数对象模式用一个配置对象代替多个参数，是建造者模式的简化形式。"))

add(10, "pat-builder", "建造者模式的应用场景",
    "建造者模式适用于：SQL查询构建、HTTP请求构建、UI组件配置、表单验证规则、测试数据生成等。",
    "// 测试数据建造者\nclass TestUserBuilder {\n    private user = { name: '默认用户', age: 25, email: 'test@test.com' };\n    \n    withName(name: string) { this.user.name = name; return this; }\n    withAge(age: number) { this.user.age = age; return this; }\n    asAdmin() { this.user.role = 'admin'; return this; }\n    build() { return { ...this.user }; }\n}\n\n// 测试中使用\nconst admin = new TestUserBuilder().withName('管理员').asAdmin().build();",
    co("排列应用场景",
       ["测试数据生成", "SQL查询构建", "UI组件配置", "HTTP请求构建"],
       [1, 3, 2, 0],
       "按常见程度排序：SQL构建 -> HTTP请求 -> UI配置 -> 测试数据。"),
    quiz("建造者模式最适合什么场景？",
         ["简单对象创建", "复杂对象需要多步骤构建", "单个参数的函数", "数组操作"],
         1, "建造者模式最适合构建过程复杂、需要多个步骤或配置的对象。"))

add(10, "pat-builder", "建造者 vs 工厂模式",
    "建造者关注构建过程（怎么建），工厂关注创建结果（建什么）。建造者一步步构建，工厂一步到位。",
    "// 工厂模式：一步到位\ninterface Shape { draw(): void; }\nfunction createShape(type: string): Shape {\n    if (type === 'circle') return new Circle();\n    if (type === 'rect') return new Rectangle();\n    throw new Error('Unknown shape');\n}\n\n// 建造者模式：分步构建\nconst house = new HouseBuilder()\n    .setFoundation('concrete')\n    .setWalls('brick')\n    .setRoof('tile')\n    .build();",
    fl("填写模式关注点",
       "建造者关注构建___（怎么建），工厂关注创建___（建什么）。",
       [{"position": 0, "answer": "过程", "options": ["过程", "结果", "类型", "性能"]},
        {"position": 1, "answer": "结果", "options": ["过程", "结果", "类型", "性能"]}],
       "建造者关注构建过程（步骤），工厂关注创建结果（实例）。"),
    quiz("建造者和工厂模式的核心区别是什么？",
         ["没有区别", "建造者关注过程，工厂关注结果", "建造者更快", "工厂更灵活"],
         1, "建造者模式关注对象的构建过程，工厂模式关注最终创建什么对象。"))

add(10, "pat-builder", "TypeScript 中的建造者最佳实践",
    "TypeScript建造者最佳实践：使用readonly产出、泛型保证类型安全、build后重置状态、提供默认值。",
    "class ConfigBuilder {\n    private config = {\n        host: 'localhost',\n        port: 3000,\n        debug: false,\n    };\n    \n    setHost(h: string) { this.config.host = h; return this; }\n    setPort(p: number) { this.config.port = p; return this; }\n    enableDebug() { this.config.debug = true; return this; }\n    \n    build(): Readonly<typeof this.config> {\n        const result = Object.freeze({ ...this.config });\n        this.config = { host: 'localhost', port: 3000, debug: false };\n        return result;\n    }\n}",
    po("两次build之间会互相影响吗？",
       "class ConfigBuilder {\n    private config = { host: 'localhost', port: 3000, debug: false };\n    setHost(h: string) { this.config.host = h; return this; }\n    setPort(p: number) { this.config.port = p; return this; }\n    enableDebug() { this.config.debug = true; return this; }\n    build(): Readonly<typeof this.config> {\n        const result = Object.freeze({ ...this.config });\n        this.config = { host: 'localhost', port: 3000, debug: false };\n        return result;\n    }\n}\nconst b = new ConfigBuilder();\nconst c1 = b.setHost('server1').build();\nconst c2 = b.setHost('server2').build();\nconsole.log(c1.host, c2.host);",
       ["server1 server1", "server1 server2", "server2 server2", "报错"],
       1, "build()重置了config状态，并用Object.freeze返回不可变副本。c1是server1，c2是server2，互不影响。"),
    quiz("build()后为什么要重置状态？",
         ["更快", "避免多次build之间互相影响", "减少内存", "类型安全"],
         1, "重置状态确保builder可以安全地复用，每次build都是独立的。"))

add(10, "pat-builder", "泛型建造者基类",
    "用泛型定义建造者基类，子类只需指定目标类型，自动获得类型安全的构建方法。",
    "abstract class BaseBuilder<T> {\n    protected data: Partial<T> = {} as Partial<T>;\n    \n    set<K extends keyof T>(key: K, value: T[K]): this {\n        this.data[key] = value;\n        return this;\n    }\n    \n    abstract build(): T;\n}\n\nclass UserBuilder extends BaseBuilder<{ name: string; age: number; email: string }> {\n    build() {\n        if (!this.data.name || !this.data.age || !this.data.email) {\n            throw new Error('缺少必填字段');\n        }\n        return this.data as { name: string; age: number; email: string };\n    }\n}\n\nconst user = new UserBuilder()\n    .set('name', '小明')\n    .set('age', 20)\n    .set('email', 'test@test.com')\n    .build();",
    fl("填写基类方法的返回类型",
       "set<K extends keyof T>(key: K, value: T[K]): ___ {\n    this.data[key] = value;\n    return this;\n}",
       [{"position": 0, "answer": "this", "options": ["this", "T", "BaseBuilder<T>", "void"]}],
       "返回this类型确保子类链式调用时类型不会丢失为父类类型。"),
    quiz("抽象建造者基类的好处是什么？",
         ["代码更短", "子类自动获得类型安全的构建方法，减少重复代码", "更快", "不需要泛型"],
         1, "泛型基类封装了通用的set方法，子类只需实现build()，减少重复代码。"))


# ============================================================
# Write output
# ============================================================

out_path = Path(__file__).parent / "data" / "kp_week10.json"
out_path.parent.mkdir(parents=True, exist_ok=True)
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(ALL_KP, f, ensure_ascii=False, indent=2)

print(f"Generated {len(ALL_KP)} knowledge points")
print(f"Written to: {out_path}")

# Count by module
from collections import Counter
module_counts = Counter(kp["module"] for kp in ALL_KP)
game_counts = Counter(kp["game"]["type"] for kp in ALL_KP)

print(f"\nBy module:")
for m in sorted(module_counts):
    print(f"  {m}: {module_counts[m]} points")

print(f"\nBy game type:")
for t in sorted(game_counts):
    print(f"  {t}: {game_counts[t]} games")
