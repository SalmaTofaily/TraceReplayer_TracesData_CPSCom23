
from ast import Dict

import numpy as np
from common.DF_helper import add_column_absoluteValOfDeltaOf2cols_in_dataframe, add_column_relative_delta_perc_of_2_cols_in_dataframe
from simulator.replayer.df_cols_temp import ColName__delta_in_total_energy__btwn_refTrace_and_predictedTrace, ColName_avg_rel_delta_perct, ColName_rel_delta_perct, colName_inst_delta_power, colName_model_inst_pow_prediction, colName_refTrace_Power, colName_refTrace_timestamp, colName_trace_power


def analyzeInstResults(df_results, model_name:str):
    # model_name: static, var-aware-uniform-dist-q1-q3, var-aware-uniform-dist-avg-stdev, var-aware-pobability-distribution
    colName_powerPrediction = colName_model_inst_pow_prediction(model_name) 
    colName_refTrace = colName_refTrace_Power()
    colName_instntDeltaPow = colName_inst_delta_power(model_name)

    add_column_absoluteValOfDeltaOf2cols_in_dataframe(df_results,
                                                      colName_powerPrediction,
                                                      colName_refTrace,
                                                      colName_instntDeltaPow)

    # todo change column name to be more readable
    colName_InstRelChngPerc_PredictionAndReferenceTrace='rel-delta-perct_'+model_name+'_pow-state-model-prediction_wrt_cmp2Trace'
    add_column_relative_delta_perc_of_2_cols_in_dataframe(df_results,
                                                          colName_powerPrediction,
                                                          colName_refTrace,
                                                          colName_InstRelChngPerc_PredictionAndReferenceTrace)
    pass

def analyzeResults(df_results, modelName) -> Dict:
    analyzeInstResults(model_name=modelName, df_results=df_results)
    avg_rel_delta_perct = df_results[ColName_rel_delta_perct(modelName)].mean()
    delta_in_total_energy__btwn_refTrace_and_predictedTrace = deltaOfTotalEnergy__BtwnPredictedTraceAndRefTrace(df_results, modelName)
    return {
        ColName_avg_rel_delta_perct(): avg_rel_delta_perct,
        ColName__delta_in_total_energy__btwn_refTrace_and_predictedTrace(): delta_in_total_energy__btwn_refTrace_and_predictedTrace,
        'modelName':modelName
        # 'replay_timestamp': replay_timestamp,
        # 'modelMode':modelMode
    }

def deltaOfTotalEnergy__BtwnPredictedTraceAndRefTrace(df_results, modelName):
    abs=False
    ref_trace_power = df_results[colName_refTrace_Power()].tolist()
    trace_predicted_power = df_results[colName_model_inst_pow_prediction(modelName)].tolist()
    timestamp_list_refTrace = df_results[colName_refTrace_timestamp()].tolist()
    TotEnergy_refTrace = np.trapz(ref_trace_power, timestamp_list_refTrace)
    TotEnergy_predicTrace = np.trapz(trace_predicted_power, timestamp_list_refTrace)
    delta_TotEnergy__PredTrace_vs_RefTrace = TotEnergy_predicTrace-TotEnergy_refTrace
    return delta_TotEnergy__PredTrace_vs_RefTrace