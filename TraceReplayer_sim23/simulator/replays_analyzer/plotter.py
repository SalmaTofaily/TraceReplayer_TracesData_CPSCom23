
from matplotlib import pyplot as plt
import numpy as np
from common.PlotHelper import my_large_figure, my_nrows, set_axes_ticks_labels_size, set_title_with_fontsize, set_xlabel_with_fontsize, set_ylabel_with_fontsize
from common.stat_helper import get_min_max_in_dic_values
from models import settings
from simulator.trace_column_names_in_csv import *

def print_power_profile(df):
    x = df[timestamp_column_name]
    y = df[power_column_name]
    # plot
    fig, ax = plt.subplots()
    ax.plot(x, y)

def plot_exps_histogram_dict_lists_distribution(dic_distinct_lists, output_filepath, fig_n_cols, my_fontsize=None, x_label=None, y_label=None, bins_count=None):
    #https://numpy.org/doc/stable/reference/generated/numpy.histogram.html
    #https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.hist.html
    #https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.bar.html
    fig = my_large_figure()
    if my_fontsize == None:
      my_fontsize = settings.fontsize_normal_scale_figures
    fig.subplots_adjust(hspace=1, wspace=1)

    plots_count = len(dic_distinct_lists)
    nrows = my_nrows(plots_count,fig_n_cols)
    ncols = fig_n_cols 
    
    min_x, max_x = get_min_max_in_dic_values(dic_distinct_lists)
    
    i=0
   
    for array_name, array in dic_distinct_lists.items():#key, value 
        counts, bins = np.histogram(array, bins=bins_count) #The Numpy histogram function doesn't draw the histogram, but it computes the occurrences of input data that fall within each bin, which in turns determines the area (not necessarily the height if the bins aren't of equal width) of each bar.
        ax = fig.add_subplot(nrows, ncols, i+1)
        i=i+1
       
        set_axes_ticks_labels_size(ax, my_fontsize)
        ax.hist(bins[:-1], bins, weights=counts)
        
        # fix same x range between all plots
        ax.set_xlim(xmin=min_x)
        ax.set_xlim(xmax=max_x)
        
        set_title_with_fontsize(
            ax, f'Distribution in {array_name}', my_fontsize)
        set_xlabel_with_fontsize(ax, x_label, my_fontsize)
        set_ylabel_with_fontsize(ax, y_label, my_fontsize)

    plt.savefig(output_filepath)
    
