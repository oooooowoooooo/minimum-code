"""
Generate 888+ atomic knowledge points for the AI Era Learning Platform.
Each point: explanation, code example, mini-game, quiz.
12 weeks, smooth learning curve for beginners.
"""

import json
from pathlib import Path

# ============================================================
# KNOWLEDGE POINT DEFINITIONS
# ============================================================

KNOWLEDGE_POINTS = []

def kp(week, module, title, explanation, code, game, quiz_q, quiz_opts, quiz_correct, quiz_explain):
    KNOWLEDGE_POINTS.append({
        "week": week,
        "module": module,
        "title": title,
        "explanation": explanation,
        "code": code,
        "game": game,
        "quiz": {
            "question": quiz_q,
            "options": quiz_opts,
            "correct": quiz_correct,
            "explanation": quiz_explain,
        },
    })

# ============================================================
# WEEK 1: Why Programming + Thinking
# ============================================================

kp(1, "cognitive-why", "What is a program?",
   "A program is a set of instructions that tells a computer what to do. Like a recipe for cooking, but for computers.",
   "# A simple program\nprint('Hello!')\n# Output: Hello!",
   "Game: Put these steps in order to make a sandwich:\n1. Put peanut butter on bread\n2. Get two slices of bread\n3. Put slices together\n4. Open jar of peanut butter",
   "What does a program do?",
   ["Tells the computer what to do", "Tells the user what to do", "Writes itself", "Nothing"],
   0, "A program is instructions FOR the computer.")

kp(1, "cognitive-why", "Why learn programming when AI writes code?",
   "AI can write code, but it cannot decide WHAT to build. You need programming knowledge to direct AI and judge its output.",
   "# AI wrote this code. Is it good?\ndef add(a, b):\n    return a + b\n# You need to know: is this the right approach?",
   "Game: Which task can AI do well?\nA) Decide what app to build\nB) Write a function to add numbers\nC) Understand user needs\nD) Design the system architecture",
   "Why learn programming in the AI era?",
   ["To memorize syntax", "To direct AI and judge its output", "To write every line yourself", "To replace AI"],
   1, "AI writes code. Humans decide what to build and whether it is good.")

kp(1, "cognitive-why", "The skill hierarchy",
   "Skills go from low to high value: Write code (AI does this) > Read code > Design systems > Make tradeoffs > Define problems (you do this).",
   "# Level 1: Write code (AI can do this)\nprint('hello')\n\n# Level 5: Define the problem\n# 'We need a system to track student grades'\n# Only a human can do this!",
   "Game: Rank these skills from lowest to highest value:\nA) Writing code\nB) Defining problems\nC) Reading code\nD) Designing systems",
   "Which skill is MOST valuable?",
   ["Writing code fast", "Defining what problem to solve", "Memorizing syntax", "Using many languages"],
   1, "Defining problems is the highest value skill. AI handles the lowest level.")

kp(1, "cognitive-why", "Code is cheap, taste is expensive",
   "In the AI era, generating code is easy. The hard part is knowing what good code looks like and what to build.",
   "# Anyone can write this:\ndef f(x): return x*2\n\n# But knowing this is better takes taste:\ndef double_value(number):\n    return number * 2",
   "Game: Which function name is better and why?\nA) f(x)\nB) double_value(number)",
   "What is 'taste' in programming?",
   ["Using fancy syntax", "Knowing what good code looks like", "Writing fast", "Using the newest framework"],
   1, "Taste means knowing what is good, clean, and maintainable.")

kp(1, "cognitive-why", "Thinking in systems",
   "A system is a collection of parts that work together. Programming teaches you to think about how parts connect.",
   "# A system: User -> Login -> Database -> Response\n# Each part has a job. They connect together.\nuser_input = 'alice'\ndatabase = {'alice': 'password123'}\nif user_input in database:\n    print('Welcome!')",
   "Game: Draw a simple system: User types password -> System checks -> Show result. What are the 3 parts?",
   "What is a system?",
   ["A single function", "Parts that work together", "A database", "A programming language"],
   1, "A system is parts working together to achieve a goal.")

kp(1, "cognitive-why", "The 80/20 rule of programming",
   "80% of programming uses 20% of the language features. Focus on the core concepts first.",
   "# The 20% you use 80% of the time:\n# 1. Variables: x = 5\n# 2. If/else: if x > 3: ...\n# 3. Loops: for i in range(10): ...\n# 4. Functions: def foo(): ...\n# 5. Lists: items = [1, 2, 3]",
   "Game: Which 3 concepts do you think are used most?\nA) Variables\nB) Decorators\nC) If/else\nD) Metaclasses\nE) Loops\nF) Functions",
   "What is the 80/20 rule in programming?",
   ["Learn everything equally", "Focus on the 20% of features used 80% of the time", "Only learn 20%", "Skip the basics"],
   1, "Focus on core concepts. Advanced features come later.")

kp(1, "cognitive-thinking", "What is a mental model?",
   "A mental model is how you think about something. In programming, your mental model of how code works determines how well you write it.",
   "# Mental model: Variables are LABELED BOXES\n# x = 5 means: put 5 in the box labeled 'x'\nx = 5\ny = x  # Copy 5 into box 'y'\nx = 10 # Change box 'x' to hold 10\n# y is still 5!",
   "Game: Draw boxes for this code:\nx = 1\ny = 2\nx = y\nWhat is in box x now?",
   "What is a mental model?",
   ["A type of computer", "How you think about how something works", "A programming language", "A debugging tool"],
   1, "Your mental model shapes how you understand and write code.")

kp(1, "cognitive-thinking", "Abstraction: hiding complexity",
   "Abstraction means hiding complex details behind a simple interface. You drive a car without knowing how the engine works.",
   "# You use print() without knowing how it works inside\nprint('hello')  # Simple interface\n\n# Behind the scenes: character encoding, buffer management,\n# system calls... all hidden from you!",
   "Game: Which is an abstraction?\nA) A TV remote (hides infrared signals)\nB) A circuit board (shows all connections)\nC) Assembly code (shows every instruction)",
   "What does abstraction do?",
   ["Makes things more complex", "Hides complexity behind a simple interface", "Removes features", "Shows all details"],
   1, "Abstraction hides complexity so you can focus on what matters.")

kp(1, "cognitive-thinking", "Decomposition: break it down",
   "Decomposition means breaking a big problem into smaller, manageable pieces. Each piece is easier to solve.",
   "# Big problem: Build a calculator\n# Decompose into pieces:\n# 1. Get user input\n# 2. Parse the operation\n# 3. Do the math\n# 4. Show the result\ndef get_input(): return input('Enter: ')\ndef calculate(expr): return eval(expr)\ndef show_result(r): print(f'Answer: {r}')",
   "Game: Break 'Make breakfast' into 4 small steps.",
   "What is decomposition?",
   ["Combining small things into big ones", "Breaking big problems into smaller pieces", "Deleting code", "Making things more complex"],
   1, "Decomposition breaks big problems into small, solvable pieces.")

kp(1, "cognitive-thinking", "Pattern recognition",
   "Recognizing patterns helps you solve problems faster. If you have seen a similar problem before, you can reuse the solution.",
   "# Pattern: Check if a list has duplicates\n# You will see this pattern many times:\ndef has_duplicates(items):\n    return len(items) != len(set(items))\n\nprint(has_duplicates([1, 2, 3]))  # False\nprint(has_duplicates([1, 2, 2]))  # True",
   "Game: What pattern do these share?\n- Check if word is palindrome\n- Check if number is prime\n- Check if list is sorted",
   "Why is pattern recognition useful?",
   ["It makes code longer", "It helps reuse solutions for similar problems", "It confuses the computer", "It is not useful"],
   1, "Recognizing patterns lets you apply known solutions to new problems.")

kp(1, "cognitive-thinking", "Algorithmic thinking",
   "An algorithm is a step-by-step procedure to solve a problem. Think of it as a recipe.",
   "# Algorithm: Find the largest number\n# Step 1: Start with the first number\n# Step 2: Compare with each other number\n# Step 3: If bigger, remember it\n# Step 4: Return the remembered number\ndef find_largest(numbers):\n    biggest = numbers[0]\n    for n in numbers:\n        if n > biggest:\n            biggest = n\n    return biggest",
   "Game: Write an algorithm to find the smallest number in [3, 7, 1, 9, 4]. What are the steps?",
   "What is an algorithm?",
   ["A programming language", "A step-by-step procedure to solve a problem", "A type of computer", "A debugging tool"],
   1, "An algorithm is a clear, step-by-step procedure.")

kp(1, "cognitive-thinking", "Debugging mindset",
   "Bugs are errors in code. The debugging mindset: observe, hypothesize, test, fix. Do not guess randomly.",
   "# Bug: This code gives wrong result\ndef average(numbers):\n    return sum(numbers) / len(numbers) + 1  # Bug: +1 is wrong!\n\n# Debug steps:\n# 1. Observe: average([2,4]) = 4.0, expected 3.0\n# 2. Hypothesize: extra +1 in calculation\n# 3. Test: remove +1, check result\n# 4. Fix: return sum(numbers) / len(numbers)",
   "Game: Find the bug:\ndef is_even(n):\n    return n / 2 == 0\nHint: what operator should it use?",
   "What is the debugging mindset?",
   ["Guess randomly until it works", "Observe, hypothesize, test, fix", "Delete everything and start over", "Ignore the error"],
   1, "Debugging is systematic: observe the error, form a hypothesis, test it, then fix.")

kp(1, "cognitive-thinking", "First principles thinking",
   "First principles means breaking something down to its basic truths, then reasoning up from there.",
   "# First principles: What is a variable?\n# Truth 1: Computer has memory (boxes)\n# Truth 2: Each box has an address\n# Truth 3: A variable is a NAME for a box\n# Conclusion: x = 5 means 'x' labels a box holding 5",
   "Game: Explain 'function' from first principles:\n1. Computers execute instructions\n2. Sometimes we repeat instructions\n3. So we group them and give them a name...",
   "What is first principles thinking?",
   ["Copying others' code", "Breaking things down to basic truths and reasoning up", "Using the latest framework", "Following trends"],
   1, "First principles: break to basics, reason up. Don't just copy patterns.")

kp(1, "cognitive-languages", "Why Python?",
   "Python is the #1 language for AI, data science, and automation. Simple syntax, huge ecosystem.",
   "# Python: simple and readable\ndef greet(name):\n    return f'Hello, {name}!'\n\nprint(greet('Alice'))  # Hello, Alice!",
   "Game: Which is Python and which is not?\nA) console.log('hi')\nB) print('hi')\nC) System.out.println('hi')",
   "Why is Python popular for AI?",
   ["It is the fastest language", "Simple syntax + huge AI ecosystem", "It only runs on Windows", "It is new"],
   1, "Python dominates AI because of its simplicity and ecosystem (PyTorch, TensorFlow, etc.).")

