from fibonacci.generateFibonacci import generateFibonacci
import allure


@allure.epic('Learning')
@allure.title('Testing method which generates fibonacci numbers')
def testFibonacci():
    expectedList = [1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610]
    assert generateFibonacci(15) == expectedList
    expectedlist1 = [1, 1, 2, 3, 5]
    assert generateFibonacci(5) == expectedlist1

