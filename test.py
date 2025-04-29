def func(a: int, b: int):
    yield a
    if a < a*b:
        yield f"a is less than a*b, a:{a}, a*b: {a*b}"
    yield f"a raise to the power of b is {a**b}"
    yield "Well, that will be the end."

func(2, 1/2)