class TargetCodeGenerator:
    def __init__(self):
        self.target_code = []  # List to store the target code

    def emit(self, instruction):
        """
        Adds an instruction to the target code.
        """
        self.target_code.append(instruction)

    def generate_target_code(self, intermediate_code):
        """
        Generate target code (e.g., assembly) based on intermediate code.
        The intermediate code will typically consist of assignments, arithmetic operations, jumps, etc.
        """
        for instruction in intermediate_code:
            if ":=" in instruction:
                var, expr = instruction.split(":=")
                var = var.strip()
                expr = expr.strip()
                self.emit(f"mov {var}, {expr}")  # Example for assigning a value
            elif "if" in instruction:
                # Handle conditional jump
                condition = instruction.split("goto")[0].strip()
                label = instruction.split("goto")[1].strip()
                operand1, operator, operand2 = condition.split()[1], condition.split()[2], condition.split()[3]
                self.emit(f"cmp {operand1}, {operand2}")  # Compare operands
                self.emit(f"je {label}")  # Jump if equal
            elif "goto" in instruction:
                label = instruction.split()[1]
                self.emit(f"jmp {label}")  # Unconditional jump to label

    def print_target_code(self):
        """
        Print the generated target code.
        """
        for instruction in self.target_code:
            print(instruction)