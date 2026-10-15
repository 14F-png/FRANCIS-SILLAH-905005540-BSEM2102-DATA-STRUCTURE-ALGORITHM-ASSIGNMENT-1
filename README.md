# Stack-Based Expression Evaluator (DCOMP320)

Reads mathematical expressions from `input.txt`, evaluates each with a stack,
and writes the results to `output.txt`.

## How to run
```
python stack_evaluator.py
```
Optional: `python stack_evaluator.py my_input.txt my_output.txt`
Requires Python 3.8+. No external libraries.

## Input format
- One expression per line.
- Separator lines (only dashes, e.g. `-----`) sit between expressions.
- Supports `+ - * /`, parentheses, decimals and unary minus, e.g. `-(4 + 2)`.

## Output format
- One result per line, in the same order as the input.
- Separator lines are copied unchanged.
- Whole numbers print without decimals (`13`); others print as decimals (`3.5`).
- Invalid expressions print `Error: <reason>` instead of stopping the program.

## How it works
Two stacks (using the `Stack` class with push, pop, peek):
an operand stack and an operator stack (shunting-yard). Operators with higher
or equal precedence are applied first; `*` and `/` bind tighter than `+` and `-`;
parentheses force grouping.

## Assumptions and limitations
- No exponent or modulo operators.
- Blank lines are ignored.
- Division by zero and mismatched parentheses are reported as errors.
- Python floats are used, so very long decimals may show small rounding.