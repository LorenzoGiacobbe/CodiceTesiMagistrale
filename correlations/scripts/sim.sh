#!/bin/bash

# HELP FUNCTION
Help()
{
    echo "Syntax: sim [-h|g|d|D]"
	echo "Options:"
	echo "h	display help"
	echo "d delays on gates"
	echo "D delays on gates and inputs"
	echo "t name of testbench to execute"
	echo "p	relative path (default '.')"
    echo
} 

# SET VARIABLES
TB=''
DEL=0

# get the options and their arguments
while getopts ":dDt:" option; do
    case $option in
	d)
	    DEL=1;;
	D)
	    DEL=2;;
        t)
            TB=$OPTARG;; 
        \?) # Invalid option
            echo "Error: Invalid option"
            exit;;
   esac
done

# echo "compiling $TB ..."
if [ $DEL -eq 0 ]; then
	VVP="./verilog/tb/vvp/correlation.vvp"
	iverilog -o $VVP -DXNOR_DELAY='#0' -DNAND_DELAY='#0' -DXOR_DELAY='#0' $TB
	# echo "simulating $VVP ..."
	vvp $VVP > ./logs/vvp_log
elif [ $DEL -eq 1 ]; then 
	VVP="./verilog/tb/vvp/correlation_del.vvp"
	iverilog -o $VVP -DXNOR_DELAY='#0.1' -DNAND_DELAY='#0.2' -DXOR_DELAY='#0.5' $TB
	# echo "simulating $VVP ..."
	vvp $VVP > ./logs/vvp_log_del
elif [ $DEL -eq 2 ]; then
	VVP="./verilog/tb/vvp/correlation_in_del.vvp"
	iverilog -o $VVP -DXNOR_DELAY='#0.1' -DNAND_DELAY='#0.2' -DXOR_DELAY='#0.5' -DIN_DEL $TB
	# echo "simulating $VVP ..."
	vvp $VVP > ./logs/vvp_log_in_del
fi

exit 1
