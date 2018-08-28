def generateFibonacci(numberOfNumbers):
    fibonacciList = []
    while len(fibonacciList) < numberOfNumbers:
        if len(fibonacciList) < 2:
            fibonacciList.append(1)
        else:
            newNumber = (fibonacciList[-1])+(fibonacciList[-2])
            fibonacciList.append(newNumber)
    return fibonacciList