kp(1, "cognitive-languages", "Why TypeScript?",
   "TypeScript adds types to JavaScript. It catches errors before runtime and makes large codebases maintainable.",
   "# TypeScript: types catch errors\nfunction add(a: number, b: number): number {\n    return a + b;\n}\n\nadd('hello', 5); // ERROR! Caught at compile time!",
   "Game: Which error does TypeScript catch?\nA) add('hello', 5) when add expects numbers\nB) Server is down\nC) Database connection failed",
   "What does TypeScript add to JavaScript?",
   ["Nothing, they are the same", "Static type checking", "A database", "A web server"],
   1, "TypeScript adds type checking that catches errors before your code runs.")

kp(1, "cognitive-languages", "Why both Python AND TypeScript?",
   "Python owns AI/data/backend. TypeScript owns web/frontend. Together they cover 90%+ of modern development.",
   "# Python: AI and backend\nimport openai\nresult = openai.ChatCompletion.create(...)\n\n# TypeScript: Frontend and full-stack\nconst data = await fetch('/api/data');\nconst json = await data.json();",
   "Game: Match the language to the task:\nA) Build a website frontend -> ?\nB) Train a machine learning model -> ?\nC) Build an API server -> ? (both!)",
   "Why learn both Python and TypeScript?",
   ["They are the same language", "Together they cover AI, web, and backend", "One is enough", "They are outdated"],
   1, "Python + TypeScript covers AI, web, backend, and frontend. Maximum versatility.")

kp(1, "cognitive-languages", "Python vs TypeScript: key differences",
   "Python uses indentation, TypeScript uses braces. Python is dynamic, TypeScript is static. Both are great tools.",
   "# Python: indentation defines blocks\nif True:\n    print('yes')\n\n# TypeScript: braces define blocks\nif (true) {\n    console.log('yes');\n}",
   "Game: Convert this Python to TypeScript style:\nif x > 5:\n    print('big')\nelse:\n    print('small')",
   "How do Python and TypeScript differ in syntax?",
   ["Python uses braces, TypeScript uses indentation", "Python uses indentation, TypeScript uses braces", "They are identical", "Python has no syntax"],
   1, "Python uses indentation for blocks. TypeScript uses braces {}.")

kp(1, "cognitive-languages", "The right tool for the job",
   "Good programmers choose the right language for the task. Don't use Python for everything or TypeScript for everything.",
   "# Wrong: Use Python for a mobile app\n# Right: Use Python for data analysis\n\n# Wrong: Use TypeScript for ML training\n# Right: Use TypeScript for web UI",
   "Game: Which language for each task?\nA) Data analysis -> ?\nB) iOS app UI -> ?\nC) Web backend -> ?",
   "How should you choose a programming language?",
   ["Always use the newest one", "Choose based on the task and ecosystem", "Use only one language", "Whatever is popular"],
   1, "Choose the language that best fits the task and has the best ecosystem for it.")

# ============================================================
# WEEK 2-3: Python Fundamentals
# ============================================================

py_basics = [
    ("What is a variable?",
     "A variable is a name that points to a value in memory. Like a label on a box.",
     "x = 5\nprint(x)  # 5\n# x is the label, 5 is the value",
     "Game: What is the value of y?\nx = 3\ny = x\nx = 10",
     "What is a variable?",
     ["A box that holds values", "A name that points to a value", "A type of computer", "A function"],
     1, "A variable is a name (label) that points to a value stored in memory."),
    ("Assigning values",
     "Use = to assign a value to a variable. The right side is evaluated first, then stored.",
     "name = 'Alice'\nage = 25\npi = 3.14\nprint(name, age)  # Alice 25",
     "Game: What is x after this?\nx = 5\nx = x + 3\nx = x * 2",
     "What does = do in Python?",
     ["Checks equality", "Assigns a value to a variable", "Deletes a variable", "Creates a function"],
     1, "= assigns. == checks equality. They are different!"),
    ("Naming rules",
     "Variable names: start with letter or _, can have letters/numbers/_. Case-sensitive. No spaces.",
     "my_name = 'Alice'     # OK\n_private = True         # OK\n2nd_place = 'Silver'   # ERROR!\nmy name = 'Bob'        # ERROR!",
     "Game: Which names are valid?\nA) user_name\nB) 2fast\nC) _count\nD) my-var",
     "Which is a valid Python variable name?",
     ["2fast", "user_name", "my-var", "class"],
     1, "Names must start with letter/_. No hyphens, no starting with numbers, no keywords."),
    ("Types: int and float",
     "int = whole numbers (42, -7, 0). float = decimal numbers (3.14, -0.5).",
     "x = 42       # int\ny = 3.14     # float\nprint(type(x))  # <class 'int'>\nprint(type(y))  # <class 'float'>",
     "Game: What type is each?\nA) 100\nB) 3.14\nC) -7\nD) 0.0",
     "What type is 3.14?",
     ["int", "float", "str", "bool"],
     1, "Numbers with decimal points are float. Whole numbers are int."),
    ("Types: str (strings)",
     "Strings are text, enclosed in quotes. Single or double quotes both work.",
     "name = 'Alice'\nmsg = \"Hello, world!\"\nprint(f'Hi {name}!')  # Hi Alice!",
     "Game: What does this print?\nname = 'Bob'\nprint(f'Hello {name}!')",
     "How do you create a string?",
     ["Using numbers", "Using quotes around text", "Using parentheses", "Using square brackets"],
     1, "Strings are text wrapped in quotes: 'hello' or \"hello\"."),
    ("Types: bool (booleans)",
     "bool = True or False. Used for conditions and logic.",
     "is_student = True\nhas_ticket = False\nprint(is_student and has_ticket)  # False\nprint(is_student or has_ticket)   # True",
     "Game: What is the result?\nTrue and False -> ?\nTrue or False -> ?\nnot True -> ?",
     "What are the two boolean values?",
     ["Yes and No", "True and False", "1 and 0", "On and Off"],
     1, "Booleans are either True or False. Used for logic and conditions."),
    ("Type checking",
     "Use type() to check what type a variable is. Use isinstance() for comparisons.",
     "x = 42\nprint(type(x))            # <class 'int'>\nprint(isinstance(x, int))  # True\nprint(isinstance(x, str))  # False",
     "Game: What does type('hello') return?",
     "How do you check a variable's type?",
     ["Use typeof()", "Use type()", "Use check()", "Use var()"],
     1, "type(variable) returns the type. isinstance(variable, Type) checks if it matches."),
    ("Type conversion",
     "Convert between types: int(), float(), str(). Some conversions lose information.",
     "x = '42'\ny = int(x)      # Convert string to int\nprint(y + 8)    # 50\n\nz = 3.99\nw = int(z)      # Truncates to 3 (not rounded!)",
     "Game: What is int('7') + int('3')?",
     "How do you convert '42' to a number?",
     ["number('42')", "int('42')", "str('42')", "float('42')"],
     1, "int('42') converts the string '42' to the integer 42."),
    ("f-strings: formatted strings",
     "f-strings let you embed variables in strings using {variable_name}.",
     "name = 'Alice'\nage = 25\nprint(f'{name} is {age} years old')\n# Output: Alice is 25 years old\nprint(f'Next year: {age + 1}')  # Next year: 26",
     "Game: Write an f-string that prints 'My score is 100' using variable score = 100",
     "What does f'Hello {name}' do?",
     ["Creates a function", "Embeds the variable value in the string", "Deletes name", "Causes an error"],
     1, "f-strings embed expressions inside strings: f'...' with {variable}."),
    ("String methods: upper, lower, strip",
     "Strings have built-in methods. .upper() makes uppercase, .lower() lowercase, .strip() removes spaces.",
     "msg = '  Hello World  '\nprint(msg.upper())   # '  HELLO WORLD  '\nprint(msg.strip())   # 'Hello World'\nprint(msg.strip().lower())  # 'hello world'",
     "Game: What does '  HI  '.strip().lower() return?",
     "What does .strip() do?",
     ["Converts to uppercase", "Removes leading/trailing spaces", "Reverses the string", "Splits into words"],
     1, ".strip() removes whitespace from the start and end of a string."),
]

for i, (title, expl, code, game, q, opts, correct, qexpl) in enumerate(py_basics):
    kp(2, "py-variables", title, expl, code, game, q, opts, correct, qexpl)

