import math
import matplotlib.pyplot as plt
import numpy as np
while True:
    
        a_input = input("Enter a: ")
        if a_input =="":
                break
        a = float(a_input)
        b = float(input("Enter b: "))
        c = float(input("Enter c: "))

        square_b = b ** 2
        discriminant = square_b - 4 * a * c


        if discriminant < 0:
            print("No real solution.")
            xopt = -b / (2 * a)
            x_min = xopt - 5
            x_max = xopt + 5
            x_values = np.linspace(x_min, x_max ,150)
            y_values = a * x_values**2 + b * x_values + c
            plt.plot(x_values, y_values)
            plt.show()
        
        elif discriminant == 0:
            x1 = -b / (2 * a)
            print(f"one solution: {x1:.5f}")
            x_min = x1 - 5
            x_max = x1 + 5
            x_values = np.linspace(x_min, x_max, 150)
            y_values = a * x_values**2 + b * x_values + c
            plt.plot(x_values, y_values)
            plt.show()
                
        else:
            sqrt_discriminant = math.sqrt(discriminant)
            x1 = (-b + sqrt_discriminant) / (2 * a)
            x2 = (-b - sqrt_discriminant) / (2 * a)
            print(f"two solutions: x1={x1:.5f} x2={x2:.5f}")
            x_min = min(x1, x2) - 5
            x_max = max(x1, x2) + 5
            x_values = np.linspace(x_min, x_max, 150)
            y_values = a * x_values**2 + b * x_values + c
            plt.plot(x_values, y_values)
            plt.show()
