import random
import statistics

import matplotlib.pyplot as plt
import pandas as pd
from common import TimeHelper
from common.DF_helper import appendRowToDF, create_combined_dataframe_each_of_1_row
from common.FilesHelper import createDir

from common.PlotHelper import mysubplot, plot_line_graph_reusable, plot_line_graph_reusable_manyDFs, set_axes_ticks_labels_size, set_title_with_fontsize, set_xlabel_with_fontsize, set_ylabel_with_fontsize
from common.stat_helper import int_digits_count
from simulator.power_models.Enums import ModelNameEnum, SpecificCalibMode
from simulator.replayer.TraceReplyer import replayUsingModel
from simulator.replayer.df_cols_temp import ColName__delta_in_total_energy__btwn_refTrace_and_predictedTrace, ColName_avg_rel_delta_perct, colName_expId_in_inputTrace, colName_iterationIndex_in_inputTrace, colName_trace_power, colName_measured_power_in_inputTrace

def plot_tradeoff_for_all_models_inputsize_and_totalDeltaEnergy(modelEnums, dataframe_model_input_trace, 
                                                                  trace_to_cmp2_power_array,
                                                                  trace2cmp2_timestamp_list,
                                                                  detailed_log_folder,
                                                                  executable_run_timestamp,
                                                                  fontsize,
                                                                  predictionBucketSize, 
                                                                  trace_state_full_name, logEachReplayResult=False):# todo pass metric name and y label :) or generate here all the graphs for other metrics
        print("start tradeoff_for_all_models_inputsize_and_totalDeltaEnergy at " + TimeHelper.now_readable())
        dataframes_results_array = [] 
        modelFullNames=[]

        for modelEnum in modelEnums:
            if modelEnum == ModelNameEnum.STATIC:
                model_Mode_MEDIAN = SpecificCalibMode._MEDIAN
                df_results, modelName = _trafeoff_calibInputLength_deltaEnrgyOfPredictionAndComp2Trace(modelNameEnum=modelEnum,
                                                                  specificCalibMode=model_Mode_MEDIAN,
                                                                  trace_state_full_name=trace_state_full_name,
                                                                  predictionBucketSize =predictionBucketSize,
                                                                  dataframe__target_calibration_trace=dataframe_model_input_trace,
                                                                  trace_to_cmp2_power_array=trace_to_cmp2_power_array,
                                                                  trace2cmp2_timestamp_list=trace2cmp2_timestamp_list,
                                                                  detailed_log_folder=detailed_log_folder,
                                                                  executable_run_timestamp=executable_run_timestamp,
                                                                  logEachReplayResult=logEachReplayResult
                                                                  )
                dataframes_results_array.append(df_results)
                modelFullNames.append(modelName)
                
                model_Mode_MEAN = SpecificCalibMode._MEAN
                df_results, modelName = _trafeoff_calibInputLength_deltaEnrgyOfPredictionAndComp2Trace(modelNameEnum=modelEnum,
                                                                  specificCalibMode=model_Mode_MEAN,
                                                                  trace_state_full_name=trace_state_full_name,
                                                                  predictionBucketSize =predictionBucketSize,
                                                                  dataframe__target_calibration_trace=dataframe_model_input_trace, 
                                                                  trace_to_cmp2_power_array=trace_to_cmp2_power_array,
                                                                  trace2cmp2_timestamp_list=trace2cmp2_timestamp_list,
                                                                  detailed_log_folder=detailed_log_folder,
                                                                  executable_run_timestamp=executable_run_timestamp,
                                                                  logEachReplayResult=logEachReplayResult
                                                                  )
                dataframes_results_array.append(df_results)
                modelFullNames.append(modelName)
            else:
                df_results, modelName = _trafeoff_calibInputLength_deltaEnrgyOfPredictionAndComp2Trace(modelNameEnum=modelEnum,
                                                                  specificCalibMode=SpecificCalibMode.NA,
                                                                  trace_state_full_name=trace_state_full_name,
                                                                  predictionBucketSize =predictionBucketSize,
                                                                  dataframe__target_calibration_trace=dataframe_model_input_trace, 
                                                                  trace_to_cmp2_power_array=trace_to_cmp2_power_array,
                                                                  trace2cmp2_timestamp_list=trace2cmp2_timestamp_list,
                                                                  detailed_log_folder=detailed_log_folder,
                                                                  executable_run_timestamp=executable_run_timestamp,
                                                                  logEachReplayResult=logEachReplayResult
                                                                  )
                dataframes_results_array.append(df_results)
                modelFullNames.append(modelName)

        fileLastName="_"+trace_state_full_name+"__tradeoff_calibTraceSize_TotalEnergyDelta_PredictionRefTrace.pdf"
        output_graph_path_nolastname = detailed_log_folder + "/" + executable_run_timestamp + "/" + executable_run_timestamp

        
        x_colName = "input_trace__iterations_count"
        y1_colName ="delta_E_total__prediction_com2Trace"
        y1_label="Delta Energy (J)"
        # save in file the results, so if we want to change the graph there is no need to wait all that time again. timestamp.
        # df_tradeoff__results=create_combined_dataframe_each_of_1_row(dataframes_results_array, x_colName, y1_colName) # can use this results later down to plot. todo
        # df_tradeoff__results.to_csv(output_graph_path_nolastname+"__trafeoff_exps_dataframe.csv")
        # print("trafeoff_exps_results logged in: "+output_graph_path_nolastname+"__trafeoff_exps_dataframe.csv")
        # todo fix.
        # index is wrong here because we define i from 1 to n? no index work. it is relative to sec
        x_label="Index of last iteration in calibration trace"
        plot_line_graph_reusable_manyDFs(# this can be from one df(df_tradeoff__results)todo enahance. ont priority
                                         y1_colName =y1_colName,
                                         y1_label =  y1_label,
                                         x_colName = x_colName,
                                         x_label = x_label,
                                         labels_for_dataframes = modelFullNames,
                                         dataframes = dataframes_results_array,
                                         title = "",
                                         my_fontsize =fontsize,
                                         output_path_wihtout_lastName = output_graph_path_nolastname,
                                         lastName = fileLastName
                                         )
        print("plot_tradeoff_for_all_models_inputsize_and_totalDeltaEnergy - end " + TimeHelper.now_readable())
        
        
        file2LastName="_"+trace_state_full_name+"__tradeoff_calibTraceSize_TotalTimeEquivOfEnergyDelta_PredictionRefTrace.pdf"
        # plot time graphs
        y2_colName="equiv_delta_Time__for_delta_E_in_a_month_h"
        y2_label ="Eqiuvalent monthly delta time (h)"
        plot_line_graph_reusable_manyDFs(# this can be from one df(df_tradeoff__results)todo enahance. ont priority
                                         y1_colName =y2_colName,
                                         y1_label =  y2_label,
                                         x_colName = x_colName,
                                         x_label = x_label,
                                         labels_for_dataframes = modelFullNames,
                                         dataframes = dataframes_results_array,
                                         title = "",
                                         my_fontsize =fontsize,
                                         output_path_wihtout_lastName = output_graph_path_nolastname,
                                         lastName = file2LastName
                                         )
        print("plot_tradeoff_for_all_models_inputsize_and_totalDeltaEnergy - end " + TimeHelper.now_readable())

           
        file3LastName="_"+trace_state_full_name+"__tradeoff_calibTraceSize_Mixed_PredictionRefTrace.pdf"
        # plot time graphs
        
        plot_line_graph_reusable_manyDFs(# this can be from one df(df_tradeoff__results)todo enahance. ont priority
                                        y1_colName = y1_colName,
                                         y1_label =  y1_label,
                                         y2_colName =y2_colName,
                                         y2_label =  y2_label,
                                         x_colName = x_colName,
                                         x_label = x_label,
                                         labels_for_dataframes = modelFullNames,
                                         dataframes = dataframes_results_array,
                                         title = "",
                                         my_fontsize =fontsize,
                                         output_path_wihtout_lastName = output_graph_path_nolastname,
                                         lastName = file3LastName
                                         )
        print("plot_tradeoff_for_all_models_inputsize_and_totalDeltaEnergy - end " + TimeHelper.now_readable())


        file4LastName="_"+trace_state_full_name+"__tradeoff_calibTraceSize_Mixed_short_PredictionRefTrace.pdf"
        # plot time graphs
        y2_label ="Monthly delta idle time (h)"
        plot_line_graph_reusable_manyDFs(# this can be from one df(df_tradeoff__results)todo enahance. ont priority
                                        y1_colName = y1_colName,
                                         y1_label =  y1_label,
                                         y2_colName =y2_colName,
                                         y2_label =  y2_label,
                                         x_colName = x_colName,
                                         x_label = x_label,
                                         labels_for_dataframes = modelFullNames,
                                         dataframes = dataframes_results_array,
                                         title = "",
                                         my_fontsize =fontsize,
                                         output_path_wihtout_lastName = output_graph_path_nolastname,
                                         lastName = file4LastName
                                         )
        print("plot_tradeoff_for_all_models_inputsize_and_totalDeltaEnergy - end " + TimeHelper.now_readable())

        
        exit() 

