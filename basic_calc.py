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
    """The core of this algorithm is that if the next operation is lower priority
    than the last(s), do the previous ones until no longer true.

    Ex. 1: 1 + 2 * 20; in this case, we do the ops in reverse order because they're
    constantly increasing in priority

    Ex. 2: 1 + 2 * 3^2 / 9; we traverse until we hit ^2, then we do ^2, unwind to do * 2,
    then continue to do / 9, and finish off with +1.

    We can implement this idea with a stack, where we put in numbers and operations until
    the lower priority condition is hit, at which point we pop off the stack and do the
    ops until we can continue

    :param in_str: "1 + 2 * 20"
    :return: 21
    """
    split_str = in_str.split(" ")
    working_split = []
    # Convert ints to working numbers
    for i in range(len(split_str)):
        if i % 2 == 0:
            working_split.append(int(split_str[i]))
        else:
            working_split.append(split_str[i])

    # Stack is a list of [num, op, num, op, ...]
    calc_stack = [working_split.pop(0)]
    calc_stack.append(working_split.pop(0))

    for num_or_symb in working_split:
        if not isinstance(num_or_symb, str):
            # Put numbers on the stack
            calc_stack.append(num_or_symb)
            continue
        while (
            len(calc_stack) > 2 and OP_LEVELS[calc_stack[-2]] > OP_LEVELS[num_or_symb]
        ):
            # Now we unwind the stack until the next operation is at least as high
            # priority as the current one
            right = calc_stack.pop()
            symb = calc_stack.pop()
            left = calc_stack.pop()
            calc_stack.append(operate(left, symb, right))
        # Put the actual symbol onto the stack to continue
        calc_stack.append(num_or_symb)

    # Do the final operation(s)
    while len(calc_stack) > 1:
        right = calc_stack.pop()
        symb = calc_stack.pop()
        left = calc_stack.pop()
        calc_stack.append(operate(left, symb, right))
    return calc_stack[0]


assert calculate("1 + 2 * 10") == 21
assert calculate("3 * 5 ^ 2 + 7 - 2 / 10") == 81.8
assert calculate("3 * 5 ^ 2 + 7") == 82
assert calculate("1 + 2 * 3 ^ 2 / 9") == 3