# More Python basics
py_basics2 = [
    ("Lists: ordered collections",
     "Lists hold multiple values in order. Use [] to create, index with [position].",
     "fruits = ['apple', 'banana', 'cherry']\nprint(fruits[0])   # apple (first)\nprint(fruits[-1])  # cherry (last)\nprint(len(fruits)) # 3",
     "Game: What is fruits[1]?\nfruits = ['a', 'b', 'c', 'd']",
     "How do you get the first item of a list?",
     ["list.first()", "list[0]", "list(0)", "list[1]"],
     1, "Lists use 0-based indexing. First item is list[0]."),
    ("List methods: append, insert, remove",
     "Add items with .append(), insert at position with .insert(), remove with .remove().",
     "nums = [1, 2, 3]\nnums.append(4)      # [1, 2, 3, 4]\nnums.insert(0, 0)   # [0, 1, 2, 3, 4]\nnums.remove(2)      # [0, 1, 3, 4]",
     "Game: What is the list after these operations?\nitems = [1, 2]\nitems.append(3)\nitems.insert(0, 0)",
     "What does .append() do?",
     ["Removes an item", "Adds an item to the end", "Sorts the list", "Reverses the list"],
     1, ".append(item) adds the item to the end of the list."),
    ("List slicing",
     "Slicing extracts a portion: list[start:end]. End is exclusive.",
     "nums = [0, 1, 2, 3, 4, 5]\nprint(nums[1:4])   # [1, 2, 3]\nprint(nums[:3])    # [0, 1, 2]\nprint(nums[3:])    # [3, 4, 5]\nprint(nums[::2])   # [0, 2, 4]",
     "Game: What does [10, 20, 30, 40, 50][1:4] return?",
     "What does list[1:4] return?",
     ["Items at index 1, 2, 3", "Items at index 1, 2, 3, 4", "Items at index 0, 1, 2, 3", "An error"],
     1, "Slicing [1:4] returns items at index 1, 2, 3 (end index is exclusive)."),
    ("For loops",
     "For loops iterate over each item in a sequence.",
     "for fruit in ['apple', 'banana', 'cherry']:\n    print(f'I like {fruit}')\n# I like apple\n# I like banana\n# I like cherry",
     "Game: What does this print?\nfor i in [1, 2, 3]:\n    print(i * 2)",
     "What does a for loop do?",
     ["Runs once", "Iterates over each item in a sequence", "Creates a list", "Deletes items"],
     1, "A for loop runs the body once for each item in the sequence."),
    ("range() for number sequences",
     "range(n) generates 0 to n-1. range(start, end, step) for custom ranges.",
     "for i in range(5):\n    print(i)  # 0, 1, 2, 3, 4\n\nfor i in range(2, 6):\n    print(i)  # 2, 3, 4, 5",
     "Game: What numbers does range(3) produce?",
     "What does range(5) produce?",
     ["1, 2, 3, 4, 5", "0, 1, 2, 3, 4", "0, 1, 2, 3, 4, 5", "5, 4, 3, 2, 1"],
     1, "range(n) produces 0 to n-1. range(5) = 0, 1, 2, 3, 4."),
    ("While loops",
     "While loops repeat as long as a condition is True.",
     "count = 0\nwhile count < 3:\n    print(count)\n    count += 1\n# Output: 0, 1, 2",
     "Game: How many times does this loop run?\nx = 0\nwhile x < 10:\n    x += 3",
     "When does a while loop stop?",
     ["After 10 iterations", "When the condition becomes False", "When you tell it to", "Never"],
     1, "A while loop runs while its condition is True. It stops when the condition becomes False."),
    ("If/elif/else",
     "Conditional statements let your code make decisions.",
     "age = 18\nif age >= 18:\n    print('Adult')\nelif age >= 13:\n    print('Teenager')\nelse:\n    print('Child')",
     "Game: What does this print?\nx = 15\nif x > 20:\n    print('big')\nelif x > 10:\n    print('medium')\nelse:\n    print('small')",
     "What does elif mean?",
     ["End the loop", "Else if - check another condition", "Delete the variable", "Start over"],
     1, "elif means 'else if'. It checks another condition if the previous ones were False."),
    ("Comparison operators",
     "Compare values: == (equal), != (not equal), > < >= <= (greater/less).",
     "print(5 == 5)    # True\nprint(5 != 3)    # True\nprint(10 > 7)    # True\nprint(3 >= 3)    # True\nprint(2 == 2.0)  # True (value equality)",
     "Game: True or False?\nA) 5 > 3\nB) 2 == 2.0\nC) 7 != 7",
     "What does == check?",
     ["Assignment", "Equality of values", "Type equality", "Memory address"],
     1, "== checks if two values are equal. = assigns a value."),
    ("Logical operators: and, or, not",
     "Combine conditions: and (both True), or (at least one True), not (reverse).",
     "age = 25\nhas_id = True\n\nif age >= 18 and has_id:\n    print('Can enter')\n\nif age < 13 or age > 65:\n    print('Discount')\n\nif not has_id:\n    print('Need ID')",
     "Game: What is the result?\nTrue and False -> ?\nFalse or True -> ?\nnot False -> ?",
     "What does 'and' return if both sides are True?",
     ["False", "True", "None", "Error"],
     1, "'and' returns True only if BOTH sides are True."),
    ("Dictionaries: key-value pairs",
     "Dictionaries store key-value pairs. Like a real dictionary: word -> definition.",
     "person = {'name': 'Alice', 'age': 25}\nprint(person['name'])  # Alice\nperson['email'] = 'alice@mail.com'\nprint(person.keys())   # ['name', 'age', 'email']",
     "Game: What does this return?\nfruit = {'apple': 3, 'banana': 5}\nprint(fruit['banana'])",
     "How do you access a dictionary value?",
     ["dict[0]", "dict['key']", "dict.get_index()", "dict.first()"],
     1, "Use dict['key'] to get the value for that key."),
    ("Dictionary methods",
     "Useful methods: .get() (safe access), .keys(), .values(), .items().",
     "data = {'a': 1, 'b': 2}\nprint(data.get('c', 0))  # 0 (default if key missing)\nprint(list(data.keys()))   # ['a', 'b']\nprint(list(data.values())) # [1, 2]",
     "Game: What does data.get('x', 'default') return if 'x' is not in data?",
     "What does .get('key', default) do?",
     ["Always returns None", "Returns value or default if key missing", "Deletes the key", "Creates a new key"],
     1, ".get() safely returns the value, or the default if the key does not exist."),
    ("Tuples: immutable sequences",
     "Tuples are like lists but cannot be changed (immutable). Use () to create.",
     "point = (3, 4)\nprint(point[0])  # 3\n# point[0] = 5  # ERROR! Tuples are immutable\n\nx, y = point  # Unpacking\nprint(x, y)    # 3 4",
     "Game: Can you change a tuple's value?\npoint = (1, 2)\npoint[0] = 99  # ?",
     "How are tuples different from lists?",
     ["Tuples are faster", "Tuples cannot be changed (immutable)", "Tuples hold more items", "Tuples use [] syntax"],
     1, "Tuples are immutable: once created, you cannot add, remove, or change items."),
    ("Sets: unique collections",
     "Sets hold unique values with no duplicates. Use {} to create.",
     "nums = {1, 2, 2, 3, 3, 3}\nprint(nums)  # {1, 2, 3} - duplicates removed!\nnums.add(4)\nprint(nums)  # {1, 2, 3, 4}",
     "Game: What does {1, 1, 2, 2, 3} become?",
     "What is special about a set?",
     ["It is ordered", "It removes duplicates", "It allows duplicates", "It uses () syntax"],
     1, "Sets automatically remove duplicates and have no defined order."),
]

for i, (title, expl, code, game, q, opts, correct, qexpl) in enumerate(py_basics2):
    kp(2, "py-variables", title, expl, code, game, q, opts, correct, qexpl)

# ============================================================
# Python Functions (Week 3)
# ============================================================

py_funcs = [
    ("Defining functions",
     "Use def to create a function. Functions group code that does one thing.",
     "def greet(name):\n    return f'Hello, {name}!'\n\nprint(greet('Alice'))  # Hello, Alice!",
     "Game: Write a function that takes a number and returns its double.",
     "How do you define a function?",
     ["function greet(name):", "def greet(name):", "func greet(name):", "fn greet(name):"],
     1, "In Python, use 'def' to define a function."),
    ("Parameters and arguments",
     "Parameters are the names in the function definition. Arguments are the values you pass in.",
     "def add(a, b):    # a, b are parameters\n    return a + b\n\nresult = add(3, 5)  # 3, 5 are arguments\nprint(result)  # 8",
     "Game: What are the parameters and arguments here?\ndef square(n): return n * n\nsquare(4)",
     "What is the difference between parameters and arguments?",
     ["They are the same", "Parameters are in definition, arguments are values passed", "Arguments are in definition", "Parameters are always numbers"],
     1, "Parameters = names in definition. Arguments = actual values passed."),
    ("Return values",
     "Use 'return' to send a value back from a function. Without return, function returns None.",
     "def double(n):\n    return n * 2\n\ndef print_hello():\n    print('hello')\n    # No return, so returns None\n\nresult = print_hello()\nprint(result)  # None",
     "Game: What does this return?\ndef mystery(x):\n    return x + 1\nresult = mystery(5)",
     "What does 'return' do in a function?",
     ["Stops the program", "Sends a value back to the caller", "Prints to screen", "Creates a variable"],
     1, "return sends a value back. Without it, the function returns None."),
    ("Default parameters",
     "Give parameters default values. They are used if no argument is passed.",
     "def greet(name, greeting='Hello'):\n    return f'{greeting}, {name}!'\n\nprint(greet('Alice'))           # Hello, Alice!\nprint(greet('Bob', 'Hi'))       # Hi, Bob!",
     "Game: What does greet('Alice') print?\ndef greet(name, msg='Hey'):\n    return f'{msg} {name}'",
     "What is a default parameter?",
     ["A required parameter", "A parameter with a fallback value", "A parameter that is always None", "A global variable"],
     1, "Default parameters have fallback values used when no argument is passed."),
    ("Variable scope",
     "Variables inside a function are local. Variables outside are global. Local shadows global.",
     "x = 10  # Global\n\ndef foo():\n    x = 20  # Local (different from global x)\n    print(x)  # 20\n\nfoo()\nprint(x)  # 10 (global unchanged)",
     "Game: What does this print?\nx = 1\ndef change():\n    x = 99\nchange()\nprint(x)",
     "What is variable scope?",
     ["Where a variable can be accessed", "The type of a variable", "The name of a variable", "The size of a variable"],
     1, "Scope determines where a variable is visible. Local variables only exist inside their function."),
    ("*args: variable arguments",
     "Use *args to accept any number of positional arguments. args becomes a tuple.",
     "def total(*numbers):\n    return sum(numbers)\n\nprint(total(1, 2, 3))      # 6\nprint(total(1, 2, 3, 4, 5)) # 15",
     "Game: What does total(10, 20) return?\ndef total(*args):\n    return sum(args)",
     "What does *args do?",
     ["Creates a list", "Accepts any number of arguments", "Makes arguments optional", "Deletes arguments"],
     1, "*args collects all positional arguments into a tuple."),
    ("**kwargs: keyword arguments",
     "Use **kwargs to accept any number of keyword arguments. kwargs becomes a dictionary.",
     "def show_info(**kwargs):\n    for key, value in kwargs.items():\n        print(f'{key}: {value}')\n\nshow_info(name='Alice', age=25)\n# name: Alice\n# age: 25",
     "Game: What does kwargs contain?\ndef f(**kwargs): print(kwargs)\nf(x=1, y=2)",
     "What does **kwargs collect?",
     ["Positional arguments", "Keyword arguments as a dictionary", "File paths", "Error messages"],
     1, "**kwargs collects keyword arguments into a dictionary."),
    ("Lambda functions",
     "Lambda creates small anonymous functions in one line.",
     "double = lambda x: x * 2\nprint(double(5))  # 10\n\n# Often used with map/filter\nnums = [1, 2, 3, 4]\nsquared = list(map(lambda x: x**2, nums))\nprint(squared)  # [1, 4, 9, 16]",
     "Game: What does this return?\nadd = lambda a, b: a + b\nprint(add(3, 4))",
     "What is a lambda function?",
     ["A named function", "A small anonymous function", "A class", "A module"],
     1, "Lambda is a small, anonymous function defined in one line."),
    ("Closures",
     "A closure is a function that remembers variables from its enclosing scope.",
     "def make_multiplier(n):\n    def multiply(x):\n        return x * n  # Remembers n!\n    return multiply\n\ndouble = make_multiplier(2)\ntriple = make_multiplier(3)\nprint(double(5))  # 10\nprint(triple(5))  # 15",
     "Game: What does this print?\ndef outer(x):\n    def inner():\n        return x\n    return inner\nf = outer(42)\nprint(f())",
     "What does a closure remember?",
     ["Everything", "Variables from its enclosing function", "Nothing", "Only global variables"],
     1, "A closure remembers variables from the function that created it."),
    ("Decorators: wrapping functions",
     "A decorator adds behavior to a function without changing it. Like gift wrapping.",
     "def log_call(func):\n    def wrapper(*args):\n        print(f'Calling {func.__name__}')\n        return func(*args)\n    return wrapper\n\n@log_call\ndef add(a, b):\n    return a + b\n\nadd(3, 5)  # Prints: Calling add, returns 8",
     "Game: What does the @log_call decorator do?\nA) Deletes the function\nB) Adds logging before the function runs\nC) Changes the function name",
     "What does a decorator do?",
     ["Deletes a function", "Adds behavior to a function without changing it", "Creates a new module", "Imports a library"],
     1, "Decorators wrap a function to add behavior before/after it runs."),
]

