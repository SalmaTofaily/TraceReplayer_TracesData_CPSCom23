# Used traces are from the variability paper, https://ieeexplore.ieee.org/document/10257281.
# We automatically cleaned start and end of each iteration from any interference from the protocol.
# on 3 nodes, 3 scenarios for taking cold-start effects into consideration are studied. Extarcted traces are using to calibration PMSs:
# Bellow follows the original naming of scenarios. In the paper, scenarios A B, and C are c, e, and d, respectivelly.
# c. all exps
# d. all except first exp
# e. all experiments without the first 20 iterations 
# Tradeoff graphs are generated for replays of multiple sizes from 1 to n in each scenario.
# !! Detailed logs (2 G files) are expected per each run if we include (my program parameters) all predicted traces data and results, and verbose logs.


num_runs=1
tradeoff_graphs=1 
logs_relative_path="resultsdemo"
mkdir $logs_relative_path

echo node-1:
ref_trace_path="./../traces/traces_nogaps/paper-sen-A__full-traces/1688044998.773062-node1/1688044998.773062-341477 341489 341501 341512 341527 341547 341565 341579 341602 341615-trace.csv"
path_original_trace=$ref_trace_path 

# c (This notes scenario A in the paper)
path_trace_to_compare_to=$ref_trace_path 
trace_state_name="idle-node1-C"
/bin/python3 /home/salma/GIT/salma-thesis/code/simulators/sim23/run_trace_replayer.py --path_original_trace "$path_original_trace" --path_trace_to_compare_to "$path_trace_to_compare_to" --trace_state_name "$trace_state_name" --num_runs $num_runs --generate_tradeoff_graphs_inputSize_metrics $tradeoff_graphs --detailed_log_folder "$logs_relative_path" 
