

from matplotlib import pyplot as plt
from common.PlotHelper import my_large_figure, my_show_plot

def mysubplot():
    return plt.subplots(figsize=(32, 18))

def mysubplot(w=16, h=9, rows_count=1, cols_count=1):  # inches
    return plt.subplots(rows_count, cols_count, figsize=(w, h))

def plot_trace(title, output_filename, timestamps, power_measurements, show=True,xlabels=None, xlabel=None, fontsize=28):
    a,ax = mysubplot(32,19)
    ax.plot(timestamps, power_measurements, linewidth='0.8')
    ax.set_title(title)
    ax.set_xlabel('Time (s)',fontsize=fontsize)
    if xlabels!=None:
        plt.xticks(timestamps, xlabels, rotation=90)
    
    if xlabel:
        ax.set_xlabel(xlabel,fontsize=fontsize)
    ax.set_ylabel('Power (W)',fontsize=fontsize)

    ax.tick_params(axis='x', labelsize=fontsize)
    ax.tick_params(axis='y', labelsize=fontsize)
    plt.savefig(output_filename)
    # my_show_plot(show)    


# def plot_trace_histogram_power_distribution(power_measurements, show=True,my_fontsize=None):
#     fig = my_large_figure()
#     if my_fontsize == None:
#       my_fontsize = settings.fontsize_normal_scale_figures
#     fig.subplots_adjust(hspace=1, wspace=1)

#     plots_count = len(experiments)
#     nrows = my_nrows(plots_count)
#     ncols = my_ncols(len(experiments))

#     for i in range(plots_count):
#         ax = fig.add_subplot(nrows, ncols, i+1)
#         set_axes_ticks_labels_size(ax, my_fontsize)
#         ax.hist(experiments[i].energy_values_in_iterations_J,
#                 experiments[i].iterations_count)
#         set_title_with_fontsize(
#             ax, f'Energy distr in exp {experiments[i].index}', my_fontsize)
#         set_xlabel_with_fontsize(ax, 'Energy Observation(J)', my_fontsize)
#         set_ylabel_with_fontsize(ax, 'count', my_fontsize)

#     plt.savefig(output_filepath)
#     my_show_plot(show)