def _trafeoff_calibInputLength_deltaEnrgyOfPredictionAndComp2Trace(
                                        dataframe__target_calibration_trace,
                                        trace_to_cmp2_power_array,
                                        trace2cmp2_timestamp_list,     
                                        detailed_log_folder,
                                        executable_run_timestamp,
                                        predictionBucketSize, modelNameEnum, specificCalibMode, trace_state_full_name,
                                        logEachReplayResult=False):
    # Function that experiment from many replays, calibration size changes each time: from 1 iteration till max iteration in dataframe__target_calibration_trace
    
    # save results of the tradeoff experiments for the model
    folderStartingPath= detailed_log_folder + "/" + executable_run_timestamp + "/replayLogs/"
    createDir(detailed_log_folder + "/" + executable_run_timestamp + "/replayLogs/")
    
    counter=0
    # print("Number of exps in original calibration trace: "+ str(len(dataframe__target_calibration_trace[colName_expId_in_inputTrace()].unique())))
    DF_RSLTS__trafeoff_itrsCount_delta_E = pd.DataFrame(columns=['simulation_id',
                                                                 'input_trace__iterations_count',#
                                                                 'input_trace__measurements_count',#
                                                                 'reference_trace_measurements_count',
                                                                 'delta_E_total__prediction_com2Trace',#
                                                                 'equiv_delta_Time__for_delta_E_in_a_month_h',
                                                                 'avgPower_Ref_Trace',
                                                                 'ref_trace_duration_h',
                                                                 'debug_pointer_at_acrossExpsIterationUniqueId',
                                                                 'calibrationsDetails',
                                                                 'modelNameAndMode'])
   
    # input trace will be processed already but no pb by keeping this check here as it is needed.
    if  _colName_crossExpsIterationUniqueIds() not in dataframe__target_calibration_trace.columns: # the method could be called many times, and it is updating the input trace, one time adding the col is enoup.
        # prepare data to step one iteration at a time
        _append_column__UniqueItersIds_acrossExpsIteration(dataframe__target_calibration_trace)
    
    for acrossExpsIterationUniqueId in dataframe__target_calibration_trace[_colName_crossExpsIterationUniqueIds()].unique():
        # select all the rows with crossExpsIterationUniqueIds equals or less the current one.

        df__curr_calib_input_trace = dataframe__target_calibration_trace.query( # todo use name _colName_crossExpsIterationUniqueIds()
            "crossExpsIterationUniqueIds <= @acrossExpsIterationUniqueId") ##############new calibration each time. this assumes that experiments are ordered in ascending order in the trace. handled input trace
        
        this_replay_folder_log=""
        if logEachReplayResult:
            replayLogsFolder= folderStartingPath + "/replays/"
            createDir(replayLogsFolder)
            this_replay_folder_log =replayLogsFolder+"/" + str(counter)+"/"
            createDir(this_replay_folder_log)
        
        # input trace should be new each time coz each time new columns are added and i do not want to have repeated cols problems.
        results_summary_dict, modelName, model = replayUsingModel(  # creates a new copy of the df inside
                    trace_power_array = list(df__curr_calib_input_trace[ colName_measured_power_in_inputTrace()]),
                    # returns the delta energy for now between prediction and calibration - todo later support other needed things
                    trace2cmp2_timestamp_list=trace2cmp2_timestamp_list,
                    trace_state_full_name = trace_state_full_name,
                    trace_to_cmp2_power_array = trace_to_cmp2_power_array,
                    bucketSize = predictionBucketSize,
                    modelNameEnum = modelNameEnum,
                    specificCalibMode = specificCalibMode, 
                    logFolder=this_replay_folder_log,
                    logResults=logEachReplayResult 
                  )
        delta_E_total__prediction_cmp2Trace =results_summary_dict[ColName__delta_in_total_energy__btwn_refTrace_and_predictedTrace()]
        # can do the same for:  ColName_avg_rel_delta_perct()
        # not dynamic here for metrics. but fine now

        avgPower_Ref_Trace = statistics.mean(trace_to_cmp2_power_array)
       
        ref_trace_duration_seconds =trace2cmp2_timestamp_list[-1]-trace2cmp2_timestamp_list[0] 
        ref_trace_duration_h=ref_trace_duration_seconds/3600
        delta_time_for__equiv_deltaE_in_month=(delta_E_total__prediction_cmp2Trace*30*24*60*60)/(ref_trace_duration_seconds*avgPower_Ref_Trace)
        delta_time_for__equiv_deltaE_in_month_h=delta_time_for__equiv_deltaE_in_month/3600
        # add the results in the df, each exp in a row
        new_row_dic = {
            'simulation_id': counter,
            # len(df__curr_calib_input_trace.index), # grows in each simulation
            'input_trace__iterations_count': df__curr_calib_input_trace[_colName_crossExpsIterationUniqueIds()].nunique(), # _colName_crossExpsIterationUniqueIds()
            'input_trace__measurements_count': len(df__curr_calib_input_trace.index),
            'reference_trace_measurements_count': len(trace_to_cmp2_power_array),
            'delta_E_total__prediction_com2Trace': delta_E_total__prediction_cmp2Trace,
            'equiv_delta_Time__for_delta_E_in_a_month_h':delta_time_for__equiv_deltaE_in_month_h,
            'avgPower_Ref_Trace':avgPower_Ref_Trace,
            'ref_trace_duration_h':ref_trace_duration_h,
            'debug_pointer_at_acrossExpsIterationUniqueId': acrossExpsIterationUniqueId,
            'calibrationsDetails':model.StateDictionary[trace_state_full_name].toString(),
            'modelNameAndMode': modelName
        }

        DF_RSLTS__trafeoff_itrsCount_delta_E = appendRowToDF(new_row_dic, DF_RSLTS__trafeoff_itrsCount_delta_E)
        counter += 1
        pass

    DF_RSLTS__trafeoff_itrsCount_delta_E.to_csv(folderStartingPath + "Tradeoffs_summary_" + modelName + ".csv")
    dataframe__target_calibration_trace.to_csv(folderStartingPath + "TargetCalibTrace"+ modelName +".csv")
    return DF_RSLTS__trafeoff_itrsCount_delta_E, modelName