for i, (title, expl, code, game, q, opts, correct, qexpl) in enumerate(py_funcs):
    kp(3, "py-functions", title, expl, code, game, q, opts, correct, qexpl)

# ============================================================
# Continue generating more knowledge points...
# ============================================================

# Python Classes (Week 3)
py_classes = [
    ("What is a class?",
     "A class is a blueprint for creating objects. Like a cookie cutter: it defines the shape, but each cookie is separate.",
     "class Dog:\n    def __init__(self, name):\n        self.name = name\n    def bark(self):\n        return f'{self.name} says Woof!'\n\nmy_dog = Dog('Rex')\nprint(my_dog.bark())  # Rex says Woof!",
     "Game: Create a Cat class with name and meow() method.",
     "What is a class?",
     ["A function", "A blueprint for creating objects", "A variable", "A loop"],
     1, "A class defines the structure and behavior. Objects are instances of a class."),
    ("__init__: the constructor",
     "__init__ runs when you create a new object. It sets up the initial state.",
     "class Person:\n    def __init__(self, name, age):\n        self.name = name\n        self.age = age\n\nalice = Person('Alice', 25)\nprint(alice.name)  # Alice",
     "Game: When does __init__ run?\nA) When you call .init()\nB) When you create a new object\nC) When you delete the object",
     "When does __init__ run?",
     ["When you import the class", "When you create a new object", "When you call .init()", "Never automatically"],
     1, "__init__ runs automatically when you create a new instance: obj = ClassName()."),
    ("Instance vs class variables",
     "Instance variables belong to each object. Class variables are shared by all instances.",
     "class Student:\n    school = 'Python Academy'  # Class variable\n    def __init__(self, name):\n        self.name = name  # Instance variable\n\na = Student('Alice')\nb = Student('Bob')\nprint(a.school)  # Python Academy\nprint(a.name)    # Alice",
     "Game: If I change Student.school, does it affect all instances?",
     "What is a class variable?",
     ["A variable that is different for each object", "A variable shared by all instances", "A global variable", "A function parameter"],
     1, "Class variables are shared. Instance variables are unique to each object."),
    ("Methods: functions inside classes",
     "Methods are functions defined inside a class. They always take 'self' as the first parameter.",
     "class Calculator:\n    def __init__(self):\n        self.result = 0\n    def add(self, n):\n        self.result += n\n        return self\n    def show(self):\n        return self.result\n\nc = Calculator()\nc.add(5).add(3)\nprint(c.show())  # 8",
     "Game: Why does every method need 'self'?\nA) It is optional\nB) It refers to the current instance\nC) It is the class name",
     "What is 'self' in a method?",
     ["The class itself", "The current instance of the object", "A global variable", "The parent class"],
     1, "self refers to the current instance. It lets methods access the object's data."),
    ("Inheritance",
     "Inheritance lets a class get methods/properties from a parent class. Child extends parent.",
     "class Animal:\n    def speak(self):\n        return '...'\n\nclass Dog(Animal):\n    def speak(self):\n        return 'Woof!'\n\nclass Cat(Animal):\n    def speak(self):\n        return 'Meow!'\n\nprint(Dog().speak())  # Woof!",
     "Game: What does Cat().speak() return?\nclass Animal:\n    def speak(self): return '...'\nclass Cat(Animal):\n    def speak(self): return 'Meow!'",
     "What does inheritance do?",
     ["Copies code", "Lets a class reuse methods from a parent class", "Deletes the parent", "Creates a function"],
     1, "Inheritance lets child classes reuse and extend parent class functionality."),
    ("Dataclasses",
     "@dataclass auto-generates __init__, __repr__, __eq__ from type hints. Less boilerplate.",
     "from dataclasses import dataclass\n\n@dataclass\nclass Point:\n    x: float\n    y: float\n\np = Point(3.0, 4.0)\nprint(p)  # Point(x=3.0, y=4.0)",
     "Game: What does @dataclass generate for you?\nA) Only __init__\nB) __init__, __repr__, __eq__\nC) Nothing",
     "What does @dataclass do?",
     ["Makes the class abstract", "Auto-generates __init__, __repr__, __eq__", "Makes the class immutable", "Deletes the class"],
     1, "@dataclass reads type hints and generates boilerplate methods automatically."),
]

for i, (title, expl, code, game, q, opts, correct, qexpl) in enumerate(py_classes):
    kp(3, "py-classes", title, expl, code, game, q, opts, correct, qexpl)

# Python Async (Week 4)
py_async = [
    ("What is async programming?",
     "Async lets your program do other work while waiting for slow operations (network, file I/O).",
     "import asyncio\n\nasync def fetch_data():\n    print('Fetching...')\n    await asyncio.sleep(1)  # Simulate waiting\n    print('Done!')\n    return {'data': 42}\n\nasyncio.run(fetch_data())",
     "Game: Why is async useful?\nA) Makes code faster\nB) Lets program do other work while waiting\nC) Uses more memory",
     "What does async programming do?",
     ["Makes everything run at once", "Lets the program do other work while waiting", "Uses multiple CPUs", "Is only for games"],
     1, "Async lets the program handle other tasks while waiting for I/O operations."),
    ("async and await keywords",
     "'async def' defines a coroutine. 'await' pauses it until the result is ready.",
     "import asyncio\n\nasync def say_hello():\n    await asyncio.sleep(1)\n    return 'Hello!'\n\nasync def main():\n    result = await say_hello()\n    print(result)\n\nasyncio.run(main())",
     "Game: What does 'await' do?\nA) Blocks the entire program\nB) Pauses the coroutine and lets others run\nC) Creates a new thread",
     "What does 'await' do?",
     ["Blocks everything", "Pauses this coroutine, lets others run", "Creates a thread", "Stops the program"],
     1, "await pauses the coroutine but not the entire event loop. Other tasks can run."),
    ("asyncio.gather: run tasks concurrently",
     "gather() runs multiple coroutines at the same time and waits for all to finish.",
     "import asyncio\n\nasync def task(name, delay):\n    await asyncio.sleep(delay)\n    return f'{name} done'\n\nasync def main():\n    results = await asyncio.gather(\n        task('A', 2),\n        task('B', 1),\n    )\n    print(results)  # ['A done', 'B done']",
     "Game: If task A takes 2s and task B takes 1s, how long does gather() take?\nA) 3 seconds\nB) 2 seconds\nC) 1 second",
     "What does asyncio.gather() do?",
     ["Runs tasks one by one", "Runs tasks concurrently and waits for all", "Cancels all tasks", "Creates threads"],
     1, "gather() runs tasks concurrently. Total time = longest task, not sum of all."),
    ("async context managers",
     "async with manages resources that need setup and cleanup in async code.",
     "import asyncio\n\nclass AsyncTimer:\n    async def __aenter__(self):\n        print('Starting...')\n        return self\n    async def __aexit__(self, *args):\n        print('Done!')\n\nasync def main():\n    async with AsyncTimer():\n        await asyncio.sleep(1)\n\nasyncio.run(main())",
     "Game: What happens when the async with block ends?\nA) Nothing\nB) __aexit__ runs automatically\nC) The program crashes",
     "What does 'async with' do?",
     ["Creates a thread", "Manages async resource setup and cleanup", "Blocks the program", "Imports a module"],
     1, "async with runs __aenter__ on entry and __aexit__ on exit, even in async code."),
]

for i, (title, expl, code, game, q, opts, correct, qexpl) in enumerate(py_async):
    kp(4, "py-async", title, expl, code, game, q, opts, correct, qexpl)

# Python Type System (Week 4)
py_types = [
    ("Why type hints?",
     "Type hints document what types a function expects and returns. They catch bugs before runtime.",
     "def greet(name: str) -> str:\n    return f'Hello, {name}!'\n\n# mypy or IDE catches:\ngreet(42)  # Warning: expected str, got int",
     "Game: What type hint goes here?\ndef add(a: ___, b: ___) -> ___:\n    return a + b",
     "Why use type hints?",
     ["To make code slower", "To document types and catch errors", "To delete variables", "To import modules"],
     1, "Type hints document expected types and help catch errors before running code."),
    ("Basic type hints",
     "Use built-in types: int, str, float, bool. For collections: list[int], dict[str, int].",
     "def process(names: list[str], count: int) -> dict[str, int]:\n    return {name: count for name in names}\n\nresult = process(['a', 'b'], 3)\nprint(result)  # {'a': 3, 'b': 3}",
     "Game: What type hint for a list of numbers?\nA) list\nB) list[int]\nC) [int]\nD) int[]",
     "How do you hint a list of integers?",
     ["list", "list[int]", "[int]", "int[]"],
     1, "Use list[int] for a list of integers. This is the modern Python syntax."),
    ("Optional and None",
     "Optional[X] means the value can be X or None. Same as X | None.",
     "from typing import Optional\n\ndef find_user(user_id: int) -> Optional[str]:\n    if user_id == 1:\n        return 'Alice'\n    return None\n\nname = find_user(2)  # None\nif name is not None:\n    print(name)",
     "Game: What does Optional[str] mean?\nA) Always a string\nB) A string or None\nC) Always None",
     "What does Optional[str] mean?",
     ["Always a string", "A string or None", "An optional parameter", "A string that can be empty"],
     1, "Optional[str] means the value is either a str or None."),
    ("TypeVar: generics",
     "TypeVar lets you write functions that work with any type while keeping type safety.",
     "from typing import TypeVar\n\nT = TypeVar('T')\n\ndef first(items: list[T]) -> T:\n    return items[0]\n\nfirst([1, 2, 3])      # Returns int\nfirst(['a', 'b'])     # Returns str",
     "Game: What type does first([1, 2, 3]) return?\nA) Any\nB) int\nC) str",
     "What does TypeVar enable?",
     ["Deleting types", "Writing type-safe generic functions", "Importing modules", "Creating classes"],
     1, "TypeVar creates placeholder types for generic functions that work with any type."),
]

