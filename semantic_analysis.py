class SemanticAnalyzer:
    def __init__(self):
        self.symbol_table = {}  # To store variable names and their types and values

    def analyze(self, ast):
        attributed_ast = []
        for node in ast:
            if node['type'] == 'declaration':
                attributed_ast.append(self.analyze_declaration(node))
            elif node['type'] == 'if_statement':
                attributed_ast.append(self.analyze_if_statement(node))
            elif node['type'] == 'return_statement':
                attributed_ast.append(self.analyze_return_statement(node))
        return attributed_ast

    def analyze_declaration(self, node):
        var_type = node['var_type']
        var_name = node['var_name']
        expression = node['expression']

        # Evaluate the expression and determine its type and value
        expr_value, expr_type = self.evaluate_expression(expression)

        # Check type consistency
        if expr_type != var_type:
            raise Exception(f"Type Error: Cannot assign {expr_type} to {var_type} for variable '{var_name}'")

        # Store in symbol table
        self.symbol_table[var_name] = {'type': var_type, 'value': expr_value}

        # Add semantic attributes to the node
        node['expression']['evaluated_type'] = expr_type
        node['expression']['evaluated_value'] = expr_value

        return node

    def analyze_if_statement(self, node):
        condition = node['condition']
        body = node['body']
        else_body = node['else_body']

        # Evaluate the condition
        left_value, left_type = self.evaluate_expression(condition['left'])
        right_value, right_type = self.evaluate_expression(condition['right'])
        operator = condition['operator']

        # Check type consistency in condition
        if left_type != right_type:
            raise Exception(f"Type Error: Cannot compare {left_type} and {right_type}")

        # Evaluate the condition expression and store the result in the AST
        condition['evaluated_type'] = 'bool'
        condition['evaluated_value'] = self.evaluate_condition(left_value, right_value, operator)

        # Recursively analyze body and else_body, adding attributes to each node
        for i in range(len(body)):
            body[i] = self.analyze(body[i])

        if else_body:
            for i in range(len(else_body)):
                else_body[i] = self.analyze(else_body[i])

        return node

    def analyze_return_statement(self, node):
        expression = node['expression']
        expr_value, expr_type = self.evaluate_expression(expression)

        # Add semantic attributes to the return expression
        node['expression']['evaluated_type'] = expr_type
        node['expression']['evaluated_value'] = expr_value

        return node

    def evaluate_expression(self, expr):
        if expr['type'] == 'number':
            return expr['value'], 'int' if isinstance(expr['value'], int) else 'float'
        elif expr['type'] == 'identifier':
            var_name = expr['name']
            if var_name in self.symbol_table:
                var_info = self.symbol_table[var_name]
                return var_info['value'], var_info['type']
            else:
                raise Exception(f"Error: Undeclared variable '{var_name}'")
        elif expr['type'] == 'binary_operation':
            left_value, left_type = self.evaluate_expression(expr['left'])
            right_value, right_type = self.evaluate_expression(expr['right'])
            operator = expr['operator']

            # Check type compatibility for binary operations
            if left_type != right_type:
                raise Exception(f"Type Error: Cannot apply '{operator}' to {left_type} and {right_type}")

            # Perform the binary operation and return the result
            result = self.perform_operation(left_value, right_value, operator)
            return result, left_type
        else:
            raise Exception(f"Error: Unknown expression type '{expr['type']}'")

    def perform_operation(self, left_value, right_value, operator):
        if operator == '+':
            return left_value + right_value
        elif operator == '-':
            return left_value - right_value
        elif operator == '*':
            return left_value * right_value
        elif operator == '/':
            return left_value / right_value
        else:
            raise Exception(f"Error: Unsupported operator '{operator}'")

    def evaluate_condition(self, left_value, right_value, operator):
        if operator == '<':
            return left_value < right_value
        elif operator == '>':
            return left_value > right_value
        elif operator == '==':
            return left_value == right_value
        else:
            raise Exception(f"Error: Unsupported comparison operator '{operator}'")

if __name__ == "__main__":
    ast = [
    {'type': 'declaration', 'var_type': 'int', 'var_name': 'a', 'expression': {'type': 'number', 'value': 5}},
    {'type': 'declaration', 'var_type': 'int', 'var_name': 'b', 'expression': {'type': 'number', 'value': 10}},
    {'type': 'declaration', 'var_type': 'int', 'var_name': 'sum', 
     'expression': {'type': 'binary_operation', 'operator': '+', 
                    'left': {'type': 'identifier', 'name': 'a'}, 
                    'right': {'type': 'identifier', 'name': 'b'}}},
    {'type': 'return_statement', 'expression': {'type': 'identifier', 'name': 'sum'}}
    ]


    # Perform semantic analysis
    analyzer = SemanticAnalyzer()
    try:
        attributed_ast = analyzer.analyze(ast)
        print("Attributed AST:")
        print(attributed_ast)
    except Exception as e:
        print(f"Error: {e}")