def _colName_crossExpsIterationUniqueIds():
    return 'crossExpsIterationUniqueIds'

def _colName_count_ellapsedIterations():
        return 'count_ellapsedIterations'

def _append_column__UniqueItersIds_acrossExpsIteration(df):
     #FIXING AN ID THAT IS ITERABLE, ORDERED, WE CAN LOOP OVER EXPERIMENTS ITERATIONS
    max_iteration_index = df[colName_iterationIndex_in_inputTrace()].max()
    digit_count_of_max_iteration_index =  int_digits_count(max_iteration_index)
    # add new column expId*10**n+iterationid
    if not df[colName_expId_in_inputTrace()].is_monotonic:
        print("input trace experiments are not sorted in expId")
        exit()
    crossExpsIterationUniqueIds = df[colName_expId_in_inputTrace()] * pow(10,digit_count_of_max_iteration_index) + df[colName_iterationIndex_in_inputTrace()]
    df[_colName_crossExpsIterationUniqueIds()] = crossExpsIterationUniqueIds


def mock_replay_model_on_dataframe(dataframe_model_input_trace, dataframe_model_calibration_trace) -> int:
    # returns the delta energy for now between prediction and calibration - todo later support other needed things
    # randomize
    print("random()")
    return random.randint(10, 100)

