from decimal import Decimal

from calc.core.errors import CalcSyntaxError, CalcMathError


class Token:
    def __init__(self, kind, value):
        # kind: "NUMBER", "OP", "LPAREN", "RPAREN"
        # value: actual text like "12.3", "+", etc
        self.kind = kind
        self.value = value

# Defining pemdas operator rules
BINARY_OPS = {"+", "-", "*", "/"}
UNARY_NEG = "NEGATIVE"

# Higher number = higher precedence
PRECEDENCE = {
    UNARY_NEG: 3, # unary minus is highest
    "*": 2,
    "/": 2,
    "+": 1,
    "-": 1,
}

# entry point for actual evaluation 
def eval_expr(expr):
    # evaluattes a math expression string and returns a Decimal
    tokens = tokenize(expr)
    postfix = convert_to_postfix(tokens)
    return eval_postfix(postfix)


# tokenization process
def tokenize(expr):
    expr = expr.strip()
    if expr == "":
        raise CalcSyntaxError("Empty expression")

    tokens = []
    i = 0

    while i < len(expr):
        char = expr[i]

        if char.isspace():
            i += 1
            continue

        if char in BINARY_OPS:
            tokens.append(Token("OP", char))
            i += 1
            continue

        if char == "(":
            tokens.append(Token("LPAREN", char))
            i += 1
            continue

        if char == ")":
            tokens.append(Token("RPAREN", char))
            i += 1
            continue

        if char.isdigit() or char == ".":
            number_str, i = read_number(expr, i)
            validate_number(number_str)
            tokens.append(Token("NUMBER", number_str))
            continue

        raise CalcSyntaxError("Unexpected chararacter: " + repr(char))

    return tokens


def read_number(expr, start_index):
    # reads a number from a string starting at start_index

    i = start_index
    decimal_count = 0

    if expr[i] == ".":
        decimal_count = 1

    i += 1
    while i < len(expr) and (expr[i].isdigit() or expr[i] == "."):
        if expr[i] == ".": # for duplicate decimal points
            decimal_count += 1
            if decimal_count > 1:
                raise CalcSyntaxError(
                    "Invalid number near: " + expr[start_index:i+1]
                )
        i += 1

    return expr[start_index:i], i


def validate_number(num_str):
    if num_str == ".":
        raise CalcSyntaxError("Invalid number '.'")
    try:
        Decimal(num_str) # tries to conver to python recognized decimal
    except Exception:
        raise CalcSyntaxError("Invalid number: " + num_str)


def convert_to_postfix(tokens):
    # convert infix tokens into postfix tokens using shunting yard algorithm

    output = [] # final postfix result
    op_stack = [] # operators waiting on stack for turn
    prev_token = None # previous token processed (for unary minus detection)

    for token in tokens:

        # numbers go straight to output stack
        if token.kind == "NUMBER":
            output.append(token)
            prev_token = token
            continue

        # '(' blocks operator popping
        if token.kind == "LPAREN":
            op_stack.append(token) # push '(' onto operator stack
            prev_token = token
            continue

        # ')' pops all operators until matching '('
        if token.kind == "RPAREN":
            while op_stack and op_stack[-1].kind != "LPAREN":
                output.append(op_stack.pop())

            if not op_stack: # no matching '(' found
                raise CalcSyntaxError("Mismatchared parentheses")

            op_stack.pop()  # remove '(' from operator stack
            prev_token = token
            continue

        # operators defined as: +, -, *, /
        if token.kind == "OP":
            next_operator = token.value

            # convert '-' to unary NEG if it is one
            if next_operator == "-" and is_unary_minus(prev_token):
                next_operator = UNARY_NEG

            # pop operators that should run before this one
            while op_stack and op_stack[-1].kind == "OP":
                top_op = op_stack[-1].value

                # if it is higher precedence, run it first
                if PRECEDENCE[top_op] > PRECEDENCE[next_operator]:
                    output.append(op_stack.pop())
                    continue

                # if it is same precedence and not unary, pop
                if PRECEDENCE[top_op] == PRECEDENCE[next_operator] and next_operator != UNARY_NEG:
                    output.append(op_stack.pop())
                    continue

                break

            op_stack.append(Token("OP", next_operator))
            prev_token = token
            continue

        raise CalcSyntaxError("Unknown token type")

    # pop remaining operators
    while op_stack:
        top = op_stack.pop()
        if top.kind == "LPAREN":
            raise CalcSyntaxError("Mismatchared parentheses")
        output.append(top)

    return output


def is_unary_minus(prev_token):
    # determines if '-' is unary based on previous token
    if prev_token is None:
        return True
    if prev_token.kind == "OP":
        return True
    if prev_token.kind == "LPAREN":
        return True
    return False


# postfix evaluation
def eval_postfix(rpn_tokens):
    stack = []

    for token in rpn_tokens:

        if token.kind == "NUMBER":
            stack.append(Decimal(token.value))
            continue

        if token.kind != "OP":
            raise CalcSyntaxError("Invalid token in RPN")

        if token.value == UNARY_NEG:
            if not stack:
                raise CalcSyntaxError("Unary '-' missing operand")
            stack.append(-stack.pop())
            continue

        # binary operators
        if len(stack) < 2:
            raise CalcSyntaxError(
                "Operator '" + token.value + "' missing operand(s)"
            )

        b = stack.pop()
        a = stack.pop()

        if token.value == "+":
            stack.append(a + b)
        elif token.value == "-":
            stack.append(a - b)
        elif token.value == "*":
            stack.append(a * b)
        elif token.value == "/":
            if b == 0:
                raise CalcMathError("Division by zero")
            stack.append(a / b)
        else:
            raise CalcSyntaxError("Unknown operator: " + token.value)

    if len(stack) != 1:
        raise CalcSyntaxError("Malformed expression")

    return stack[0]
