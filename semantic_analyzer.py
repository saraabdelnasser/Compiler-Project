from lexer import lexer
from symbol_table import SymbolTable

class SemanticAnalyzer:
    def __init__(self):
        self.symbol_table = SymbolTable()
        self.errors = []
        self.state = "initial"

    def analyze(self, tokens):
        current_type = None
        var_name = None

        print("=== Debug: Starting Semantic Analysis ===")

        for token_type, token_value in tokens:
            try:
                print(f"=== Debug: Processing Node: ({token_type}, {token_value}) ===")
                if self.state == "initial":
                    if token_value == "var":
                        self.state = "declaration"
                    elif token_value == "if":
                        self.state = "if_condition"
                    elif token_value == "while":
                        self.state = "while_condition"
                    elif token_value == "print" or token_value == "input":
                        self.state = "output"
                    elif token_type == "ID":
                        var_name = token_value  # Assign variable name directly
                    elif token_value == "=":
                        self.state = "assignment"
                    # Add further rules for syntax or type-checking here
            except Exception as e:
                print(f"Error occurred during semantic analysis: {e}")
                continue

    def get_errors(self):
        # Return the list of semantic errors
        return self.errors
