import numpy as np
import pandas as pd
import math
import matplotlib.pyplot as plt
from tqdm import tqdm
from scipy import stats
from path_loss_algorithm import l3m, l3m_c, l3m_mre, l3m_w, compute_parameters_linear

path_loss_n = 1.5
path_loss_A = -64
noise_levels = np.arange(4, 9, 1)
repretitions = 1
algorithm_list = ['l3m', 'l3m_c', 'l3m_mre','l3m_w','l3m_a','l3m_c_a','l3m_mre_a','l3m_w_a']

# Assuming the simulate_rssi and analyze_localization_errors functions are defined here
# Function to simulate RSSI values based on the path loss model
def simulate_rssi(x, y, noise_level):
    d = np.sqrt(x**2 + y**2) if x**2 + y**2 != 0 else 0.1
    # set random prop if more than 0.7 add noise
    if np.random.rand() > 0.1: 
        estimated_rssi = -10 * path_loss_n * np.log10(d) + path_loss_A + np.random.normal(0, noise_level)
    else:
        estimated_rssi = -10 * path_loss_n * np.log10(d) + path_loss_A
    return estimated_rssi

# def caclulate_str():
#     # Generate node data
#     x_coords = np.random.uniform(-100, 100, 100)
#     y_coords = np.random.uniform(-100, 100, 100)
#     for i in range(100):
#         rssi_values = [simulate_rssi(x, y, 5) for x, y in zip(x_coords, y_coords)]
#         fix_combined_data = [{'x': x, 'y': y, 'rssi': rssi} for x, y, rssi in zip(x_coords, y_coords, rssi_values)]
#         n, C, str = compute_parameters_linear(fix_combined_data)
#         print(n,C,str)

# caclulate_str()
# exit()
def analyze_parameters_error():
    noise_levels = [5, 10]
    nodes_range = range(15, 51, 5)
    repetitions = 50

    # Import or define the simulate_rssi and compute_parameters_linear functions here

    # Results storage
    results_n = {noise: {nodes: [] for nodes in nodes_range} for noise in noise_levels}
    results_C = {noise: {nodes: [] for nodes in nodes_range} for noise in noise_levels}

    # Simulation loop
    np.random.seed(42)
    for noise in noise_levels:
        for nodes in nodes_range:
            for _ in range(repetitions):
                # Generate node data
                x_coords = np.random.uniform(-500, 500, nodes)
                y_coords = np.random.uniform(-500, 500, nodes)
                rssi_values = [simulate_rssi(x, y, noise) for x, y in zip(x_coords, y_coords)]
                
                # Gather data and compute parameters
                fix_combined_data = [{'x': x, 'y': y, 'rssi': rssi} for x, y, rssi in zip(x_coords, y_coords, rssi_values)]
                n, C, _ = compute_parameters_linear(fix_combined_data)
                
                # Store results
                results_n[noise][nodes].append(n)
                results_C[noise][nodes].append(C)

    # Prepare the figure
    fig, axs = plt.subplots(2, 2, figsize=(12, 10))  # 2x2 plot
    print(results_C[noise_levels[0]][nodes_range[0]])
    for i, noise in enumerate(noise_levels):
        # Calculate means and confidence intervals
        mean_ns = [np.mean(results_n[noise][nodes]) for nodes in nodes_range]
        ci_ns = [1.96 * np.std(results_n[noise][nodes]) for nodes in nodes_range]
        mean_cs = [np.mean(results_C[noise][nodes]) for nodes in nodes_range]
        ci_cs = [1.96 * np.std(results_C[noise][nodes]) for nodes in nodes_range]
        
        # Plotting for parameter n
        # plot ten point n for each noise
        axs[i][0].set_ylim(-2,5)
        axs[i][0].errorbar(nodes_range, mean_ns, yerr=ci_ns, label=f'Noise {noise}')
        axs[i][0].set_title(f'Parameter n vs Number of Nodes (Noise {noise})')
        axs[i][0].set_xlabel('Number of Nodes')
        axs[i][0].set_ylabel('Estimated n')
        axs[i][0].legend()

        # Plotting for parameter C
        axs[i][1].set_ylim(-120,0)
        axs[i][1].errorbar(nodes_range, mean_cs, yerr=ci_cs, label=f'Noise {noise}')
        axs[i][1].set_title(f'Parameter C vs Number of Nodes (Noise {noise})')
        axs[i][1].set_xlabel('Number of Nodes')
        axs[i][1].set_ylabel('Estimated C')
        axs[i][1].legend()

    plt.tight_layout()
    plt.show()


