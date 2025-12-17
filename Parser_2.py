from graphviz import Digraph
from lexer import lexer

# AST Node
class Node:
    def __init__(self, node_type, children=None, value=None):
        self.node_type = node_type
        self.value = value
        self.children = children or []

    def __str__(self):
        return f"{self.node_type}: {self.value or ''}"

    def add_child(self, child):
        self.children.append(child)

    def render(self, graph=None, parent_name=None):
        if graph is None:
            graph = Digraph('AST')
        # Create a node for the current node
        node_name = f"{id(self)}"
        graph.node(node_name, label=self.node_type)
        # Create edges to its children
        if parent_name:
            graph.edge(parent_name, node_name)
        for child in self.children:
            child.render(graph, node_name)
        return graph

    def generate_code(self):
        """ Recursively generates code from the AST. """
        if self.node_type == 'var_decl':
            return f"var {self.children[0].value};"
        elif self.node_type == 'assign':
            var_name = self.children[0].value
            expr_code = self.children[1].generate_code()
            return f"{var_name} = {expr_code};"
        elif self.node_type == 'number':
            return str(self.value)
        elif self.node_type == 'id':
            return self.value
        elif self.node_type == 'if':
            condition_code = self.children[0].generate_code()
            then_code = "\n".join([stmt.generate_code() for stmt in self.children[1]])
            if len(self.children) > 2:
                else_code = "\n".join([stmt.generate_code() for stmt in self.children[2]])
                return f"if ({condition_code}) {{\n{then_code}\n}} else {{\n{else_code}\n}}"
            return f"if ({condition_code}) {{\n{then_code}\n}}"
        elif self.node_type == 'while':
            condition_code = self.children[0].generate_code()
            body_code = "\n".join([stmt.generate_code() for stmt in self.children[1]])
            return f"while ({condition_code}) {{\n{body_code}\n}}"
        elif self.node_type == 'function_def':
            func_name = self.children[0].value
            params_code = ", ".join([param.value for param in self.children[1].children])
            body_code = "\n".join([stmt.generate_code() for stmt in self.children[2]])
            return f"function {func_name}({params_code}) {{\n{body_code}\n}}"
        elif self.node_type == 'function_call':
            func_name = self.children[0].value
            args_code = ", ".join([arg.generate_code() for arg in self.children[1:]])
            return f"{func_name}({args_code})"
        elif self.node_type == 'print' or self.node_type == 'input':
            expr_code = self.children[0].generate_code()
            return f"{self.node_type}({expr_code});"
        elif self.node_type in {'+', '-', '*', '/', '>', '<', '==', '!='}:
            left_code = self.children[0].generate_code()
            right_code = self.children[1].generate_code()
            return f"({left_code} {self.node_type} {right_code})"
        else:
            raise ValueError(f"Unknown node type: {self.node_type}")

