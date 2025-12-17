class Optimizer:
    def __init__(self, instructions):
        self.instructions = instructions
        self.labels = set()  # To track labels that have been used
        self.label_counter = 0  # For generating new labels if needed

    def constant_folding(self):
        optimized_instructions = []
        for instruction in self.instructions:
            if ":=" in instruction:
                var, expr = instruction.split(":=")
                expr = expr.strip()
                if expr.isdigit():
                    optimized_instructions.append(f"{var.strip()} := {expr}")
                else:
                    optimized_instructions.append(instruction)
            else:
                optimized_instructions.append(instruction)
        self.instructions = optimized_instructions

    def peephole_optimization(self):
        optimized_instructions = []
        skip_next = False
        for i in range(len(self.instructions) - 1):
            if skip_next:
                skip_next = False
                continue

            current = self.instructions[i]
            next_instr = self.instructions[i + 1]

            # Simplify redundant jumps
            if "goto" in current and "goto" in next_instr:
                if current == next_instr:
                    continue  # Remove redundant goto

            optimized_instructions.append(current)

            if i == len(self.instructions) - 2:
                optimized_instructions.append(next_instr)

        self.instructions = optimized_instructions

    def eliminate_dead_code(self):
        optimized_instructions = []
        used_variables = set()

        # First pass: identify all variables that are used
        for instruction in self.instructions:
            if ":=" in instruction:
                var, _ = instruction.split(":=")
                used_variables.add(var.strip())

        # Second pass: remove instructions with variables that are not used
        for instruction in self.instructions:
            if ":=" in instruction:
                var, _ = instruction.split(":=")
                if var.strip() not in used_variables:
                    continue
            optimized_instructions.append(instruction)

        self.instructions = optimized_instructions

    def remove_duplicate_labels(self):
        optimized_instructions = []
        seen_labels = set()

        for instruction in self.instructions:
            if ":" in instruction:  # It is a label
                label = instruction.split(":")[0]
                if label in seen_labels:
                    continue  # Skip this label if it was already used
                seen_labels.add(label)

            optimized_instructions.append(instruction)

        self.instructions = optimized_instructions

    def optimize(self):
        self.constant_folding()
        self.peephole_optimization()
        self.eliminate_dead_code()
        self.remove_duplicate_labels()
        return self.instructions  # Explicitly return the optimized code
