# chat gbt updated
from typing import Dict

# experiment_function_returning_dic_and_expIdentifier: return results dic (metric key and its value, and an exp_id key its name is configurable in method) and exp_id
# used chatgbt and enhanced
def accumulate_n_runs_results(num_runs, exp_identifier_key, experiment_function_returning_dic_and_expIdentifier, *args, **kwargs) -> Dict[str, list]:
    # https://www.geeksforgeeks.org/args-kwargs-python/
    #  # *args (Non-Keyword Arguments)
    # **kwargs (Keyword Arguments)
    accumulated_results_dict = {}
    for _ in range(num_runs):
        # Call the provided experiment_function_returning_dic_and_expIdentifier with arguments
        run_results, exp_identifier_val, other = experiment_function_returning_dic_and_expIdentifier(*args, **kwargs)
        for key, value in run_results.items():
            if key in accumulated_results_dict:
                accumulated_results_dict[key].append(value)
            else:
                accumulated_results_dict[key] = [value]

        list_exp_identifiers= accumulated_results_dict[exp_identifier_key]
        if list_exp_identifiers[0]!= exp_identifier_val:
            raise Exception("You are repeating non identical experiments")
    return accumulated_results_dict
    # Example usage
    # num_runs = 5
    # param1 = 10
    # param2 = 5

    # final_results = accumulate_results(num_runs, run_function_multiple_times, param1, param2)
    # for key, values in final_results.items():
    #     print(f'{key}: {values}')
