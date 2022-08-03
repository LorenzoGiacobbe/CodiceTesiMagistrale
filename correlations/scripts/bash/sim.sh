#!/bin/bash

# variables initialization
TB=''

# DEL has three possible values:
#	- 0: gadget without delays is simulated
#	- 1: gadget with only gate delays is simulated
#	- 2: gagdet with gate and input delays is simulated
DEL=0

# arguments retrieval
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
	vvp $VVP > ./logs/vvp_log.log
elif [ $DEL -eq 1 ]; then 
	VVP="./scripts/verilog/vvp/correlation_del.vvp"
	iverilog -o $VVP -DDEL $TB
	vvp $VVP > ./logs/vvp_log_del.log
elif [ $DEL -eq 2 ]; then
	VVP="./scripts/verilog/vvp/correlation_in_del.vvp"
	iverilog -o $VVP -DDEL -DIN_DEL $TB
	vvp $VVP > ./logs/vvp_log_in_del.log
fi

exit 1
