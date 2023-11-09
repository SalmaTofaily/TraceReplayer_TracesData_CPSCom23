
import csv
import pandas as pd
from matplotlib import pyplot as plt
from common.TracePlotter import plot_trace

from common.PlotHelper import my_show_plot
import matplotlib.pyplot as plt
from matplotlib import cm
from simulator.trace_column_names_in_csv import *

csv_header = [exp_ids_column_name, 'iteration_index', timestamp_column_name, power_column_name]

def from_experiments_generate_traces_file(experiments, filepath):
    # append mode
    file = open(filepath, 'a')
    writer = csv.writer(file)
    writer.writerow(csv_header)
    for experiment in experiments:
        for exp_itr_res in experiment.iterations_results:
            int_measurement_count = len(exp_itr_res.measurement_timestamps)
            # zip matches arrays whose indexes are correlated into tuples.
            rows = list(zip([experiment.id]*int_measurement_count,
                            [exp_itr_res.index]*int_measurement_count,
                            exp_itr_res.measurement_timestamps,
                            exp_itr_res.power_metrics_W)
                        )
            writer.writerows(rows)
    file.close()
    # check:read file and plot it
    #https://stackoverflow.com/questions/62929509/get-arrays-from-csv-file-to-plot-a-chart
   
    
def plot_exps_traces_from_file(filepath):
    dataframe = pd.read_csv(filepath, parse_dates=True) 
    power_array = dataframe[power_column_name].tolist()
    timestamp_array = dataframe[timestamp_column_name].tolist()
    #ChatGPT: The unique() method returns a numpy array containing the unique values in the specified column
    unique_expids = dataframe[exp_ids_column_name].unique()
    expids_space_separated = " ".join(list(map(str, unique_expids)))

    plot_trace(expids_space_separated,filepath+'.pdf',timestamp_array,power_array)

def from_experiment_generate_traces_file(experiment, filename):
    # append mode
    file = open(filename, 'a')
    writer = csv.writer(file)
    writer.writerow(csv_header)

    for exp_itr_res in experiment.iterations_results:
        int_measurement_count = len(exp_itr_res.measurement_timestamps)
        # zip matches arrays whose indexes are correlated into tuples.
        #ChatGPT list,zip
        rows = list(zip([experiment.id]*int_measurement_count,
                        [exp_itr_res.index]*int_measurement_count,
                        exp_itr_res.measurement_timestamps,
                        exp_itr_res.power_metrics_W)
                    )
        writer.writerows(rows)
    file.close()