from collections import Counter
import random
import statistics
from typing import Dict

import numpy as np

from common.ListsHelper import getCountOfUniqueItemsInList

def calculate_avg_stdev_for_dic_of_values(dictionary: Dict, exp_identifier: str) -> Dict[str, float]:

    # if modelName unique count != 1 error.
    # used chatgpt and updated code
    results_sumForBulk = {}
    context_names =  dictionary[exp_identifier] # ex modelName
    count_exps = len(dictionary[exp_identifier])
    if getCountOfUniqueItemsInList(context_names) != 1:
        raise Exception("Passed results_sumForBulk for different experiments")
    # calculate all except for the modelName key
    for key, values in dictionary.items():
        if key == exp_identifier:
            continue
        average = statistics.mean(values)
        stdev = statistics.stdev(values)
        results_sumForBulk[key] = (average, stdev)
    print("Results for: "+ exp_identifier + "= " +context_names[0] + ":")
    for key, (average, stdev) in results_sumForBulk.items():
          print(f'       {key}: Average={average}, Standard Deviation={stdev}')
    return results_sumForBulk



def get_min_max_in_dic_values(dic_distinct_lists):
    l_All=[]
    for l in dic_distinct_lists.values():
        l_All=l_All+l
    _min = min(l_All)
    _max = max(l_All)
    return _min, _max

def calculate_median_q1_q3_avg_stdev(filename:str):#chatgpt
    # def calculate_median(filename):get_median_of_numbers_in_file_line_separated
    # Read the file and store the numbers in a list
    numbers = []
    with open(filename, 'r') as file:
        for line in file:
            number = float(line.strip())
            numbers.append(number)

    # Calculate the median using statistics.median
    median = statistics.median(numbers)
    mean = statistics.mean(numbers)
    stdev = statistics.stdev(numbers)
    q1 = np.percentile(numbers, [25])
    q3 = np.percentile(numbers, [75])
    
    print("numbers count = " + str(len(numbers)))
    print("median = " + str(median))
    print("q1 = " + str(q1))
    print("q3 = " + str(q3))
    print ("avg = " + str(mean))
    print("stdev = " + str(stdev))
    print()
    return median

def int_digits_count(num):
    count=0
    while num != 0:
        num //= 10
        count += 1
    return count