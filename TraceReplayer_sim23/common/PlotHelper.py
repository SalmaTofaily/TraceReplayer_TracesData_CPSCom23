

import pandas as pd
import matplotlib.pyplot as plt

from models.settings import *
import matplotlib.pyplot as plt
from matplotlib import cm
from .myColors import arr_color_blind

def my_show_plot(show_allowed):
    if show_allowed:
        plt.show()  # save should always be called before show (  # https://mldoodles.com/matplotlib-saves-blank-plot/ )

def get_cmap(n, name='virdis'): # default is virdis #https://cran.r-project.org/web/packages/viridis/vignettes/intro-to-viridis.html
    return  cm.get_cmap(name, n) 

def set_axes_ticks_labels_size(ax, my_fontsize):
    ax.tick_params(axis='x', labelsize=my_fontsize)
    ax.tick_params(axis='y', labelsize=my_fontsize)

def set_axeslabels_with_fontsize(ax, x_label, y_label, my_fontsize):
    ax.set_xlabel(x_label, fontsize = my_fontsize)
    ax.set_ylabel(y_label,fontsize = my_fontsize)

def set_axes_ticks_labels_size(ax, my_fontsize):
    ax.tick_params(axis='x', labelsize=my_fontsize)
    ax.tick_params(axis='y', labelsize=my_fontsize)

def set_title_with_fontsize(ax, txt, my_fontsize):
    ax.set_title(txt, fontsize=my_fontsize)

def set_xlabel_with_fontsize(ax, txt, my_fontsize):
    ax.set_xlabel(txt, fontsize=my_fontsize)

def set_ylabel_with_fontsize(ax, txt, my_fontsize):
    ax.set_ylabel(txt, fontsize=my_fontsize)

def set_legend_with_fontsize(ax, legend, my_fontsize):
    ax.legend(legend, prop={'size': my_fontsize})

def double_plot_size():
    figure_size = plt.gcf().get_size_inches()
    factor = 2
    plt.gcf().set_size_inches(factor * figure_size)

def adjust_save_plot(output_figure_name):
    # plt.tight_layout()
    # double_plot_size()
    plt.savefig(output_figure_name)
    # show should be used once in a python session, at the end.

def mysubplot():
    return plt.subplots(figsize=(32, 18))

def mysubplot(w=16, h=9, rows_count=1, cols_count=1):  # inches
    return plt.subplots(rows_count, cols_count, figsize=(w, h))

def my_large_figure():
    return plt.figure(figsize=(32, 18))

# called many times, but it is ok for now.
def my_nrows(plots_count):
    cols_count = my_ncols(plots_count)
    n_rows = plots_count//cols_count
    if plots_count % cols_count != 0:
        n_rows = n_rows + 1
    return n_rows

def my_ncols(plots_count):
    if plots_count < settings.subplots_ncols:
        return plots_count
    return settings.subplots_ncols

def plot_line_graph_reusable(x_list,x_label,y1_list,y1_label, title, my_fontsize, output_path_wihtout_lastName, lastName):
    fig, ax = mysubplot()
    ax.plot(x_list, y1_list, label = y1_label)
    if my_fontsize != None:
        set_axes_ticks_labels_size(ax, my_fontsize)
        set_title_with_fontsize(ax,title , my_fontsize)
        set_xlabel_with_fontsize(ax,x_label , my_fontsize)
        set_ylabel_with_fontsize(ax, y1_label, my_fontsize)
    else:
        ax.set_title(title)
        ax.set_ylabel(y1_label)
        ax.set_xlabel(x_label)
    # plt.legend()
    file_path=output_path_wihtout_lastName + lastName
    plt.savefig(file_path)
    # plt.show()
    print("_plot_trafeoff_figure figure saved in " + file_path)
    pass


def plot_line_graph_reusable_manyDFs(x_colName,x_label,y1_colName,y1_label, dataframes, labels_for_dataframes, title, my_fontsize, output_path_wihtout_lastName, lastName, y2_colName=None,y2_label=None):
    # dataframes and labels_for_dataframes elements have corresponding related indexes. So label 1 is for df 1
    fig, ax = mysubplot()
    ax2= None
    if y2_colName is not None:
        ax2 = ax.twinx()
        ax2.set_ylabel(y2_label)  # we already handled the x-label with ax1

    #loop bychatgbt
    i_color= 0
    linewidth=3
    for i, df in enumerate(dataframes):
        ax.plot(df[x_colName], df[y1_colName], label = labels_for_dataframes[i], color= arr_color_blind[i_color], linewidth=linewidth)
        if y2_colName is not None:
            ax2.plot(df[x_colName], df[y2_colName], label = labels_for_dataframes[i], color= arr_color_blind[i_color], linewidth=linewidth)
            ax2.tick_params(axis='y')
        
        i_color+= 1

    if my_fontsize != None:
        set_axes_ticks_labels_size(ax, my_fontsize)
        set_title_with_fontsize(ax,title , my_fontsize)
        set_xlabel_with_fontsize(ax,x_label , my_fontsize)
        set_ylabel_with_fontsize(ax, y1_label, my_fontsize)
        if y2_colName is not None:
            set_axes_ticks_labels_size(ax2, my_fontsize)
            set_ylabel_with_fontsize(ax2, y2_label, my_fontsize)
    else:
        ax.set_title(title)
        ax.set_ylabel(y1_label)
        ax.set_xlabel(x_label)
        if y2_colName is not None:
            ax2.set_ylabel(y2_label)

   
    # Shrink current axis by 20%
    # box = ax.get_position()
    # ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])

    # # Put a legend to the right of the current axis
    # ax.legend(fontsize= my_fontsize, loc='center left',bbox_to_anchor=(1, 0.5))

    # Shrink current axis's height by 10% on the bottom
    # box = ax.get_position()
    # ax.set_position([box.x0, box.y0 + box.height * 0.2,
    #              box.width, box.height * 0.8])

    # Put a legend below current axis
    # ax.legend(fontsize= my_fontsize,loc= 'upper center', bbox_to_anchor=(0.5, 1.3), ncol=2)

           #   loc='lower center', bbox_to_anchor=(0.5, -0.15), ncol=3)
    ax.legend(fontsize= my_fontsize,loc= 'center right')
    file_path=output_path_wihtout_lastName + lastName
    plt.savefig(file_path)
    # plt.show()
    print("_plot_trafeoff_figure figure saved in " + file_path)
    pass
     
def my_nrows(plots_count, cols_count):
    n_rows = plots_count//cols_count
    if plots_count % cols_count != 0:
        n_rows = n_rows + 1
    return n_rows
