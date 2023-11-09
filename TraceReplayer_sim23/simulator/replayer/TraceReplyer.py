import numpy as np
import pandas as pd
from common.DF_helper import insert_new_column_in_df
from common.DictionaryHelper import dictionaryToFile
from common.ListsHelper import deepCopyL1AndExtendWithNoneToMatchL2Size
from simulator.power_models.PowerStateModels import ParentPowerStateModel, constructModel 
from simulator.replayer.df_cols_temp import  colName_model_inst_pow_prediction, colName_refTrace_Power, colName_refTrace_timestamp, colName_trace_power
from simulator.replays_analyzer.trace_replay_analyzer import analyzeResults
   
def initiate_results_df(trace_power_array, reference_trace_power_array, ref_trace_timestamps):#assuming same sampling rate
    trace_power_array_view_extended = deepCopyL1AndExtendWithNoneToMatchL2Size(trace_power_array, reference_trace_power_array) 
    df_results = pd.DataFrame(
        list(
            zip(trace_power_array_view_extended,
                reference_trace_power_array,
                ref_trace_timestamps)
        ), columns=[colName_trace_power(),
                    colName_refTrace_Power(),
                    colName_refTrace_timestamp()
                    ]
    )
    return df_results

# for repeating n times identical experiments
def replayUsingModel( # creates its own results array and does not return it coz it is used for bulk exps(repeat same exp n times for example).
                    trace_power_array,
                    trace2cmp2_timestamp_list,
                    trace_state_full_name,
                    trace_to_cmp2_power_array,
                    bucketSize,
                    modelNameEnum,
                    specificCalibMode, 
                    logFolder=None, logResults=False
                  ): 
    
    df_results_details = initiate_results_df(trace_power_array, trace_to_cmp2_power_array, trace2cmp2_timestamp_list)
    model:ParentPowerStateModel = constructModel(modelNameEnum, specificCalibMode, bucketSize)
        
    return replay(
                    df_results_details,
                    trace_power_array,
                    trace2cmp2_timestamp_list,
                    trace_state_full_name,
                    trace_to_cmp2_power_array,
                    bucketSize,
                    model, logFolder=logFolder, logResults=logResults), model.name, model

def replay(df_results,trace_power_array, trace2cmp2_timestamp_list, trace_state_full_name, compare_to_trace_power_array=None,predictionBucketSize=None, model:ParentPowerStateModel=None, logFolder=None, logResults = False) -> pd.DataFrame:
    
    model.calibrate(stateName=trace_state_full_name,trace_power_array=trace_power_array)
    
    power_prediction = []
    for timestamp in trace2cmp2_timestamp_list:
        p = model.get_power_prediction(trace_state_full_name)
        power_prediction.append(p)

    insert_new_column_in_df(df_results, colName_model_inst_pow_prediction(model.name), power_prediction)# add the mode to the name if it is not NA
    
    dic_resultsSumamry  = analyzeResults(df_results, model.name) # updates df_results and return a summary of that
   
    if logFolder != None and logResults:
        df_results.to_csv(logFolder + "replay_res_details_"+model.name + "_" + trace_state_full_name + ".csv")
        dictionaryToFile(logFolder + "replay_res_summary_"+model.name + "_" + trace_state_full_name + ".csv",dic_resultsSumamry)

    return dic_resultsSumamry 