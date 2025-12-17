class SymbolTable:
    def __init__(self):
        self.symbols = {}

    def declare(self, var_name):
        if var_name not in self.symbols:
            self.symbols[var_name] = {'type': None, 'initialized': False}

    def assign(self, var_name, var_type):
        if var_name in self.symbols:
            self.symbols[var_name]['initialized'] = True  # Mark as initialized
            self.symbols[var_name]['type'] = var_type  # Store the type
        else:
            raise RuntimeError(f"Variable '{var_name}' not declared.")

    def is_initialized(self, var_name):
        return self.symbols.get(var_name, {}).get('initialized', False)

    def get_type(self, var_name):
        return self.symbols.get(var_name, {}).get('type', None)