# Main analysis function
def analyze_localization_errors(repetitions=100):
    predictions = {algorithm: [] for algorithm in algorithm_list}
    errors = {algorithm: [] for algorithm in algorithm_list}
    
    for noise in tqdm(noise_levels):
        temp_errors = {algorithm: [] for algorithm in algorithm_list}
        for _ in tqdm(range(repetitions)):
            
            anchors = np.random.uniform(-500, 500, (10, 2))
            rssi_values = [simulate_rssi(x, y, noise) for x, y in anchors]
            df = pd.DataFrame(anchors, columns=['x', 'y'])
            df['rssi'] = rssi_values

            # caculate parameter
            anchors_p = np.random.uniform(-500, 500, (15, 2))
            rssi_values_p = [simulate_rssi(x, y, noise) for x, y in anchors_p]

            data = [{'x':x, 'y':y, 'rssi':rssi} for x, y, rssi in zip(anchors_p[:,0], anchors_p[:,1], rssi_values_p)]
            path_loss_A_a, path_loss_n_a, _ = compute_parameters_linear(data)


            
            # True position
            true_position = np.array([0, 0])
            
            # Calculate and store errors for each algorithm
            for algorithm in algorithm_list:
                if algorithm == 'l3m':
                    predicted_position = l3m(df, path_loss_A, path_loss_n)
                    rl3m = predicted_position
                elif algorithm == 'l3m_c':
                    predicted_position = l3m_c(df, path_loss_A, path_loss_n, R=5, K=3)
                    rl3m_c = predicted_position
                elif algorithm == 'l3m_mre':
                    predicted_position = l3m_mre(df, path_loss_A, path_loss_n, R=5)
                    rl3m_mre = predicted_position
                elif algorithm == 'l3m_w':
                    predicted_position = l3m_w(df,path_loss_A,path_loss_n, [rl3m,rl3m_c,rl3m_mre])
                elif algorithm == 'l3m_a':
                    predicted_position = l3m(df, path_loss_A_a, path_loss_n_a)
                    rl3m_a = predicted_position
                elif algorithm == 'l3m_c_a':
                    predicted_position = l3m_c(df, path_loss_A_a, path_loss_n_a, R=5, K=3)
                    rl3m_c_a = predicted_position
                elif algorithm == 'l3m_mre_a':
                    predicted_position = l3m_mre(df, path_loss_A_a, path_loss_n_a, R=4)
                    rl3m_mre_a = predicted_position
                elif algorithm == 'l3m_w_a':
                    predicted_position = l3m_w(df,path_loss_A_a,path_loss_n_a, [rl3m_a,rl3m_c_a,rl3m_mre_a])
               
                error = np.linalg.norm(predicted_position - true_position)
                error = min(error,5000)
                if algorithm == 'l3m_a' and path_loss_A_a< 1:
                    print(noise, error,path_loss_A_a, path_loss_n_a)
                temp_errors[algorithm].append(error)
                predictions[algorithm].append(predicted_position)
        
        # Calculate mean error
        for algorithm in temp_errors:
            mean_error = np.mean(temp_errors[algorithm])
            errors[algorithm].append(mean_error)
    
    return errors, predictions


