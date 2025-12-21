def parse_ranges(input_text: str) -> list[tuple[int, int]]:
    """
    Parse a string of ranges into a list of tuples representing the ranges.

    Examples:
        >>> parse_ranges("10-20,30-40")
        [(10, 20), (30, 40)]
        >>> parse_ranges("1-5,100-200")
        [(1, 5), (100, 200)]
        >>> parse_ranges("50-60")
        [(50, 60)]
        >>> parse_ranges("5-10,15-20,25-30,35-40")
        [(5, 10), (15, 20), (25, 30), (35, 40)]
        >>> parse_ranges("100-150,200-250,300-350")
        [(100, 150), (200, 250), (300, 350)]
    """
    ranges = []
    for interval in input_text.strip().split(','):
        start, end = map(int, interval.split('-'))
        ranges.append((start, end))
    return ranges

def is_invalid_part1(id: int, debug=False):
    """
    Check if a given ID is invalid, if it has an even length and its two halves are identical.

    Examples:
        >>> is_invalid_part1(22)
        True
        >>> is_invalid_part1(3464)
        False
        >>> is_invalid_part1(103903)
        False
        >>> is_invalid_part1(1212)
        True
        >>> is_invalid_part1(123123)
        True
    """
    id_length = len(str(id))
    if id_length % 2 == 0:
        n = id_length // 2
        return id // (10 ** n) == id % (10 ** n)
    else:
        return False
    
def is_invalid_part2(id: int, debug=False):
    """
    Check if a given ID is invalid, if it can be broken into a pattern repeating N times

    Examples:
        >>> is_invalid_part2(22)
        True
        >>> is_invalid_part2(1212)
        True
        >>> is_invalid_part2(123123123)
        True
        >>> is_invalid_part2(7777777)
        True
        >>> is_invalid_part2(1212121212)
        True
        >>> is_invalid_part2(103903)
        False
        >>> is_invalid_part2(1234)
        False
        >>> is_invalid_part2(111222)
        False
        >>> is_invalid_part2(123456)
        False
        >>> is_invalid_part2(987654321)
        False
    """
    id_length = len(str(id))
    if debug: print(f"Checking ID: {id}, Length: {id_length}")

    # for sizes that are multiple of ID length
    for n in range(2, id_length + 1):
        if debug: print(f"Trying with n = {n}")
        if n > 1 and id_length % n == 0:
            pattern_size = id_length // n
            if debug: print(f"Pattern size: {pattern_size}")
            
            pattern_candidate = id // (10 ** (id_length - pattern_size))
            if debug: print(f"Pattern candidate: {pattern_candidate}")
            id_remainder = id
            
            for i in range(n):
                pattern = id_remainder // (10 ** (id_length - (i+1) * pattern_size))
                if debug: print(f"Checking pattern at iteration {i}: {pattern}")
                
                if pattern != pattern_candidate:
                    if debug: print("Pattern mismatch found.")
                    break
                else:
                    id_remainder = id_remainder % (10 ** (id_length - (i+1) * pattern_size))
                    if debug: print(f"Updated remainder: {id_remainder}")
            if debug: print("Valid repeating pattern found.")
            if pattern == pattern_candidate: return True

    if debug: print("No valid repeating pattern found.")
    return False

    
if __name__ == "__main__":
    import sys
    import doctest
    doctest.testmod()

    DEBUG = False

    day2_part = int(sys.argv[1])
    assert day2_part in (1, 2), "Specify part 1 or 2 as first argument."

    # Parse ranges from input text
    with open(sys.argv[2], 'r') as f:
        input_text = f.read()
    intervals = parse_ranges(input_text)

    f_invalid = is_invalid_part1 if day2_part == 1 else is_invalid_part2
    print("Checking for invalid IDs using part", day2_part, "criteria.")

    n_invalid = 0
    total_sum = 0
    for start, end in intervals:
        for id in range(start, end + 1):
            if f_invalid(id, debug=DEBUG):
                print("invalid:", id)
                n_invalid += 1
                total_sum += id

    print(f"# of invalid IDs: {n_invalid}")
    print(f"Sum of invalid IDs: {total_sum}")
 