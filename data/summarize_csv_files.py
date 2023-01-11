import json
from scipy.stats import mannwhitneyu as mwu
from scipy.stats import normaltest

from os.path import join
import numpy as np

RESULTS = {
    "airfoil_1hl" : "/Users/rmn/github/master_thesis/data/airfoil_1hl_maxIndSize_fullRun_30gens",
    "airfoil_2hl" : "/Users/rmn/github/master_thesis/data/airfoil_2hl_maxIndSize_fullRun_30gens",
    "bostonHousing": "/Users/rmn/github/master_thesis/data/bostonHousing_2hl_maxIndSize_fullRun_30gens",
    "energyCooling": "/Users/rmn/github/master_thesis/data/energyCooling_2hl_FullRun_30gens",
    #"concrete": "/Users/rmn/github/master_thesis/data/concrete_2hl_FullRun_30gens"
}


FILENAME="best_final_fitness.json"

def getPVal(sampleA, sampleB):
    stats, pval = mwu(sampleA, sampleB)

    assert len(sampleA) > 6 and len(sampleB) >= 8

    if pval <= 0.01:
        return f"{pval:.4f}***"
    elif pval <= 0.05:
        return f"{pval:.4f}**"
    elif pval <= 0.1:
        return f"{pval:.4f}*"
    else:
        return f"{pval:.4f}"


# Fitness
# ---

# summarize by mean
csv_string = "Problem,Hidden_Layer,Dataset,DAE-GP,Pre-Trained_DAE-GP,P_Value\n"

for problem,path in RESULTS.items():

    d = json.load(open(join(path, FILENAME),"r",encoding="utf-8"))

    # test for normal distribution ?
    # ----
    # reg_train = d["DAE-GP (train)"]
    # pt_train = d["Pre-Trained (train)"]
    # reg_test = d["DAE-GP (test)"]
    # pt_test = d["Pre-Trained (test)"]

    # for vals in (reg_train, pt_train, reg_test, pt_test):
    #     s, p = normaltest(vals)
    #     print("p_val:", p)

    reg_mean_train = np.mean(d["DAE-GP (train)"])
    pt_mean_train = np.mean(d["Pre-Trained (train)"])
    reg_mean_test = np.mean(d["DAE-GP (test)"])
    pt_mean_test = np.mean(d["Pre-Trained (test)"])

    assert d["DAE-GP (train)"] != d["Pre-Trained (train)"]
    assert d["DAE-GP (test)"] != d["Pre-Trained (test)"]


    csv_string += f"{d['problem']},{d['hiddenLayer']},Train,{reg_mean_train},{pt_mean_train},{getPVal(d['DAE-GP (train)'], d['Pre-Trained (train)'])}\n,{d['hiddenLayer']},Test,{reg_mean_test},{pt_mean_test},{getPVal(d['DAE-GP (test)'], d['Pre-Trained (test)'])}\n"


with open("/Users/rmn/github/master_thesis/data/summary_table_final_fit_mean.csv", "w", encoding="utf-8") as f:
    f.write(csv_string)


# summarize by median
csv_string = "Problem,Hidden_Layer,Dataset,DAE-GP,Pre-Trained_DAE-GP,P_Value\n"

for problem,path in RESULTS.items():

    d = json.load(open(join(path, FILENAME),"r",encoding="utf-8"))

    reg_med_train = np.median(d["DAE-GP (train)"])
    pt_med_train = np.median(d["Pre-Trained (train)"])
    reg_med_test = np.median(d["DAE-GP (test)"])
    pt_med_test = np.median(d["Pre-Trained (test)"])

    assert d["DAE-GP (train)"] != d["Pre-Trained (train)"]
    assert d["DAE-GP (test)"] != d["Pre-Trained (test)"]


    csv_string += f"{d['problem']},{d['hiddenLayer']},Train,{reg_med_train},{pt_med_train},{getPVal(d['DAE-GP (train)'], d['Pre-Trained (train)'])}\n,{d['hiddenLayer']},Test,{reg_med_test},{pt_med_test},{getPVal(d['DAE-GP (test)'], d['Pre-Trained (test)'])}\n"


with open("/Users/rmn/github/master_thesis/data/summary_table_final_fit_median.csv", "w", encoding="utf-8") as f:
    f.write(csv_string)



FILENAME_SIZE = "size_best_solution.json"

# Solution Size
# ---

# summarize by mean
csv_string = "Problem,Hidden_Layer,DAE-GP,Pre-Trained_DAE-GP,P_Value\n"

for problem,path in RESULTS.items():

    d = json.load(open(join(path, FILENAME_SIZE),"r",encoding="utf-8"))

    
    reg_mean = np.mean(d["DAE-GP"])
    pt_mean = np.mean(d["Pre-Trained"])


    csv_string += f"{d['problem']},{d['hiddenLayer']},{reg_mean},{pt_mean},{getPVal(d['DAE-GP'], d['Pre-Trained'])}\n"


with open("/Users/rmn/github/master_thesis/data/summary_table_best_size_mean.csv", "w", encoding="utf-8") as f:
    f.write(csv_string)
