
def trilateration(coords, radii):
    x1, y1 = coords[0]
    x2, y2 = coords[1]
    x3, y3 = coords[2]
    
    r1 = radii[0]
    r2 = radii[1]
    r3 = radii[2]
    
    A = 2*(x2 - x1)
    B = 2*(y2 - y1)
    C = r1**2 - r2**2 + x2**2 - x1**2 + y2**2 - y1**2
    
    D = 2*(x3 - x1)
    E = 2*(y3 - y1)
    F = r1**2 - r3**2 + x3**2 - x1**2 + y3**2 - y1**2
    
    x = (C*E - F*B) / (E*A - B*D)
    y = (C*D - A*F) / (B*D - A*E)
    
    return x, y

import numpy as np
from scipy.optimize import minimize

def best_fit_trilateration(coords, radii):
    def objective(p, coords, radii):
        x, y = p
        residuals = [(x - x_i)**2 + (y - y_i)**2 - r**2 for (x_i, y_i), r in zip(coords, radii)]
        return np.sum(np.square(residuals))

    # Start the optimization with an initial guess (can be improved)
    initial_guess = (np.mean([x for x, y in coords]), np.mean([y for x, y in coords]))

    result = minimize(objective, initial_guess, args=(coords, radii), method='L-BFGS-B')

    return result.x

# Example usage
from math import sqrt
coords = [(0, 0), (2, 0), (3, 3)]
radii = [sqrt(2), sqrt(2), sqrt(8)]
x, y = trilateration(coords, radii)
print(f"The coordinates are: x={x}, y={y}")

coords = [(0, 0), (2, 0), (0, 2), (3, 3)]
radii = [sqrt(2), sqrt(2), sqrt(2), 3]

x, y = best_fit_trilateration(coords, radii)
print(f"The best fit coordinates are: x={x}, y={y}")

