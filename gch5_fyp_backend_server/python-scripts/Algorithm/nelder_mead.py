'''
    Reference: https://github.com/fchollet/nelder-mead/tree/master
    Clear explanation video: https://www.youtube.com/watch?v=vOYlVvT3W80&ab_channel=MilesChen
'''

import numpy as np
import copy

def my_nelder_mead(f, x_start, step=100, no_improve_thr=3,
                no_improv_break=10, max_iter=100,
                alpha=1., gamma=2., rho=-0.5, sigma=0.5):
    
    # Initialize the simplex.
    dim = len(x_start)
    prev_best = f(x_start)
    no_improv = 0
    res = [[x_start, prev_best]]
    all_points = [[x_start, prev_best]]  # Initialize the list to store all evaluated points

    for i in range(dim):
        x = copy.copy(x_start)
        x[i] = x[i] + step
        score = f(x)
        res.append([x, score])
        all_points.append([x, score])

    iters = 0
    while True:
        # Order by best score.
        res.sort(key=lambda x: -x[1]) 
        best = res[0][1]

        # Break after max_iter.
        if max_iter and iters >= max_iter:
            return res[0] , all_points
        iters += 1

        movement = np.linalg.norm(res[0][0] - res[1][0]) 
        if movement < no_improve_thr:
            no_improv += 1
        if no_improv >= no_improv_break:
            return res[0], all_points

        # Calculate the centroid of the simplex excluding the worst point.
        x0 = [0.] * dim
        for tup in res[:-1]:
            for i, c in enumerate(tup[0]):
                x0[i] += c / (len(res)-1)
        x0 = np.array(x0)

        # Reflection.
        xr = x0 + alpha * (x0 - res[-1][0])
        rscore = f(xr)
        all_points.append([xr, rscore])  # Store the evaluated point
        if res[0][1] >= rscore > res[-2][1]:
            del res[-1]
            res.append([xr, rscore])
            continue

        # Expansion.
        if rscore > res[0][1]:
            xe = x0 + gamma * (x0 - res[-1][0])
            escore = f(xe)
            all_points.append([xe, escore])  # Store the evaluated point
            if escore > rscore:
                del res[-1]
                res.append([xe, escore])
                continue
            else:
                del res[-1]
                res.append([xr, rscore])
                continue

        # Contraction.
        xc = x0 + rho * (x0 - res[-1][0])
        cscore = f(xc)
        all_points.append([xc,cscore])  # Store the evaluated point
        if cscore > res[-1][1]:
            del res[-1]
            res.append([xc, cscore])
            continue

        # Reduction.
        x1 = res[0][0]
        nres = []
        for tup in res:
            redx = x1 + sigma * (tup[0] - x1)
            score = f(redx)
            nres.append([redx, score])
        res = nres
    
# Test the algorithm
if __name__ == '__main__':
    # Define an objective function to minimize.
    def objective_function(x):
        return (x[0] - 1)**2 + (x[1] - 2)**2

    # Initial guess.
    x_start = np.array([-20, 15])

    # Call the Nelder-Mead algorithm.
    result,all_points = my_nelder_mead(objective_function, x_start,step=2, max_iter= 15)
    print("Optimized Parameters:", result[0])
    print("Objective Function Value:", result[1])
    print("All evaluated points:", all_points)

    def plot_simplex_path(all_points, title='Nelder-Mead Simplex Path'):
        import matplotlib.pyplot as plt
        # Convert the list of points to a NumPy array for easier slicing
        all_points = np.array(all_points)
        
        plt.figure(figsize=(10, 6))
        plt.scatter(all_points[:, 0], all_points[:, 1], label='Evaluated Points')
        
        # Optionally, you can also plot lines between consecutive points
        # to see the path more clearly:
        plt.plot(all_points[:, 0], all_points[:, 1], 'r-', lw=1, alpha=0.6)

        # Highlight the start and end points
        plt.scatter(all_points[0, 0], all_points[0, 1], c='green', label='Start Point', zorder=5)
        plt.scatter(all_points[-1, 0], all_points[-1, 1], c='red', label='End Point', zorder=5)

        plt.title(title)
        plt.xlabel('X Coordinate')
        plt.ylabel('Y Coordinate')
        plt.legend()
        plt.grid(True)
        plt.show()
    
    plot_simplex_path(all_points)
        