for i, (title, expl, code, game, q, opts, correct, qexpl) in enumerate(py_types):
    kp(4, "py-types", title, expl, code, game, q, opts, correct, qexpl)

# Python Modules (Week 4)
py_mods = [
    ("Importing modules",
     "Use import to bring in code from other files or libraries.",
     "import math\nprint(math.pi)        # 3.14159...\nprint(math.sqrt(16))  # 4.0\n\nfrom math import pi, sqrt\nprint(pi)  # 3.14159...",
     "Game: What is the difference?\nA) import math\nB) from math import sqrt",
     "What does 'import math' do?",
     ["Creates math", "Makes math functions available", "Deletes math", "Runs math code"],
     1, "import loads a module and makes its functions available in your code."),
    ("Creating your own modules",
     "Any .py file is a module. Put functions in a file, import them from another.",
     "# utils.py\ndef double(n):\n    return n * 2\n\n# main.py\nfrom utils import double\nprint(double(5))  # 10",
     "Game: You have helpers.py with function add(). How do you use it in main.py?",
     "How do you create a module?",
     ["Create a .py file with functions", "Use the module keyword", "Import from Python", "You cannot create modules"],
     1, "Any .py file is automatically a module. Import functions from it."),
    ("__name__ and __main__",
     "__name__ is '__main__' when the file is run directly, or the module name when imported.",
     "# check.py\nprint(f'__name__ is: {__name__}')\n\n# Run directly: __name__ is __main__\n# Imported: __name__ is check",
     "Game: What is __name__ when you run python check.py?",
     "What is __name__ when running a file directly?",
     ["The filename", "'__main__'", "None", "The path"],
     1, "__name__ is '__main__' when the file is the entry point. Otherwise it is the module name."),
    ("Packages: organizing modules",
     "A package is a folder with __init__.py. It groups related modules together.",
     "# mypackage/\n#   __init__.py\n#   math_utils.py\n#   string_utils.py\n\nfrom mypackage.math_utils import add\nfrom mypackage.string_utils import capitalize",
     "Game: What makes a folder a Python package?\nA) Having a main.py\nB) Having an __init__.py\nC) Having 10+ files",
     "What makes a folder a Python package?",
     ["Having a main.py file", "Having an __init__.py file", "Having more than 5 files", "Being in the root directory"],
     1, "A folder becomes a package when it contains __init__.py (can be empty)."),
]

for i, (title, expl, code, game, q, opts, correct, qexpl) in enumerate(py_mods):
    kp(4, "py-modules", title, expl, code, game, q, opts, correct, qexpl)

# ============================================================
# WEEK 5-6: TypeScript Fundamentals
# ============================================================

ts_basics = [
    ("What is TypeScript?",
     "TypeScript is JavaScript with static types. It catches errors at compile time, not runtime.",
     "// JavaScript: no error until runtime\nfunction add(a, b) { return a + b; }\nadd('hello', 5); // Works but wrong!\n\n// TypeScript: error at compile time\nfunction add(a: number, b: number) {\n    return a + b;\n}\nadd('hello', 5); // ERROR!",
     "Game: When does TypeScript catch errors?\nA) At runtime\nB) At compile time\nC) Never",
     "When does TypeScript catch type errors?",
     ["At runtime", "At compile time (before running)", "Never", "Only in production"],
     1, "TypeScript catches errors at compile time, before the code runs."),
    ("Basic types: string, number, boolean",
     "The three most common types: string (text), number (all numbers), boolean (true/false).",
     "let name: string = 'Alice';\nlet age: number = 25;\nlet active: boolean = true;\n\n// TypeScript infers types too!\nlet city = 'NYC'; // inferred as string",
     "Game: What type is inferred?\nlet x = 42;\nlet y = 'hello';\nlet z = true;",
     "What type is 'hello' in TypeScript?",
     ["text", "string", "char", "word"],
     1, "Text values are string type in TypeScript."),
    ("Arrays and tuples",
     "Arrays hold multiple values of the same type. Tuples hold fixed-length with specific types.",
     "let nums: number[] = [1, 2, 3];\nlet names: Array<string> = ['a', 'b'];\n\n// Tuple: fixed types at each position\nlet pair: [string, number] = ['Alice', 25];",
     "Game: What type is [1, 'hello', true]?\nA) Array\nB) Tuple [number, string, boolean]\nC) object",
     "What is a tuple?",
     ["An array that can hold any types", "A fixed-length array with specific types at each position", "A dictionary", "A function"],
     1, "Tuples have fixed length with specific types at each position."),
    ("Interfaces: defining shapes",
     "Interfaces define the shape of an object: what properties and methods it must have.",
     "interface User {\n    name: string;\n    age: number;\n    email?: string; // optional\n}\n\nconst alice: User = {\n    name: 'Alice',\n    age: 25,\n};",
     "Game: Is email required in this interface?\ninterface User {\n    name: string;\n    email?: string;\n}",
     "What does an interface define?",
     ["A class", "The shape/structure of an object", "A function", "A variable"],
     1, "Interfaces define what properties and methods an object must have."),
    ("Type aliases with 'type'",
     "'type' creates reusable type names. Can represent unions, intersections, and more.",
     "type ID = string | number;\ntype Point = { x: number; y: number; };\n\ntype Result =\n    | { success: true; data: string }\n    | { success: false; error: string };",
     "Game: What does string | number mean?\nA) String and number\nB) String or number\nC) Neither",
     "What does the | (pipe) mean in types?",
     ["And", "Or (union type)", "Not", "Delete"],
     1, "| creates a union type: the value can be either type."),
    ("Functions with types",
     "Type function parameters and return values. TypeScript infers return type from the code.",
     "function greet(name: string): string {\n    return `Hello, ${name}!`;\n}\n\n// Arrow function\nconst double = (n: number): number => n * 2;\n\n// Optional parameter\nfunction hi(name: string, greeting?: string) {\n    return `${greeting ?? 'Hi'} ${name}`;\n}",
     "Game: What type does this return?\nfunction add(a: number, b: number) {\n    return a + b;\n}",
     "How do you type a function parameter?",
     ["function greet(name: str)", "function greet(name: string)", "function greet(name: String)", "function greet(name)"],
     1, "Use lowercase 'string' (not 'String') for TypeScript type annotations."),
    ("Generics: type parameters",
     "Generics let you write code that works with any type while keeping type safety.",
     "function identity<T>(value: T): T {\n    return value;\n}\n\nidentity<string>('hello'); // T = string\nidentity<number>(42);      // T = number\n\n// TypeScript can infer T!\nidentity('hello'); // T inferred as string",
     "Game: What type does identity(42) return?\nA) any\nB) number\nC) unknown",
     "What does <T> mean in a function?",
     ["It is a comment", "It is a type parameter that gets replaced with a real type", "It is an HTML tag", "It is an error"],
     1, "<T> is a type parameter. It gets replaced with the actual type when called."),
    ("Union types",
     "Union types allow a value to be one of several types. Use | to combine types.",
     "type StringOrNumber = string | number;\n\nfunction format(value: StringOrNumber): string {\n    if (typeof value === 'string') {\n        return value.toUpperCase();\n    }\n    return value.toFixed(2);\n}",
     "Game: What must you do before using a union type?\nA) Nothing\nB) Narrow the type (check which one it is)\nC) Convert it to string",
     "What is a union type?",
     ["A type that is always one thing", "A type that can be one of several things", "A type that is nothing", "A type that is everything"],
     1, "Union types let a value be one of several types. You narrow before using type-specific features."),
    ("Type narrowing",
     "TypeScript narrows types after checks. After 'if typeof x === string', x is known to be string.",
     "function process(value: string | number) {\n    if (typeof value === 'string') {\n        // TypeScript knows: value is string here\n        return value.toUpperCase();\n    }\n    // TypeScript knows: value is number here\n    return value.toFixed(2);\n}",
     "Game: After this check, what type is x?\nif (typeof x === 'number') { ... }\nA) string\nB) number\nC) unknown",
     "What is type narrowing?",
     ["Making types smaller", "TypeScript learning the exact type after a check", "Deleting types", "Creating new types"],
     1, "Narrowing: after a type check, TypeScript knows the exact type in that branch."),
    ("Literal types",
     "Literal types restrict a value to specific exact values.",
     "type Direction = 'up' | 'down' | 'left' | 'right';\ntype DiceRoll = 1 | 2 | 3 | 4 | 5 | 6;\n\nfunction move(dir: Direction) {\n    console.log(`Moving ${dir}`);\n}\n\nmove('up');    // OK\nmove('fly');   // ERROR!",
     "Game: What values can Direction hold?\ntype Direction = 'up' | 'down' | 'left' | 'right';",
     "What is a literal type?",
     ["Any string", "A type restricted to specific exact values", "A number", "A boolean"],
     1, "Literal types restrict values to specific strings, numbers, or booleans."),
]

for i, (title, expl, code, game, q, opts, correct, qexpl) in enumerate(ts_basics):
    kp(5, "ts-types", title, expl, code, game, q, opts, correct, qexpl)

# TypeScript Functions (Week 5)
ts_funcs = [
    ("Function overloads",
     "Overloads let a function accept different parameter combinations with different return types.",
     "function format(value: string): string;\nfunction format(value: number): string;\nfunction format(value: string | number): string {\n    if (typeof value === 'string') return value;\n    return value.toFixed(2);\n}\n\nformat('hello'); // OK\nformat(3.14);    // OK",
     "Game: Why use overloads instead of just string | number?\nA) For better type safety per call\nB) They are the same\nC) Overloads are faster",
     "What are function overloads?",
     ["Multiple functions with the same name", "Multiple type signatures for one function implementation", "Functions that overload the CPU", "Functions with too many parameters"],
     1, "Overloads define multiple signatures for one function, giving precise types per call."),
    ("Higher-order functions",
     "Functions that take other functions as arguments or return functions.",
     "function apply(fn: (x: number) => number, value: number): number {\n    return fn(value);\n}\n\nconst double = (x: number) => x * 2;\nconst triple = (x: number) => x * 3;\n\nconsole.log(apply(double, 5)); // 10\nconsole.log(apply(triple, 5)); // 15",
     "Game: What does apply(x => x + 1, 10) return?",
     "What is a higher-order function?",
     ["A function with many parameters", "A function that takes or returns other functions", "A fast function", "A class method"],
     1, "Higher-order functions take functions as arguments or return functions."),
    ("Currying",
     "Currying transforms a function with multiple arguments into a chain of functions with one argument each.",
     "function add(a: number): (b: number) => number {\n    return (b) => a + b;\n}\n\nconst add5 = add(5);\nconsole.log(add5(3));  // 8\nconsole.log(add5(10)); // 15",
     "Game: What does add(2)(3) return?\nfunction add(a: number) {\n    return (b: number) => a + b;\n}",
     "What is currying?",
     ["A cooking technique", "Transforming multi-arg functions into single-arg chains", "A loop pattern", "A type error"],
     1, "Currying transforms f(a, b) into f(a)(b). Each call takes one argument."),
    ("Pipe and compose",
     "Pipe chains functions left-to-right. Compose chains right-to-left.",
     "const pipe = <T>(...fns: Array<(x: T) => T>) =>\n    (x: T) => fns.reduce((acc, fn) => fn(acc), x);\n\nconst process = pipe(\n    (x: number) => x + 1,\n    (x: number) => x * 2,\n    (x: number) => x - 3,\n);\n\nconsole.log(process(5)); // ((5+1)*2)-3 = 9",
     "Game: What does pipe(x => x+1, x => x*2)(3) return?",
     "What does pipe() do?",
     ["Creates a pipe in plumbing", "Chains functions left-to-right", "Deletes functions", "Runs functions in parallel"],
     1, "Pipe chains functions: output of one becomes input of the next, left to right."),
]

