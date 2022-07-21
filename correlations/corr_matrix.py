import sys
import time

from scripts.python.excel import write_excel
from scripts.python.logic import *
from scripts.python.simulation import simulate
from scripts.python.cm_hist import create_cm_hist
from config.config import config

def done_in(start_time):
    elapsed_time = "{:.4f}".format(time.time() - start_time)
    print("Done in %s seconds" % elapsed_time)


if __name__ == "__main__":
    
    start_time = time.time()

    module = sys.argv[1]
    spreadsheet = sys.argv[2]

    config()

    vvp_logs = simulate(module)

    data = create_cm_hist(vvp_logs)
    print(data[0])
    
    write_excel(spreadsheet, data)
    done_in(start_time)

        