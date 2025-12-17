class IntermediateCodeGenerator:
    def __init__(self):
        self.instruction_list = []  # List to store intermediate code instructions
        self.label_count = 0  # Counter for generating unique labels
        self.temp_count = 0  # Counter for generating temporary variables

    def new_label(self):
        """
        Generates a new label for control flow (e.g., for loops or conditionals).
        """
        label = f"label_{self.label_count}"
        self.label_count += 1
        return label

    def get_new_temp(self):
        """
        Generates a new temporary variable (e.g., t1, t2, etc.).
        """
        temp = f"t{self.temp_count}"
        self.temp_count += 1
        return temp

    def emit(self, instruction):
        """
        Adds an instruction to the list of intermediate code.
        """
        self.instruction_list.append(instruction)

    def print_instructions(self):
        """
        Prints the list of intermediate code instructions.
        """
        for instruction in self.instruction_list:
            print(instruction)

    def generate_code_for_assignment(self, var, value):
        """
        Generate intermediate code for an assignment (e.g., var := value).
        """
        instruction = f"{var} := {value}"
        self.emit(instruction)

    def generate_code_for_arithmetic(self, operand1, operator, operand2):
        """
        Generate intermediate code for an arithmetic operation.
        e.g., a + b -> temp_var := a + b
        """
        temp_var = self.get_new_temp()
        instruction = f"{temp_var} := {operand1} {operator} {operand2}"
        self.emit(instruction)
        return temp_var

    def generate_code_for_comparison(self, operand1, operator, operand2, true_label, false_label):
        """
        Generate intermediate code for a comparison (e.g., a < b).
        If true, jump to true_label, else jump to false_label.
        """
        instruction = f"if {operand1} {operator} {operand2} goto {true_label}"
        self.emit(instruction)
        self.emit(f"goto {false_label}")

    def generate_code_for_conditional(self, condition, true_label, false_label):
        """
        Generate intermediate code for a conditional jump (if-else).
        """
        self.emit(f"if {condition} goto {true_label}")
        self.emit(f"goto {false_label}")

    def generate_code_for_loop(self, loop_condition, loop_body, loop_end_label):
        """
        Generate intermediate code for a while loop.
        The loop will continue while the condition is true.
        """
        start_label = self.new_label()
        self.emit(f"{start_label}:")  # Start label for the loop
        self.generate_code_for_comparison(loop_condition[0], loop_condition[1], loop_condition[2], loop_end_label, start_label)
        self.emit(f"{loop_body}:")  # Body of the loop
        self.emit(f"goto {start_label}")  # Jump back to the start of the loop

    def optimize(self):
        """
        A placeholder for optimization methods (e.g., constant folding, dead code elimination).
        """
        # For now, we just return the instructions as-is.
        return self.instruction_list
