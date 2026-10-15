import re
import sys


class Stack:
    """A simple stack (LIFO) backed by a Python list."""

    def __init__(self):
        self._items = []

    def push(self, item):
        self._items.append(item)

    def pop(self):
        if self.is_empty():
            raise IndexError("pop from empty stack")
        return self._items.pop()

    def peek(self):
        if self.is_empty():
            raise IndexError("peek from empty stack")
        return self._items[-1]

    def is_empty(self):
        return len(self._items) == 0

    def size(self):
        return len(self._items)


PRECEDENCE = {"+": 1, "-": 1, "*": 2, "/": 2, "u-": 3}  # u- = unary minus
TOKEN_RE = re.compile(r"\s*(\d+\.?\d*|\.\d+|[-+*/()])")


def tokenize(expression):
    """Split an expression string into numbers, operators and parentheses."""
    tokens, pos = [], 0
    expression = expression.strip()
    while pos < len(expression):
        match = TOKEN_RE.match(expression, pos)
        if not match:
            raise ValueError(f"invalid character '{expression[pos]}'")
        tokens.append(match.group(1))
        pos = match.end()
        while pos < len(expression) and expression[pos].isspace():
            pos += 1
    return tokens


def apply_operator(operators, operands):
    """Pop one operator and its operand(s), compute, push the result."""
    op = operators.pop()
    if op == "(":
        raise ValueError("mismatched parentheses")
    if op == "u-":
        operands.push(-operands.pop())
        return
    if operands.size() < 2:
        raise ValueError("malformed expression")
    right, left = operands.pop(), operands.pop()
    if op == "+":
        operands.push(left + right)
    elif op == "-":
        operands.push(left - right)
    elif op == "*":
        operands.push(left * right)
    elif op == "/":
        if right == 0:
            raise ZeroDivisionError("division by zero")
        operands.push(left / right)


def evaluate(expression):
    """Evaluate an expression using an operand stack and an operator stack."""
    operands, operators = Stack(), Stack()
    prev = None  # previous token type: 'num', 'op', '(' or ')'

    for tok in tokenize(expression):
        if re.fullmatch(r"\d+\.?\d*|\.\d+", tok):
            if prev in ("num", ")"):
                raise ValueError("malformed expression")
            operands.push(float(tok))
            prev = "num"
        elif tok == "(":
            if prev in ("num", ")"):
                raise ValueError("malformed expression")
            operators.push("(")
            prev = "("
        elif tok == ")":
            if prev in (None, "op", "("):
                raise ValueError("malformed expression")
            while not operators.is_empty() and operators.peek() != "(":
                apply_operator(operators, operands)
            if operators.is_empty():
                raise ValueError("mismatched parentheses")
            operators.pop()  # discard "("
            prev = ")"
        else:  # + - * /
            if prev in (None, "op", "(") :
                if tok == "-":          # unary minus
                    operators.push("u-")
                    prev = "op"
                    continue
                raise ValueError("malformed expression")
            while (not operators.is_empty()
                   and operators.peek() != "("
                   and PRECEDENCE[operators.peek()] >= PRECEDENCE[tok]):
                apply_operator(operators, operands)
            operators.push(tok)
            prev = "op"

    if prev in (None, "op", "("):
        raise ValueError("malformed expression")
    while not operators.is_empty():
        apply_operator(operators, operands)
    if operands.size() != 1:
        raise ValueError("malformed expression")
    return operands.pop()


def format_result(value):
    """Show whole numbers without a decimal point."""
    if value == int(value):
        return str(int(value))
    return f"{value:.6f}".rstrip("0").rstrip(".")


def is_separator(line):
    """A separator is a line made only of dashes, e.g. -----"""
    return bool(re.fullmatch(r"-{2,}", line.strip()))


def process_file(input_path="input.txt", output_path="output.txt"):
    with open(input_path, "r", encoding="utf-8") as infile:
        lines = infile.read().splitlines()

    output_lines = []
    for line in lines:
        if not line.strip():
            continue                      # skip blank lines
        if is_separator(line):
            output_lines.append(line.strip())   # keep the same separator
            continue
        try:
            output_lines.append(format_result(evaluate(line)))
        except (ValueError, ZeroDivisionError, IndexError) as err:
            output_lines.append(f"Error: {err}")

    with open(output_path, "w", encoding="utf-8") as outfile:
        outfile.write("\n".join(output_lines) + "\n")


if __name__ == "__main__":
    in_file = sys.argv[1] if len(sys.argv) > 1 else "input.txt"
    out_file = sys.argv[2] if len(sys.argv) > 2 else "output.txt"
    process_file(in_file, out_file)
    print(f"Done. Results written to {out_file}")