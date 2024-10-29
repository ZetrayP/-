import time
import functools
import os
print(os.getcwd())


def timing_decorator(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"{func.__name__} took {end_time - start_time:.6f} seconds to execute.")
        return result
    return wrapper

@timing_decorator
def calculate_sum(a, b):
    print(f"The sum of {a} and {b} is {a + b}")
    return a + b

@timing_decorator
def read_and_write_numbers():
    input_path = 'Task5/input.txt'
    output_path = 'Task5/output.txt'
    with open(input_path, "r") as file:
        numbers = file.read().strip().split(',')
        a = float(numbers[0])
        b = float(numbers[1])    
    result = a + b   
    with open(output_path, "w") as file:
        file.write(f"The sum of {a} and {b} is {result}\n")   
    print(f"The result has been written to output.txt")
    return result


#Тест
calculate_sum(5, 3)
read_and_write_numbers()