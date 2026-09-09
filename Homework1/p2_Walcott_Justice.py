import math
def find_Pythagorean(n):
    results = []
    for a in range(1, n+ 1):
        for b in range (1, n + 1):
            sqrt_c = math.sqrt(a**2 + b**2)
            rounded_c = round(sqrt_c)
            if rounded_c**2 == a**2 + b**2 and rounded_c <= n:
                results.append((a, b, rounded_c))
    return results



if __name__ == "__main__":
    n = int(input("Enter a number: "))
    if n <= 0:
        print("Please enter a positive integer.")
    else:
        print("The Pythagorean triples are: ", find_Pythagorean(n))