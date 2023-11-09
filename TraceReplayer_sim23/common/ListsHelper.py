from collections import Counter
import copy
import datetime

def deepCopyL1AndExtendWithNoneToMatchL2Size(l1_trace_power_list,l2_cmp2PowerList) -> list:
    l1_view_extended = deepCopyList(l1_trace_power_list)
     # calibration trace could be shorter than trace2cmp2
    if len(l2_cmp2PowerList) > len(l1_trace_power_list):
        # make the size of 2 arrays equal by filling None values to trace_power_array (zip will only otherwise take the minimum array size and remove the extra cmp2 array rows).
       diff_elements_count = len(l2_cmp2PowerList) - len(l1_trace_power_list)
       # create array of n elements, each of value None
       append_none_Array = [None] * (diff_elements_count)
       l1_view_extended.extend(append_none_Array)
    return l1_view_extended

def deepCopyList(lst):
    return copy.deepcopy(lst)

def getCountOfUniqueItemsInList(myList):
    return len(Counter(myList).keys()) 

def save_list_to_file(data):#chatgbt generated
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")  # Generate timestamp
    file_name = f"file_{timestamp}.txt"  # Create file name with timestamp

    with open(file_name, "w") as file:
        for item in data:
            file.write(str(item) + "\n")

    print(f"File '{file_name}' saved successfully.")


def calculate_average_of_nums_in_file(file_path):# each num on a line
    #chatgbt method
    try:
        # Open the file in read mode
        with open(file_path, 'r') as file:
            numbers = file.readlines()
            # Remove newline characters and convert to integers
            numbers = [float(number.strip()) for number in numbers]

            # Calculate the average
            if numbers:
                average = sum(numbers) / len(numbers)
                print("Average:", average)
            else:
                print("The file is empty.")
    except FileNotFoundError:
        print("File not found.")
# # Example usage
# file_path = "file_2023-06-01_16-55-00.txt"  
# # 1.4152824299688656
# calculate_average(file_path)