for i, (title, expl, code, game, q, opts, correct, qexpl) in enumerate(ts_funcs):
    kp(5, "ts-functions", title, expl, code, game, q, opts, correct, qexpl)

# TypeScript Interfaces (Week 6)
ts_interfaces = [
    ("Mapped types",
     "Mapped types transform existing types by applying a transformation to each property.",
     "type Optional<T> = {\n    [K in keyof T]?: T[K];\n};\n\ntype User = { name: string; age: number; };\ntype PartialUser = Optional<User>;\n// { name?: string; age?: number; }",
     "Game: What does this produce?\ntype Readonly<T> = {\n    readonly [K in keyof T]: T[K];\n};\nReadonly<{x: number}>",
     "What does a mapped type do?",
     ["Creates a new type by transforming each property", "Maps coordinates", "Deletes properties", "Imports types"],
     1, "Mapped types iterate over keys of a type and transform each one."),
    ("Conditional types",
     "Conditional types create types based on conditions, like ternary operators for types.",
     "type IsString<T> = T extends string ? 'yes' : 'no';\n\ntype A = IsString<string>;  // 'yes'\ntype B = IsString<number>;  // 'no'\n\ntype ElementType<T> = T extends (infer E)[] ? E : never;\ntype N = ElementType<number[]>;  // number",
     "Game: What is IsString<boolean>?\ntype IsString<T> = T extends string ? 'yes' : 'no';",
     "What does a conditional type do?",
     ["Checks at runtime", "Creates types based on conditions at compile time", "Deletes types", "Imports modules"],
     1, "Conditional types use extends + ternary to create types based on conditions."),
    ("Utility types: Partial, Required, Pick, Omit",
     "TypeScript has built-in utility types that transform other types.",
     "type User = { name: string; age: number; email: string; };\n\ntype PartialUser = Partial<User>;     // all optional\ntype RequiredUser = Required<User>;   // all required\ntype NameOnly = Pick<User, 'name'>;   // { name: string }\ntype NoEmail = Omit<User, 'email'>;   // { name, age }",
     "Game: What does Pick<User, 'name' | 'age'> produce?",
     "What does Partial<T> do?",
     ["Makes all properties required", "Makes all properties optional", "Deletes all properties", "Renames properties"],
     1, "Partial<T> makes every property optional (?)."),
    ("Discriminated unions",
     "Discriminated unions use a common property to distinguish between union members.",
     "type Shape =\n    | { kind: 'circle'; radius: number }\n    | { kind: 'rectangle'; width: number; height: number };\n\nfunction area(shape: Shape): number {\n    switch (shape.kind) {\n        case 'circle':\n            return Math.PI * shape.radius ** 2;\n        case 'rectangle':\n            return shape.width * shape.height;\n    }\n}",
     "Game: After checking shape.kind === 'circle', what properties are available?\nA) radius\nB) width and height\nC) All of them",
     "What is a discriminated union?",
     ["A union with no common property", "A union that uses a common property to distinguish members", "A type with one option", "A deleted type"],
     1, "Discriminated unions use a literal type property (like 'kind') to narrow the union."),
]

for i, (title, expl, code, game, q, opts, correct, qexpl) in enumerate(ts_interfaces):
    kp(6, "ts-interfaces", title, expl, code, game, q, opts, correct, qexpl)

# TypeScript Async (Week 6)
ts_async = [
    ("Promises basics",
     "A Promise represents a future value. It can be pending, fulfilled, or rejected.",
     "const promise = new Promise<string>((resolve, reject) => {\n    setTimeout(() => resolve('Done!'), 1000);\n});\n\npromise.then(result => console.log(result)); // 'Done!'",
     "Game: What states can a Promise be in?\nA) pending, fulfilled, rejected\nB) start, middle, end\nC) open, closed",
     "What is a Promise?",
     ["A guarantee of quality", "A future value that may be available now, later, or never", "A function", "A variable"],
     1, "A Promise represents a value that may not be available yet."),
    ("async/await",
     "async/await is syntactic sugar for Promises. It makes async code look synchronous.",
     "async function fetchUser(): Promise<string> {\n    const response = await fetch('/api/user');\n    const data = await response.json();\n    return data.name;\n}\n\n// Equivalent to:\nfetchUser().then(name => console.log(name));",
     "Game: What does 'await' do?\nA) Blocks the thread\nB) Pauses until the Promise resolves\nC) Creates a new Promise",
     "What does 'await' do?",
     ["Blocks the entire program", "Pauses until the Promise resolves", "Creates a new Promise", "Deletes the Promise"],
     1, "await pauses execution until the Promise resolves, then returns the value."),
    ("Promise.all: wait for all",
     "Promise.all takes an array of Promises and resolves when ALL of them resolve.",
     "const results = await Promise.all([\n    fetch('/api/users'),\n    fetch('/api/posts'),\n    fetch('/api/comments'),\n]);\n// All three fetch at the same time!\n// Total time = longest request, not sum",
     "Game: If each fetch takes 1s, how long does Promise.all of 3 fetches take?\nA) 3 seconds\nB) 1 second\nC) 0 seconds",
     "What does Promise.all do?",
     ["Runs Promises one by one", "Waits for all Promises to resolve", "Takes the fastest result", "Cancels all Promises"],
     1, "Promise.all runs all Promises concurrently and waits for all to complete."),
    ("Promise.allSettled",
     "Unlike Promise.all, allSettled never rejects. It waits for all to settle (resolve or reject).",
     "const results = await Promise.allSettled([\n    fetch('/api/ok'),\n    fetch('/api/fail'), // This might fail\n]);\n\nresults.forEach(result => {\n    if (result.status === 'fulfilled') {\n        console.log('Success:', result.value);\n    } else {\n        console.log('Failed:', result.reason);\n    }\n});",
     "Game: Does Promise.allSettled reject if one Promise fails?\nA) Yes\nB) No, it always resolves with all results",
     "What is the difference between all and allSettled?",
     ["They are the same", "allSettled never rejects, it always resolves with results", "allSettled is faster", "allSettled only takes one Promise"],
     1, "Promise.allSettled waits for all to complete, regardless of success or failure."),
    ("AbortController",
     "AbortController lets you cancel async operations like fetch requests.",
     "const controller = new AbortController();\n\nfetch('/api/data', { signal: controller.signal })\n    .then(res => res.json())\n    .catch(err => {\n        if (err.name === 'AbortError') {\n            console.log('Request cancelled!');\n        }\n    });\n\n// Cancel after 5 seconds\nsetTimeout(() => controller.abort(), 5000);",
     "Game: How do you cancel a fetch request?\nA) fetch.cancel()\nB) Use AbortController\nC) You cannot cancel fetches",
     "How do you cancel a fetch request?",
     ["call .cancel()", "Use AbortController with a signal", "Close the browser", "Wait for timeout"],
     1, "AbortController provides a signal that, when aborted, cancels the fetch."),
]

for i, (title, expl, code, game, q, opts, correct, qexpl) in enumerate(ts_async):
    kp(6, "ts-async", title, expl, code, game, q, opts, correct, qexpl)

# TypeScript Modules (Week 6)
ts_modules = [
    ("ES modules: import/export",
     "ES modules are the standard way to share code between files in TypeScript.",
     "// math.ts\nexport function add(a: number, b: number) {\n    return a + b;\n}\nexport const PI = 3.14159;\n\n// main.ts\nimport { add, PI } from './math';\nconsole.log(add(2, 3));",
     "Game: How do you import 'add' from './math'?\nA) require('./math').add\nB) import { add } from './math'\nC) include add from './math'",
     "How do you export a function?",
     ["export function add(){}", "function add(){} export", "module.exports = add", "public function add()"],
     1, "Put 'export' before the function/const to make it available to other files."),
    ("Default exports",
     "A module can have one default export. Import it without braces.",
     "// Logger.ts\nexport default class Logger {\n    log(msg: string) { console.log(msg); }\n}\n\n// main.ts\nimport Logger from './Logger';\nconst logger = new Logger();",
     "Game: What is the difference?\nimport Logger from './Logger';\nimport { Logger } from './Logger';",
     "How do you import a default export?",
     ["import { X } from 'module'", "import X from 'module'", "require('module')", "include X from 'module'"],
     1, "Default exports use 'import X from ...' (no braces). Named exports use braces."),
    ("Dynamic import",
     "import() loads modules on demand, returning a Promise. Useful for code splitting.",
     "async function loadChart() {\n    const { Chart } = await import('./Chart');\n    const chart = new Chart();\n    chart.render();\n}\n\n// Only loads when called, not at startup!",
     "Game: When does dynamic import load the module?\nA) At startup\nB) When import() is called\nC) Never",
     "What is dynamic import?",
     ["import at the top of the file", "Loading modules on demand with import()", "Deleting modules", "Importing from the internet"],
     1, "Dynamic import() loads modules on demand, returning a Promise."),
    ("Barrel files (index.ts)",
     "Barrel files re-export from multiple modules for cleaner imports.",
     "// utils/index.ts\nexport { add, subtract } from './math';\nexport { formatDate } from './dates';\nexport { validate } from './validation';\n\n// main.ts - one clean import\nimport { add, formatDate, validate } from './utils';",
     "Game: What does a barrel file do?\nA) Stores data\nB) Re-exports from multiple modules for cleaner imports\nC) Deletes modules",
     "What is a barrel file?",
     ["A file that stores barrels", "An index.ts that re-exports from multiple modules", "A configuration file", "A test file"],
     1, "Barrel files aggregate exports for cleaner imports."),
]

for i, (title, expl, code, game, q, opts, correct, qexpl) in enumerate(ts_modules):
    kp(6, "ts-modules", title, expl, code, game, q, opts, correct, qexpl)

