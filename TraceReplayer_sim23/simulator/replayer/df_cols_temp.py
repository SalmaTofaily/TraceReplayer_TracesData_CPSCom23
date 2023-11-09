

# raw trace file  ### this can vary depending on input trace vsc
def colName_measured_power_in_inputTrace():
    return 'measured_power'
def colName_expId_in_inputTrace(): # a trace can be a concatenation of multiple experiments, each of multiple iterations
    return 'exp_id'

def colName_iterationIndex_in_inputTrace():
    return "iteration_index"



# df results details cols (min exp setup, inst results)

def colName_model_inst_pow_prediction(modelName):
    return modelName+'_pow-state-model-prediction'

def ColName_rel_delta_perct(modelName):
    return "rel-delta-perct_" + modelName + "_pow-state-model-prediction_wrt_cmp2Trace"

def colName_inst_delta_power(model_name):    
    return 'delta_POW_' + model_name + '_pow-state-model-prediction_wrt_cmp2Trace'

def colName_trace_power():
    return 'trace_power'

def colName_refTrace_Power():
    return 'cmp2Trace'

def colName_refTrace_timestamp():
    return 'timestamp_for_refTrace'

# summary df cols
def ColName_avg_rel_delta_perct(): # power or energy?
    return "average_of__rel_delta_percentage__of_prediction_wrt_trace2cmp"

def ColName__delta_in_total_energy__btwn_refTrace_and_predictedTrace():
    return 'Delta_in_total_energy__btwn_refTrace_and_predictedTrace'
