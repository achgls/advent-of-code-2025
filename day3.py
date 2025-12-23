def parse_battery_banks(input_text: str):
    """
    Parse a string of battery bank charge levels into a list of lists of integers.

    Each line in the input string represents a battery bank, and each digit in the line
    represents a joltage rating of a battery.

    Args:
        input_text (str): A string where each line contains single-digit integers
                          representing charge levels of a battery bank.

    Returns:
        list[list[int]]: A list of lists, where each inner list contains integers
                         representing the joltage ratings of the batteries in a bank.

    Examples:
        >>> input_text = "123456789"
        >>> parse_battery_banks(input_text)
        [[1, 2, 3, 4, 5, 6, 7, 8, 9]]
    """
    return [list(map(int, line.strip())) for line in input_text.strip().splitlines()]

def max_joltage(bank: list[int], number_of_batteries: int = 12):
    """
    Scans the list `number_of_batteries` times, each time starting the scan just after the index of the maximum value found in the previous scan.
    Returns the maximum possible joltage a bank can produce by combining `number_of_batteries` batteries according to the rules given in AoC 2025 Day 3.

    Args:
        bank (list[int]): A list of integers representing the joltage ratings of the batteries in a bank.

    Returns:
        int: the highest possible joltage a bank can produce by combining `number_of_batteries` batteries.
    
    Examples:
        >>> max_joltage([1, 2, 3, 4, 5])
        45
        >>> max_joltage([5, 4, 3, 2, 1])
        54
        >>> max_joltage([3, 1, 4, 1, 5])
        45
        >>> max_joltage_part2([9, 8, 7, 6, 5, 4, 3, 2, 1, 1, 1, 1, 1, 1, 1])
        987654321111
        >>> max_joltage_part2([2, 3, 4, 2, 3, 4, 2, 3, 4, 2, 3, 4, 2, 7, 8])
        434234234278
        >>> max_joltage_part2([8, 1, 8, 1, 8, 1, 9, 1, 1, 1, 1, 2, 1, 1, 1])
        888911112111

    """
    n = len(bank)

    max_joltage_values = []
    max_joltage_indices = []
    max_index = -1
    for digit_n in range(number_of_batteries):
        max_value = bank[max_index+1]
        max_index = max_index + 1

        for i in range(max_index + 1, n - (number_of_batteries - digit_n - 1)):
            if bank[i] > max_value:
                max_value = bank[i]
                max_index = i
        
        max_joltage_values.append(max_value)
        max_joltage_indices.append(max_index)
    
    return sum(value * (10 ** (number_of_batteries - digit_n - 1)) for digit_n, value in enumerate(max_joltage_values))


if __name__ == "__main__":
    import sys
    import doctest
    doctest.testmod() 

    DEBUG = False

    day3_part = int(sys.argv[1])
    assert day3_part in (1, 2), "Specify part 1 or 2 as first argument."

    # Parse banks from input text
    with open(sys.argv[2], 'r') as f:
        input_text = f.read()
    banks = parse_battery_banks(input_text)

    number_of_batteries = 2 if day3_part == 1 else 12
    print(f"Using exactly {number_of_batteries} batteries per bank according to part {day3_part} rules.")

    total_joltage = 0
    for i, bank in enumerate(banks):
        joltage = max_joltage(bank, number_of_batteries=2 if day3_part == 1 else 12)
        print(f"Max joltage for bank #{i+1}:", joltage)
        total_joltage += joltage
    print(f"Total max joltage from all banks: {total_joltage}")
