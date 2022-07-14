import sys

from scripts.python.excel import write_excel
from scripts.python.logic import *
from scripts.python.simulation import simulate
from scripts.python.cm_hist import create_cm_hist
from config.config import config

if __name__ == "__main__": 

    # tb = sys.argv[1]
    # conf = sys.argv[2]
    
    module = sys.argv[1]
    spreadsheet = sys.argv[2]

    config()

    vvp_logs = simulate(module)

    data = create_cm_hist(vvp_logs)
    print(data[0])
    
    write_excel(spreadsheet, data)

        