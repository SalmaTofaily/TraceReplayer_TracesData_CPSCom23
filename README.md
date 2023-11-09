
# Trace Relayer Overview
For the paper " Representing Power Variability of an Idle IoT Edge Node in the Power State Model"

Trace Replayer for comparing power models predictions with real power measurements, evaluating models accuracy.
It includes three updates of the Power State Model, considering power variability of a state in different ways.
It also allows to conduct tradeoff experiments between calibration trace size and models accuracy.
In addition, it allows evaluating the standard deviation of results, when a replay is repeated n times.

# Get Started with the code

run_trace_replayer.py has several arguments for configuration.
A demo is prepared to run tradeoff experiments.
To run the demo, update the filepath of the traces to match the traces folder.

chmod +x run_demo.sh
./run_demo.sh

Code follows the original naming of scenarios. Scenarios A B, and C in the paper are c, e, and d in the code, respectively.
c. all exps
d. all except first exp
e. all experiments without the first 20 iterations

The Original Trace is presented for each node in the traces folders.
