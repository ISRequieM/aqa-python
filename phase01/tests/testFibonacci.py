from phase01.generateFibonacci import generateFibonacci


def testFibonacci():
    expectedList = [1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610]
    assert generateFibonacci(15) == expectedList