# MiniLang Compiler 🧠⚙️

A **complete compiler implementation** for a simple programming language called **MiniLang**, written in **Python**.  
This project follows the classical compiler design pipeline and is developed as a **course project**.

---

## 📌 Project Overview

The MiniLang Compiler processes source code through **five main compiler phases**:

1. **Lexical Analysis** – Converts source code into tokens
2. **Syntax Analysis** – Validates grammar and builds a parse tree
3. **Semantic Analysis** – Ensures logical correctness using a symbol table
4. **Intermediate Code Generation (ICG)** – Produces three-address code
5. **Optimization & Target Code Generation** – Improves and translates code to target form

Each phase is implemented in a **separate Python module** for clarity and modularity.

---

## 🗂️ Project Structure

```
MiniLang-Compiler/
│── main.py
│── lexer.py
│── Parser_2.py
│── semantic_analyzer.py
│── symbol_table.py
│── ICG.py
│── Optimizer.py
│── TargetCodeGenerator.py
│── Parse_Tree_Visualizer.py
│── sorted_parse_tree.png
│── README.md
```

---

## 🧩 File Descriptions

### `main.py`
- Entry point of the compiler
- Controls the execution flow of all compiler phases

### `lexer.py`
- Performs lexical analysis
- Converts source code into tokens using regular expressions

### `Parser_2.py`
- Implements syntax analysis
- Validates grammar rules and constructs the parse tree

### `Parse_Tree_Visualizer.py`
- Generates a visual representation of the parse tree
- Outputs `sorted_parse_tree.png`

### `symbol_table.py`
- Manages the symbol table
- Stores variable names, types, and scope information

### `semantic_analyzer.py`
- Performs semantic checks
- Detects undeclared variables, type mismatches, and scope errors

### `ICG.py`
- Generates intermediate code (Three Address Code)

### `Optimizer.py`
- Applies code optimization techniques
- Includes constant folding and dead code elimination

### `TargetCodeGenerator.py`
- Converts optimized intermediate code into target-level code

---

## ▶️ How to Run the Compiler

### Requirements
- Python 3.x

### Execution

```bash
python main.py
```

Make sure all files are in the same directory.


