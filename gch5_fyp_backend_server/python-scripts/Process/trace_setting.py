
from shared_state import device_id, find_device_id, fix_device_id,algorithm_list,algorithm_use
    
def trace_setting():
    
    while True:
        print("The device_id list is: ", device_id)
        find_device_id = input("Please enter the device_id you want to find: ")
        if find_device_id not in device_id:
            print("The device_id is not in the list.")
            continue
        else:
            print("The device_id is set.")
            break
            
    while True:
        fix_parameters = input("Is there device_id for updating the path_loss parameters? (y/n): ")
        if fix_parameters == "n":
            fix_device_id = None
            break
        elif fix_parameters == "y":
            print("The device_id list is: ", device_id)
            fix_device_id = input("Please enter the device_id you want to update: ")
            if fix_device_id not in device_id:
                print("The device_id is not in the list.")
                fix_device_id = None
                continue
                
    while True:
        # which algorithm to use 
        print("The algorithm list is: ", algorithm_list)
        algorithm = input("Please enter the algorithm you want to use: ")
        if algorithm not in algorithm_list:
            print("The algorithm is not in the list.")
            continue
        else:
            algorithm_use = algorithm
            break
