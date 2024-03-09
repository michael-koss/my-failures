from numbers import Number

"""
If someone asks you for a calculator, USE A STACK
"""

OP_LEVELS = {"^": 3, "*": 2, "/": 2, "+": 1, "-": 1}


def operate(left, symb, right) -> Number:
    match symb:
        case "^":
            return pow(left, right)
        case "*":
            return left * right
        case "/":
            return left / right
        case "+":
            return left + right
        case "-":
            return left - right
        case _:
            raise ValueError("Invalid op!")


def calculate(in_str: str) -> Number:
    """I don't think this is exactly my question, since it was over 5 years ago, but
    I may as well implement the calculator anyway.

    In Reverse Polish Notation, operators follow their operands.
    3 4 x 5 6 x + means
    (3 x 4) (5 x 6) +
    (12) + (30)
    42

    This algo just needs to build a stack and apply the last 2 items in the stack once
    an operator is introduced

    :param in_str: "3 4 x 5 6 x +"
    :return: (12 + 30 = 42)
    """
    split_str = in_str.split(" ")

    # Stack is a list of [num, num, num, ...]
    calc_stack = []
    for num_or_symb in split_str:
        if num_or_symb not in OP_LEVELS:
            # Put numbers on the stack
            calc_stack.append(int(num_or_symb))
            continue
        # Once we hit a symbol, pop off the numbers and go to town
        right = calc_stack.pop()
        left = calc_stack.pop()
        calc_stack.append(operate(left, num_or_symb, right))

    return calc_stack[0]


assert calculate("6 4 +") == 10
assert calculate("3 4 * 5 6 * +") == 42
assert calculate("3 4 2 * -") == -5
assert calculate("3 4 - 2 *") == -2
