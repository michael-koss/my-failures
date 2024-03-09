from numbers import Number

"""
If someone asks you for a calculator, USE A STACK
"""

OP_LEVELS = {"^": 3, "*": 2, "/": 2, "+": 1, "-": 1, "(": 0, ")": 0}


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

################# Let's do the reverse reverse! ########################


def reverse_calc(in_str: str) -> str:
    """Given an input string "6 + 4", convert it to the RPN format "6 4 +"

    Note: Should take parentheses into account, just to make it harder on myself.

    Soln: Just like the basic calculator, except instead of doing the calculation when
    we unwind the stack, we just put it into a string
    """
    # Don't have to worry about making ints, since we're not doing the actual calculation
    split_str = in_str.split(" ")
    working_stack = []
    symbol_stack = []
    final_str = ""

    for num_symb in split_str:
        if num_symb not in OP_LEVELS:
            final_str += num_symb + " "
            continue
        symbol_stack.append(num_symb)
        while (
            len(symbol_stack) > 1
            and OP_LEVELS[symbol_stack[-1]] < OP_LEVELS[symbol_stack[-2]]
        ):
            final_str += symbol_stack.pop() + " "

    # Add last missing symbols


"""What are the commonalities here? Ignoring parentheses.
1. If symbol order increases, add the number to the command and save the symbol for later. 
2. Once symbol order decreases, add all symbols then carry on

If parentheses, do the usual until the end of the paren, at which point you _must_
unwind the stack until the opening paren
"""
assert reverse_calc("6 + 4") == "6 4 +"
assert reverse_calc("3 * 4 + 5 * 6") == "3 4 * 5 6 * +"
assert reverse_calc("3 + 4 ^ 5 * 6 / 7") == "3 4 5 ^ 6 7 / * +"
assert reverse_calc("3 - 4 * 2") == "3 4 2 * -"
assert reverse_calc("( 3 - 4 ) * 2") == "3 4 - 2 *"
assert reverse_calc("( ( 3 - 4 ) ^ 2 ) * 2") == "3 4 - 2 ^ 2 *"
assert reverse_calc("( ( 3 - 4 ) ^ ( 1 * 3 ) ) * 2") == "3 4 - 1 3 * ^ 2 *"