def analyze_incremental_points_addition(max_points, noise_level, repetitions=100):
    base_errors = {algorithm: [] for algorithm in algorithm_list}
    incremental_predictions = {algorithm: [] for algorithm in algorithm_list}
    
    # Loop over each repetition
    for _ in tqdm(range(repetitions)):
        # Reset the initial set of anchors for each repetition
        current_anchors = np.random.uniform(-500, 500, (4, 2))
        current_rssi_values = [simulate_rssi(x, y, noise_level) for x, y in current_anchors]
        
        anchors_p = np.random.uniform(-500, 500, (15, 2))
        rssi_values_p = [simulate_rssi(x, y, noise_level) for x, y in anchors_p]

        data = [{'x':x, 'y':y, 'rssi':rssi} for x, y, rssi in zip(anchors_p[:,0], anchors_p[:,1], rssi_values_p)]
        path_loss_A_a, path_loss_n_a, _ = compute_parameters_linear(data)
        # Loop over the range of points from 3 to max_points
        for point_count in tqdm(range(3, max_points + 1)):  # Start adding from the 4th point
            # Add a new anchor point
            new_anchor = np.random.uniform(-500, 500, (1, 2))
            current_anchors = np.vstack([current_anchors, new_anchor])
            
            # Calculate RSSI for the new anchor point and append it
            new_rssi_value = simulate_rssi(new_anchor[0][0], new_anchor[0][1], noise_level)
            current_rssi_values.append(new_rssi_value)
            
            # Create DataFrame for the current set of anchor points and their RSSI values
            df = pd.DataFrame(current_anchors, columns=['x', 'y'])
            df['rssi'] = current_rssi_values
            
            true_position = np.array([0, 0])
            
            # Initialize temporary storage for errors in this iteration
            temp_errors = {algorithm: [] for algorithm in algorithm_list}
            
            # Calculate and store errors and predictions for each algorithm
            for algorithm in algorithm_list:
                if algorithm == 'l3m':
                    predicted_position = l3m(df, path_loss_A, path_loss_n)
                    r_l3m = predicted_position
                elif algorithm == 'l3m_c':
                    predicted_position = l3m_c(df, path_loss_A, path_loss_n, R=min(point_count, 5), K=3)
                    r_l3m_c = predicted_position
                elif algorithm == 'l3m_mre':
                    predicted_position = l3m_mre(df, path_loss_A, path_loss_n, R=min(point_count,4))
                    r_l3m_mre = predicted_position
                elif algorithm == 'l3m_w':
                    predicted_position = l3m_w(df, path_loss_A, path_loss_n, [r_l3m, r_l3m_c, r_l3m_mre])
                elif algorithm == 'l3m_a':
                    predicted_position = l3m(df, path_loss_A_a, path_loss_n_a)
                    r_l3m_a = predicted_position
                elif algorithm == 'l3m_c_a':
                    predicted_position = l3m_c(df, path_loss_A_a, path_loss_n_a, R=min(point_count, 5), K=3)
                    r_l3m_c_a = predicted_position
                elif algorithm == 'l3m_mre_a':
                    predicted_position = l3m_mre(df, path_loss_A_a, path_loss_n_a, R=min(point_count, 4))
                    r_l3m_mre_a = predicted_position
                elif algorithm == 'l3m_w_a':
                    predicted_position = l3m_w(df, path_loss_A_a, path_loss_n_a, [r_l3m_a, r_l3m_c_a, r_l3m_mre_a])
                error = np.linalg.norm(predicted_position - true_position)
                error = min(error, 5000)
                temp_errors[algorithm].append(error)
            
            # Store the mean error and the latest prediction for each algorithm
            for algorithm in temp_errors:
                mean_error = np.mean(temp_errors[algorithm])
                base_errors[algorithm].append(mean_error)
                incremental_predictions[algorithm].append(predicted_position)
    # Calculate average errors over all repetitions for plotting
    avg_errors = {alg: np.mean(np.reshape(errors, (repetitions, -1)), axis=0).tolist() for alg, errors in base_errors.items()}
    return avg_errors, incremental_predictions


