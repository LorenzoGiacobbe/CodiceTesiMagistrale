import sys

from scripts.python.excel import write_excel
from scripts.python.logic import *
from scripts.python.simulation import simulate
from scripts.python.cm_hist import create_cm_hist
from config.config import config

if __name__ == "__main__": 

    tb = sys.argv[1]
    conf = sys.argv[2]
    spreadsheet = sys.argv[3]

    config(conf)

    vvp_logs = simulate(tb)

    data = create_cm_hist(vvp_logs)
    
    write_excel(spreadsheet, data)

        