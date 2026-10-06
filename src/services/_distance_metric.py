def hamming_distance(num1: int, num2: int) -> int:
    return (num1 ^ num2).bit_count()