# TypeScript Decorators (Week 6)
ts_decorators = [
    ("What are decorators?",
     "Decorators are special declarations that can modify classes, methods, or properties at definition time.",
     "function Log(target: any, key: string) {\n    console.log(`Property ${key} was defined`);\n}\n\nclass User {\n    @Log\n    name: string = 'Alice';\n}",
     "Game: When does a decorator run?\nA) When you create an instance\nB) When the class is defined\nC) Never",
     "When do decorators execute?",
     ["When creating instances", "When the class/method is defined", "At runtime on every call", "Never"],
     1, "Decorators execute at class definition time, not at instantiation."),
    ("Class decorators",
     "A class decorator receives the constructor and can return a new one.",
     "function Sealed(constructor: Function) {\n    Object.seal(constructor);\n    Object.seal(constructor.prototype);\n}\n\n@Sealed\nclass User {\n    name: string = 'Alice';\n}",
     "Game: What does a class decorator receive?\nA) An instance\nB) The constructor function\nC) Nothing",
     "What does a class decorator receive?",
     ["An instance of the class", "The constructor function", "The class name", "Nothing"],
     1, "Class decorators receive the constructor function and can modify or replace it."),
    ("Method decorators",
     "Method decorators can modify, replace, or wrap method behavior.",
     "function Log(target: any, key: string, descriptor: PropertyDescriptor) {\n    const original = descriptor.value;\n    descriptor.value = function(...args: any[]) {\n        console.log(`Calling ${key} with`, args);\n        return original.apply(this, args);\n    };\n}\n\nclass Calculator {\n    @Log\n    add(a: number, b: number) { return a + b; }\n}",
     "Game: What can a method decorator do?\nA) Only log\nB) Modify, replace, or wrap the method\nC) Delete the method",
     "What can a method decorator do?",
     ["Only print messages", "Modify, replace, or wrap the method", "Delete the method", "Nothing"],
     1, "Method decorators receive the method descriptor and can modify its behavior."),
    ("Property decorators",
     "Property decorators can define metadata or modify property behavior.",
     "function Required(target: any, key: string) {\n    // Store metadata that this property is required\n    Reflect.defineMetadata('required', true, target, key);\n}\n\nclass User {\n    @Required\n    name: string = '';\n    email: string = '';\n}",
     "Game: What is a common use of property decorators?\nA) Deleting properties\nB) Adding validation rules or metadata\nC) Making properties public",
     "What is a property decorator used for?",
     ["Deleting properties", "Adding validation or metadata", "Creating new properties", "Importing modules"],
     1, "Property decorators commonly add validation rules or metadata to class properties."),
]

for i, (title, expl, code, game, q, opts, correct, qexpl) in enumerate(ts_decorators):
    kp(6, "ts-decorators", title, expl, code, game, q, opts, correct, qexpl)

# ============================================================
# WEEK 7-8: Design Patterns
# ============================================================

patterns = [
    ("Dependency Injection: what and why",
     "Instead of creating dependencies inside, pass them from outside. This makes code testable and flexible.",
     "# Without DI (rigid):\nclass UserService:\n    def __init__(self):\n        self.db = MySQLDatabase()  # Hardcoded!\n\n# With DI (flexible):\nclass UserService:\n    def __init__(self, db):\n        self.db = db  # Passed in!",
     "Game: Which is easier to test?\nA) class with new MySQLDatabase() inside\nB) class that receives db as a parameter",
     "What is Dependency Injection?",
     ["Creating dependencies inside a class", "Passing dependencies from outside", "A database pattern", "A loop pattern"],
     1, "DI passes dependencies from outside instead of creating them inside. Enables testing and flexibility."),
    ("DI in FastAPI",
     "FastAPI uses DI extensively. Declare dependencies as function parameters.",
     "# FastAPI DI pattern\ndef get_db():\n    db = Session()\n    try:\n        yield db\n    finally:\n        db.close()\n\n@app.get('/users')\ndef list_users(db = Depends(get_db)):\n    return db.query(User).all()",
     "Game: What does Depends() do in FastAPI?\nA) Creates a dependency\nB) Resolves and injects a dependency\nC) Deletes a dependency",
     "How does FastAPI resolve dependencies?",
     ["You call them manually", "It reads type hints and auto-injects", "Through config files", "Via environment variables"],
     1, "FastAPI inspects type hints and automatically resolves the dependency chain."),
    ("Middleware: intercepting requests",
     "Middleware sits between the request and response. It can modify, log, or reject requests.",
     "# Middleware pattern\nasync def auth_middleware(request, next):\n    token = request.headers.get('Authorization')\n    if not token:\n        return Response('Unauthorized', 401)\n    request.user = decode_token(token)\n    return await next(request)\n\n# Chain: request -> middleware -> handler -> response",
     "Game: Where does middleware sit?\nA) Inside the database\nB) Between request and handler\nC) After the response",
     "Where does middleware execute?",
     ["Inside the database", "Between the request and the handler", "After the response is sent", "Only on errors"],
     1, "Middleware intercepts requests before they reach the handler and can modify the response."),
    ("Builder: step-by-step construction",
     "Builder pattern constructs complex objects step by step. Each method returns 'this' for chaining.",
     "class QueryBuilder:\n    def __init__(self):\n        self._table = ''\n        self._where = []\n        self._limit = None\n    def table(self, name):\n        self._table = name\n        return self\n    def where(self, condition):\n        self._where.append(condition)\n        return self\n    def limit(self, n):\n        self._limit = n\n        return self\n    def build(self):\n        return f'SELECT * FROM {self._table} WHERE {\" AND \".join(self._where)} LIMIT {self._limit}'",
     "Game: What does .table('users').where('age > 18').limit(10).build() produce?",
     "Why use the Builder pattern?",
     ["To make code shorter", "To construct complex objects step by step with chaining", "To delete objects", "To import modules"],
     1, "Builder lets you construct complex objects step by step, with method chaining."),
    ("Strategy: interchangeable algorithms",
     "Strategy encapsulates algorithms behind a common interface, making them swappable at runtime.",
     "class Sorter:\n    def __init__(self, strategy):\n        self.strategy = strategy\n    def sort(self, data):\n        return self.strategy(data)\n\nbubble_sort = lambda data: sorted(data)  # simplified\nquick_sort = lambda data: sorted(data)   # simplified\n\nsorter = Sorter(bubble_sort)\nprint(sorter.sort([3, 1, 2]))\n\n# Swap strategy at runtime!\nsorter.strategy = quick_sort",
     "Game: How do you swap the algorithm at runtime?\nA) Rewrite the class\nB) Change the strategy object\nC) You cannot swap",
     "What does the Strategy pattern do?",
     ["Deletes algorithms", "Makes algorithms interchangeable at runtime", "Runs all algorithms", "Creates new algorithms"],
     1, "Strategy encapsulates algorithms behind an interface so they can be swapped at runtime."),
    ("Observer: event notification",
     "Observer pattern: when one object changes, all subscribers are notified.",
     "class EventEmitter:\n    def __init__(self):\n        self._listeners = {}\n    def on(self, event, callback):\n        self._listeners.setdefault(event, []).append(callback)\n    def emit(self, event, *args):\n        for cb in self._listeners.get(event, []):\n            cb(*args)\n\nemitter = EventEmitter()\nemitter.on('click', lambda: print('Clicked!'))\nemitter.emit('click')  # Clicked!",
     "Game: What happens when emit('click') is called?\nA) Nothing\nB) All listeners for 'click' are called\nC) The program exits",
     "What does the Observer pattern do?",
     ["Deletes events", "Notifies subscribers when something changes", "Creates loops", "Imports modules"],
     1, "Observer enables one-to-many notification: one object changes, many are notified."),
    ("Factory: creating objects",
     "Factory creates objects without specifying the exact class. The factory decides which class to use.",
     "class AnimalFactory:\n    @staticmethod\n    def create(animal_type):\n        if animal_type == 'dog':\n            return Dog()\n        elif animal_type == 'cat':\n            return Cat()\n        raise ValueError(f'Unknown: {animal_type}')\n\nanimal = AnimalFactory.create('dog')\nanimal.speak()  # Woof!",
     "Game: What does the Factory decide?\nA) How to delete objects\nB) Which class to instantiate\nC) How to sort objects",
     "What does a Factory do?",
     ["Deletes objects", "Creates objects without specifying the exact class", "Sorts objects", "Imports modules"],
     1, "Factory encapsulates object creation, letting subclasses decide what to instantiate."),
    ("Repository: data access abstraction",
     "Repository provides a collection-like interface for data access, hiding storage details.",
     "class UserRepository:\n    def __init__(self, db):\n        self.db = db\n    def find_by_id(self, id):\n        return self.db.query('SELECT * FROM users WHERE id = ?', [id])\n    def save(self, user):\n        self.db.execute('INSERT INTO users ...', user)\n    def delete(self, id):\n        self.db.execute('DELETE FROM users WHERE id = ?', [id])",
     "Game: Why use a Repository?\nA) To write SQL directly\nB) To hide database details from business logic\nC) To make code slower",
     "What does the Repository pattern hide?",
     ["The UI", "Data access details from business logic", "The network", "The file system"],
     1, "Repository abstracts data access so business logic doesn't know about the database."),
    ("Pipeline: sequential processing",
     "Pipeline chains processing stages. Output of one stage feeds into the next.",
     "class Pipeline:\n    def __init__(self):\n        self.stages = []\n    def add(self, fn):\n        self.stages.append(fn)\n        return self\n    def execute(self, data):\n        result = data\n        for stage in self.stages:\n            result = stage(result)\n        return result\n\npipe = Pipeline()\npipe.add(lambda x: x.strip())\npipe.add(lambda x: x.lower())\npipe.add(lambda x: x.replace(' ', '_'))\nprint(pipe.execute('  Hello World  '))  # hello_world",
     "Game: What does this pipeline produce?\npipe.add(x => x + 1).add(x => x * 2).execute(5)",
     "What does a Pipeline do?",
     ["Runs stages in parallel", "Chains stages: output of one feeds the next", "Deletes data", "Imports modules"],
     1, "Pipeline chains processing stages sequentially: input -> stage1 -> stage2 -> output."),
]

for i, (title, expl, code, game, q, opts, correct, qexpl) in enumerate(patterns):
    kp(7, "patterns", title, expl, code, game, q, opts, correct, qexpl)

# ============================================================
# WEEK 9-10: Python Projects
# ============================================================

