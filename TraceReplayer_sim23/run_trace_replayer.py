from ast import FunctionDef
import collections
import copy
import os
import statistics
import matplotlib.pyplot as plt
import argparse
import datetime
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from common.FilesHelper import createDir
from common.PlotHelper import my_large_figure, my_ncols, my_nrows, my_show_plot, set_axes_ticks_labels_size, set_title_with_fontsize, set_xlabel_with_fontsize, set_ylabel_with_fontsize
from common.TracePlotter import plot_trace
from simulator.power_models.PowerStateModels import constructModel
from simulator.power_models.Enums import ModelNameEnum, SpecificCalibMode
from simulator.replayer.TraceReplyer import initiate_results_df, replayUsingModel
from simulator.replayer.df_cols_temp import ColName_avg_rel_delta_perct, colName_expId_in_inputTrace, colName_iterationIndex_in_inputTrace, colName_model_inst_pow_prediction
from simulator.replays_analyzer.plotter import plot_exps_histogram_dict_lists_distribution
from simulator.replays_analyzer.trace_replays_analyzer import _append_column__UniqueItersIds_acrossExpsIteration, _colName_count_ellapsedIterations, _colName_crossExpsIterationUniqueIds, int_digits_count, plot_tradeoff_for_all_models_inputsize_and_totalDeltaEnergy
from simulator.replays_analyzer.trace_replays_repeater import replayNTimes_calculatingAvgAndStdevOfAllResults
from simulator.simulator_common import *
from simulator.replayer.TraceReplyer import replay
import csv
from simulator.trace_column_names_in_csv import *
import matplotlib.pyplot as plt
import matplotlib.dates as md
import datetime as dt
import time

def formulate_state_name(trace_state_name, trace_substate_name):
    trace_state_full_name = trace_state_name
    if trace_substate_name != '':
        trace_state_full_name += '-'+trace_substate_name
    return trace_state_full_name

    
def plot_density_kde():
    df_all = pd.DataFrame(
        {  
            'original-trace': trace_power_array_view_extended_withNons_to_match_trace2cmp2_size, 
            'My model prediction':var_aware_probability_distribution_POWER_PREDICTION,
            'uniform-distribution-prediction-between-q1-and-q3': var_aware_UniformDistributionBetweenQ1Q3_POWER_PREDICTION,
            'uniform-distribution-prediction-stdev-around-median': var_aware_uniform_distribution_stdev_avg_POWER_PREDICTION
        }
    )
    ax = df_all.plot.kde() 
    # legend
    plt.xlabel("Trace Power Measurement(W)")
    plt.title("Kernel Density Estimate plot using Gaussian kernels")
    plt.savefig( detailed_log_folder+"/"+executable_run_timestamp+"/"+executable_run_timestamp+"_kde.pdf")


def readReferenceTrace(path_trace_to_compare_to:str, calibrationTrace_power_array):
    trace_to_cmp2_power_array = []
    dataframe_trace_to_cmp2 = None
    if path_trace_to_compare_to.strip()!= '':
        dataframe_trace_to_cmp2=pd.read_csv(path_trace_to_compare_to, parse_dates=True)
        trace_to_cmp2_power_array = dataframe_trace_to_cmp2[power_column_name].tolist()
    else:
        print("Reference trace is not passed. Will use calibration trace for comparison")
        trace_to_cmp2_power_array = calibrationTrace_power_array
    return trace_to_cmp2_power_array,dataframe_trace_to_cmp2

def _add_column__countIterationsIncludedTillCurrentObservation(df):
    if  _colName_crossExpsIterationUniqueIds() not in df.columns:
        _append_column__UniqueItersIds_acrossExpsIteration(df)
    
    newColValues=[]
    count_uniqueIteration=0 
    keyAnchor=-1 # not existing expIdItId key :)
    iterationsKeysForAllObs = df[_colName_crossExpsIterationUniqueIds()]
    count_observation_in_iterationdecimal=0 
    displayStep=25
    progress_in_DisplayStep=0
    for iterationKey in iterationsKeysForAllObs:
        if keyAnchor != iterationKey:
            count_uniqueIteration+=1
            keyAnchor = iterationKey
            progress_in_DisplayStep+=1
            if progress_in_DisplayStep == displayStep:
                newColValues.append(count_uniqueIteration)
                progress_in_DisplayStep=0
            else: # do not display for each iteration in exp
                newColValues.append("")

        else: # do not display for each observation in iteration
            newColValues.append("")
    df['count_ellapsedIterations'] =newColValues 
    pass


