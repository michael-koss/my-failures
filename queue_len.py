# Your server processes a queue of messages, one message per time-step
# Each element in the queue has a wait time
# If t >= wait[i], the message expires and is immediately removed from the queue
# You start at t=0
# 1 <= len(wait) <= 1e5
# 1 <= elem(wait) <= 1e5
# What is the length of the wait queue at each timestep?

"""
Example:  A queue of [2, 1, 3, 1, 2, 7]
At t=0, there are 6 elements in the queue
At t=1, you've processed '2', both '1's have expired, so you're left with [3, 2, 7]
At t=2, you've processed '3', '2' expired, so you're left with [7]
At t=3, the queue is empty after processing 7

The output should be [6, 3, 1, 0]
"""

from collections import Counter


def queue_lengths(wait: list[int]):
    """Too stressful during the test, this one is actually quite simple when stepping
    away. Each number in the queue contributes 1 to each slot in the solution up to
    its size, minus 1 because they expire _at_ time t.
    In the example above, '7' contributes 1 to each slot from 0 to 6,
    the 2 in front of it contributes 1 to slots 0 and 1, the 1 contributes to slot 0, etc

    The counterbalance is that it only contributes _until we process it_. For example,
    the 7 is at the front of the queue at t=2, meaning it will actually only contribute
    to slots 0, 1, and 2.

    So all we have to do is add 1 to each spot between 0 and min(time_examined, num-1)
    for each number.

    Example: [2, 1, 3, 1, 2, 7]
    Front of queue at t= [0, 1, 1, 2, 2, 2] (expired numbers will still be analyzed but
    time is not advanced due to them not actually getting to be processed)
    slots: [0, 0, 0, 0]

    [item, front of queue t, min(time_examined, num-1), slots after applying 1s]
    [2, 0, 0, [1, 0, 0, 0]]
    [1, 1, 0, [2, 0, 0, 0]]  # expired
    [3, 1, 1, [3, 1, 0, 0]]
    [1, 2, 0, [4, 1, 0, 0]]  # expired
    [2, 2, 1, [5, 2, 0 ,0]]  # expired
    [7, 2, 2, [6, 3, 1, 0]]
    """
    # Construct the min(t_e, num - 1) array
    working_arr = []
    time = 0
    for num in wait:
        working_arr.append(min(time, num - 1))
        if time < num:
            time += 1
    # Rearrange array into dict[add_num, number of times found in working]
    # Example above is {0: 3, 1: 2, 2: 1}
    working_dict = Counter(working_arr)
    # Note that soln[0] = len(working_arr)
    # soln[1] = soln[0] - working_dict[0] (ie all the sums minus those that went exclusively to 0)
    # soln[2] = soln[0] - wd[0] - wd[1] (ie all sums, except ones going to 0, 1)
    # because every +1 going to "2" for example, also goes to 1 and 0
    solution = [len(wait)]
    for i in range(1, max(working_dict.keys()) + 1):
        solution.append(solution[i - 1] - working_dict[i - 1])
    solution.append(0)
    return solution


assert queue_lengths([2, 1, 3, 1, 2, 7]) == [6, 3, 1, 0]
assert queue_lengths([4, 1, 1, 1, 1]) == [5, 0]
assert queue_lengths([1, 2, 3, 2, 1]) == [5, 3, 1, 0]
