import time
import pytest
from square import SquareType, classify_square

def check_classification(squares, expected_result):
    for square in squares:
        assert classify_square(*square) == expected_result

def test_invalid_squares():
    squares = [(1, 1, 1, -1), (1, 1, -1, 1), (-1, 1, 1, 1), (1, 2, 3, 4), (1, 2, 1, 2)]
    check_classification(squares, SquareType.INVALID)

def test_valid_squares():
    squares = [(2, 2, 2, 2), (5, 5, 5, 5), (999, 999, 999, 999) ]
    check_classification(squares, SquareType.EQUAL)

def test_equal_squares():
    squares = [(1, 1, 1, 1), (100, 100, 100, 100), (99, 99, 99, 99)]
    check_classification(squares, SquareType.EQUAL)

def test_non_equal_squares():
    squares = [(5, 5, 4, 4), (2, 2, 3, 3), (100, 100, 100, 99), (99, 99, 100, 100), (1, 100, 100, 1)]
    check_classification(squares, SquareType.NON_EQUAL)

def test_non_equal_squares_with_negatives():
    squares = [(1, 1, 1, -2), (1, -1, -1, 1), (-1, 1, 1, 1), (-1, -1, -1, -1)]
    check_classification(squares, SquareType.INVALID)

def test_negative_squares():
    squares = [(-1, -1, -1, -1), (-100, -100, 100, -100), (-99, -99, -99, -99)]
    check_classification(squares, SquareType.INVALID)
   


@pytest.fixture(scope="session", autouse=True)
def starter(request):
    start_time = time.time()

    def finalizer():
        print("runtime: {}".format(str(time.time() - start_time)))

    request.addfinalizer(finalizer)
