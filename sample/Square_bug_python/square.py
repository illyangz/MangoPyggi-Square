import time
from enum import Enum

class SquareType(Enum):
    INVALID, EQUAL, NON_EQUAL = 0, 1, 2

def delay():
    time.sleep(0.01)

def classify_square(a, b, c, d):
    delay()

    # Check for any non-positive sides
    if a <= 0 or b <= 0 or c <= 0 or d <= 0:
        return SquareType.INVALID

    # Check if all sides are equal
    if a == b == c == d:
        return SquareType.EQUAL

    # If sides are not all equal, it's a non-equal square
    return SquareType.NON_EQUAL

if __name__ == "__main__":  # pragma: no cover
    import sys
    print(classify_square(int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4])))
