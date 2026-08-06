# this code is just for testing the explain_code function
print("HELLO")

from explain.explainer import explain_code

print("Starting test...")

sample_code = """
def factorial(n):
    if n == 0:
        return 1
    return n * factorial(n-1)
"""

result = explain_code(sample_code)

print(result)