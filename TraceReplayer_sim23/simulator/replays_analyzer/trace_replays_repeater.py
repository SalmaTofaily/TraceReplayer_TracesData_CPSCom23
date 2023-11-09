from common.TimeHelper import now_readable
from common.automation_helper import accumulate_n_runs_results
from common.stat_helper import calculate_avg_stdev_for_dic_of_values

# exp_identifier_key the name of the result description, it should be the same. 
# exp_method_returning_results_dict should return a dictionary of results with floats values, args and kwargs are the methods named and unnamed args
def replayNTimes_calculatingAvgAndStdevOfAllResults(num_runs: int, exp_identifier_key: str, exp_method_returning_results_dict_and_expId, *args, **kwargs):
    # repeat n times the replay for this model with this calibration trace and reference trace
    # avg and stdev all results
    print("\n\n.... repeating exps(" + str(num_runs) + " runs) at "+ now_readable())
    # exp_method_returning_results_dict return dictionary. it is repeated n times.{ key:[v1,v2,v3],key2:[a,b,c]}
    accumelated_results_dic_metricKey_values = accumulate_n_runs_results(
        num_runs, exp_identifier_key, exp_method_returning_results_dict_and_expId, *args, **kwargs)
    
    dic_metricKey_valuesAvgAndStdev = calculate_avg_stdev_for_dic_of_values(
        accumelated_results_dic_metricKey_values, exp_identifier_key )
    print("Finished replay set at "+ now_readable())
    return dic_metricKey_valuesAvgAndStdev
   