# used traces from variability paper, (cleaned first and last 10 power measurements in each iteration):
# on 5 nodes, 5 scenarios of calibration such that calibration from:
# a. 1st exp
# b. 2rd exp
# c. all exps
# d. all except first exp
# e. all experiments without the first 20 iterations(based on our exps 20 is intersting nb 75 % after that is met in many cases)
# tradeoff graphs are generated for repays of multiple sizes 1 to n in each scenario.
# detailed logs. 2 G files are expected per each run if we keep all predicted traces data and results, and verbose logs.


num_runs=1
tradeoff_graphs=1 
logs_relative_path="resultsdemo"
mkdir $logs_relative_path

echo node-1: ----------------------------------------------------------------
ref_trace_path="./_traces/concatinated_cleaned/node1-1688044998.773062-341477 341489 341501 341512 341527 341547 341565 341579 341602 341615-trace.csv"
path_original_trace=$ref_trace_path 
# c
path_trace_to_compare_to=$ref_trace_path 
trace_state_name="idle-node1-C"
/bin/python3 /home/salma/GIT/salma-thesis/code/simulators/sim23/run_trace_replayer.py --path_original_trace "$path_original_trace" --path_trace_to_compare_to "$path_trace_to_compare_to" --trace_state_name "$trace_state_name" --num_runs $num_runs --generate_tradeoff_graphs_inputSize_metrics $tradeoff_graphs --detailed_log_folder "$logs_relative_path" 
