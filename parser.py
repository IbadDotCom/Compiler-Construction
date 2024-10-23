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
            token_value = self.current_token
            self.advance()
            return token_value
        else:
            raise SyntaxError(
                f"Syntax error at line {self.current_token[2]}: Expected {expected_type}, got {self.current_token}"
            )

    def parse_program(self):
        """Parse a program, which is a sequence of statements, and return the AST."""
        ast = []
        while self.current_token:
            ast.append(self.parse_statement())
        return ast

    def parse_statement(self):
        """Parse a single statement and return the corresponding AST node."""
        if self.current_token[0] == 'KEYWORD':
            if self.current_token[1] in ('int', 'float'):
                return self.parse_declaration()
            elif self.current_token[1] == 'if':
                return self.parse_if_statement()
            elif self.current_token[1] == 'return':
                return self.parse_return_statement()
            else:
                raise SyntaxError(
                    f"Unexpected keyword {self.current_token[1]} at line {self.current_token[2]}"
                )
        elif self.current_token[0] == 'IDENTIFIER':
            return self.parse_assignment()
        else:
            raise SyntaxError(
                f"Unexpected token {self.current_token} at line {self.current_token[2]}"
            )

    def parse_declaration(self):
        """Parse a variable declaration and return the AST node."""
        var_type = self.consume('KEYWORD')  # int or float
        var_name = self.consume('IDENTIFIER')  # variable name
        self.consume('OPERATOR')  # =
        expression = self.parse_expression()  # right-hand side expression
        self.consume('SEMICOLON')  # ;
        return {
            'type': 'declaration',
            'var_type': var_type[1],
            'var_name': var_name[1],
            'expression': expression
        }

    def parse_assignment(self):
        """Parse an assignment statement and return the AST node."""
        var_name = self.consume('IDENTIFIER')  # variable name
        self.consume('OPERATOR')  # =
        expression = self.parse_expression()  # right-hand side expression
        self.consume('SEMICOLON')  # ;
        return {
            'type': 'assignment',
            'var_name': var_name[1],
            'expression': expression
        }

    def parse_if_statement(self):
        """Parse an if statement and return the AST node."""
        self.consume('KEYWORD')  # if
        self.consume('PAREN')    # (
        condition = self.parse_expression()  # condition
        self.consume('PAREN')    # )
        body = self.parse_block()  # block of code

        else_body = None
        if self.current_token and self.current_token[0] == 'KEYWORD' and self.current_token[1] == 'else':
            self.consume('KEYWORD')  # else
            else_body = self.parse_block()  # else block

        return {
            'type': 'if_statement',
            'condition': condition,
            'body': body,
            'else_body': else_body
        }

    def parse_return_statement(self):
        """Parse a return statement and return the AST node."""
        self.consume('KEYWORD')  # return
        expression = self.parse_expression()  # return value
        self.consume('SEMICOLON')  # ;
        return {
            'type': 'return_statement',
            'expression': expression
        }

    def parse_block(self):
        """Parse a block of code (enclosed in curly braces) and return the AST node."""
        self.consume('BRACE')  # {
        block = []
        while self.current_token and self.current_token[0] != 'BRACE':
            block.append(self.parse_statement())  # inner statements
        self.consume('BRACE')  # }
        return block

    def parse_expression(self):
        """Parse an expression, including comparison operators."""
        left = self.parse_arithmetic_expression()
        while self.current_token and self.current_token[0] == 'OPERATOR' and self.current_token[1] in ('<', '>', '<=', '>=', '==', '!='):
            operator = self.consume('OPERATOR')
            right = self.parse_arithmetic_expression()
            left = {
                'type': 'binary_operation',
                'operator': operator[1],
                'left': left,
                'right': right
            }
        return left

    def parse_arithmetic_expression(self):
        """Parse an arithmetic expression and return the corresponding AST node."""
        left = self.parse_term()
        while self.current_token and self.current_token[0] == 'OPERATOR' and self.current_token[1] in ('+', '-'):
            operator = self.consume('OPERATOR')  # + or -
            right = self.parse_term()
            left = {
                'type': 'binary_operation',
                'operator': operator[1],
                'left': left,
                'right': right
            }
        return left

    def parse_term(self):
        """Parse a term and return the corresponding AST node."""
        left = self.parse_factor()
        while self.current_token and self.current_token[0] == 'OPERATOR' and self.current_token[1] in ('*', '/'):
            operator = self.consume('OPERATOR')  # * or /
            right = self.parse_factor()
            left = {
                'type': 'binary_operation',
                'operator': operator[1],
                'left': left,
                'right': right
            }
        return left

    def parse_factor(self):
        """Parse a factor and return the corresponding AST node."""
        if self.current_token[0] == 'NUMBER':
            number = self.consume('NUMBER')
            return {'type': 'number', 'value': float(number[1])}
        elif self.current_token[0] == 'IDENTIFIER':
            identifier = self.consume('IDENTIFIER')
            return {'type': 'identifier', 'name': identifier[1]}
        elif self.current_token[0] == 'PAREN' and self.current_token[1] == '(':
            self.consume('PAREN')  # (
            expression = self.parse_expression()
            self.consume('PAREN')  # )
            return expression
        else:
            raise SyntaxError(
                f"Unexpected token {self.current_token} at line {self.current_token[2]}"
            )
        
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

    # Syntax Analysis
    parser = SyntaxAnalyzer(tokens)
    ast = parser.parse_program()
    print(ast)
