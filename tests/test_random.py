import random


def test_random():
    result = random.randint(1, 2)
    assert result == 2
