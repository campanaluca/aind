assignments = []

rows = 'ABCDEFGHI'
cols = '123456789'


def cross(A, B):
    "Cross product of elements in A and elements in B."
    return [s + t for s in A for t in B]


boxes = cross(rows, cols)
row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC', 'DEF', 'GHI')
                for cs in ('123', '456', '789')]
unitlist = row_units + column_units + square_units
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s], [])) - set([s])) for s in boxes)


def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """

    # Don't waste memory appending actions that don't actually change any values
    if values[box] == value:
        return values

    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values


def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """
    for unit in unitlist:
        # create a dictonary with the box.value as key and the box.key as value
        twins = {}
        for box in unit:
            key = "".join(sorted(values[box]))
            if (key in twins):
                twins[key].append(box)
            else:
                twins[key] = [box]
        # list the twin values
        twin_values = [k for k in twins if len(k) == 2 and len(twins[k]) == 2]
        # eliminate the twin values
        for value in twin_values:
            for box in (set(unit) - set(twins[value])):
                assign_value(values, box, "".join(sorted(set(values[box]) - set(value))))
    return values


def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Args:
        grid(string) - A grid in string form.
    Returns:
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """
    assert len(grid) == 81
    return {boxes[x]: grid[x] if grid[x] != '.' else cols for x in range(81)}


def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    width = 1 + max(len(values[s]) for s in boxes)
    line = '+'.join(['-' * (width * 3)] * 3)
    for r in rows:
        print(''.join(values[r + c].center(width) + ('|' if c in '36' else '')
                      for c in cols))
        if (r in 'CF'):
            print(line)
    return


def eliminate(values):
    for k, v in values.items():
        if len(v) == 1:
            continue
        a = {values[x] for x in peers[k] if len(values[x]) == 1}
        assign_value(values, k, "".join(set(v) - a))
    return values


def only_choice(values):
    for unit in unitlist:
        for n in '123456789':
            occur = [box for box in unit if n in values[box]]
            if len(occur) == 1:
                assign_value(values, occur[0], n)
    return values


def reduce_puzzle(values):
    stalled = False
    while not stalled:
        # Check how many boxes have a determined value
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])

        # Your code here: Use the Eliminate Strategy
        values = eliminate(values)
        # Your code here: Use the Only Choice Strategy
        values = only_choice(values)
        # Check how many boxes have a determined value, to compare
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        # If no new values were added, stop the loop.
        stalled = solved_values_before == solved_values_after
        # Sanity check, return False if there is a box with zero available values:
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values


def search(values):
    # "Using depth-first search and propagation, create a search tree and solve the sudoku."
    # First, reduce the puzzle using the previous function
    values = reduce_puzzle(values)
    if values is False:
        return False
    if all(len(values[x]) == 1 for x in boxes):
        return values
    # Choose one of the unfilled squares with the fewest possibilities
    box = min(filter(lambda k: len(values[k]) > 1, values), key=lambda k: len(values[k]))    
    # Now use recursion to solve each one of the resulting sudokus, and if one returns a value (not False), return that answer!
    for digit in values[box]:
        temp = values.copy()
        temp[box] = digit
        solution = search(temp)
        if solution:
            return solution


def diagonal(func):
    def wrapper(*args, **kwargs):
        diag_units = [['A1', 'B2', 'C3', 'D4', 'E5', 'F6', 'G7', 'H8', 'I9'],
                      ['A9', 'B8', 'C7', 'D6', 'E5', 'F4', 'G3', 'H2', 'I1']]
        global unitlist, units, peers
        unitlist = row_units + column_units + square_units + diag_units
        units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
        peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)
        result = func(*args, **kwargs)
        unitlist = row_units + column_units + square_units
        units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
        peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)
        return result
    return wrapper


@diagonal
def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    return search(grid_values(grid))



if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(solve(diag_sudoku_grid))

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
