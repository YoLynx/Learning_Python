import math  # Importing the Python math library

def add(numbers):  # Function for addition
    return sum(numbers)

def subtract(numbers):  # Function for subtraction
    result = numbers[0]
    for num in numbers[1:]:
        result -= num
    return result

def multiply(numbers):  # Function for multiplication
    result = 1
    for num in numbers:
        result *= num
    return result

def divide(numbers):  # Function for division
    result = numbers[0]
    for num in numbers[1:]:
        if num == 0:
            return "Error! Division by zero."
        result /= num
    return result

def modulus(x, y):  # Function for modulus
    return x % y

def reciprocal(x):  # Function for reciprocal
    if x == 0:
        return "Error! Division by zero."
    return 1 / x

def square_root(x):  # Function for square root
    if x < 0:
        return "Error! Negative value for square root."
    return round(math.sqrt(x), 10)  # Rounded for consistency

def logarithm(x):  # Function for natural logarithm
    if x <= 0:
        return "Error! Logarithm of non-positive value."
    return round(math.log(x), 10)  # Rounded for consistency

def sine(x):  # Function for sine in degrees
    return round(math.sin(math.radians(x)), 10)  # Rounded for consistency

def cosine(x):  # Function for cosine in degrees
    return round(math.cos(math.radians(x)), 10)  # Rounded for consistency

def tangent(x):  # Function for tangent in degrees
    result = math.tan(math.radians(x))
    # Handle edge cases where tan(x) is undefined (e.g., x = 90, 270, etc.)
    if abs(result) > 1e10:  # Extremely large value due to tangent undefined behavior
        return "Error! Tangent undefined."
    return round(result, 10)  # Rounded for consistency

def power(base, exponent):  # Function for power (base^exponent)
    return round(math.pow(base, exponent), 10)  # Rounded for consistency

