import numpy as np
import pandas as pd
import random
from .path_loss_algorithm import l3m, l3m_c, l3m_mre
from shared_state import Z0, alpha


def move_towards_l3m(f, x_start, step=50, max_iter=100,all_points=[]):
    
    data_entries = [{'x': point['x'], 'y': point['y'], 'rssi': point['rssi']} for point in all_points]
    df = pd.DataFrame(data_entries)

    for _ in range(max_iter):
        Z = Z0
        n = alpha

        estimated_position, index = l3m_mre(df, Z, n)
        if np.isnan(estimated_position).any() or np.isinf(estimated_position).any():
            print('No estimated position')
            estimated_position = np.array([random.randint(-500, 500), random.randint(-500, 500)])
            index = random.randint(0, len(df))
        if len(df) > 8:
            df = df.drop(index)
        
        last_position = (all_points[-1]['x'], all_points[-1]['y'])
        # if the distance is smaller than step, move to the estimated position
        if np.linalg.norm(estimated_position - last_position) < step:
            new_position = estimated_position
            if np.linalg.norm(estimated_position - last_position) < 10:
                angle = random.uniform(0, 2*np.pi)
                new_position = last_position + step * np.array([np.cos(angle), np.sin(angle)])
            rssi = f(new_position)
        else:
            rssi = f(estimated_position)
            new_position = last_position + step * (estimated_position - last_position) / np.linalg.norm(estimated_position - last_position)
        
        all_points.append({'x': new_position[0], 'y': new_position[1], 'rssi': rssi})
        rssi = rssi.round(2)
        new_position = new_position.round(2)
        df = pd.concat([df, pd.DataFrame([{'x': new_position[0], 'y': new_position[1], 'rssi': rssi}])], ignore_index=True)
    
    # Find the best point visited
    best_point = max(all_points, key=lambda x: x[1])

    return best_point, all_points