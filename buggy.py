def calculate_average(numbers):
    total = sum(numbers)
    # Bug: Division by zero if list is empty
    return total / len(numbers) 

data = []
print(calculate_average(data))