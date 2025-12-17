import re
from collections import namedtuple

# Define the Token structure
Token = namedtuple('Token', ['type', 'value'])

# Define token patterns
token_specification = [
    ('KEYWORD',  r'\b(momo|int|float|var|if|else|while|function|return|print|def|input)\b'),
    ('NUMBER',   r'\d+(\.\d*)?'),
    ('ASSIGN',   r'='),
    ('ID',       r'[A-Za-z_][A-Za-z0-9_]*'),
    ('STRING',   r'"[^"\n]*"'),            
    ('OPERATOR', r'(==|!=|<=|>=|&&|\|\||[\+\-\*/<>\!])'),
    ('DELIM',    r'[;,\(\)\{\}]'),
    ('COMMENT',  r'#.*'),
    ('NEWLINE',  r'\n'),
    ('WHITESPACE', r'\s+'),
    ('MISMATCH', r'.'),
]

# Combine the patterns into a single regex
master_pattern = '|'.join(f'(?P<{pair[0]}>{pair[1]})' for pair in token_specification)

# Define the lexer function
def lexer(code):
    line_num = 1
    line_start = 0
    for match in re.finditer(master_pattern, code):
        kind = match.lastgroup
        value = match.group()

        # Debug output to see what the lexer is processing
        print(f"Token kind: {kind}, value: {repr(value)}")

        if kind in ('WHITESPACE', 'NEWLINE'):  # Ignore whitespace and newlines
            continue
        elif kind == 'MISMATCH':
            raise RuntimeError(f'Illegal character at line {line_num}, column {match.start() - line_start}')
        
        # Yield token as a named tuple
        yield Token(kind, value)

        if value == '\n':
            line_num += 1
            line_start = match.end()