# def _plot_trafeoff_figure(df,x_list,x_label,y1_list,y1_label,y2_list,y2_label, title):  
def _plot_trafeoff_figure(x_list,x_label,y1_list,y1_label, title, my_fontsize, output_path_wihtout_lastName):
    output_file__last_name="__tradeoff_calibrationTraceSize_EnergyDeltaPredictionCmp2Trace.pdf"
    plot_line_graph_reusable(x_list,x_label,y1_list,y1_label, title, my_fontsize, output_path_wihtout_lastName, output_file__last_name)
 



 #https://sparkbyexamples.com/pandas/pandas-filter-by-column-value/
    # unique_exp_ids = dataframe_model_input_trace["exp_id"].unique() 
    # for exp_id in  unique_exp_ids:
    #     df_curr_exp= dataframe_model_input_trace.query("exp_id == @exp_id")
    #     curr_iteration_index = 0

    #     # loop over iterations
    #     # df_curr_exp= dataframe_model_input_trace.query("iteration_index <= @curr_iteration_index and exp_id == @exp_id")
    #     print(max_iteration_index)
    #     t = df_curr_exp["measured_power"].tolist()
    #     df_curr_exp.to_csv("test.csv")
    #     pass
  
    # but we have multiple experiments too, so i need to loop over all unique expid_iteration_index
    # detailed_log_folder+"/"+executable_run_timestamp+"models-predictions.csv")

