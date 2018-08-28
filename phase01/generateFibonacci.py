def generateFibonacci(length):
    fibonacci_list = []
    while len(fibonacci_list) < length:
        if len(fibonacci_list) < 2:
            fibonacci_list.append(1)
        else:
            new_number = (fibonacci_list[-1])+(fibonacci_list[-2])
            fibonacci_list.append(new_number)
    return fibonacci_list