if __name__ == "__main__":
    executable_run_timestamp = str(datetime.datetime.now().timestamp())
    
    parser = argparse.ArgumentParser()

    parser.add_argument('--path_original_trace',
                        help='Filepath for original trace. Trace should be ordered chronologically.',
                        default='./_traces/concatinated_cleaned/node1-1688044998.773062-341477 341489 341501 341512 341527 341547 341565 341579 341602 341615-trace.csv',
                        type=str
                        )
    parser.add_argument('--trace_state_name',
                        help='trace_state_name',
                        default='idle',
                        type=str)
    parser.add_argument('--trace_substate_name',
                        help='trace_substate_name. add it if u have substates',
                        default='',
                        type=str)
    parser.add_argument('--path_trace_to_compare_to',
                        help='Filepath for the trace to compare to. Trace should be ordered. exp ids and iterations chronologically as executed.',
                        default='./_traces/concatinated_cleaned/node1-1688044998.773062-341477 341489 341501 341512 341527 341547 341565 341579 341602 341615-trace.csv',
                        type=str)
    parser.add_argument(
        '--num_runs',
        help='How many times you want to repeat each replay? You get avg and stdev of important results then.',
        default=1,
        type=int
    )

    parser.add_argument(
        '--generate_tradeoff_graphs_inputSize_metrics',
        help=" 1 for tradeoff graphs, <1 for normal operation",
        default="1",
        type= int
    )
    parser.add_argument("--verbose_in_tradeoff_exps", action="store_true",
                    help="logEachReplayDetailedResults_for_tradeoff_exps")
    #  The store_true option has a default value of False. 
    #  Whereas, store_false has a default value of True. 
   
    parser.add_argument(
        '--detailed_log_folder',
        help="parent directory for results",
        default="./results",
        type= str
    )

    predictionBucketSize = 5000 
    fontsize = 28
    args = parser.parse_args()

    logEachReplayDetailedResults_for_tradeoff_exps = False
    if args.verbose_in_tradeoff_exps:
        logEachReplayDetailedResults_for_tradeoff_exps=True


    detailed_log_folder = args.detailed_log_folder
    num_runs=int( args.num_runs)
    generate_tradeoff_graphs_inputSize_metrics= args.generate_tradeoff_graphs_inputSize_metrics
    print()
    print("------------------------------------------------------------------------------ ")
    print("Trace replay..")
    print("replay timestamp (executable_run_timestamp): "+ executable_run_timestamp)
    print(args)

    # create program run folder
    createDir(detailed_log_folder+"/"+executable_run_timestamp)
     #--------------------- Read and cleaned traces----------------------------
    # log program arguments
    parser_config_file = open(detailed_log_folder+"/"+executable_run_timestamp+ "/"+executable_run_timestamp+"_run_args.log", "a")
    parser_config_file.write(str(args))
    parser_config_file.close()

    # allow having sub states: "stateName-subStateName"
    trace_state_full_name = formulate_state_name(args.trace_state_name, args.trace_substate_name)
    
    #cleaned no gaps already
    dataframe_model_calibration_trace = pd.read_csv(args.path_original_trace, parse_dates=True) 

    calibration_trace_timestamp_list = dataframe_model_calibration_trace[timestamp_column_name].tolist() # problem here in the dataframe used.
    trace_power_array = dataframe_model_calibration_trace[power_column_name].tolist()   

    # Plot the calibration Trace
    plot_filename_calibrationTrace = detailed_log_folder+"/"+executable_run_timestamp+"/"+executable_run_timestamp+"_" + trace_state_full_name + "_calibration_trace.pdf"
    plot_trace("", plot_filename_calibrationTrace , calibration_trace_timestamp_list, trace_power_array,fontsize=fontsize)
    
    # new calibration trace plot with iteration ellapsed in x axes
    _add_column__countIterationsIncludedTillCurrentObservation(dataframe_model_calibration_trace)
    filename_calibTrace__x_as_countEllapsedUniqIter=detailed_log_folder+"/"+executable_run_timestamp+"/"+executable_run_timestamp+"_" + trace_state_full_name + "_calibration_trace__XaxesIterationsElallpsed.pdf"
    plot_trace("",
               filename_calibTrace__x_as_countEllapsedUniqIter, 
               calibration_trace_timestamp_list,
               trace_power_array,
               xlabels=list(dataframe_model_calibration_trace[_colName_count_ellapsedIterations()]),xlabel="Number of elapsed iterations",fontsize=fontsize)

    # The reference trace
    trace_to_cmp2_power_array,dataframe_trace_to_cmp2 = readReferenceTrace(args.path_trace_to_compare_to, trace_power_array)
    
    # As calibration trace can be shorter from compare-2-trace, we use timestamps from compare-to trace. And generate power measurements matching that length.
    trace2cmp2_timestamp_list = dataframe_trace_to_cmp2[timestamp_column_name].tolist()
    plot_trace("",  detailed_log_folder + "/" + executable_run_timestamp+"/"+executable_run_timestamp+"_"+trace_state_full_name+"_reference_trace.pdf", trace2cmp2_timestamp_list, trace_to_cmp2_power_array, show=True,
               fontsize=fontsize)
    
    # new ref trace plot with iteration ellapsed in x axes
    _add_column__countIterationsIncludedTillCurrentObservation(dataframe_trace_to_cmp2)    
    filename_refTrace__x_as_countEllapsedUniqIter=detailed_log_folder+"/"+executable_run_timestamp+"/"+executable_run_timestamp+"_" + trace_state_full_name + "_reference_trace__XaxesIterationsElallpsed.pdf"
    plot_trace("",
               filename_refTrace__x_as_countEllapsedUniqIter, 
               trace2cmp2_timestamp_list,
               trace_to_cmp2_power_array,
               xlabels=list(dataframe_trace_to_cmp2[_colName_count_ellapsedIterations()]),xlabel="Number of elapsed iterations",fontsize=fontsize)
    
    print("\nlen(trace_power_array): " + str(len(trace_power_array)))
    print("trace_to_cmp2_power_array: " + str(len(trace_to_cmp2_power_array)))
    print("power array for reference-trace size is " + str(len(trace_to_cmp2_power_array) /len(trace_power_array) ) + " times calibration-trace size")
    print()
    print("detailed_log_folder: " + detailed_log_folder)
    print()

    #---------------------- End Read and cleaned traces-----------------------------------------------------

    # --------------------- Program in mode repeating many experiments for all models ----------------------
    modelEnums = [ModelNameEnum.STATIC, ModelNameEnum.EMPIRICAL_DIST, ModelNameEnum.UNIFORM_Q1_Q3, ModelNameEnum.UNIFORM_AVG_STDEV]
    if num_runs > 1:
        #run n times one model and report values.
        #2nd. run n times multiple models and report value per each. # can do it one after the other. but code not dynamic then, or can do dynamic code
        exp_id_key='modelName'
        for modelEnum in modelEnums:
            if modelEnum == ModelNameEnum.STATIC:
                model_Mode_MEDIAN = SpecificCalibMode._MEDIAN
                replayNTimes_calculatingAvgAndStdevOfAllResults(num_runs=num_runs,
                                                        exp_identifier_key=exp_id_key,
                                                        exp_method_returning_results_dict_and_expId=replayUsingModel,
                                                        trace_power_array=trace_power_array,
                                                        trace2cmp2_timestamp_list=trace2cmp2_timestamp_list,
                                                        trace_state_full_name=trace_state_full_name,
                                                        trace_to_cmp2_power_array=trace_to_cmp2_power_array,
                                                        bucketSize=None,
                                                        modelNameEnum=modelEnum,
                                                        specificCalibMode=model_Mode_MEDIAN
                                                        )
                model_Mode_MEAN = SpecificCalibMode._MEAN
                replayNTimes_calculatingAvgAndStdevOfAllResults(num_runs=num_runs,
                                                        exp_identifier_key=exp_id_key,
                                                        exp_method_returning_results_dict_and_expId=replayUsingModel,
                                                        trace_power_array=trace_power_array,
                                                        trace2cmp2_timestamp_list=trace2cmp2_timestamp_list,
                                                        trace_state_full_name=trace_state_full_name,
                                                        trace_to_cmp2_power_array=trace_to_cmp2_power_array,
                                                        bucketSize=None,
                                                        modelNameEnum=modelEnum,
                                                        specificCalibMode=model_Mode_MEAN
                                                        )
            else:
                replayNTimes_calculatingAvgAndStdevOfAllResults(num_runs=num_runs,
                                                        exp_identifier_key=exp_id_key,
                                                        exp_method_returning_results_dict_and_expId=replayUsingModel,
                                                        trace_power_array=trace_power_array,
                                                        trace2cmp2_timestamp_list=trace2cmp2_timestamp_list,
                                                        trace_state_full_name=trace_state_full_name,
                                                        trace_to_cmp2_power_array=trace_to_cmp2_power_array,
                                                        bucketSize=predictionBucketSize,
                                                        modelNameEnum=modelEnum,
                                                        specificCalibMode=SpecificCalibMode.NA
                                                        )
        exit() 
    # --------------------- End Program in mode repeating many experiments for all models ----------------------
    
    # --------------------- Program in mode of doing tradeoff experiments for trace input size and metrics ----------------------
    if generate_tradeoff_graphs_inputSize_metrics >= 1 :
        plot_tradeoff_for_all_models_inputsize_and_totalDeltaEnergy(modelEnums,
                                                                    dataframe_model_input_trace =  dataframe_model_calibration_trace,
                                                                    trace_to_cmp2_power_array = trace_to_cmp2_power_array, 
                                                                    trace2cmp2_timestamp_list = trace2cmp2_timestamp_list, 
                                                                    detailed_log_folder = detailed_log_folder,
                                                                    executable_run_timestamp = executable_run_timestamp,
                                                                    fontsize = fontsize,
                                                                    predictionBucketSize = predictionBucketSize,
                                                                    trace_state_full_name = trace_state_full_name,
                                                                    logEachReplayResult= logEachReplayDetailedResults_for_tradeoff_exps)
        exit() 
    # --------------------- END Program in mode of doing tradeoff experiments for trace input size and metrics ----------------------
   

    # ----------------------- Program in mode of conducting one single replay for models (refactor todo in display) -------------------------------------------------------
 
    df_results_details = initiate_results_df(trace_power_array, trace_to_cmp2_power_array, trace2cmp2_timestamp_list)
        
    model_static_avg = constructModel(ModelNameEnum.STATIC, SpecificCalibMode._MEAN,None)
    df_summary_res_static= replay( 
        df_results_details,
        trace_power_array,
        trace2cmp2_timestamp_list,
        trace_state_full_name,
        trace_to_cmp2_power_array, 
        None,
        model_static_avg)
    staticPowerStatModelTracePrediction = list(df_results_details[colName_model_inst_pow_prediction(model_static_avg.name)]) #list()

    trace_power_array_view_extended_withNons_to_match_trace2cmp2_size = df_results_details['trace_power']

    model_uniform_dist_q1_q3 = constructModel(ModelNameEnum.UNIFORM_Q1_Q3,None,predictionBucketSize)
    df_summary_res_uniformDist_Q1_Q3= replay(
        df_results_details, 
        trace_power_array,
        trace2cmp2_timestamp_list, 
        trace_state_full_name,
        trace_to_cmp2_power_array,
        predictionBucketSize,
        model_uniform_dist_q1_q3)
    var_aware_UniformDistributionBetweenQ1Q3_POWER_PREDICTION=list(df_results_details[colName_model_inst_pow_prediction(model_uniform_dist_q1_q3.name)])
    
    model_uniform_dist_stdev_avg = constructModel(ModelNameEnum.UNIFORM_AVG_STDEV, None, predictionBucketSize)
    df_summary_res_uniform_dist_stdev_avg= replay(
        df_results_details,
        trace_power_array,
        trace2cmp2_timestamp_list,
        trace_state_full_name,
        trace_to_cmp2_power_array,
        predictionBucketSize,
        model_uniform_dist_stdev_avg)
    var_aware_uniform_distribution_stdev_avg_POWER_PREDICTION = list(df_results_details[colName_model_inst_pow_prediction(model_uniform_dist_stdev_avg.name)])

    model_empiricalDist = constructModel(ModelNameEnum.EMPIRICAL_DIST,None,predictionBucketSize)
    df_summary_res_empiricalDist= replay( 
        df_results_details,
        trace_power_array,
        trace2cmp2_timestamp_list,
        trace_state_full_name,
        trace_to_cmp2_power_array,
        predictionBucketSize,
        model_empiricalDist)
    var_aware_probability_distribution_POWER_PREDICTION = list(df_results_details[colName_model_inst_pow_prediction(model_empiricalDist.name)])
   
    # save the results
    df_results_details.to_csv(
        detailed_log_folder+"/"+executable_run_timestamp+"models-predictions.csv")
    print("replay-details logged in: "+  detailed_log_folder+"/"+executable_run_timestamp+"models-predictions.csv")