py_projects = [
    ("FastAPI: what is it?",
     "FastAPI is a modern Python web framework. Async-first, type-safe, auto-generates API docs.",
     "from fastapi import FastAPI\napp = FastAPI()\n\n@app.get('/hello')\ndef hello(name: str = 'World'):\n    return {'message': f'Hello {name}!'}\n\n# Auto-generates docs at /docs",
     "Game: What URL shows auto-generated API docs?\nA) /api\nB) /docs\nC) /help",
     "Where does FastAPI show auto-generated docs?",
     ["/api", "/docs", "/help", "/swagger"],
     1, "FastAPI auto-generates interactive API docs at /docs (Swagger UI)."),
    ("FastAPI: path parameters",
     "Path parameters are parts of the URL that vary. Declare them in the function signature.",
     "@app.get('/users/{user_id}')\ndef get_user(user_id: int):\n    return {'user_id': user_id}\n\n# GET /users/42 -> {'user_id': 42}",
     "Game: What is user_id for GET /users/123?\nA) '123'\nB) 123 (int)\nC) /users/123",
     "How do you get a path parameter in FastAPI?",
     ["request.params['id']", "Declare it as a function parameter with type", "Use request.body", "Use environment variables"],
     1, "Path parameters are declared as function parameters with type hints."),
    ("FastAPI: query parameters",
     "Query parameters are after ? in the URL. They have defaults or are optional.",
     "@app.get('/search')\ndef search(q: str, limit: int = 10):\n    return {'query': q, 'limit': limit}\n\n# GET /search?q=python&limit=5",
     "Game: What is the limit for GET /search?q=test?\nA) 0\nB) 10 (default)\nC) None",
     "How do you set a default for a query parameter?",
     ["Use @default decorator", "Give the parameter a default value in the function signature", "Use a config file", "You cannot set defaults"],
     1, "Give the parameter a default value: limit: int = 10."),
    ("LangChain: what is it?",
     "LangChain is a framework for building LLM applications. It provides chains, agents, and RAG.",
     "from langchain.llms import OpenAI\nfrom langchain.chains import LLMChain\nfrom langchain.prompts import PromptTemplate\n\nprompt = PromptTemplate(template='Tell me about {topic}')\nchain = LLMChain(llm=OpenAI(), prompt=prompt)\nresult = chain.run(topic='Python')",
     "Game: What are the 3 main LangChain concepts?\nA) Chains, Agents, RAG\nB) Models, Views, Controllers\nC) Input, Process, Output",
     "What is LangChain?",
     ["A Python web framework", "A framework for building LLM applications", "A database", "A testing tool"],
     1, "LangChain provides building blocks for LLM apps: chains, agents, tools, and RAG."),
    ("Next.js: what is it?",
     "Next.js is a React framework with SSR, SSG, and the App Router. It is the standard for production React apps.",
     "// App Router: file-based routing\n// app/blog/[slug]/page.tsx -> /blog/:slug\n\nexport default async function BlogPost({ params }) {\n    const post = await getPost(params.slug);\n    return <article>{post.content}</article>;\n}",
     "Game: What does app/users/[id]/page.tsx map to?\nA) /users\nB) /users/:id\nC) /users/id",
     "What does Next.js App Router use for routing?",
     ["Configuration files", "The file system (file-based routing)", "A router library", "Manual registration"],
     1, "Next.js uses the file system as the router. app/blog/[slug]/page.tsx -> /blog/:slug."),
    ("tRPC: type-safe APIs",
     "tRPC provides end-to-end type safety: client calls server functions with full TypeScript types.",
     "// server/router.ts\nconst userRouter = router({\n    getById: publicProcedure\n        .input(z.object({ id: z.string() }))\n        .query(({ input }) => {\n            return db.user.findUnique({ where: { id: input.id } });\n        }),\n});\n\n// client: full type safety!\nconst user = await trpc.user.getById.query({ id: '123' });",
     "Game: What does tRPC eliminate?\nA) The need for a server\nB) Code generation for type-safe client calls\nC) TypeScript\nD) The database",
     "What does tRPC provide?",
     ["A REST API", "End-to-end type safety without code generation", "A database ORM", "A UI library"],
     1, "tRPC gives you end-to-end type safety: the client knows the server types without code generation."),
]

for i, (title, expl, code, game, q, opts, correct, qexpl) in enumerate(py_projects):
    kp(9, "projects", title, expl, code, game, q, opts, correct, qexpl)

# ============================================================
# WEEK 11-12: AI Mastery + Practice
# ============================================================

ai_mastery = [
    ("Prompt engineering basics",
     "Good prompts are clear, specific, and provide context. Bad prompts are vague.",
     "# Bad prompt:\n'Write code'\n\n# Good prompt:\n'Write a Python function that takes a list of\nnumbers and returns the average, handling empty lists.'",
     "Game: Which prompt is better?\nA) 'Do stuff'\nB) 'Write a function that validates email addresses using regex'",
     "What makes a good prompt?",
     ["Being as short as possible", "Being clear, specific, and providing context", "Using fancy words", "Being vague"],
     1, "Good prompts are clear, specific, and provide enough context for the AI to understand."),
    ("Chain-of-thought prompting",
     "Ask the AI to think step by step. This improves accuracy for complex problems.",
     "# Without chain-of-thought:\n'What is 23 * 47?'\n\n# With chain-of-thought:\n'Think step by step: What is 23 * 47?\nBreak it down: 23 * 40 = 920, 23 * 7 = 161\nThen add: 920 + 161 = 1081'",
     "Game: Which approach gives better results?\nA) Just ask the question\nB) Ask the AI to think step by step",
     "What is chain-of-thought prompting?",
     ["Writing very long prompts", "Asking the AI to show its reasoning step by step", "Using multiple models", "Prompting in a chain"],
     1, "Chain-of-thought asks the model to reason step-by-step, improving accuracy."),
    ("AI code review",
     "Use AI to review code for bugs, security issues, and performance problems.",
     "# Ask AI to review:\n'Review this function for:\n1. Potential bugs\n2. Security vulnerabilities\n3. Performance issues\n4. Edge cases\n\ndef process(data):\n    return eval(data)  # AI flags: eval() is dangerous!'",
     "Game: What should AI code review check?\nA) Only syntax\nB) Bugs, security, performance, edge cases\nC) Only formatting",
     "What should AI code review focus on?",
     ["Only style", "Bugs, security, performance, and edge cases", "Only variable names", "Only imports"],
     1, "AI review is most valuable for catching bugs, security holes, and edge cases."),
    ("AI-assisted architecture",
     "Use AI to explore design options and tradeoffs. You make the final decision.",
     "# Ask AI:\n'Compare these approaches for our API:\n1. REST with FastAPI\n2. GraphQL with Strawberry\n3. tRPC\n\nList pros/cons of each for our use case:\n- 3 frontend developers\n- Simple CRUD operations\n- Need real-time updates'",
     "Game: Who makes the final architecture decision?\nA) The AI\nB) You (the human)\nC) The framework",
     "Who should make architecture decisions?",
     ["The AI", "The human developer", "The framework", "The client"],
     1, "AI explores options and tradeoffs. Humans make the final judgment call."),
]

for i, (title, expl, code, game, q, opts, correct, qexpl) in enumerate(ai_mastery):
    kp(11, "ai-mastery", title, expl, code, game, q, opts, correct, qexpl)

practice = [
    ("Requirements: what to build",
     "Before writing code, understand what you are building. Write down requirements clearly.",
     "# Requirements for a todo app:\n1. Users can add tasks\n2. Users can mark tasks complete\n3. Users can delete tasks\n4. Tasks persist between sessions\n5. Users can filter by status",
     "Game: What is missing from these requirements?\n'Build a calculator'\nA) What operations?\nB) What UI?\nC) Both A and B",
     "Why write requirements before coding?",
     ["To waste time", "To understand what to build before building it", "Because the teacher said so", "To make the code longer"],
     1, "Requirements define what to build. Without them, you build the wrong thing."),
    ("Architecture: how parts connect",
     "Architecture defines how components connect. Good architecture makes code maintainable.",
     "# Simple architecture:\nFrontend (React) -> API (FastAPI) -> Database (SQLite)\n\n# Each layer has ONE job:\n# Frontend: display UI\n# API: business logic\n# Database: store data",
     "Game: What is the job of the API layer?\nA) Display UI\nB) Business logic\nC) Store data",
     "What does architecture define?",
     ["The color scheme", "How components connect and their responsibilities", "The file names", "The import order"],
     1, "Architecture defines how components connect and what each one is responsible for."),
    ("Testing: verify your code",
     "Tests verify that your code works correctly. Write tests alongside your code.",
     "def test_add():\n    assert add(2, 3) == 5\n    assert add(-1, 1) == 0\n    assert add(0, 0) == 0\n\ndef test_add_edge_cases():\n    assert add(0.1, 0.2) == pytest.approx(0.3)",
     "Game: What does this test verify?\ndef test_divide():\n    assert divide(10, 2) == 5\n    assert divide(0, 5) == 0",
     "Why write tests?",
     ["To make code longer", "To verify code works and catch regressions", "Because the teacher said so", "To slow down development"],
     1, "Tests verify correctness and catch regressions when you change code."),
    ("Deployment: getting it live",
     "Deployment makes your application available to users. Use Docker for consistent environments.",
     "# Dockerfile\nFROM python:3.11-slim\nWORKDIR /app\nCOPY requirements.txt .\nRUN pip install -r requirements.txt\nCOPY . .\nCMD ['uvicorn', 'main:app', '--host', '0.0.0.0']\n\n# Build and run:\n# docker build -t myapp .\n# docker run -p 8000:8000 myapp",
     "Game: What does Docker do?\nA) Writes code for you\nB) Creates consistent, reproducible environments\nC) Designs UI",
     "What does Docker provide?",
     ["A code editor", "Consistent, reproducible environments", "A database", "A programming language"],
     1, "Docker packages your app with all dependencies into a consistent environment."),
]

for i, (title, expl, code, game, q, opts, correct, qexpl) in enumerate(practice):
    kp(12, "practice", title, expl, code, game, q, opts, correct, qexpl)

# ============================================================
# Generate output
# ============================================================

def main():
    # Organize by week and module
    weeks = {}
    for kp_item in KNOWLEDGE_POINTS:
        week = kp_item["week"]
        module = kp_item["module"]
        if week not in weeks:
            weeks[week] = {}
        if module not in weeks[week]:
            weeks[week][module] = []
        weeks[week][module].append(kp_item)

    output = {
        "total_points": len(KNOWLEDGE_POINTS),
        "weeks": len(weeks),
        "points": KNOWLEDGE_POINTS,
        "by_week": weeks,
    }

    out_path = Path(__file__).parent / "data" / "knowledge_points.json"
    out_path.write_text(json.dumps(output, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Generated {len(KNOWLEDGE_POINTS)} knowledge points -> {out_path}")

    # Print summary
    for week, modules in sorted(weeks.items()):
        total = sum(len(v) for v in modules.values())
        print(f"  Week {week}: {total} points across {len(modules)} modules")

if __name__ == "__main__":
    main()
