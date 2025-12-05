def parse_commands(input_text: str):
    """
    Parses a string of commands into a list of tuples, where each tuple contains
    a command character and an integer value.
    Args:
        input_text (str): A string containing commands, one per line. Each command
                          starts with a single character followed by an integer.
    Returns:
        list[tuple[str, int]]: A list of tuples, where each tuple contains a command
                               character (str) and an integer (int).
    Example:
        >>> input_text = "F10\\nN3\\nR90"
        >>> parse_commands(input_text)
        [('F', 10), ('N', 3), ('R', 90)]
        >>> input_text = "L270\\nS15"
        >>> parse_commands(input_text)
        [('L', 270), ('S', 15)]
        >>> input_text = "F10\\nN3\\nR90\\n"
        >>> parse_commands(input_text)
        [('F', 10), ('N', 3), ('R', 90)]
        >>> input_text = "L270\\nS15\\n"
        >>> parse_commands(input_text)
        [('L', 270), ('S', 15)]
        >>> input_text = "F10\\nN3\\nR90\\n   "
        >>> parse_commands(input_text)
        [('F', 10), ('N', 3), ('R', 90)]
        >>> input_text = "L270\\nS15\\n   "
        >>> parse_commands(input_text)
        [('L', 270), ('S', 15)]
    """
    str_commands = input_text.strip().splitlines()
    parser = lambda s: (s[0], int(s[1:]))

    return list(map(parser, str_commands))

def rotation(init_val: int, steps: int, direction: str) -> int:
    """
    Rotates a value within a circular range [MIN_VAL, MAX_VAL) by a given number of steps 
    in the specified direction ('L' for left, towards lower values, 'R' for right, towards higher values).

    The function ensures the result wraps around within the range [MIN_VAL, MAX_VAL). It also calculates
    the number of zero-crossings that occur during the rotation.

    Args:
        init_val (int): The initial value to rotate. Must be within the range [MIN_VAL, MAX_VAL).
        steps (int): The number of steps to rotate.
        direction (str): The direction of rotation. 'L' for left, 'R' for right.

    Returns:
        tuple[int, int]: A tuple containing:
            - The resulting value after rotation, constrained within the range [MIN_VAL, MAX_VAL).
            - The number of zero-crossings that occurred during the rotation.

    Raises:
        AssertionError: If the direction is not 'L' or 'R'.

    Examples:
        >>> rotation(10, 5, 'L')
        (5, 0)
        >>> rotation(10, 5, 'R')
        (15, 0)
        >>> rotation(95, 10, 'R')
        (5, 1)
        >>> rotation(5, 10, 'L')
        (95, 1)
        >>> rotation(0, 100, 'R')
        (0, 1)
        >>> rotation(0, 100, 'L')
        (0, 1)
        >>> rotation(10, 205, 'R')
        (15, 2)
        >>> rotation(95, 210, 'L')
        (85, 2)
    """

    MIN_VAL = 0
    MAX_VAL = 100
    # Such that val in [[MIN_VAL, MAX_VAL-1]]

    assert direction in ('L', 'R')
    d = int(direction == 'R') * 2 - 1

    new_dial_value = (init_val + d * steps) % MAX_VAL
    zero_crossings = abs((init_val + d * steps) // MAX_VAL) \
        + (new_dial_value == 0 and direction == 'L') \
        - (init_val == 0 and direction == 'L') # only for part 2

    return new_dial_value, zero_crossings


if __name__ == "__main__":
    import sys
    from tqdm import tqdm
    import doctest

    # Run docstring tests
    doctest.testmod()
    
    aoc_day1_part = int(sys.argv[1])
    assert aoc_day1_part in (1, 2), "Specify part 1 or 2 as first argument."

    # Parse input text into commands
    print("Parsing input...", end='')
    with open(sys.argv[2], 'r') as f:
        input_text = f.read()
    commands = parse_commands(input_text)
    print("Done.")

    print(f"{len(commands)} rotations to be executed on the dial.")

    # Run commands and track zero-ending rotations
    running_dial_value = 50
    password_cpt = 0
    pbar = tqdm(commands, desc="Processing commands",
                postfix={
                    "command": f"{'':>3s}",
                    "dial": f"{running_dial_value:>2d}",
                    "0-count": f"{password_cpt:>4d}"
                })
    for direction, steps in pbar:
        running_dial_value, zero_crossings = rotation(init_val=running_dial_value, steps=steps, direction=direction)
        
        if aoc_day1_part == 1:
            password_cpt += int(running_dial_value == 0)
        else:
            password_cpt += zero_crossings
        
        pbar.set_postfix({
            "command": f"{direction}{steps:>3d}",
            "dial": f"{running_dial_value:>2d}",
            "password-count": f"{password_cpt:>4d}"
        })

    print(f"Actual password: {password_cpt}")
