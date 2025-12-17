import sys
from lexer import lexer
from semantic_analyzer import SemanticAnalyzer
from ICG import IntermediateCodeGenerator
from Optimizer import Optimizer
from TargetCodeGenerator import TargetCodeGenerator  # Import the new TargetCodeGenerator
from Parse_Tree_Visualizer import generate_sorted_parse_tree  # Import the function

def main():
    # Initialize an empty string to store the code
    code = ""

    print("Please enter your code (type 'exit' to end input):")

    while True:
        # Read a line of code from the user
        line = input()

        # Check if the user typed 'exit'
        if line.lower() == "exit":
            break  # Exit the loop if 'exit' is typed

        # Append the line to the code string
        code += line + "\n"  # Add newline to preserve line structure

    # Step 1: Tokenize the code using the lexer
    tokens = list(lexer(code))
    
    # Step 2: Filter out unwanted tokens (NEWLINE, WHITESPACE)
    filtered_tokens = [(token.type, token.value) for token in tokens if token.type not in ["NEWLINE", "WHITESPACE"]]

    # Print tokens exactly as required
    print("Tokens:", filtered_tokens)

    # Step 3: Generate sorted parse tree (you can now call this after tokenizing)
    generate_sorted_parse_tree(filtered_tokens)  # Call the function to generate the parse tree

    # Step 4: Perform semantic analysis
    analyzer = SemanticAnalyzer()
    analyzer.analyze(filtered_tokens)
    errors = analyzer.get_errors()

    print("\nSemantic Analysis:")
    if errors:
        for error in errors:
            print(f"Error: {error}")
        return  # Exit if errors are found
    else:
        print("No errors found.")

    # Step 5: Generate intermediate code from the tokens
    icg = IntermediateCodeGenerator()
    var_name = None
    current_type = None
    i = 0  # Token index for manual iteration through tokens
    loop_start_label = icg.new_label()
    loop_end_label = icg.new_label()

    # Step 6: Process the tokens and generate intermediate code
    while i < len(filtered_tokens):
        token_type, token_value = filtered_tokens[i]

        if token_type == "KEYWORD" and token_value == "var":
            current_type = None  # Reset type for variable declarations
        elif token_type == "KEYWORD" and token_value in ("int", "float", "string"):
            current_type = token_value  # Set current type for variable declarations
        elif token_type == "ID":
            var_name = token_value  # Store variable name
        elif token_type == "ASSIGN":
            pass  # Handle assignment (handled below)
        elif token_type in ("NUMBER", "STRING"):
            # Handle value assignment (e.g., x = 5)
            if var_name:
                icg.generate_code_for_assignment(var_name, token_value)
                var_name = None  # Reset variable after assignment
        elif token_type == "OPERATOR":
            # Handle arithmetic operations (e.g., x + y)
            if var_name:
                operand1 = var_name
                operator = token_value
                i += 1  # Move to the next token (operand)
                if i < len(filtered_tokens):
                    operand2 = filtered_tokens[i][1]  # Get the operand
                    temp_var = icg.generate_code_for_arithmetic(operand1, operator, operand2)
                    var_name = temp_var  # Use the temporary variable result
        elif token_type == "KEYWORD" and token_value == "while":
            # Handle while loop
            icg.emit(f"{loop_start_label}:")  # Label for the start of the loop
            i += 1  # Move to condition tokens
            condition_operand1 = filtered_tokens[i][1]  # Left operand of condition
            i += 1
            operator = filtered_tokens[i][1]  # Comparison operator
            i += 1
            condition_operand2 = filtered_tokens[i][1]  # Right operand of condition
            icg.generate_code_for_comparison(condition_operand1, operator, condition_operand2, loop_end_label, loop_start_label)
        elif token_type == "DELIM" and token_value == "}":
            # Handle closing curly brace (end of while loop)
            icg.emit(f"goto {loop_start_label}")  # Jump back to the start of the loop
            icg.emit(f"{loop_end_label}:")  # Label for the end of the loop

        i += 1  # Move to the next token

    # Step 7: Print the generated intermediate code before optimization
    print("\nGenerated Intermediate Code (Before Optimization):")
    icg.print_instructions()

    # Step 8: Optimize the intermediate code
    optimizer = Optimizer(icg.instruction_list)
    optimized_code = optimizer.optimize()

    # Step 9: Output the optimized intermediate code
    print("\nOptimized Intermediate Code:")
    for instruction in optimized_code:
        print(instruction)

    # Step 10: Generate the target code from the optimized intermediate code
    target_code_generator = TargetCodeGenerator()
    target_code_generator.generate_target_code(optimized_code)

    # Step 11: Output the generated target code 
    print("\nGenerated Target Code:")
    target_code_generator.print_target_code()

if __name__ == "__main__":
    main()
