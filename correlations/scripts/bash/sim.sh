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
	VVP="./scripts/verilog/vvp/correlation.vvp"
	iverilog -o $VVP $TB
	# echo "simulating $VVP ..."
	vvp $VVP > ./logs/vvp_log.log
elif [ $DEL -eq 1 ]; then 
	VVP="./scripts/verilog/vvp/correlation_del.vvp"
	iverilog -o $VVP -DDEL $TB
	# echo "simulating $VVP ..."
	vvp $VVP > ./logs/vvp_log_del.log
elif [ $DEL -eq 2 ]; then
	VVP="./scripts/verilog/vvp/correlation_in_del.vvp"
	iverilog -o $VVP -DDEL -DIN_DEL $TB
	# echo "simulating $VVP ..."
	vvp $VVP > ./logs/vvp_log_in_del.log
fi

exit 1
