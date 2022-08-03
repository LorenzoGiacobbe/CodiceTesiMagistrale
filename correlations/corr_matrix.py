import sys
import time

from scripts.python.excel import write_excel
from scripts.python.simulation import simulate
from scripts.python.cm_hist import create_cm_hist
from config.config import config

# auxiliary function to check time taken for the computations
def done_in(start_time):
    elapsed_time = "{:.4f}".format(time.time() - start_time)
    print("Done in %s seconds" % elapsed_time)


if __name__ == "__main__":
    
    start_time = time.time()

    # takes as inputs from the user:
    #   - the name of the gadget present in the src folder to simulate
    #   - the configuration file corresponding to the gadget that needs to be simulated
    #   - the name that the spreadsheet containing the results will get
    module = sys.argv[1]
    conf_file = "./config/" + sys.argv[2]
    spreadsheet = sys.argv[3]

    # starting from the configuration file global variables are defined
    # and the verilog file with all the needed `define is created
    config(conf_file)

    # the gadget passed as parameter is simulated three times:
    #   - 1st simulation: ideal gadget with no delays
    #   - 2nd simulation: the gates of the gadget have a delay in the computaion
    #   - 3rd simulation: in addition to the previous delays also the inputs have delays
    # and the results are saved in the logs contained in the logs folder
    vvp_logs = simulate(module, conf_file)

    # the lists containing the number of toggles for the different simulations are created
    # through the selection function and the consume model function (that can be changed by the user)
    # the correlations are calculated between the chosen inputs and the number of toggles
    data = create_cm_hist(vvp_logs)
    
    # the correlation function is printed on terminal as well as saved on the spreadsheet
    print(data[0])
    write_excel(spreadsheet, data)
    
    done_in(start_time)

        