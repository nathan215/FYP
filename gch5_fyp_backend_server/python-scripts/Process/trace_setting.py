from shared_state import device_id, find_device_id, fix_device_id,algorithm_list,algorithm_use
    
def trace_setting():
    global find_device_id, fix_device_id, algorithm_use

    while True:
        print("The device_id list is: ", device_id)
        find_device_id_i = input("Please enter the device_id you want to find: ")
        if find_device_id_i not in device_id:
            print("The device_id is not in the list.")
            continue
        else:
            find_device_id.append(find_device_id_i)
            print("The device_id is set.")
            break

    while True:
        # which algorithm to use 
        print("The algorithm list is: ", algorithm_list)
        algorithm = input("Please enter the algorithm you want to use: ")
        if algorithm not in algorithm_list:
            print("The algorithm is not in the list.")
            continue
        else:
            algorithm_use.append(algorithm)
            print("The algorithm is set to ",algorithm_use)
            break
            
    if algorithm_use[0] == 'l3m':
        while True:
            fix_parameters = input("Is there device_id for updating the path_loss parameters? (y/n): ")
            if fix_parameters == "n":
                break
            elif fix_parameters == "y":
                print("The device_id list is: ", device_id)
                fix_device_id_i = input("Please enter the device_id you want to update: ")
                if fix_device_id_i not in device_id:
                    print("The device_id is not in the list.")
                    continue
                else:
                    fix_device_id.append(fix_device_id_i)
                    print("The device_id is set.")
                    break
                
    
