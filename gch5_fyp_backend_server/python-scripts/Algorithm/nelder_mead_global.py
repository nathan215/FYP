import numpy as np
import copy


def estimate_new_start(all_points, maximizing=True, step_size=150 ):

    # Convert all_points to array for of points and values
    points = np.array([p[0] for p in all_points])
    values = np.array([p[1] for p in all_points])
    
    values_normalized = (values - values.min()) / (values.max() - values.min())
    
    # Calculate the weighted centroid
    weighted_centroid = np.average(points, axis=0, weights=values_normalized)
    
    # Estimate the direction and distance for the new point towards the area of highest density
    direction = np.mean(points, axis=0) - weighted_centroid
    direction_normalized = direction / np.linalg.norm(direction)

    new_start =  all_points[-1][0] - step_size * direction_normalized
    print("New start: ", new_start)
    return new_start

def my_nelder_mead(f, x_start, step=100, no_improve_thr= 15,
                no_improv_break=4, max_iter=100,
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

    iters = 2
    while True:
        # Order by best score.
        res.sort(key=lambda x: -x[1]) 
        best = res[0][1]

        # Break after max_iter.
        if max_iter and iters >= max_iter:
            return res[0] , all_points
        iters += 1
        

        if no_improv >= no_improv_break:
            new_start = estimate_new_start(all_points, maximizing=True, step_size=step)  # Assuming you're maximizing
            x_start = new_start
            no_improv = 0
            res = [[x_start, f(x_start)]]
            for i in range(dim):
                x = copy.copy(x_start)
                x[i] = x[i] + step
                score = f(x)
                res.append([x, score])
            iters += 2
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
            no_improv +=1
            continue

        # Reduction.
        x1 = res[0][0]
        nres = []
        for tup in res:
            print("Reduction")
            redx = x1 + sigma * (tup[0] - x1)
            score = f(redx)
            nres.append([redx, score])
        res = nres
        no_improv +=1