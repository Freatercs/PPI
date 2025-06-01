class Calculator:
    """Калькулятор с поддержкой ОПН (обратной польской нотации)"""

    def __init__(self):
        self.precedence = {'+': 1, '-': 1, '*': 2, '/': 2, '^': 3}

    def _is_number(self, token):
        """Проверяет, является ли токен числом (целым или дробным)"""
        try:
            float(token)
            return True
        except ValueError:
            return False

    def _validate_expression(self, expression):
        """Проверяет корректность выражения перед вычислением"""
        if not expression.strip():
            raise ValueError("Пустое выражение")

        # Проверка на последовательные операторы
        prev_char = None
        for char in expression:
            if char in '+-*/^' and prev_char in '+-*/^':
                raise ValueError("Два оператора подряд")
            prev_char = char if char != ' ' else prev_char

    def infix_to_rpn(self, expression):
        """Преобразует инфиксную запись в ОПН"""
        self._validate_expression(expression)
        output = []
        operator_stack = []
        i = 0

        while i < len(expression):
            char = expression[i]

            if char == ' ':
                i += 1
                continue

            if char.isdigit() or char == '.':
                num = ''
                while i < len(expression) and (expression[i].isdigit() or expression[i] == '.'):
                    num += expression[i]
                    i += 1
                output.append(num)
                continue

            elif char in self.precedence:
                while (operator_stack and operator_stack[-1] != '(' and
                       self.precedence[operator_stack[-1]] >= self.precedence[char]):
                    output.append(operator_stack.pop())
                operator_stack.append(char)

            elif char == '(':
                operator_stack.append(char)

            elif char == ')':
                while operator_stack and operator_stack[-1] != '(':
                    output.append(operator_stack.pop())
                if not operator_stack:
                    raise ValueError("Несбалансированные скобки")
                operator_stack.pop()  # Удаляем '('

            i += 1

        while operator_stack:
            if operator_stack[-1] == '(':
                raise ValueError("Несбалансированные скобки")
            output.append(operator_stack.pop())

        return output

    def evaluate_rpn(self, rpn):
        """Вычисляет выражение в ОПН"""
        stack = []

        for token in rpn:
            if self._is_number(token):
                stack.append(float(token))
            else:
                if len(stack) < 2:
                    raise ValueError("Недостаточно операндов для оператора")
                b = stack.pop()
                a = stack.pop()
                if token == '+':
                    stack.append(a + b)
                elif token == '-':
                    stack.append(a - b)
                elif token == '*':
                    stack.append(a * b)
                elif token == '/':
                    if b == 0:
                        raise ZeroDivisionError("Деление на ноль")
                    stack.append(a / b)
                elif token == '^':
                    stack.append(a ** b)

        if len(stack) != 1:
            raise ValueError("Некорректное выражение")
        return stack[0]

    def calculate(self, expression):
        """Основной метод для вычисления выражения"""
        try:
            rpn = self.infix_to_rpn(expression)
            return self.evaluate_rpn(rpn)
        except (ValueError, ZeroDivisionError) as e:
            raise ValueError(f"Ошибка вычисления: {str(e)}")
