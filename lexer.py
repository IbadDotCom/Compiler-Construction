import re

# Define token types
TOKENS = [
    ('KEYWORD', r'\b(if|else|while|return|int|float)\b'),   # Keywords
    ('IDENTIFIER', r'\b[a-zA-Z_][a-zA-Z0-9_]*\b'),          # Identifiers
    ('NUMBER', r'\b\d+(\.\d+)?\b'),                         # Integer or float numbers
    ('OPERATOR', r'[+\-*/=<>!]'),                           # Operators
    ('PAREN', r'[()]'),                                     # Parentheses
    ('BRACE', r'[\{\}]'),                                   # Braces
    ('SEMICOLON', r';'),                                    # Semicolon
    ('WHITESPACE', r'\s+'),                                 # Whitespace (to be ignored)
    ('UNKNOWN', r'.'),                                      # Unknown characters (fallback)
]

# Lexical Analyzer
class LexicalAnalyzer:
    def __init__(self, source_code):
        self.source_code = source_code.lstrip()
        self.tokens = []
        self.current_line = 1

    def tokenize(self):
        position = 0
        while position < len(self.source_code):
            match_found = False

            if self.source_code[position] == '\n':
                self.current_line += 1
                position += 1
                continue

            for token_type, pattern in TOKENS:
                regex = re.compile(pattern)
                match = regex.match(self.source_code, position)
                if match:
                    lexeme = match.group(0)
                    if token_type != 'WHITESPACE':
                        self.tokens.append((token_type, lexeme, self.current_line))
                    position = match.end()
                    match_found = True
                    break

            if not match_found:
                raise SyntaxError(f"Illegal character '{self.source_code[position]}' at line {self.current_line}, position {position}")
        
        return self.tokens

if __name__ == '__main__':
    source_code = '''
    int x = 10;
    float y = 20.5;
    if (x < y) {
        return x;
    } else {
        return y;
    }
    '''
    
    lexer = LexicalAnalyzer(source_code)
    tokens = lexer.tokenize()
    print(tokens)