class Parser:
    def __init__(self, tokens):
        self.tokens = iter(tokens)
        self.current_token = None
        self.next_token()

    def next_token(self):
        try:
            self.current_token = next(self.tokens)
        except StopIteration:
            self.current_token = None

    def expect(self, token_type, value=None):
        if self.current_token and self.current_token.type == token_type and (value is None or self.current_token.value == value):
            token_value = self.current_token.value
            self.next_token()
            return token_value
        raise SyntaxError(f"Expected {token_type} {value or ''}, got {self.current_token}")

    def parse_program(self):
        return self.parse_stmt_list()

    def parse_stmt_list(self):
        stmts = []
        while self.current_token and (self.current_token.type != 'DELIM' or self.current_token.value != '}'):
            stmts.append(self.parse_stmt())
        return stmts

    def parse_stmt(self):
        if self.current_token.type == 'KEYWORD' and self.current_token.value == 'var':
            return self.parse_var_decl()
        elif self.current_token.type == 'ID':
            return self.parse_assignment_or_call()
        elif self.current_token.type == 'KEYWORD' and self.current_token.value == 'if':
            return self.parse_if_stmt()
        elif self.current_token.type == 'KEYWORD' and self.current_token.value == 'while':
            return self.parse_while_stmt()
        elif self.current_token.type == 'KEYWORD' and self.current_token.value == 'print':
            return self.parse_io_stmt()
        else:
            raise SyntaxError(f"Unexpected token: {self.current_token}")

    def parse_var_decl(self):
        """ Parses a variable declaration like 'var x;' """
        self.expect('KEYWORD', 'var')
        var_name = self.expect('ID')
        self.expect('DELIM', ';')
        return Node("var_decl", [Node("id", [Node(var_name)])])

    def parse_assignment_or_call(self):
        id_name = self.expect('ID')
        if self.current_token.type == 'ASSIGN':
            self.next_token()
            expr = self.parse_expr()
            self.expect('DELIM', ';')
            return Node("assign", [Node("id", [Node(id_name)]), expr])
        elif self.current_token.type == 'DELIM' and self.current_token.value == '(':
            return self.parse_function_call(Node(id_name))
        else:
            raise SyntaxError(f"Unexpected token: {self.current_token}")

    def parse_expr(self):
        left = self.parse_term()
        while self.current_token and self.current_token.type == 'OPERATOR' and self.current_token.value in ('+', '-', '*', '/', '>', '<', '==', '!='):
            operator = self.current_token.value
            self.next_token()
            right = self.parse_term()
            left = Node(operator, [left, right])
        return left

    def parse_term(self):
        factor = self.parse_factor()
        while self.current_token and self.current_token.type == 'OPERATOR' and self.current_token.value in {'*', '/', '&&'}:
            op = self.current_token.value
            self.next_token()
            factor = Node(op, [factor, self.parse_factor()])
        return factor

    def parse_factor(self):
        if self.current_token.type == 'NUMBER':
            value = self.expect('NUMBER')
            return Node("number", [Node(value)])
        elif self.current_token.type == 'ID':
            value = self.expect('ID')
            return Node("id", [Node(value)])
        elif self.current_token.type == 'DELIM' and self.current_token.value == '(':
            self.next_token()
            expr = self.parse_expr()
            self.expect('DELIM', ')')
            return expr
        else:
            raise SyntaxError(f"Unexpected token in factor: {self.current_token}")

    def parse_if_stmt(self):
        self.expect('KEYWORD', 'if')
        self.expect('DELIM', '(')
        condition = self.parse_expr()
        self.expect('DELIM', ')')
        self.expect('DELIM', '{')
        then_branch = self.parse_stmt_list()
        self.expect('DELIM', '}')
        else_branch = None
        if self.current_token and self.current_token.type == 'KEYWORD' and self.current_token.value == 'else':
            self.next_token()
            self.expect('DELIM', '{')
            else_branch = self.parse_stmt_list()
            self.expect('DELIM', '}')
        if else_branch:
            return Node("if", [condition, then_branch, else_branch])
        return Node("if", [condition, then_branch])

    def parse_while_stmt(self):
        self.expect('KEYWORD', 'while')
        self.expect('DELIM', '(')
        condition = self.parse_expr()
        self.expect('DELIM', ')')
        self.expect('DELIM', '{')
        body = self.parse_stmt_list()
        self.expect('DELIM', '}')
        return Node("while", [condition, body])

    def parse_io_stmt(self):
        io_keyword = self.expect('KEYWORD', 'print')
        self.expect('DELIM', '(')
        expr = self.parse_expr()
        self.expect('DELIM', ')')
        self.expect('DELIM', ';')
        return Node(io_keyword, [expr])

# Example usage
if __name__ == "__main__":
    code = """
    var a;
    var b;
    a = 5;
    b = 10;
    if (a + b > 10) {
        print(a);
    } else {
        print(b);
    }
    """

    # Tokenize the code
    tokens = lexer(code)
    
    # Initialize the parser with the tokens
    parser = Parser(tokens)
    
    try:
        # Parse the program and generate the AST
        parse_tree = parser.parse_program()

        # Print the generated code from the AST
        print("Generated Code:")
        for stmt in parse_tree:
            print(stmt.generate_code())

        # Render the AST using Graphviz
        if parse_tree:
            ast_graph = parse_tree[0].render()  # Assuming parse_tree returns a list of nodes
            ast_graph.render('parse_tree', format='png', cleanup=True)
            print("AST visualization saved as 'parse_tree.png'")

    except SyntaxError as e:
        print(f"Syntax Error: {e}")
