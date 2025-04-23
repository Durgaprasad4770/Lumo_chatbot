from flask import Flask, render_template, request, jsonify
import os
import google.generativeai as genai
import re
from dotenv import load_dotenv

app = Flask(__name__)

# Load API key from .env file
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Gemini model
model = genai.GenerativeModel("gemini-1.5-pro-latest")

# Valid programming keywords
VALID_KEYWORDS = [
    # Languages
    "c", "c++", "python", "java", "javascript", "html", "css", "sql", "bash","cpp",

    # Programming Concepts
    "oop", "object-oriented", "class", "object", "function", "method", "variable", "loop",
    "for loop", "while loop", "do while", "if", "else", "switch", "case", "operator",
    "recursion", "lambda", "closure", "inheritance", "polymorphism", "encapsulation", "abstraction",
    "constructor", "destructor", "pointer", "reference", "null", "exception", "error", "try", "catch",
    "interface", "implementation", "overload", "override", "stack overflow", "stack", "queue", "deque",

    # Data Structures & Algorithms
    "array", "linked list", "doubly linked list", "stack", "queue", "hashmap", "map", "set", "tree",
    "binary tree", "binary search tree", "graph", "heap", "priority queue", "sorting", "bubble sort",
    "merge sort", "quick sort", "binary search", "linear search", "hashing", "trie", "segment tree",

    # Memory & Compilation
    "memory", "heap", "stack memory", "pointer", "malloc", "calloc", "free", "garbage collection",
    "compile", "compiler", "interpreter", "runtime", "build", "linker", "segmentation fault",

    # Git & Tools
    "git", "github", "commit", "push", "pull", "merge", "branch", "clone", "fork",

    # Miscellaneous
    "syntax", "debug", "debugger", "IDE", "terminal", "shell", "command", "program", "programming",
    "code", "coding", "algorithm", "data structure", "example", "explain", "definition", "usage", "implementation"

]


def is_prompt_valid(prompt):
    prompt = prompt.lower()
    for keyword in VALID_KEYWORDS:
        if re.search(rf'\b{re.escape(keyword)}\b', prompt):
            return True
    return False

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    prompt = data.get("message", "")  # <- fix is here
    
    if not is_prompt_valid(prompt):
        return jsonify({"reply": "This prompt is out of scope."})

    try:
        response = model.generate_content(prompt)
        return jsonify({"reply": response.text})
    except Exception as e:
        print("Error:", e)
        return jsonify({"reply": "API Error."})

if __name__ == "__main__":
    app.run(debug=True)