# Function to plot the results
def plot_errors_with_confidence(errors, noise_levels):
    plt.figure(figsize=(12, 8))
    algorithms = errors.keys()
    
    for algorithm in ['l3m', 'l3m_c', 'l3m_mre','l3m_w']:    
        mean_errors = errors[algorithm]
        plt.plot(noise_levels, mean_errors, label=algorithm)
    

    plt.xlabel('Noise Level')
    plt.ylabel('Mean Error')
    plt.title('Localization Error by Noise Level')
    plt.legend()
    plt.grid(True)
    plt.show()

    for algorithm in ['l3m_a', 'l3m_c_a', 'l3m_mre_a','l3m_w_a']:    
        mean_errors = errors[algorithm]
        plt.plot(noise_levels, mean_errors, label=algorithm)
   
    plt.ylim(0, 500)
    plt.xlabel('Noise Level')
    plt.ylabel('Mean Error')
    plt.title('Localization Error by Noise Level')
    plt.legend()
    plt.grid(True)
    plt.show()

    for algorithm in ['l3m_mre','l3m_mre_a']:    
        mean_errors = errors[algorithm]
        plt.plot(noise_levels, mean_errors, label=algorithm)
    plt.xlabel('Noise Level')
    plt.ylabel('Mean Error')
    plt.title('Localization Error by Noise Level')
    plt.legend()
    plt.grid(True)
    plt.show()

def plot_incremental_errors(errors, max_points):
    # Define categories or groups of algorithms
    groups = {
        'Group 1': ['l3m', 'l3m_c', 'l3m_mre', 'l3m_w'],
        'Group 2': ['l3m_a', 'l3m_c_a', 'l3m_mre_a', 'l3m_w_a'],
        'Group 3': ['l3m_mre', 'l3m_mre_a']
    }

    # Plot settings
    point_range = list(range(3, max_points + 1))  # Starting from 3 up to max_points

    # Loop over each group and plot
    for group_name, algorithms in groups.items():
        plt.figure(figsize=(12, 8))  # Create a new figure for each group

        for algorithm in algorithms:
            if algorithm in errors:  # Check if the algorithm's errors are in the dictionary
                plt.plot(point_range, errors[algorithm], label=algorithm, marker='o', markersize=8)
        
        plt.ylim(0, 800)
        plt.xlabel('Number of Anchor Points', fontsize=14)
        plt.ylabel('Mean Localization Error', fontsize=14)
        plt.title(f'{group_name} - Localization Error as More Anchor Points are Added', fontsize=16)
        plt.xticks(point_range, fontsize=12)
        plt.yticks(fontsize=12)
        plt.legend(fontsize=12)
        plt.grid(True)
        plt.tight_layout()  # Adjust layout to make room for larger text
        plt.show()

errors, predictions = analyze_localization_errors()
plot_errors_with_confidence(errors, noise_levels)

# max_points = 12
# base_errors, incremental_predictions = analyze_incremental_points_addition(max_points, 4)
# plot_incremental_errors(base_errors, max_points)

def analyze_path_loss_A_variation(max_points, noise_level, path_loss_n_range, repetitions=10):
    errors_by_path_loss_n = []

    # Loop over each path_loss_A value
    for path_loss_na in np.linspace(path_loss_n_range[0], path_loss_n_range[1], num=10):
        local_errors = []
        
        for _ in tqdm(range(repetitions), desc=f'Analyzing A={path_loss_A:.2f}'):
            # Generate initial anchor points
            anchors = np.random.uniform(0, 500, (4, 2))
            rssi_values = [simulate_rssi(x, y, noise_level) for x, y in anchors]
            df = pd.DataFrame(anchors, columns=['x', 'y'])
            df['rssi'] = rssi_values
            
            # Assume path_loss_n is constant, e.g., 2.5
            path_loss_n = 2.5
            true_position = np.array([0, 0])  # Assuming the true position to test against
            
            # Calculate the prediction using l3m
            predicted_position = l3m(df, path_loss_A, path_loss_na)
            print(predicted_position)
            error = np.linalg.norm(predicted_position - true_position)
            local_errors.append(error)
        
        mean_error = np.mean(local_errors)
        errors_by_path_loss_n.append(mean_error)
    
    # Plotting
    plt.figure(figsize=(10, 6))
    plt.plot(np.linspace(path_loss_A_range[0], path_loss_A_range[1], num=10), errors_by_path_loss_n, marker='o')
    plt.xlabel('Path Loss Coefficient A')
    plt.ylabel('Mean Localization Error')
    plt.title('Effect of Path Loss Coefficient A on Localization Error')
    plt.grid(True)
    plt.show()

    return errors_by_path_loss_n

path_loss_A_range = (1.3, 2)
max_points = 12
noise_level = 4
analyze_path_loss_A_variation(max_points, noise_level, path_loss_A_range)