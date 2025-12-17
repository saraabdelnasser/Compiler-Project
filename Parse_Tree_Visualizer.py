from lexer import lexer
from collections import namedtuple
from graphviz import Digraph


# Wrapper class for lexer to implement token() method
class LexerWrapper:
    def __init__(self, code):
        self.lexer_gen = lexer(code)  # Generator from lexer function

    def token(self):
        try:
            return next(self.lexer_gen)
        except StopIteration:
            return None  # Return None when there are no more tokens


def generate_sorted_parse_tree(tokens):

    dot = Digraph()

    # Helper to generate unique node names
    counter = 0

    def unique_node(label):
        nonlocal counter
        counter += 1
        return f"{label}_{counter}"

    # Root node
    root_node = unique_node("Root")
    dot.node(root_node, "Root")

    # Separate tokens into sections
    declarations = []
    assignments = []
    operations = []

    for token in tokens:
        if token[0] == "KEYWORD" and token[1] == "var":
            declarations.append(token)
        elif token[0] in {"ID", "ASSIGN", "NUMBER"}:
            assignments.append(token)
        elif token[0] in {"ID", "OPERATOR", "NUMBER"}:
            operations.append(token)

    # Add Declarations to the tree
    declare_node = unique_node("Declarations")
    dot.node(declare_node, "Declarations")
    dot.edge(root_node, declare_node)

    for token in declarations:
        if token[0] == "KEYWORD" and token[1] == "var":
            var_node = unique_node(f"Declare_{token[1]}")
            dot.node(var_node, f"Declare: {token[1]}")
            dot.edge(declare_node, var_node)

    # Add Assignments to the tree
    assign_node = unique_node("Assignments")
    dot.node(assign_node, "Assignments")
    dot.edge(root_node, assign_node)

    for token in assignments:
        if token[0] == "ID":
            id_node = unique_node(f"ID_{token[1]}")
            dot.node(id_node, f"ID: {token[1]}")
            dot.edge(assign_node, id_node)
        elif token[0] == "ASSIGN":
            assign_op_node = unique_node("AssignOp")
            dot.node(assign_op_node, "Assign Operation")
            dot.edge(assign_node, assign_op_node)
        elif token[0] == "NUMBER":
            num_node = unique_node(f"Num_{token[1]}")
            dot.node(num_node, f"Number: {token[1]}")
            dot.edge(assign_node, num_node)

    # Add Operations to the tree
    operations_node = unique_node("Operations")
    dot.node(operations_node, "Operations")
    dot.edge(root_node, operations_node)

    for token in operations:
        if token[0] == "ID":
            id_node = unique_node(f"ID_{token[1]}")
            dot.node(id_node, f"ID: {token[1]}")
            dot.edge(operations_node, id_node)
        elif token[0] == "OPERATOR":
            operator_node = unique_node(f"Operator_{token[1]}")
            dot.node(operator_node, f"Operator: {token[1]}")
            dot.edge(operations_node, operator_node)
        elif token[0] == "NUMBER":
            num_node = unique_node(f"Num_{token[1]}")
            dot.node(num_node, f"Number: {token[1]}")
            dot.edge(operations_node, num_node)

    # Generate the sorted parse tree
    dot.render("sorted_parse_tree", format="png", cleanup=True)
    print("Sorted parse tree generated as sorted_parse_tree.png")


def main():
    code = """
    var a;
    var b;
    a=5;
    b=10;
    if a == 5 {
        print a;
    } else {
        while b < 10 {
            print b;
            b = b + 1;
        }
    }
    """

    # Use LexerWrapper to get tokens
    lexer_wrapper = LexerWrapper(code)
    tokens = []
    token = lexer_wrapper.token()
    while token:
        tokens.append((token.type, token.value))
        token = lexer_wrapper.token()

    print("\nTokens: ", tokens)  # Cleaner token output

    generate_sorted_parse_tree(tokens)


if __name__ == "__main__":
    main()