# def trafeoff_calibInputLength_deltaEnrgyOfPredictionAndComp2Trace(dataframe_model_input_trace, 
#                                                                   trace_to_cmp2_power_array,
#                                                                   trace2cmp2_timestamp_list,
#                                         detailed_log_folder,
#                                         executable_run_timestamp,
#                                         fontsize,
#                                         predictionBucketSize, modelNameEnum, specificCalibMode,
#                                         trace_state_full_name
#                                         ):
#     df_results, modelName = _trafeoff_calibInputLength_deltaEnrgyOfPredictionAndComp2Trace(
#                                         dataframe_model_input_trace,
#                                         trace_to_cmp2_power_array,
#                                         trace2cmp2_timestamp_list,
#                                         detailed_log_folder,
#                                         executable_run_timestamp, 
#                                         predictionBucketSize, modelNameEnum, specificCalibMode,
#                                         trace_state_full_name
#                                         )
#     x_list = list(df_results['input_trace__iterations_count'])
#     y_list = list(df_results['delta_E_total__prediction_com2Trace']) 
#     title = "Replays Results: Tradeoff between input trace size and TotalEnergyDelta (between prediction and compare-to-trace)"
#     x_label = "Calibration trace size:iterations count" # size #("Replay index") or seconds
#     y_label = "Total Energy Delta(J)"
#     output_graph_path_nolastname = detailed_log_folder + "/" + executable_run_timestamp + "/" + executable_run_timestamp + "_model_" + modelName + "_"
#     _plot_trafeoff_figure( x_list, x_label, y_list, y_label, title, fontsize, output_graph_path_nolastname)
