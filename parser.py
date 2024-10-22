from lexer import LexicalAnalyzer

class SyntaxAnalyzer:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.current_token = self.tokens[self.pos] if self.tokens else None

    def advance(self):
        """Move to the next token."""
        self.pos += 1
        if self.pos < len(self.tokens):
            self.current_token = self.tokens[self.pos]
        else:
            self.current_token = None

    def consume(self, expected_type):
        """Consume a token if it matches the expected type."""
        if self.current_token and self.current_token[0] == expected_type:
            self.advance()
        else:
            token = self.current_token[1] if self.current_token else None
            line_number = self.current_token[2] if self.current_token else 'unknown'
            raise SyntaxError(f"Syntax error at line {line_number}: Expected {expected_type}, got {token}")

    def parse_program(self):
        """Parse a program, which is a sequence of statements."""
        while self.current_token:
            self.parse_statement()

    def parse_statement(self):
        """Parse a single statement."""
        if self.current_token[0] == 'KEYWORD':
            if self.current_token[1] in ('int', 'float'):
                self.parse_declaration()
            elif self.current_token[1] == 'if':
                self.parse_if_statement()
            elif self.current_token[1] == 'return':
                self.parse_return_statement()
            else:
                line_number = self.current_token[2]
                raise SyntaxError(f"Unexpected keyword '{self.current_token[1]}' at line {line_number}")
        elif self.current_token[0] == 'IDENTIFIER':
            self.parse_assignment()
        else:
            line_number = self.current_token[2]
            raise SyntaxError(f"Unexpected token '{self.current_token[1]}' at line {line_number}")

    def parse_declaration(self):
        """Parse a variable declaration."""
        self.consume('KEYWORD')  # int or float
        self.consume('IDENTIFIER')  # variable name
        self.consume('OPERATOR')  # =
        self.parse_expression()  # right-hand side expression
        self.consume('SEMICOLON')  # ;

    def parse_assignment(self):
        """Parse an assignment statement."""
        self.consume('IDENTIFIER')  # variable name
        self.consume('OPERATOR')  # =
        self.parse_expression()  # right-hand side expression
        self.consume('SEMICOLON')  # ;

    def parse_if_statement(self):
        """Parse an if statement."""
        self.consume('KEYWORD')  # if
        self.consume('PAREN')  # (
        self.parse_expression()  # condition
        self.consume('PAREN')  # )
        self.parse_block()  # block of code
        if self.current_token and self.current_token[0] == 'KEYWORD' and self.current_token[1] == 'else':
            self.consume('KEYWORD')  # else
            self.parse_block()  # else block

    def parse_return_statement(self):
        """Parse a return statement."""
        self.consume('KEYWORD')  # return
        self.parse_expression()  # return value
        self.consume('SEMICOLON')  # ;

    def parse_block(self):
        """Parse a block of code (enclosed in curly braces)."""
        self.consume('BRACE')  # {
        while self.current_token and self.current_token[0] != 'BRACE':
            self.parse_statement()  # inner statements
        self.consume('BRACE')  # }

    def parse_expression(self):
        """Parse an expression, including comparison operators."""
        self.parse_term()
        # Add support for comparison operators like <, >, <=, >=, ==, !=
        while self.current_token and self.current_token[0] == 'OPERATOR' and self.current_token[1] in ('+', '-', '<', '>', '<=', '>=', '==', '!='):
            self.consume('OPERATOR')  # comparison or arithmetic operator
            self.parse_term()

    def parse_term(self):
        """Parse a term."""
        self.parse_factor()
        while self.current_token and self.current_token[0] == 'OPERATOR' and self.current_token[1] in ('*', '/'):
            self.consume('OPERATOR')  # * or /
            self.parse_factor()

    def parse_factor(self):
        """Parse a factor (NUMBER, IDENTIFIER, or an expression in parentheses)."""
        if self.current_token[0] == 'NUMBER':
            self.consume('NUMBER')
        elif self.current_token[0] == 'IDENTIFIER':
            self.consume('IDENTIFIER')
        elif self.current_token[0] == 'PAREN':
            self.consume('PAREN')  # (
            self.parse_expression()
            self.consume('PAREN')  # )
        else:
            line_number = self.current_token[2]
            raise SyntaxError(f"Unexpected token '{self.current_token[1]}' at line {line_number}")

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

    # Lexical Analysis
    lexer = LexicalAnalyzer(source_code)
    tokens = lexer.tokenize()
    # print("Tokens:", tokens)

    # Syntax Analysis
    parser = SyntaxAnalyzer(tokens)
    parser.parse_program()

    print("Parsing completed successfully!")
